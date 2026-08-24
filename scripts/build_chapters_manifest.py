from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
OUT_PATH = ROOT / "site" / "chapters.json"
REQUIRED_FIELDS = ["id", "order", "section", "status", "title", "description", "updated_at"]
VALID_STATUS = {"published", "draft", "planned", "legacy"}
LANGS = {"zh": "zh-CN", "en": "en-US"}
IGNORE_NAMES = {"index.md", "README.md"}


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = parse_scalar(value.strip())
    body = "\n".join(lines[end + 1:]).lstrip("\n")
    if text.endswith("\n"):
        body += "\n"
    return meta, body


def parse_scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def markdown_files() -> list[Path]:
    return sorted(
        p for p in DOCS_DIR.rglob("*.md")
        if p.name not in IGNORE_NAMES and "__pycache__" not in p.parts
    )


def lang_for(path: Path) -> str:
    rel = path.relative_to(DOCS_DIR)
    if rel.parts and rel.parts[0] in LANGS:
        return LANGS[rel.parts[0]]
    raise ValueError(f"Cannot infer language from {path}")


def article_url(path: Path) -> str:
    rel = path.relative_to(DOCS_DIR).with_suffix("")
    return "/".join(rel.parts) + "/"


def validate(path: Path, meta: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in meta or meta[field] == "":
            errors.append(f"{path}: missing front matter field {field}")
    if meta.get("status") and meta["status"] not in VALID_STATUS:
        errors.append(f"{path}: invalid status {meta['status']!r}")
    if "order" in meta and not isinstance(meta["order"], int):
        errors.append(f"{path}: order must be an integer")
    if meta.get("updated_at") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(meta["updated_at"])):
        errors.append(f"{path}: updated_at must be YYYY-MM-DD")
    return errors


def build_manifest() -> dict:
    grouped: dict[str, dict] = defaultdict(dict)
    errors: list[str] = []

    for path in markdown_files():
        meta, _ = split_front_matter(path.read_text(encoding="utf-8-sig"))
        errors.extend(validate(path, meta))
        if errors:
            continue
        locale = lang_for(path)
        article_id = str(meta["id"])
        grouped[article_id][locale] = {"meta": meta, "path": path}

    if errors:
        raise SystemExit("Front matter validation failed:\n" + "\n".join(errors))

    chapters = []
    for article_id, by_lang in grouped.items():
        primary = by_lang.get("zh-CN") or by_lang.get("en-US")
        if primary is None:
            continue
        primary_meta = primary["meta"]
        title = {}
        description = {}
        urls = {}
        for locale in ("zh-CN", "en-US"):
            if locale in by_lang:
                meta = by_lang[locale]["meta"]
                title[locale] = meta["title"]
                description[locale] = meta["description"]
                urls[locale] = article_url(by_lang[locale]["path"])

        chapter = {
            "id": article_id,
            "order": primary_meta["order"],
            "section": primary_meta["section"],
            "status": primary_meta["status"],
            "title": title,
            "description": description,
            "url": urls.get("zh-CN") or urls.get("en-US"),
            "urls": urls,
            "translation_status": "complete" if {"zh-CN", "en-US"}.issubset(by_lang) else "pending",
            "updated_at": max(str(item["meta"]["updated_at"]) for item in by_lang.values()),
        }
        chapters.append(chapter)

    chapters.sort(key=lambda item: (item["order"], item["id"]))
    now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    return {
        "project_status": "active",
        "updated_at": now,
        "curriculum_modules": 18,
        "chapters": chapters,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the public chapters manifest from Markdown front matter.")
    parser.add_argument("--output", type=Path, default=OUT_PATH)
    args = parser.parse_args()

    manifest = build_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output.relative_to(ROOT)} with {len(manifest['chapters'])} chapters")


if __name__ == "__main__":
    main()
