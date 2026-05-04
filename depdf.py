#!/usr/bin/env python3
"""
depdf.py — Remove OceanofPDF hyperlinks, blank/ad pages, OceanofPDF
               text on pages, and OceanofPDF references from filename/metadata.

Usage:
    python depdf.py input.pdf [output.pdf]

If output.pdf is omitted, the file is cleaned in place (overwritten).

Requirements:
    pip install pymupdf
"""

import sys
import re
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF is required. Install it with: pip install pymupdf")


OCEAN_PATTERN = re.compile(r"[_\-\s]*oceanofpdf(\.com)?[_\-\s]*", re.IGNORECASE)
# Broader search pattern for finding text on pages (just the base phrase + .com)
OCEAN_TEXT_PATTERN = re.compile(r"oceanofpdf(\.com)?", re.IGNORECASE)


def clean_string(s: str) -> str:
    return OCEAN_PATTERN.sub("", s).strip(" _-")


def page_has_ocean_link(page: fitz.Page) -> bool:
    for link in page.get_links():
        uri = link.get("uri", "") or ""
        if OCEAN_PATTERN.search(uri):
            return True
    return False


def is_visually_blank(page: fitz.Page, text_threshold: int = 30) -> bool:
    text = page.get_text().strip()
    if len(text) >= text_threshold:
        return False
    if page.get_images(full=False):
        return False
    return True


def redact_ocean_text(page: fitz.Page) -> int:
    """Find and redact (erase) any visible OceanofPDF text on the page."""
    count = 0
    hits = page.search_for("oceanofpdf", quads=False)
    for rect in hits:
        page.add_redact_annot(rect, fill=(1, 1, 1))  # white fill
        count += 1
    # Also try with .com suffix
    hits2 = page.search_for("oceanofpdf.com", quads=False)
    for rect in hits2:
        page.add_redact_annot(rect, fill=(1, 1, 1))
        count += 1
    if count:
        page.apply_redactions()
    return count


def clean_pdf(input_path: str, output_path: str) -> None:
    src = Path(input_path).resolve()
    out = Path(output_path).resolve()

    if not src.exists():
        sys.exit(f"File not found: {input_path}")

    # ── Clean the output filename ────────────────────────────────────────────
    clean_stem = clean_string(out.stem)
    if not clean_stem:
        clean_stem = "book"
    out = out.with_stem(clean_stem)
    print(f"Output filename : {out.name}")

    print(f"Opening: {src}")
    doc = fitz.open(str(src))
    total = len(doc)
    print(f"Total pages: {total}")

    # ── Clean embedded metadata ──────────────────────────────────────────────
    meta = doc.metadata or {}
    cleaned_meta = {}
    changed_fields = []
    for key in ("title", "author", "subject", "keywords", "creator", "producer"):
        val = meta.get(key, "") or ""
        cleaned = clean_string(val)
        cleaned_meta[key] = cleaned
        if cleaned != val:
            changed_fields.append(f"{key}: '{val}' -> '{cleaned}'")
    if changed_fields:
        doc.set_metadata(cleaned_meta)
        for f in changed_fields:
            print(f"  META  {f}")
    else:
        print("  META  no OceanofPDF references found in metadata")

    # ── Process pages ────────────────────────────────────────────────────────
    pages_to_delete = []

    for i in range(total):
        page = doc[i]

        if i == 0:
            print(f"  KEEP  page {i + 1:4d}: cover — always kept")
            continue

        has_ocean = page_has_ocean_link(page)
        blank = is_visually_blank(page)

        if has_ocean and blank:
            print(f"  DROP  page {i + 1:4d}: blank page with OceanofPDF link")
            pages_to_delete.append(i)
        else:
            # Strip links
            if has_ocean:
                removed = 0
                for link in page.get_links():
                    uri = link.get("uri", "") or ""
                    if OCEAN_PATTERN.search(uri):
                        page.delete_link(link)
                        removed += 1
                if removed:
                    print(f"  KEEP  page {i + 1:4d}: stripped {removed} OceanofPDF link(s)")

            # Redact visible text
            redacted = redact_ocean_text(page)
            if redacted:
                print(f"  TEXT  page {i + 1:4d}: erased {redacted} OceanofPDF text instance(s)")

    for i in reversed(pages_to_delete):
        doc.delete_page(i)

    dropped = len(pages_to_delete)
    kept = total - dropped
    print(f"\nPages dropped : {dropped}")
    print(f"Pages kept    : {kept}")

    orig_size = src.stat().st_size

    tmp = src.with_suffix(".tmp.pdf")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()

    tmp.replace(out)
    if src != out and src.exists():
        src.unlink()
        print(f"Removed original: {src.name}")

    print(f"\nCleaned PDF saved to: {out}")
    print(f"Original size : {orig_size / 1024:.1f} KB")
    print(f"Output size   : {out.stat().st_size / 1024:.1f} KB")

    input("\nPress Enter to close...")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        input("\nPress Enter to close...")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) >= 3 else input_pdf

    clean_pdf(input_pdf, output_pdf)
