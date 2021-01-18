r"""translate text dia deepl up to 5000 chars.

cf deepl-tr-async-free\deepl_tr_async\deepl_tr_async.py
"""
# pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements

from typing import (
    # List,
    Optional,
    # Tuple,
    Union,
)

from pathlib import Path
import re
import asyncio
from urllib.parse import quote

from pyppeteer import launch
from pyquery import PyQuery as pq
from itertools import zip_longest
import logzero
from logzero import logger

# from deepl_tr_pp.load_env import load_env
from deepl_tr_pp.config import Settings

URL = r"https://www.deepl.com/translator"
LOOP = asyncio.get_event_loop()

_ = """
try:
    HEADFUL = bool(load_env("headful", "bool"))
except Exception as exc:
    logger.info("exc: %s", exc)
    HEADFUL = False
try:
    DEBUG = bool(load_env("DEBUG", "bool"))
except Exception as exc:
    logger.info("exc: %s", exc)
    DEBUG = False
try:
    PROXY = str(load_env("PROXY", "str"))
except Exception as exc:
    logger.info("exc: %s", exc)
    PROXY = ""
# """
CONFIG = Settings()  # CONFIG = Settings(env=dotenv.find_dotenv())
HEADFUL = CONFIG.headful
DEBUG = CONFIG.debug
PROXY = "" if CONFIG.proxy is None else CONFIG.proxy

logger.info(" HEADFUL: %s", HEADFUL)
logger.info(" DEBUG: %s", DEBUG)
logger.info(" PROXY: %s", PROXY)


# fmt: off
async def get_ppbrowser(
        headless: bool = not HEADFUL,
        proxy: Optional[str] = PROXY,
        executable_path: Optional[Union[str, Path]] = None,
):
    # fmt: on
    """Get a puppeeter browser.

    headless=not HEADFUL; proxy: str = PROXY
    """
    # half-hearted attempt to use an existing chrome
    if Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe").exists():
        executable_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    elif Path(r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe").exists():
        executable_path = r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    try:
        browser = await launch(
            args=[
                "--disable-infobars",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "--window-size=1440x900",
                # "--autoClose=False",
                # f"--proxy-server={PROXY}",
                f"--proxy-server={proxy}",
                "--disable-popup-blocking",  #
            ],
            executablePath=executable_path,  # use chrome
            # autoClose=False,
            headless=headless,
            dumpio=True,
            userDataDir="",
        )
    except Exception as exc:
        logger.error("get_ppbrowser exc: %s", exc)
        raise
    # page = await browser.newPage()
    # await page.goto(url)
    # logger.debug("page.goto deepl time: %.2f s", default_timer() - then)
    return browser


try:
    BROWSER = LOOP.run_until_complete(get_ppbrowser(not HEADFUL))
except Exception as exc:
    logger.error(" Unable to pyppeteer.launch exc: %s", exc)
    logger.info(
        "\n\t%s",
        r"Possible cause: abnormal exit from a previous session. Try `taskkill /f /im chrome.exe`",
    )
    logger.warning(" %s", "Note that this will also kill your chrome browser.")
    raise SystemExit(1)


# fmt: off
# browser = LOOP.run_until_complete(get_ppbrowser(not HEADFUL))
async def deepl_tr_pp(  # noqa: C901
        text: str,
        from_lang: str = "en",  # "auto",
        to_lang: str = "zh",  # "auto",
        # headless: bool = not HEADFUL,
        debug: bool = DEBUG,  # DEEPLTR_DEBUG in os.envrions and .env
        # proxy: Optional[str] = None,
        # waitfor: Optional[float] = None,
        browser=BROWSER,
        sep: str = "\n_x_\n",  # in separate line in order to be kept
) -> Optional[str]:
    """Deepl via pyppeteer.

    from_lang = 'en'
    to_lang = 'zh'
    debug = 1
    """
    # fmt: on

    if debug:
        logzero.loglevel(10)
    else:
        logzero.loglevel(20)

    try:
        text = text.strip()
    except Exception as exc:
        logger.error(" text.strip() exc: %s, exiting", exc)
        raise SystemExit(1)

    if not text:
        logger.warning(" Empty text for whatever reason, end")
        return ""

    langs = ["en", "de", "zh", "fr", "es", "pt", "it", "nl", "pl", "ru", "ja"]

    try:
        from_lang = from_lang.lower().strip()
    except Exception as exc:
        from_lang = "en"
        logger.warning("%s, setting to en", exc)
    try:
        to_lang = to_lang.lower().strip()
    except Exception as exc:
        to_lang = "zh"
        logger.warning("%s, setting to zh", exc)

    if from_lang not in langs:
        logger.warning(" from_lang [%s] not in the langs set %s, setting to en", from_lang, langs)
        from_lang = "en"
    if to_lang not in langs:
        logger.warning(" to_lang [%s] not in the langs set %s, setting to zh", to_lang, langs)
        to_lang = "zh"

    if from_lang == to_lang:
        logger.warning(
            " from_lang [%s] and to_lang [%s] are idnetical, nothing to do",
            from_lang,
            to_lang,
        )
        return text

    # try to start a page
    count = 0
    while count < 3:
        count += 1
        try:
            page = await browser.newPage()
            break
        except Exception as exc:
            logger.error(" browser.newPage exc: %s, failed attempt: %s", exc, count)
            await asyncio.sleep(0)
    else:
        # giving up
        logger.error("Cant launch a page, tried three times, giving up...")
        return

    # set timeout to 10 min for headless, no timeout headful
    # for 5000 chars
    if HEADFUL:
        page.setDefaultNavigationTimeout(0)
    else:
        page.setDefaultNavigationTimeout(600000)  # 10 min

    # remove |][ which seem to interfer with \n_x_\n
    text = re.sub(r"[ |[\]]+", " ", text)
    _ = [elm.strip() for elm in text.splitlines() if elm.strip()]
    len0 = len(text.splitlines())
    text = sep.join(_)
    if len(text) > 5000:
        text = text[:5000]
        logger.warning(" text length (%s) > 5000, trimming to 5000", len(text))

    url_ = f"{URL}#{from_lang}/{to_lang}/{quote(text)}"

    count = 0
    while count < 3:
        count += 1
        try:
            # await page.goto(url_)
            await page.goto(url_, {"timeout": 600000})
            # await page.goto(url_, {"timeout": 0})
            break
        except Exception as exc:
            await asyncio.sleep(0)
            page = await browser.newPage()
            logger.warning("page.goto exc: %s, attempt %s", str(exc)[:100], count)
    else:
        # return
        raise Exception("Unable to fetch %s..." % url_[:20])

    # send text
    count = 0
    while count < 3:
        count += 1
        try:
            # await page.goto(url_)
            await page.goto(url_, {"timeout": 600000})
            # await page.goto(url_, {"timeout": 0})
            break
        except Exception as exc:
            await asyncio.sleep(0)
            page = await browser.newPage()
            logger.warning("page.goto exc: %s, attempt %s", str(exc)[:100], count)
    else:
        # return
        raise Exception("Unable to fetch %s... tried 3 timse" % url_[:20])

    # wait for input area ".lmt__source_textarea"
    try:
        # await page.waitFor(".lmt__message_box2__content")
        await page.waitForSelector(".lmt__source_textarea", {"timeout": 600000})  # ms
        logger.debug(" *** .lmt__source_textarea success")
    except TimeoutError as exc:
        if debug:
            logger.error("Timedout: %s, ", exc)
            logger.error("text: %s", text)
        # await asyncio.sleep(3 * 60000)
    except Exception as exc:
        # raise
        logger.error("wait for input area exc: %s, ", exc)

    # page content
    try:
        content = await page.content()
    except Exception as exc:
        logger.warning(" page.waitFor exc: %s", exc)
        content = '<div class="lmt__translations_as_text">%s</div>' % exc

    # processing html
    doc = pq(content)
    res = doc(".lmt__translations_as_text").text()

    count = -1
    while count < 50:
        count += 1
        logger.debug(" extra %s x 10 s", count + 1)
        await page.waitFor(10000)

        content = await page.content()
        doc = pq(content)
        res = doc(".lmt__translations_as_text").text()
        if res:
            break
        await asyncio.sleep(0)
        await asyncio.sleep(0)

    # logger.debug("res: %s", res.splitlines()[-3:])
    logger.debug("res: %s", res.split(sep.strip())[-3:])

    res = res.replace(sep.strip(), "\n")

    if not debug:
        ...
    await page.close()

    # warn if # of paras not match
    _ = len(res.splitlines())
    if not len0 == _:
        logger.error(" # of original paras (%s) not match # of translated paras (%s)", len0, _)
        logger.error(" something weird may have occurred.")
        logger.error(" But we proceed nevertheless.")

    await asyncio.sleep(0.1)

    # copy('\n'.join(wrap(res, 45)))
    # logger.info('exit: %s', text[:200])

    # make up some lines when necessary
    return res + "\n " * min(0, _ - len0)
