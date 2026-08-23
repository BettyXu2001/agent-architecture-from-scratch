import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZH_DIR = ROOT / "docs" / "zh"
EN_DIR = ROOT / "docs" / "en"


class DocsStructureTests(unittest.TestCase):
    def test_english_docs_mirror_chinese_filenames(self):
        zh_files = {path.name for path in ZH_DIR.glob("*.md")}
        en_files = {path.name for path in EN_DIR.glob("*.md")}

        self.assertEqual(zh_files, en_files)

    def test_chinese_docs_are_canonical_source(self):
        for path in ZH_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("lang: zh", text)

    def test_english_docs_track_source_file(self):
        for path in EN_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("lang: en", text)
            self.assertIn(f"source: ../zh/{path.name}", text)
            self.assertIn("source_hash:", text)


if __name__ == "__main__":
    unittest.main()
