#!/usr/bin/env python3
"""Emit a Markdown inventory table (size + short sha256) for handoff documents.

Usage:
    python inventory.py <path> [<path> ...]

Directories are walked recursively. Zip-family archives (.zip, .skill, .docx, .xlsx,
.pptx, .jar, .epub) are listed by member rather than hashed as a container: repacking changes
the container bytes even when nothing inside changed, so a container hash produces false
drift alarms. Hashing the members instead means the inventory only moves when the content
actually does.
"""

import hashlib
import os
import sys
import zipfile

ARCHIVE_EXTS = {".zip", ".skill", ".docx", ".xlsx", ".pptx", ".jar", ".epub"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".idea", ".vscode"}
HASH_LEN = 12


def short_hash(data):
    return hashlib.sha256(data).hexdigest()[:HASH_LEN]


def rows_for_archive(path):
    """One row per member, so the inventory tracks content rather than packaging."""
    rows = []
    try:
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                rows.append((
                    "{}!{}".format(os.path.basename(path), info.filename),
                    info.file_size,
                    short_hash(z.read(info.filename)),
                ))
    except (zipfile.BadZipFile, OSError) as exc:
        rows.append((os.path.basename(path), 0, "unreadable: {}".format(exc)))
    return rows


def rows_for_file(path, display):
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return [(display, 0, "unreadable: {}".format(exc))]
    return [(display, len(data), short_hash(data))]


def collect(target):
    if os.path.isdir(target):
        rows = []
        for root, dirs, files in os.walk(target):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(files):
                full = os.path.join(root, name)
                rel = os.path.relpath(full, target).replace(os.sep, "/")
                if os.path.splitext(name)[1].lower() in ARCHIVE_EXTS:
                    rows.extend(rows_for_archive(full))
                else:
                    rows.extend(rows_for_file(full, rel))
        return rows
    if os.path.splitext(target)[1].lower() in ARCHIVE_EXTS:
        return rows_for_archive(target)
    return rows_for_file(target, os.path.basename(target))


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 1

    missing = [t for t in argv if not os.path.exists(t)]
    for t in missing:
        print("not found: {}".format(t), file=sys.stderr)

    rows = []
    for target in argv:
        if os.path.exists(target):
            rows.extend(collect(target))

    if not rows:
        print("nothing to inventory", file=sys.stderr)
        return 1

    print("| File | Bytes | sha256 |")
    print("|---|---:|---|")
    for name, size, digest in rows:
        print("| `{}` | {} | `{}` |".format(name, size, digest))

    # A missing path still fails the run even when other paths produced rows: a silently
    # incomplete inventory is worse than none, since the handoff reader trusts it.
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
