# deepl-tr-pyppeteer
Badge](https://app.codacy.com/project/badge/Grade/83b7b2cb3ade4589812917f187a8abab)](https://www.codacy.com/gh/ffreemt/deepl-tr-pyppeteer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/deepl-tr-pyppeteer&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-tr-pyppeteer.svg)](https://badge.fury.io/py/deepl-tr-pyppeteer)
deepl translate via pyppeteer

## Installation
```bash
pip install deepl-tr-pyppeteer
```
or clone the github repo and install from source
```bash
git clone https://github.com/ffreemt/deepl-tr-pyppeteer
cd deepl-tr-pyppeteer
pip install poetry
poetry install --no-dev
```

## Usage
```bash
deepl-tr-pp -p file.txt -f en -t zh
```
### Finer Control Using .env and Environ Variables
To show the browser in action or set debug or set proxy, create `.env` and set the corresponding environ variables (these can also be set from the command line, e.g., `set DEEPLTR_HEADFUL=true`):
```bash
# .env
DEEPLTR_HEADFUL=true
DEEPLTR_DEBUG=true

# DEEPLTR_HEADFUL=True
# DEEPLTR_HEADFUL=tRue  # also works
# DEEPLTR_HEADFUL=False
# DEEPLTR_HEADFUL=fAlse
# DEEPLTR_HEADFUL=1
# DEEPLTR_HEADFUL='1'
# must use capitals
# DEEPLTR_PROXY=SOCKS5://127.0.0.1:1080

```

## Help
```bash
deepl-tr-pp  --helpshort
```
or

```bash
deepl-tr-pp --helpfull
```