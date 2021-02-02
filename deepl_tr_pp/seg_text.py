"""Segment text to paras containning no more than 5000 chars."""
# pylint:

from typing import (
    List,
    # Optional,
    Union,
)

import re
import textwrap
from logzero import logger


def seg_text(
    text: Union[str, List[str]], maxchars: int = 4500, extra: int = 5
) -> List[str]:
    """Segment text to paras containning no more than maxchars=4500 chars.

    extra \n_x_\n (5) per line
    """
    if isinstance(text, str):
        # remove blank lines
        _ = [elm.strip() for elm in text.splitlines() if elm.strip()]
        # remove non-single space
        text = [re.sub(r"\s+", " ", elm) for elm in _]

    # split paras longer than maxchars for extreme cases
    _ = []
    for para in text:
        if len(para) < maxchars:
            _.append(para)
        else:
            _.extend(textwrap.wrap(para, maxchars))

    # text = [elm[0] for elm in _]
    text = _.copy()

    res = []
    buff = []
    for elm in text:
        if len(elm) > maxchars:
            logger.warning(
                "single lines (%s) longer than limit (%s), trimming", len(elm), maxchars
            )
            elm = elm[:maxchars]

        # each additonal paras needs len(\n_x_\n) = extra
        if len("\n".join(buff + [elm])) + len(buff) * extra > maxchars:
            res.append(buff)
            buff = [elm]
        else:
            buff.append(elm)

    if buff:
        res.append(buff)

    # return res

    # _ = """
    _ = []
    for elm in res:
        _.append("\n".join(elm))

    return _
    # """
