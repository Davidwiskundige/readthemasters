#!/usr/bin/env python3
"""ReadTheMasters Tier-3 transcription pipeline — scan pages -> house-style LaTeX.

Runs on the CONTRIBUTOR's own Anthropic account via the Batch API (PLAN.md §4.1, §7.4). One
Batch request per scan page (pinned prompt + page image + previous page's tail), stitched into
corpus/<work-id>/original.tex, then an optional cheap verification pass. The project pays for no AI
compute — this is invoked by a contributor with their own ANTHROPIC_API_KEY.

Usage:
    python pipeline/transcribe.py <work-id> --pages 293-297 --images ./scans
        [--model claude-opus-4-8] [--verify-model claude-haiku-4-5]
        [--effort high] [--no-verify] [--corpus corpus] [--poll-seconds 30]

The gate is a hard precondition: a work that is not public domain (per pipeline/validate.py) is
refused. The script writes the corpus files and STOPS — it never commits or pushes. The contributor
reviews, runs `python pipeline/validate.py` + `pytest pipeline/tests`, then opens a DCO-signed PR.

`anthropic` is a contributor-only dependency, imported lazily so the free CI gate (validate.py)
keeps its single PyYAML dependency.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import re
import sys
import time
from pathlib import Path

import yaml

# Reuse the gate — validate.py lives next to this file.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # noqa: E402

DEFAULT_MODEL = "claude-opus-4-8"        # hard material (Fraktur, dense 18th-19th c. math)
DEFAULT_VERIFY_MODEL = "claude-haiku-4-5"  # cheap second-pass check (PLAN.md §4.1 step 4)
MAX_TOKENS = 8000                        # a page of LaTeX is ~1-2k tokens; leave headroom
IMAGE_MEDIA_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp",
}

SCAFFOLD_HEADER = (
    "% Faithful transcription — AI draft (Tier-3 Batch API pipeline). Transcribed page-by-page from\n"
    "% the source scan; \\origpage uses the PRINTED page numbers. Machine output pending human\n"
    "% review — see provenance.yaml. Notation preserved, typography normalized (PLAN.md §4.4)."
)


# --------------------------------------------------------------------------- #
# Pure helpers (no network — unit-tested in tests/test_transcribe.py)
# --------------------------------------------------------------------------- #
def parse_pages(spec: str) -> list[int]:
    """Parse a page spec like "293-297" or "293,295,300-302" into a sorted, de-duped list."""
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo_s, hi_s = part.split("-", 1)
            lo, hi = int(lo_s), int(hi_s)
            if hi < lo:
                raise ValueError(f"bad page range '{part}': end before start")
            pages.update(range(lo, hi + 1))
        else:
            pages.add(int(part))
    if not pages:
        raise ValueError(f"no pages in spec '{spec}'")
    return sorted(pages)


def load_prompt(prompt_path: Path) -> tuple[str, str]:
    """Return (instruction_body, prompt_version) from prompts/transcribe-chat.md.

    The version is in the H1 (`prompt_version: transcribe-vN`); the instruction is everything after
    the first `---` separator line (the copy-paste box), so pipeline and chat share one prompt.
    """
    text = prompt_path.read_text(encoding="utf-8")
    m = re.search(r"prompt_version:\s*(\S+)", text)
    if not m:
        raise ValueError(f"no prompt_version found in {prompt_path}")
    version = m.group(1)

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---":
            body = "\n".join(lines[i + 1:]).strip()
            if not body:
                break
            return body, version
    raise ValueError(f"no instruction body (after '---') found in {prompt_path}")


def image_source(path: Path) -> dict:
    """Encode an image file as a base64 content-block source (no newlines in the data)."""
    media_type = IMAGE_MEDIA_TYPES.get(path.suffix.lower())
    if media_type is None:
        raise ValueError(f"unsupported image type '{path.suffix}' for {path.name}")
    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
    return {"type": "base64", "media_type": media_type, "data": data}


def resolve_page_images(images_dir: Path, pages: list[int]) -> dict[int, Path]:
    """Map each page number to an image file whose stem is the page number (zero-padding allowed)."""
    by_page: dict[int, Path] = {}
    candidates = [p for p in sorted(images_dir.iterdir())
                  if p.is_file() and p.suffix.lower() in IMAGE_MEDIA_TYPES]
    missing: list[int] = []
    for n in pages:
        match = next((p for p in candidates
                      if p.stem == str(n) or (p.stem.isdigit() and int(p.stem) == n)), None)
        if match is None:
            missing.append(n)
        else:
            by_page[n] = match
    if missing:
        raise FileNotFoundError(
            f"no image found in {images_dir} for page(s): {', '.join(map(str, missing))}. "
            f"Name each scan file by its printed page number, e.g. 293.png"
        )
    return by_page


def build_page_request(page: int, instruction: str, img_source: dict, prev_tail: str,
                       model: str, effort: str, custom_id: str | None = None) -> dict:
    """Build one Batch request for a single scan page.

    The pinned instruction is a cached system prefix (byte-identical across pages, so the shared
    prompt is billed once, PLAN.md §7.5); the per-page user turn carries the image, the printed page
    number, and the tail of the previous page for continuity.
    """
    prev = (f"\n\nFor continuity, the previous page ended with:\n{prev_tail}"
            if prev_tail else "")
    user_text = (
        f"Transcribe this single scanned page. Its printed page number is {page}; begin the "
        f"output with \\origpage{{{page}}}. Output only the LaTeX body — no commentary, no "
        f"preamble, no \\documentclass or \\begin{{document}}.{prev}"
    )
    return {
        "custom_id": custom_id or f"page-{page}",
        "params": {
            "model": model,
            "max_tokens": MAX_TOKENS,
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": effort},
            "system": [{"type": "text", "text": instruction,
                        "cache_control": {"type": "ephemeral"}}],
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": img_source},
                    {"type": "text", "text": user_text},
                ],
            }],
        },
    }


def build_verify_request(page: int, img_source: dict, fragment: str,
                         model: str, custom_id: str | None = None) -> dict:
    """Build one Batch request that checks a page's transcription against its scan (PLAN.md §4.1)."""
    system = (
        "You verify a LaTeX transcription against the original scanned page for a public-domain "
        "digitization project. Compare the transcription below to the image, focusing on formulas, "
        "equation numbers, labels, and the \\origpage marker. If it faithfully matches the scan, "
        "reply with exactly the single word MATCH. Otherwise reply starting with FLAG: followed by "
        "a terse list of the specific discrepancies. Do not rewrite the transcription."
    )
    return {
        "custom_id": custom_id or f"verify-{page}",
        "params": {
            "model": model,
            "max_tokens": 1024,
            "system": system,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image", "source": img_source},
                    {"type": "text", "text": f"Transcription of page {page}:\n\n{fragment}"},
                ],
            }],
        },
    }


def tail_of(latex: str, max_chars: int = 400) -> str:
    """Return the last ~max_chars of a transcription for cross-page continuity."""
    latex = latex.strip()
    return latex if len(latex) <= max_chars else latex[-max_chars:].lstrip()


_FENCE_RE = re.compile(r"^```(?:latex|tex)?\s*$", re.IGNORECASE)
_SCAFFOLD_RE = re.compile(r"^\s*\\(documentclass|usepackage\{readmasters\}|begin\{document\}|"
                          r"end\{document\})")


def clean_fragment(page: int, latex: str) -> str:
    """Strip stray code fences / document scaffold the model may add, and ensure \\origpage{N}."""
    kept = [ln for ln in latex.splitlines()
            if not _FENCE_RE.match(ln.strip()) and not _SCAFFOLD_RE.match(ln)]
    body = "\n".join(kept).strip()
    if f"\\origpage{{{page}}}" not in body:
        body = f"\\origpage{{{page}}}\n{body}"
    return body


def stitch(fragments: dict[int, str], header: str = SCAFFOLD_HEADER) -> str:
    """Assemble per-page fragments (keyed by page, any arrival order) into a full LaTeX document."""
    body = "\n\n".join(clean_fragment(n, fragments[n]) for n in sorted(fragments))
    return (
        f"{header}\n"
        "\\documentclass{article}\n"
        "\\usepackage{readmasters}\n"
        "\\begin{document}\n\n"
        f"{body}\n\n"
        "\\end{document}\n"
    )


def is_flagged(verify_text: str) -> bool:
    """A page is flagged unless the verifier replied with a clean MATCH."""
    return verify_text.strip().upper() != "MATCH"


def build_provenance(model: str, effort: str, prompt_version: str, batch_ids: list[str],
                     flagged_pages: list[int], verify_model: str | None,
                     produced: str | None = None) -> dict:
    """Build the transcription provenance block (status always ai-draft — machine output)."""
    prov: dict = {
        "status": "ai-draft",
        "model": model,
        "effort": effort,
        "prompt_version": prompt_version,
        "submitted_via": "pipeline",
        "produced": produced or datetime.date.today().isoformat(),
        "batch_ids": batch_ids,
    }
    if verify_model is not None:
        prov["verification"] = {
            "model": verify_model,
            "flagged_pages": flagged_pages,
            "date": produced or datetime.date.today().isoformat(),
        }
    return prov


# --------------------------------------------------------------------------- #
# Gate precondition
# --------------------------------------------------------------------------- #
def check_gate(work_dir: Path, now_year: int) -> dict:
    """Load work.yaml and compute the copyright verdict; raise if the work is not publishable."""
    work_yaml = work_dir / "work.yaml"
    if not work_yaml.exists():
        raise SystemExit(f"error: {work_yaml} not found — author it before transcribing "
                         f"(see .claude/skills/transcribe/templates/work.yaml).")
    work = validate.load_yaml(work_yaml)
    prov_path = work_dir / "provenance.yaml"
    prov = validate.load_yaml(prov_path) if prov_path.exists() else {}
    assessment = validate.evaluate_copyright(work, prov or {}, now_year)
    if not assessment["public_domain"]:
        failed = [rule for rule, r in assessment["evaluated"].items() if r["verdict"] == "fail"]
        raise SystemExit(f"error: {work_dir.name} is NOT public domain — failing rule(s): "
                         f"{', '.join(failed)}. This work cannot be transcribed or published.")
    return work


# --------------------------------------------------------------------------- #
# Batch API (network — lazily imports anthropic)
# --------------------------------------------------------------------------- #
def _client():
    try:
        import anthropic  # noqa: PLC0415 — contributor-only dependency, imported lazily
    except ImportError:
        raise SystemExit("error: the 'anthropic' package is required for Tier-3 runs.\n"
                         "  pip install anthropic   (and set ANTHROPIC_API_KEY)")
    return anthropic.Anthropic()


def run_batch(client, requests: list[dict], poll_seconds: int, label: str) -> tuple[str, dict]:
    """Submit a batch, poll to completion, and return (batch_id, {custom_id: text})."""
    batch = client.messages.batches.create(requests=requests)
    print(f"  {label}: submitted batch {batch.id} ({len(requests)} requests)")
    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        counts = batch.request_counts
        print(f"  {label}: {batch.processing_status} "
              f"(processing {counts.processing}, done {counts.succeeded})...")
        time.sleep(poll_seconds)

    texts: dict[str, str] = {}
    errored: list[str] = []
    for result in client.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            msg = result.result.message
            texts[result.custom_id] = "".join(
                b.text for b in msg.content if getattr(b, "type", None) == "text"
            ).strip()
        else:
            errored.append(result.custom_id)
    if errored:
        print(f"  {label}: WARNING — {len(errored)} request(s) did not succeed: "
              f"{', '.join(sorted(errored))}", file=sys.stderr)
    return batch.id, texts


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Tier-3 Batch API transcription (contributor-run).")
    ap.add_argument("work_id", help="corpus work id (directory name under --corpus)")
    ap.add_argument("--pages", required=True, help="page spec, e.g. 293-297 or 293,295,300-302")
    ap.add_argument("--images", required=True, type=Path,
                    help="directory of scan images named by printed page number (e.g. 293.png)")
    ap.add_argument("--corpus", default="corpus", type=Path, help="corpus root (default: corpus)")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"transcription model (default: {DEFAULT_MODEL}; use claude-sonnet-5 for "
                         "clean modern typography)")
    ap.add_argument("--verify-model", default=DEFAULT_VERIFY_MODEL,
                    help=f"verification model (default: {DEFAULT_VERIFY_MODEL})")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"],
                    help="thinking/effort level (default: high; recorded in provenance)")
    ap.add_argument("--no-verify", action="store_true", help="skip the verification pass")
    ap.add_argument("--poll-seconds", type=int, default=30, help="batch poll interval (default: 30)")
    ap.add_argument("--now-year", type=int, default=datetime.date.today().year,
                    help="year used for the copyright gate (default: current year)")
    args = ap.parse_args(argv)

    work_dir = args.corpus / args.work_id
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "transcribe-chat.md"

    # 1. Gate — hard precondition.
    check_gate(work_dir, args.now_year)
    print(f"gate: {args.work_id} is public domain — proceeding.")

    # 2. Resolve inputs.
    try:
        pages = parse_pages(args.pages)
        if not args.images.is_dir():
            raise FileNotFoundError(f"--images: {args.images} is not a directory")
        page_images = resolve_page_images(args.images, pages)
        instruction, prompt_version = load_prompt(prompt_path)
    except (ValueError, FileNotFoundError) as exc:
        raise SystemExit(f"error: {exc}")
    print(f"transcribing {len(pages)} page(s) [{pages[0]}..{pages[-1]}] with {args.model} "
          f"(effort={args.effort}, prompt {prompt_version}).")

    client = _client()

    # 3. Transcription batch — one request per page.
    # Pages in a single batch are transcribed in parallel, so a page cannot see a *prior page's
    # output* as its tail; build_page_request still supports a continuity tail (a future sequential
    # mode, or a re-run of a single page, can supply one). Cross-page continuity here is caught by
    # the verification pass and the human review, not by chaining output.
    requests = [build_page_request(n, instruction, image_source(page_images[n]),
                                   prev_tail="", model=args.model, effort=args.effort)
                for n in pages]
    batch_id, page_texts = run_batch(client, requests, args.poll_seconds, "transcribe")

    fragments = {n: page_texts[f"page-{n}"] for n in pages if f"page-{n}" in page_texts}
    if not fragments:
        raise SystemExit("error: no pages transcribed successfully — nothing written.")
    document = stitch(fragments)
    (work_dir / "original.tex").write_text(document, encoding="utf-8")
    print(f"wrote {work_dir / 'original.tex'} ({len(fragments)} page(s)).")

    batch_ids = [batch_id]
    flagged_pages: list[int] = []
    verify_model = None

    # 4. Verification pass.
    if not args.no_verify:
        verify_model = args.verify_model
        vreqs = [build_verify_request(n, image_source(page_images[n]), fragments[n], verify_model)
                 for n in sorted(fragments)]
        vbatch_id, vtexts = run_batch(client, vreqs, args.poll_seconds, "verify")
        batch_ids.append(vbatch_id)
        flagged_pages = sorted(n for n in fragments
                               if is_flagged(vtexts.get(f"verify-{n}", "FLAG: no result")))
        print(f"verification: {len(flagged_pages)} page(s) flagged"
              + (f" — {flagged_pages}" if flagged_pages else " — none"))

    # 5. Provenance (merge, preserving any existing translations block).
    prov_path = work_dir / "provenance.yaml"
    prov = validate.load_yaml(prov_path) if prov_path.exists() else {}
    prov = prov or {}
    prov["transcription"] = build_provenance(args.model, args.effort, prompt_version, batch_ids,
                                             flagged_pages, verify_model)
    with prov_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(prov, fh, allow_unicode=True, sort_keys=False)
    print(f"wrote {prov_path} (status: ai-draft).")

    # 6. Human-review checkpoint — never commit/push.
    print("\nNext steps (nothing has been committed):")
    print("  1. Review original.tex against the scans"
          + (f"; start with flagged page(s) {flagged_pages}." if flagged_pages else "."))
    print("  2. python pipeline/validate.py && python -m pytest pipeline/tests -q")
    print(f"  3. git checkout -b transcribe/{args.work_id}")
    print(f"     git add {work_dir}/ && git commit -s -m \"Add {args.work_id} transcription "
          "(ai-draft)\"")
    print("     gh pr create --fill   # state pages, model, prompt_version, flagged pages, scan URL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
