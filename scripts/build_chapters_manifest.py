from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
OUT_PATH = ROOT / "site" / "chapters.json"
SITE_BASE_URL = "https://bettyxu2001.github.io/agent-architecture-from-scratch"
REPO_BASE_URL = "https://github.com/BettyXu2001/agent-architecture-from-scratch/blob/main/docs"
REQUIRED_FIELDS = ["id", "slug", "order", "section", "status", "title", "description", "updated_at"]
VALID_STATUS = {"complete", "draft", "planned", "legacy"}
LANGS = {"zh": "zh-CN", "en": "en-US"}
IGNORE_NAMES = {"index.md", "README.md"}
SECTION_LABELS = {
    "overview": "00 Overview",
    "workflows": "01 Workflows",
    "single-agent": "02 Single Agent",
    "planning": "03 Planning",
    "context": "04 Context",
    "memory": "05 Memory",
    "multi-agent-fundamentals": "06 Multi-Agent Fundamentals",
    "multi-agent-patterns": "07 Multi-Agent Patterns",
    "hierarchical": "08 Hierarchical",
    "communication": "09 Communication",
    "protocols": "10 Protocols",
    "orchestration": "11 Orchestration",
    "coordination-scheduling": "12 Scheduling",
    "scheduling": "12 Scheduling",
    "governance": "13 Governance",
    "reliability": "14 Reliability",
    "evaluation-observability": "15 Evaluation",
    "evaluation": "15 Evaluation",
    "framework-comparison": "16 Framework Comparison",
    "real-system": "17 Real System",
    "product-foundations": "Product Foundations",
    "basic-agent-loop": "Basic Agent Loop",
}
ORDER_BASES = {
    "OR": 1200,
    "SC": 1300,
    "GV": 1400,
    "RL": 1500,
    "EV": 1600,
    "FC": 1700,
    "RS": 1800,
}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text

    meta: dict[str, Any] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = parse_scalar(value.strip())

    body = "\n".join(lines[end + 1:]).lstrip("\n")
    if text.endswith("\n"):
        body += "\n"
    return meta, body


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in DOCS_DIR.rglob("*.md")
        if path.name not in IGNORE_NAMES and "__pycache__" not in path.parts
    )


def lang_for(path: Path) -> str:
    rel = path.relative_to(DOCS_DIR)
    if rel.parts and rel.parts[0] in LANGS:
        return LANGS[rel.parts[0]]
    raise ValueError(f"Cannot infer language from {path}")


def article_slug(path: Path) -> str:
    rel = path.relative_to(DOCS_DIR).with_suffix("")
    return "/".join(rel.parts)


def site_url(slug: str) -> str:
    return f"{SITE_BASE_URL}/{slug}/"


def repo_url(path: Path) -> str:
    rel = path.relative_to(DOCS_DIR).as_posix()
    return f"{REPO_BASE_URL}/{rel}"


def section_from_path(path: Path) -> str:
    rel = path.relative_to(DOCS_DIR)
    if len(rel.parts) == 2 and rel.parts[0] in LANGS:
        return "basic-agent-loop"
    dirname = rel.parts[1] if rel.parts[0] in LANGS and len(rel.parts) > 2 else rel.parts[0]
    return re.sub(r"^\d{2}-", "", dirname)


def section_label(section: str) -> str:
    return SECTION_LABELS.get(section, section.replace("-", " ").title())


def derived_order(meta: dict[str, Any]) -> int | None:
    if isinstance(meta.get("order"), int):
        return meta["order"]
    match = re.fullmatch(r"([A-Z]{2})(\d{2})", str(meta.get("id", "")))
    if not match:
        return None
    base = ORDER_BASES.get(match.group(1))
    if base is None:
        return None
    return base + int(match.group(2))


def first_problem_statement(body: str) -> str:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "## 它解决什么问题":
            for candidate in lines[index + 1:]:
                text = candidate.strip()
                if text and not text.startswith("#"):
                    return text
    for line in lines:
        text = line.strip()
        if text and not text.startswith("#") and not text.startswith("```") and not text.startswith("~~~"):
            return text
    return ""


def normalize_meta(path: Path, meta: dict[str, Any], body: str) -> dict[str, Any]:
    normalized = dict(meta)
    normalized.setdefault("slug", article_slug(path))
    normalized.setdefault("section", section_from_path(path))
    order = derived_order(normalized)
    if order is not None:
        normalized["order"] = order
    normalized.setdefault("description", first_problem_statement(body))
    return normalized


def validate(path: Path, meta: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in meta or meta[field] == "":
            errors.append(f"{path}: missing front matter field {field}")
    if meta.get("status") and meta["status"] not in VALID_STATUS:
        errors.append(f"{path}: invalid status {meta['status']!r}")
    if "order" in meta and not isinstance(meta["order"], int):
        errors.append(f"{path}: order must be an integer")
    if meta.get("slug") and meta["slug"] != article_slug(path):
        errors.append(f"{path}: slug must be {article_slug(path)!r}")
    if meta.get("updated_at") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(meta["updated_at"])):
        errors.append(f"{path}: updated_at must be YYYY-MM-DD")
    return errors


def build_manifest() -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    errors: list[str] = []
    zh_orders: dict[int, Path] = {}
    zh_ids: dict[str, Path] = {}

    for path in markdown_files():
        meta, body = split_front_matter(path.read_text(encoding="utf-8-sig"))
        meta = normalize_meta(path, meta, body)
        path_errors = validate(path, meta)
        errors.extend(path_errors)
        if path_errors:
            continue

        locale = lang_for(path)
        article_id = str(meta["id"])
        order = meta["order"]
        if locale == "zh-CN":
            if order in zh_orders:
                errors.append(f"{path}: duplicate order {order} also used by {zh_orders[order]}")
            zh_orders[order] = path
            if article_id in zh_ids:
                errors.append(f"{path}: duplicate id {article_id} also used by {zh_ids[article_id]}")
            zh_ids[article_id] = path
        grouped[article_id][locale] = {"meta": meta, "path": path}

    if errors:
        raise SystemExit("Front matter validation failed:\n" + "\n".join(errors))

    chapters: list[dict[str, Any]] = []
    for article_id, by_lang in grouped.items():
        primary = by_lang.get("zh-CN") or by_lang.get("en-US")
        if primary is None:
            continue
        primary_meta = primary["meta"]
        section = section_label(str(primary_meta["section"]))
        title: dict[str, str] = {}
        description: dict[str, str] = {}

        for locale in ("zh-CN", "en-US"):
            if locale not in by_lang:
                continue
            meta = by_lang[locale]["meta"]
            title[locale] = str(meta["title"])
            description[locale] = str(meta["description"])

        fallback_title = title.get("zh-CN") or title.get("en-US") or str(primary_meta["title"])
        fallback_description = (
            description.get("zh-CN")
            or description.get("en-US")
            or str(primary_meta["description"])
        )
        title.setdefault("zh-CN", fallback_title)
        title.setdefault("en-US", fallback_title)
        description.setdefault("zh-CN", fallback_description)
        description.setdefault("en-US", fallback_description)

        zh_source = by_lang.get("zh-CN", primary)
        en_source = by_lang.get("en-US", primary)
        urls = {
            "zh-CN": site_url(str(zh_source["meta"]["slug"])),
            "en-US": repo_url(en_source["path"]),
        }

        chapters.append(
            {
                "id": article_id,
                "slug": primary_meta["slug"],
                "order": primary_meta["order"],
                "status": primary_meta["status"],
                "section": {
                    "zh-CN": section,
                    "en-US": section,
                },
                "title": title,
                "description": description,
                "url": urls,
            }
        )

    chapters.sort(key=lambda item: (item["order"], item["id"]))
    return chapters


def main() -> None:
    parser = argparse.ArgumentParser(description="Build site/chapters.json from Markdown front matter.")
    parser.add_argument("--output", type=Path, default=OUT_PATH)
    args = parser.parse_args()

    manifest = build_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output.relative_to(ROOT)} with {len(manifest)} chapters")


if __name__ == "__main__":
    main()
