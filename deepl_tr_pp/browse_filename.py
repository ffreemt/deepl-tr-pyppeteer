r"""Browse for a filename.

https://pythonspot.com/tk-file-dialogs/
filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
"""
# import sys
from pathlib import Path

import tkinter
from tkinter import filedialog


# fmt: off
def browse_filename(
        initialdir=Path.cwd(),
        title="Select a file",
        filetypes=(
            ("text files", "*.txt"),
            ("docx files", "*.docx"),
            # ("gzip files", "*.gz"),
            # ("bzip2 files", "*.bz2"),
            ("all files", "*.*"),
        )
):
    # fmt: on
    """Browse for a filename.

    or None when cancelled.
    """
    root = tkinter.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(
        parent=root,
        initialdir=initialdir,
        title=title,
        filetypes=filetypes,
    )
    return filename
