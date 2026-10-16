"""Check maintained documents and archived evidence; standard library only."""

from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED = {".git", ".runs", ".context-compactor", "__pycache__"}


def anchors(text):
    fence = r"(?ms)^([" + chr(96) + r"~]{3,})[^\n]*\n.*?^\1\s*$"
    text = re.sub(fence, "", text)
    result = set()
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        heading = re.sub(r"<[^>]+>", "", heading).lower().strip()
        result.add("".join(c for c in heading if c.isalnum() or c in "_- ").replace(" ", "-"))
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    errors = []
    documents = {}
    for path in ROOT.rglob("*.md"):
        if EXCLUDED.intersection(path.relative_to(ROOT).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
            if "\ufffd" in text:
                errors.append(f"{path.relative_to(ROOT)}: replacement character")
            documents[path.resolve()] = text
        except (OSError, UnicodeError) as error:
            errors.append(f"{path.relative_to(ROOT)}: {error}")

    links = 0
    for path, text in documents.items():
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if re.match(r"^[a-z]+://", link):
                continue
            target, _, anchor = link.partition("#")
            destination = (path.parent / unquote(target)).resolve() if target else path
            links += 1
            if not destination.is_file():
                errors.append(f"{path.relative_to(ROOT)}: missing {link}")
            elif anchor:
                content = documents.get(destination)
                if content is None or unquote(anchor).lower() not in anchors(content):
                    errors.append(f"{path.relative_to(ROOT)}: missing anchor {link}")

    cases_text = documents.get((ROOT / "evals/cases.md").resolve(), "")
    cases = re.findall(r"^## (\d{2})：(.*?)(?=^## \d{2}：|\Z)", cases_text, re.M | re.S)
    if not cases or [number for number, _ in cases] != [f"{n:02}" for n in range(1, len(cases) + 1)]:
        errors.append("evals/cases.md: missing or nonsequential cases")
    for number, body in cases:
        for label in ("**測試輸入**", "**預期行為**", "**失敗判準**"):
            if label not in body:
                errors.append(f"case {number}: missing {label}")

    archived_files = 0
    reports = 0
    manifests = sorted((ROOT / "evals/evidence").glob("*.json"))
    if not manifests:
        errors.append("evals/evidence: no archive manifest")
    for path in manifests:
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
            archive = path.parent / manifest["archive"]
            if digest(archive.read_bytes()) != manifest["sha256"]:
                errors.append(f"{archive.relative_to(ROOT)}: SHA-256 mismatch")
            with zipfile.ZipFile(archive) as package:
                expected = {item["path"] for item in manifest["files"]}
                if set(package.namelist()) != expected or len(package.namelist()) != len(expected):
                    errors.append(f"{archive.name}: archive member mismatch")
                for item in manifest["files"]:
                    data = package.read(item["path"])
                    if len(data) != item["size"] or digest(data) != item["sha256"]:
                        errors.append(f"{archive.name}/{item['path']}: content mismatch")
                    archived_files += 1
            for item in manifest["reports"]:
                report = (path.parent / item["path"]).resolve()
                data = report.read_bytes()
                json.loads(data)
                if digest(data) != item["sha256"]:
                    errors.append(f"{report.relative_to(ROOT)}: SHA-256 mismatch")
                reports += 1
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
            errors.append(f"{path.relative_to(ROOT)}: {error}")

    print(json.dumps({
        "documents": len(documents), "local_links": links, "cases": len(cases),
        "archived_files": archived_files, "reports": reports,
        "errors": errors, "passed": not errors,
    }, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
