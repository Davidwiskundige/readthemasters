"""Tests for agent skills metadata, discovery conventions, and referenced path integrity."""
from pathlib import Path
import re
import yaml

REPO = Path(__file__).resolve().parents[2]


def test_antigravity_skill_exists_and_has_valid_frontmatter():
    skill_file = REPO / ".agents" / "skills" / "transcribe" / "SKILL.md"
    assert skill_file.exists(), f"Missing skill file: {skill_file}"

    content = skill_file.read_text(encoding="utf-8")
    assert content.startswith("---"), "SKILL.md must start with YAML frontmatter"

    parts = content.split("---", 2)
    assert len(parts) >= 3, "Malformed YAML frontmatter in SKILL.md"

    frontmatter = yaml.safe_load(parts[1])
    assert isinstance(frontmatter, dict), "Frontmatter must be a YAML dictionary"
    assert frontmatter.get("name") == "transcribe", "Skill name must be 'transcribe'"
    assert "description" in frontmatter and len(frontmatter["description"].strip()) > 0


def test_claude_skill_coexistence():
    claude_skill = REPO / ".claude" / "skills" / "transcribe" / "SKILL.md"
    assert claude_skill.exists(), "Claude Code skill must coexist at .claude/skills/transcribe/SKILL.md"

    content = claude_skill.read_text(encoding="utf-8")
    parts = content.split("---", 2)
    assert len(parts) >= 3
    fm = yaml.safe_load(parts[1])
    assert fm.get("name") == "transcribe"


def test_antigravity_skill_referenced_repo_paths_exist():
    skill_file = REPO / ".agents" / "skills" / "transcribe" / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")

    # Known key files and scripts explicitly referenced in the instructions
    expected_paths = [
        "pipeline/validate.py",
        "pipeline/houselint.py",
        "pipeline/texcompare.py",
        "pipeline/prepare_pages.py",
        "pipeline/magnify.py",
        "prompts/transcribe-chat.md",
        "prompts/transcribe-housestyle-extract.md",
        "corpus/HOUSESTYLE.md",
        "corpus/preamble/readmasters.sty",
        ".agents/skills/transcribe/templates/work.yaml",
    ]

    for rel_path in expected_paths:
        assert rel_path in content, f"Expected reference to {rel_path} in SKILL.md"
        target_path = REPO / Path(rel_path)
        assert target_path.exists(), f"Referenced path {rel_path} does not exist on disk"


def test_work_yaml_template_validity():
    template_file = REPO / ".agents" / "skills" / "transcribe" / "templates" / "work.yaml"
    assert template_file.exists(), f"Missing template: {template_file}"

    data = yaml.safe_load(template_file.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "Template must be valid YAML mapping"

    required_fields = ["id", "title", "authors", "publication", "edition", "discipline", "tags", "language", "type", "source", "sources"]
    for field in required_fields:
        assert field in data, f"Template missing required field: {field}"

    assert isinstance(data["authors"], list) and len(data["authors"]) > 0
    assert "wikidata_id" in data["authors"][0]
    assert "death_year" in data["authors"][0]
    assert "year" in data["publication"]


def test_skills_branch_isolation_and_worktrees():
    skills = [
        REPO / ".agents" / "skills" / "transcribe" / "SKILL.md",
        REPO / ".claude" / "skills" / "transcribe" / "SKILL.md",
    ]

    for skill_file in skills:
        assert skill_file.exists(), f"Missing skill file: {skill_file}"
        content = skill_file.read_text(encoding="utf-8")

        # Phase 1 must contain branch isolation and worktree instruction
        assert "git checkout -b transcribe/<work-id> origin/main" in content, (
            f"{skill_file} missing Phase 1 branch creation instruction"
        )
        assert "git worktree add ../rtm-<work-id> -b transcribe/<work-id> origin/main" in content, (
            f"{skill_file} missing worktree instruction"
        )

        # Phase 8 must NOT instruct creating the branch again
        phase_8_idx = content.find("## Phase 8")
        assert phase_8_idx != -1, f"Missing Phase 8 in {skill_file}"
        phase_8_text = content[phase_8_idx:]
        assert "git checkout -b" not in phase_8_text, (
            f"{skill_file} must not run 'git checkout -b' in Phase 8; branch is established in Phase 1"
        )
        assert "git worktree remove" in phase_8_text, (
            f"{skill_file} must document worktree cleanup in Phase 8"
        )

