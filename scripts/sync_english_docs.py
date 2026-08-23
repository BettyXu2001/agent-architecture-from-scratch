from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZH_DIR = ROOT / "docs" / "zh"
EN_DIR = ROOT / "docs" / "en"


def source_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def front_matter_value(text: str, key: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    for line in text[4:end].splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return None


def title_from_markdown(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return "Untitled"


def translate_markdown(markdown: str, source_path: Path) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to update English docs.")

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-5-mini")
    prompt = (
        "Translate this Chinese Markdown tutorial into clear technical English.\n"
        "Preserve Markdown structure, heading levels, code fences, diagrams, file paths, "
        "commands, identifiers, and front matter delimiters. Translate prose only.\n"
        f"Source file: {source_path.as_posix()}\n\n"
        f"{markdown}"
    )
    payload = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}],
            }
        ],
    }
    request = urllib.request.Request(
        f"{base_url}/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Translation request failed: {exc.code} {detail}") from exc

    for item in data.get("output", []):
        if item.get("type") == "message":
            parts = item.get("content", [])
            text_parts = [
                part.get("text", "") for part in parts if part.get("type") == "output_text"
            ]
            if text_parts:
                return "".join(text_parts).strip() + "\n"

    raise RuntimeError("Translation response did not contain output text.")


def with_sync_front_matter(markdown: str, zh_file: Path, digest: str) -> str:
    source = f"../zh/{zh_file.name}"
    title = title_from_markdown(markdown)

    if markdown.startswith("---\n"):
        end = markdown.find("\n---\n", 4)
        body = markdown[end + 5 :] if end != -1 else markdown
    else:
        body = markdown

    return (
        "---\n"
        f"title: {title}\n"
        "lang: en\n"
        f"source: {source}\n"
        f"source_hash: {digest}\n"
        "---\n\n"
        f"{body.lstrip()}"
    )


def stale_files() -> list[tuple[Path, Path, str]]:
    stale: list[tuple[Path, Path, str]] = []
    for zh_file in sorted(ZH_DIR.glob("*.md")):
        zh_text = zh_file.read_text(encoding="utf-8")
        digest = source_hash(zh_text)
        en_file = EN_DIR / zh_file.name
        if not en_file.exists():
            stale.append((zh_file, en_file, digest))
            continue
        en_text = en_file.read_text(encoding="utf-8")
        if front_matter_value(en_text, "source_hash") != digest:
            stale.append((zh_file, en_file, digest))
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync English tutorial docs from Chinese source.")
    parser.add_argument("--check", action="store_true", help="Only report missing or stale English docs.")
    args = parser.parse_args()

    stale = stale_files()
    if args.check:
        for zh_file, en_file, _ in stale:
            print(f"stale: {zh_file.relative_to(ROOT)} -> {en_file.relative_to(ROOT)}")
        return 1 if stale else 0

    if not stale:
        print("English docs are already in sync.")
        return 0

    EN_DIR.mkdir(parents=True, exist_ok=True)
    for zh_file, en_file, digest in stale:
        zh_text = zh_file.read_text(encoding="utf-8")
        translated = translate_markdown(zh_text, zh_file.relative_to(ROOT))
        en_file.write_text(with_sync_front_matter(translated, zh_file, digest), encoding="utf-8")
        print(f"updated: {en_file.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
