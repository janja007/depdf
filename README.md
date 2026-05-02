# depdf
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
Lightweight python script for cleaning OceanofPDF watermarks from pirated PDFs: removes inserted links, deletes visible text of the watermark, deletes blank pages created just for inserting watermarks, and also cleans the file name and metadata. Book cover is always saved.

FEATURES

Deletes OceanofPDF link annotations
Deletes visible text of the watermark (oceanofpdf.com)
Deletes blank pages with watermarks only (Sometimes keeps them but removes the text, I do not see this as a bug rather as a feature)
Keeps the book cover on page 1 by default
Deletes OceanofPDF from file name and metadata (title, author, etc.)
Replaces the original file on disk

Requirements

Python 3.8 or higher
PyMuPDF
