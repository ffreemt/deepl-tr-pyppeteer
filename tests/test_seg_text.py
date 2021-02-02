"""Test seg_text."""

from deepl_tr_pp.seg_text import seg_text


def test_seg_text1():
    """Test seg_text."""
    text = """Reformat     the single paragraph\n in 'text' so it fits in\n a b c"""

    res = seg_text(text, 10)
    assert len(res) == 7

    res = seg_text(text)
    assert len(res) == 1

    paras = text.splitlines()

    res = seg_text(paras, 10)
    assert len(res) == 7

    res = seg_text(paras)
    assert len(res) == 1
