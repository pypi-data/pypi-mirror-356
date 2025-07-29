import os
import json
import shlex
import shutil
import tempfile
import subprocess
import logging
import asyncio

from os.path import dirname, join as pathjoin

from pyppeteer import launch

from placards import config
from placards.errors import ConfigError


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())
STARTUP = [
    # Hide mouse cursor.
    'unclutter',

    # Disable screen blanking and screensaver.
    'xset s noblank',
    'xset s off',
    'xset -dpms',
]
PREFERENCES_PATH = 'Default/Preferences'


async def chrome(chrome_bin, profile_dir, debug=False):
    "Launch Chrome browser and navigate to placards server."
    args = [
        '--start-maximized',
        '--start-fullscreen',
        '--no-default-browser-check',
        '--autoplay-policy=no-user-gesture-required',
    ]
    if config.getbool('IGNORE_CERTIFICATE_ERRORS', False):
        args.append('--ignore-certificate-errors')
    if not debug:
        args.extend([
            '--noerrdialogs',
            '--disable-infobars',
            '--kiosk',
        ])
    browser = await launch(
        headless=False,
        args=args,
        ignoreDefaultArgs=["--enable-automation"],
        dumpio=debug,
        executablePath=chrome_bin,
        userDataDir=profile_dir,
        defaultViewport=None,
        autoClose=False,
    )
    pages = await browser.pages()
    if len(pages):
        page = pages[0]
    else:
        page = await browser.newPage()
    return browser, page


async def goto(page, url):
    page.setDefaultNavigationTimeout(0)
    await page.goto(url, waitUntil='networkidle2')
    await page.screenshot({
        'type': 'png',
    })


def edit_json_file(path, **kwargs):
    try:
        with open(path, 'r') as f:
            o = json.load(f)
        for key, value in kwargs.items():
            o[key] = value
        with tempfile.NamedTemporaryFile('wt',
                                         prefix=dirname(path),
                                         delete=False) as f:
            json.dump(o, f)
            os.remove(path)
            os.rename(f.name, path)

    except Exception:
        LOGGER.exception('Error modifying JSON file: %s', path)


def setup(profile_dir):
    "Set up directories, permission, environment."
    # Ensure profile directory exists.
    try:
        os.makedirs(profile_dir)

    except FileExistsError:
        pass

    # Run startup commands to prepare X.
    for command in STARTUP:
        cmd = shlex.split(command)
        bin = shutil.which(cmd[0])
        if not bin:
            LOGGER.warning('Could not find program', cmd[0])
            continue
        LOGGER.debug('Running startup command', [bin, *cmd[1:]])
        subprocess.Popen(
            [bin, *cmd[1:]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # Clear away crash status from Chrome prefs.
    edit_json_file(
        pathjoin(profile_dir, PREFERENCES_PATH),
        exited_cleanly=True,
        exit_type='Normal',
    )


async def main():
    "Main entry point."
    log_level_name = config.get('LOG_LEVEL', 'ERROR').upper()
    log_level = getattr(logging, log_level_name)
    debug = (log_level_name == 'DEBUG')

    root = logging.getLogger()
    root.addHandler(logging.StreamHandler())
    root.setLevel(log_level)

    LOGGER.debug('Loading web client...')

    try:
        url = config.SERVER_URL
        chrome_bin = config.CHROME_BIN_PATH
        profile_dir = config.PROFILE_DIR

    except ConfigError as e:
        LOGGER.error(f'You must configure {e.args[0]} in config.ini!')
        return

    setup(profile_dir)

    browser, page = await chrome(chrome_bin, profile_dir, debug)
    try:
        await goto(page, url)

        while not page.isClosed():
            await asyncio.sleep(0.1)

    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
