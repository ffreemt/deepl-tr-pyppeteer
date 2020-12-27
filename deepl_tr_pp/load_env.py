"""Load .env from or parent dirs."""
from pathlib import Path
import dotenv
from environs import Env

from logzero import logger


def load_env(var="hotkey", attr="str"):
    """Load .env from or parent dirs.

    os.environ has priority
    cwd / .env
    Path(__file__).parent / .env

    load_env("debug", "bool")
    load_env("hotkey")

    """
    env = Env()
    _ = dotenv.find_dotenv(Path.cwd() / ".env")
    if not _:
        _ = dotenv.find_dotenv()
    if _:
        logger.info("Loading os.environ and .env from\n\t [%s]", _)
        env.read_env(_)
    else:
        logger.info(" No .env file found, os.environ only")

    try:
        return getattr(env, attr)(var)  # OK
    except Exception as exc:
        logger.warning('\n\t %s, return empty str ""', exc)
        return ""


def main():
    """Main."""
    print(load_env("hotkey"))


if __name__ == "__main__":
    main()
