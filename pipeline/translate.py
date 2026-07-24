#!/usr/bin/env python3
"""ReadTheMasters Tier-3 translation pipeline — our LaTeX transcription -> translated LaTeX.

Runs on the CONTRIBUTOR's own Anthropic account via the Batch API (PLAN.md §4.2). Translates only
from OUR OWN transcription (`original.tex`), never from an existing human translation — the
`translation_source` copyright rule (PLAN.md §2.2). The original is chunked by `\\origpage`
boundaries; each chunk is one Batch request that translates the prose while reproducing every math
expression, marker, and label verbatim. A post-run check (pipeline/texcompare.py) confirms the math
survived; the same check runs in the CI gate.

Usage:
    python pipeline/translate.py <work-id> --lang en [--model claude-opus-4-8] [--effort high]
        [--glossary corpus/<id>/glossary.yaml] [--no-check] [--corpus corpus] [--poll-seconds 30]

The gate is a hard precondition (a work that is not public domain is refused). The script writes
corpus/<work-id>/translations/<lang>.tex + provenance and STOPS — no commit/push. The contributor
reviews, runs the gate + tests, then opens a DCO-signed PR.

`anthropic` is a contributor-only dependency, imported lazily (reused from transcribe.py) so the
free CI gate stays PyYAML-only.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import texcompare  # noqa: E402
import validate  # noqa: E402
from transcribe import _client, load_prompt, run_batch  # noqa: E402

DEFAULT_MODEL = "claude-opus-4-8"
MAX_TOKENS = 8000
LANGUAGE_NAMES = {"en": "English", "fr": "French", "de": "German", "it": "Italian",
                  "la": "Latin", "es": "Spanish", "nl": "Dutch", "ru": "Russian"}
_PLACEHOLDER = "{TARGET LANGUAGE, e.g. English}"  # literal token in prompts/translate-chat.md

_SCAFFOLD_LINE_RE = re.compile(r"^\s*\\(documentclass|usepackage|begin\{document\}|end\{document\})")
_ORIGPAGE_SPLIT_RE = re.compile(r"(?=\\origpage\{)")


# --------------------------------------------------------------------------- #
# Pure helpers (no network — unit-tested in tests/test_translate.py)
# --------------------------------------------------------------------------- #
def language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code.lower(), code)


def strip_scaffold(latex: str) -> str:
    """Return the document body: drop the leading comment header and the LaTeX scaffold lines."""
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", latex, re.DOTALL)
    inner = m.group(1) if m else latex
    kept = [ln for ln in inner.splitlines()
            if not _SCAFFOLD_LINE_RE.match(ln) and not ln.lstrip().startswith("%")]
    return "\n".join(kept).strip()


def split_chunks(body: str) -> list[str]:
    """Split a transcription body into translation units at each `\\origpage` boundary."""
    parts = [p.strip() for p in _ORIGPAGE_SPLIT_RE.split(body) if p.strip()]
    return parts


def format_glossary(glossary: dict | None) -> str:
    """Render a {term: rendering} glossary as prompt text (empty string if none)."""
    if not glossary:
        return ""
    terms = glossary.get("terms", glossary) if isinstance(glossary, dict) else {}
    lines = [f'  - "{src}" -> "{dst}"' for src, dst in terms.items()]
    if not lines:
        return ""
    return ("\n\nGlossary — render these terms consistently as given (keep the author's own period "
            "term where the mapping says so):\n" + "\n".join(lines))


def render_prompt(instruction: str, language: str, glossary_text: str = "") -> str:
    """Fill the target language into the pinned prompt and append any glossary."""
    return instruction.replace(_PLACEHOLDER, language) + glossary_text


def build_chunk_request(index: int, chunk: str, prompt: str, model: str, effort: str,
                        custom_id: str | None = None) -> dict:
    """Build one Batch request translating a single chunk (prose translated, math verbatim)."""
    return {
        "custom_id": custom_id or f"chunk-{index}",
        "params": {
            "model": model,
            "max_tokens": MAX_TOKENS,
            "thinking": {"type": "adaptive"},
            "output_config": {"effort": effort},
            "system": [{"type": "text", "text": prompt,
                        "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": [{"type": "text", "text": chunk}]}],
        },
    }


_FENCE_RE = re.compile(r"^```(?:latex|tex)?\s*$", re.IGNORECASE)


def clean_chunk(latex: str) -> str:
    """Strip stray code fences / scaffold lines a model may wrap around a translated chunk."""
    kept = [ln for ln in latex.splitlines()
            if not _FENCE_RE.match(ln.strip()) and not _SCAFFOLD_LINE_RE.match(ln)]
    return "\n".join(kept).strip()


def assemble_translation(chunks_by_index: dict[int, str], header: str) -> str:
    """Reassemble translated chunks in order into a full LaTeX document."""
    body = "\n\n".join(clean_chunk(chunks_by_index[i]) for i in sorted(chunks_by_index))
    return (
        f"{header}\n"
        "\\documentclass{article}\n"
        "\\usepackage{readmasters}\n"
        "\\begin{document}\n\n"
        f"{body}\n\n"
        "\\end{document}\n"
    )


def translation_header(language: str) -> str:
    return (
        f"% {language} translation — AI draft (Tier-3 Batch API pipeline). Made from our own\n"
        "% transcription (original.tex), NOT from any existing translation (PLAN.md §2.2). Prose is\n"
        "% translated; every math expression, \\origpage marker, and label is preserved unchanged.\n"
        "% Machine output pending human review — see provenance.yaml."
    )


def build_translation_provenance(model: str, effort: str, prompt_version: str,
                                 batch_ids: list[str], produced: str | None = None) -> dict:
    """Build a translation provenance block (status ai-draft; source is always our transcription)."""
    return {
        "status": "ai-draft",
        "model": model,
        "effort": effort,
        "prompt_version": prompt_version,
        "submitted_via": "pipeline",
        "source": "transcription",   # translation_source rule: from our original.tex only
        "produced": produced or datetime.date.today().isoformat(),
        "batch_ids": batch_ids,
    }


# --------------------------------------------------------------------------- #
# Gate precondition
# --------------------------------------------------------------------------- #
def check_gate(work_dir: Path, now_year: int) -> None:
    """Refuse a work that is not public domain or has no transcription to translate from."""
    work_yaml = work_dir / "work.yaml"
    if not work_yaml.exists():
        raise SystemExit(f"error: {work_yaml} not found.")
    if not (work_dir / "original.tex").exists():
        raise SystemExit(f"error: {work_dir / 'original.tex'} not found — transcribe the work "
                         "before translating (we translate only from our own transcription).")
    work = validate.load_yaml(work_yaml)
    prov_path = work_dir / "provenance.yaml"
    prov = validate.load_yaml(prov_path) if prov_path.exists() else {}
    assessment = validate.evaluate_copyright(work, prov or {}, now_year)
    if not assessment["public_domain"]:
        failed = [r for r, v in assessment["evaluated"].items() if v["verdict"] == "fail"]
        raise SystemExit(f"error: {work_dir.name} is NOT public domain — failing rule(s): "
                         f"{', '.join(failed)}. This work cannot be translated or published.")


def load_glossary(work_dir: Path, explicit: Path | None) -> dict | None:
    path = explicit if explicit is not None else (work_dir / "glossary.yaml")
    if path and path.exists():
        return validate.load_yaml(path) or {}
    return None


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Tier-3 Batch API translation (contributor-run).")
    ap.add_argument("work_id", help="corpus work id (directory name under --corpus)")
    ap.add_argument("--lang", required=True, help="target language code, e.g. en, fr, de")
    ap.add_argument("--corpus", default="corpus", type=Path, help="corpus root (default: corpus)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"model (default: {DEFAULT_MODEL})")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"],
                    help="thinking/effort level (default: high; recorded in provenance)")
    ap.add_argument("--glossary", type=Path,
                    help="glossary YAML (default: corpus/<id>/glossary.yaml if present)")
    ap.add_argument("--no-check", action="store_true",
                    help="skip the math-preservation check on the assembled translation")
    ap.add_argument("--poll-seconds", type=int, default=30, help="batch poll interval (default: 30)")
    ap.add_argument("--now-year", type=int, default=datetime.date.today().year,
                    help="year used for the copyright gate (default: current year)")
    args = ap.parse_args(argv)

    work_dir = args.corpus / args.work_id
    lang = args.lang.lower()
    lang_name = language_name(lang)
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "translate-chat.md"

    # 1. Gate — hard precondition.
    check_gate(work_dir, args.now_year)
    print(f"gate: {args.work_id} is public domain — translating into {lang_name}.")

    # 2. Prepare inputs.
    try:
        instruction, prompt_version = load_prompt(prompt_path)
    except (ValueError, FileNotFoundError) as exc:
        raise SystemExit(f"error: {exc}")
    original_text = (work_dir / "original.tex").read_text(encoding="utf-8")
    chunks = split_chunks(strip_scaffold(original_text))
    if not chunks:
        raise SystemExit("error: original.tex has no translatable body.")
    glossary = load_glossary(work_dir, args.glossary)
    prompt = render_prompt(instruction, lang_name, format_glossary(glossary))
    print(f"{len(chunks)} chunk(s) with {args.model} (effort={args.effort}, prompt "
          f"{prompt_version}{', glossary' if glossary else ''}).")

    client = _client()

    # 3. Translation batch — one request per chunk.
    requests = [build_chunk_request(i, chunk, prompt, args.model, args.effort)
                for i, chunk in enumerate(chunks)]
    batch_id, texts = run_batch(client, requests, args.poll_seconds, "translate")

    translated = {i: texts[f"chunk-{i}"] for i in range(len(chunks)) if f"chunk-{i}" in texts}
    if len(translated) != len(chunks):
        missing = [i for i in range(len(chunks)) if i not in translated]
        raise SystemExit(f"error: {len(missing)} chunk(s) failed to translate ({missing}) — "
                         "not writing a partial translation.")

    document = assemble_translation(translated, translation_header(lang_name))
    out_dir = work_dir / "translations"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{lang}.tex"
    out_path.write_text(document, encoding="utf-8")
    print(f"wrote {out_path} ({len(translated)} chunk(s)).")

    # 4. Math-preservation check (also enforced by the CI gate).
    check_ok = True
    if not args.no_check:
        report = texcompare.preservation_report(original_text, document)
        check_ok = report["ok"]
        if check_ok:
            print("preservation: math, \\origpage markers, and refs all preserved.")
        else:
            print("preservation: MISMATCH — the translation altered invariant tokens:\n"
                  + texcompare.format_report(report), file=sys.stderr)

    # 5. Provenance (merge, preserving transcription block and other languages).
    prov_path = work_dir / "provenance.yaml"
    prov = validate.load_yaml(prov_path) if prov_path.exists() else {}
    prov = prov or {}
    prov.setdefault("translations", {})
    prov["translations"][lang] = build_translation_provenance(
        args.model, args.effort, prompt_version, [batch_id])
    with prov_path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(prov, fh, allow_unicode=True, sort_keys=False)
    print(f"wrote {prov_path} (translations.{lang}: ai-draft, source: transcription).")

    # 6. Human-review checkpoint — never commit/push.
    print("\nNext steps (nothing has been committed):")
    if not check_ok:
        print("  0. FIX the preservation mismatch above before anything else — the CI gate "
              "will reject an altered formula.")
    print(f"  1. Review translations/{lang}.tex against original.tex (prose only should differ).")
    print("  2. python pipeline/validate.py && python -m pytest pipeline/tests -q")
    print(f"  3. git checkout -b translate/{args.work_id}-{lang}")
    print(f"     git add {work_dir}/ && git commit -s -m \"Add {args.work_id} {lang} translation "
          "(ai-draft)\"")
    print("     gh pr create --fill   # state work, language, model, prompt_version, source")
    return 0 if check_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
