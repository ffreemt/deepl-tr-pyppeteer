"""Load text from filepath.

Currently only handles txt and docx
"""
from typing import (
    # Optional,
    Union,
)

from pathlib import Path
import re
import cchardet as chardet
import docx2txt
from logzero import logger


def load_text(filepath: Union[str, Path]) -> str:
    r"""Load text from filepath.

    Currently only handles txt and docx
    """
    fpath = Path(filepath).expanduser().resolve()
    if not fpath.is_file():
        logger.error("File (%s) does not exit or is not a file")
        logger.info("Cant do nothing, bye.")
        raise SystemExit(1)

    if fpath.suffix in [".docx"]:
        logger.info(
            "%s is a docx file, we try to convert to text (images and format will be lost.)",
            filepath,
        )
        try:
            text = docx2txt.process(fpath)
        except Exception as exc:
            logger.error("Too bad, unsuccessful, exc: %s", exc)
            logger.info("Exiting...")
            raise SystemExit(1)

    else:
        if fpath.suffix not in [".txt"]:
            logger.warning("The current version only handles docx and txt")
            logger.warning("Your file does not end with .txt")
            logger.info("We'll give it a try tho.")

        try:
            encoding = chardet.detect(fpath.read_bytes()).get("encoding")
        except Exception as exc:
            logger.error("chardet.detect exc: %s, setting encoding=utf-8", exc)
            encoding = "utf-8"

        if encoding is None:
            logger.warning("Something fishy: encoding is None.")
            logger.info("Makes no sense to go on, exiting...")
            raise SystemExit(1)

        try:
            text = fpath.read_text(encoding)
        except Exception as exc:
            logger.error(" Reading %s exc: %s", filepath, exc)
            logger.info(" Nothing more we can do for you, end.")
            raise SystemExit(1)

    text = "\n".join(
        [re.sub(r"\s+", " ", elm).strip() for elm in text.splitlines() if elm.strip()]
    )
    tot_lines = len(text.splitlines())

    logger.info(
        "Good news: we collected a total of %s paras, about %s characters",
        tot_lines,
        len(text),
    )
    _ = """
    if len(text) + (tot_lines - 1) * 5 > 5000:
        logger.warning(
            " Text too long (the current version is limited to 5000 chars), text will be trimmed."
        )
        logger.info(
            "Future versions of deepl-tr-pyppeteer will support longer text, stay tuned."
        )
    # """
    return text
