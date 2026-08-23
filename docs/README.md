# Docs Workflow

This folder is structured as a bilingual tutorial website.

## Source of Truth

`docs/zh/` is the canonical source. Write new tutorials and edits there first.

`docs/en/` mirrors the same filenames and chapter order. English files include a `source_hash` front matter value generated from the corresponding Chinese file.

## Sync English Pages

Set `OPENAI_API_KEY`, then run:

```bash
python scripts/sync_english_docs.py
```

Optional environment variables:

- `OPENAI_MODEL`: defaults to `gpt-5-mini`
- `OPENAI_BASE_URL`: defaults to `https://api.openai.com/v1`

Use `--check` in CI or before publishing:

```bash
python scripts/sync_english_docs.py --check
```

This exits with a non-zero status if any English page is missing or stale.

## Writing Convention

- Chinese pages should be product-oriented, practical, and tutorial-first.
- Every core article must contain a `## 产品视角` section following `ARTICLE_TEMPLATE.md`.
- Start from the user problem and product decision before introducing architecture terminology.
- Include both a user experience flow and a system execution flow.
- English pages should preserve headings, code blocks, diagrams, file paths, commands, and terminology.
- Keep examples runnable and dependency-light.
