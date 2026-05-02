# depdf

Lightweight python script for cleaning OceanofPDF watermarks from pirated PDFs: removes inserted links, deletes visible text of the watermark, deletes blank pages created just for inserting watermarks, and also cleans the file name and metadata. Book cover is always saved.

FEATURES

Deletes OceanofPDF hyperlink

Deletes visible text of the watermark (oceanofpdf.com)

Deletes blank pages with watermarks only (Sometimes keeps them but removes the text, I do not see this as a bug rather as a feature)

Keeps the book cover on page 1 by default

Deletes OceanofPDF from file name and metadata (title, author, etc.)

Replaces the original file on disk


Requirements

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white) or higher

PyMuPDF

# How to install
1. Install Python
2. Use the following command:
```
python -m pip install pymupdf
```
   If for some reason Terminal throws an error about app association, use 
 ```
py -m pip install pymupdf
```

   # How to use
   
   There are 2 ways to use.
   1. Drag and drop - Drag your PDF file and drop it onto depdf.py in Windows Explorer. Simple.
   2. Advanced - Terminal
   
   WINDOWS
   1. Open Terminal — press Win + R, type cmd, press Enter
Navigate to your Downloads folder:
 ```
cd C:\Users\YourName\Downloads
```
   
Run the script using your PDF's file location when you right click on it followed by copy as path:
 ```
 python clean_pdf.py "Your Book.pdf"
```
  The window will show what was cleaned and say press Enter to close when done.

MAC

Open Terminal — press Cmd + Space, type Terminal, press Enter
Navigate to your Downloads folder:
 ```
  cd ~/Downloads
```

Run the script on your PDF:
 ```
  python3 clean_pdf.py "Your Book.pdf"
```
 
The window will show what was cleaned and say Press Enter to close when done.


# Example Output
Output filename : My_Book.pdf

Opening: C:\Users\you\Downloads\OceanofPDF_My_Book - Author.pdf

Total pages: 312

  META  title: 'OceanofPDF.com - My Book - Author' -> 'My_Book - Author'
  
  KEEP  page    1: cover — always kept
  
  DROP  page    2: blank page with OceanofPDF link
  
  TEXT  page   312: erased 1 OceanofPDF text instance(s)
  

Pages dropped : 1

Pages kept    : 311


Cleaned PDF saved to: My_Book.pdf

Original size : 4821.3 KB

Output size   : 4712.6 KB


Personally, I prefer the drag and drop method over this method as it's much more efficient.

# Why did I make this?
I noticed others have made these already but I wanted to make something like this as a challenge for myself and I am proud to share it. It seems stupid to upload when you can make it yourself or there are other programs that do the same job already but I hope depdf will be your best friend.

# Found a bug/issue?
Feel free to put it in the Issues tab and I will do my best to fix it or help.

# Want to support this project?
Star it, tell your friends, spread the word. I appreciate everything you do.
