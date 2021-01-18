# deepl-tr-pyppeteer
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ba7c2468eb574642892676deafb98ecc)](https://www.codacy.com/gh/ffreemt/deepl-tr-pyppeteer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/deepl-tr-pyppeteer&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-tr-pp.svg)](https://badge.fury.io/py/deepl-tr-pp)

deepl translate via pyppeteer

## Installation
```bash
pip install deepl-tr-pp
```
To update to the latest version:
```bash
pip install deepl-tr-pp -U
# poetry add deepl-tr-pp@latest  # if you use poetry
```
or clone the github repo, install and run from the source
```bash
git clone clone https://github.com/ffreemt/deepl-tr-pyppeteer
cd deepl-tr-pyppeteer
pip install poetry
poetry install --no-dev

poetry run python -m deepl_tr_pp  # equivalent to executing `deepl-tr-pp` below
```

## Usage
Languages supported: `["en", "de", "zh", "fr", "es", "pt", "it", "nl", "pl", "ru", "ja"]` (currently supported by the website)

Input file formats currently supported: txt and docx, files with other suffix (e.g., .csv, .tsv) will simply treated as text.

To interrupt anytime: `Ctrl-c`. The first few versions may not run too smoothly. If it hangs, press `control` and `c` at the same time to exit.

```bash
deepl-tr-pp -p file.txt  # en to zh, default en to zh, dualtext output, docx format
deepl-tr-pp -p file.txt -f de   # de to zh
deepl-tr-pp -p file.txt -f de -t en  # de to en

deepl-tr-pp   # browse for a file, en to zh

deepl-tr-pp --copyfrom   # text from the clipboard, en to zh

deepl-tr-pp -p file.txt --nodualtext  # en to zh, default en to zh, just translate text

deepl-tr-pp -p file.txt --nooutput-docx  # default en to zh, dualtext, text format
```

By default, the text version of the output is copied to the clipboard, turn this off by --nocopyto
```bash
deepl-tr-pp -p file.txt --nocopyto
```

### Finer Control Using .env and Environ Variables
To show the browser in action or set debug or proxy, create an `.env` file and set the corresponding environ variables (these can also be set from the command line, e.g., `set DEEPLTR_HEADFUL=true` (in Windows) or `export DEEPLTR_HEADFUL=true` (in Linux) ):
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
```bash
  --[no]copyfrom: copy from clipboard, default false, will attempt to browser
    for a filepath if copyfrom is set false)
    (default: 'false')
  --[no]copyto: copy the result to clipboard
    (default: 'true')
  --[no]debug: print debug messages.
    (default: 'false')
  -d,--[no]dualtext: dualtext or no dualtext output
    (default: 'true')
  -p,--filepath: source text filepath (relative or absolute), if not provided,
    clipboard content will be used as source text.
    (default: '')
  -f,--from-lang: source language, default english)
    (default: 'en')
  -o,--[no]output-docx: output docx or text
    (default: 'true')
  -t,--to-lang: target language, default chinese
    (default: 'zh')
  --[no]version: print version and exit
    (default: 'false')
```
or

```bash
deepl-tr-pp --helpfull
```

## For Developers
  * Install `poetry` the way you like it.

  * git clone the repo `https://github.com/ffreemt/deepl-tr-pyppeteer`,
`cd deepl-tr-pyppeteer`
    * Or fork first and `git pull` your own repo.

  * `poetry install`

  * Activate the virtual environment, e.g., `.venv\Scripts\activate` (In Windows) or `source .venv/bin/activate` (in Linux) provided you set `poetry config --local virtualenvs.in-project true`
    * `python -m deepl_tr_pp`

  * Code and optionally submit PR
