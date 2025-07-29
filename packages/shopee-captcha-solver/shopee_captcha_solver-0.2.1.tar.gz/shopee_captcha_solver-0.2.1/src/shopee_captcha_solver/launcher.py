import logging
import tempfile
from typing import Any

from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc
from .download_crx import download_extension_to_unpacked

import nodriver
from playwright import sync_api
from playwright import async_api

LOGGER = logging.getLogger(__name__)

async def make_nodriver_solver(
    api_key: str,
    **nodriver_start_kwargs
) -> nodriver.Browser:
    """Create a nodriver Browser patched with SadCaptcha.
    
    Args:
        api_key (str): SadCaptcha API key
        nodriver_start_args: Keyword arguments for nodriver.start()
    """
    ext_dir = download_extension_to_unpacked()
    _patch_extension_file_with_key(ext_dir.name, api_key)
    add_extension_argument = f'--load-extension={ext_dir.name}'
    browser_args = nodriver_start_kwargs.get("browser_args")
    if isinstance(browser_args, list):
        nodriver_start_kwargs["browser_args"].append(add_extension_argument)
        LOGGER.debug("Appended add extension argument to browser args: " + add_extension_argument)
    else:
        nodriver_start_kwargs["browser_args"] = [add_extension_argument]
        LOGGER.debug("Set browser arg to " + add_extension_argument)
    nodriver_start_kwargs["browser_args"].append("--disable-features=DisableLoadExtensionCommandLineSwitch")
    chrome = await nodriver.start(**nodriver_start_kwargs)
    LOGGER.debug("created new nodriver Browser patched with sadcaptcha")
    return chrome

def make_undetected_chromedriver_solver(
    api_key: str,
    options: ChromeOptions | None = None,
    **uc_chrome_kwargs
) -> uc.Chrome:
    """Create an undetected chromedriver patched with SadCaptcha.
    
    Args:
        api_key (str): SadCaptcha API key
        options (ChromeOptions | None): Options to launch uc.Chrome with
        uc_chrome_kwargs: keyword arguments for call to uc.Chrome
    """
    if options is None:
        options = ChromeOptions()
    ext_dir = download_extension_to_unpacked()
    _patch_extension_file_with_key(ext_dir.name, api_key)
    options.add_argument(f'--load-extension={ext_dir.name}')
    options.add_argument("--disable-features=DisableLoadExtensionCommandLineSwitch")
    chrome = uc.Chrome(options=options, **uc_chrome_kwargs)
    LOGGER.debug("created new undetected chromedriver patched with sadcaptcha")
    return chrome

def make_playwright_solver_context(
    playwright: sync_api.Playwright,
    api_key: str,
    user_data_dir: str | None = None,
    **playwright_context_kwargs
) -> sync_api.BrowserContext:
    """Create a playwright context patched with SadCaptcha.
    
    Args:
        playwright (playwright.sync_api.playwright) - Playwright instance
        api_key (str): SadCaptcha API key
        user_data_dir (str | None): User data dir that is passed to playwright.chromium.launch_persistent_context. If None, a temporary directory will be used.
        **playwright_context_kwargs: Keyword args which will be passed to playwright.chromium.launch_persistent_context()
    """
    ext_dir = download_extension_to_unpacked()
    if user_data_dir is None:
        user_data_dir_tempdir = tempfile.TemporaryDirectory()
        user_data_dir = user_data_dir_tempdir.name
    _patch_extension_file_with_key(ext_dir.name, api_key)
    playwright_context_kwargs = _prepare_pw_context_args(playwright_context_kwargs, ext_dir.name)
    ctx = playwright.chromium.launch_persistent_context(
        user_data_dir,
        **playwright_context_kwargs
    )
    LOGGER.debug("created patched playwright context")
    return ctx

async def make_async_playwright_solver_context(
    async_playwright: async_api.Playwright,
    api_key: str,
    user_data_dir: str | None = None,
    **playwright_context_kwargs
) -> async_api.BrowserContext:
    """Create a async playwright context patched with SadCaptcha.
    
    Args:
        playwright (playwright.async_api.playwright) - Playwright instance
        api_key (str): SadCaptcha API key
        user_data_dir (str | None): User data dir that is passed to playwright.chromium.launch_persistent_context. If None, a temporary directory will be used.
        **playwright_context_kwargs: Keyword args which will be passed to playwright.chromium.launch_persistent_context()
    """
    ext_dir = download_extension_to_unpacked()
    if user_data_dir is None:
        user_data_dir_tempdir = tempfile.TemporaryDirectory()
        user_data_dir = user_data_dir_tempdir.name
    _patch_extension_file_with_key(ext_dir.name, api_key)
    playwright_context_kwargs = _prepare_pw_context_args(playwright_context_kwargs, ext_dir.name)
    ctx = await async_playwright.chromium.launch_persistent_context(
        user_data_dir,
        **playwright_context_kwargs
    )
    LOGGER.debug("created patched async playwright context")
    return ctx

def _prepare_pw_context_args(
        playwright_context_kwargs: dict[str, Any],
        ext: str
) -> dict[str, Any]:
    if "args" in playwright_context_kwargs.keys():
        playwright_context_kwargs["args"] = playwright_context_kwargs["args"] + [
            f"--disable-extensions-except={ext}",
            f"--load-extension={ext}",
        ]
    else:
        playwright_context_kwargs["args"] = [
            f"--disable-extensions-except={ext}",
            f"--load-extension={ext}",
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',         
            '--disable-web-security',
            '--disable-infobars',  
            '--start-maximized',  
        ]
    playwright_context_kwargs["args"].append("--disable-features=DisableLoadExtensionCommandLineSwitch")
    if playwright_context_kwargs.get("headless") == True:
        if "--headless=new" not in playwright_context_kwargs["args"]:
            _ = playwright_context_kwargs["args"].append("--headless=new")
        playwright_context_kwargs["headless"] = None
        LOGGER.debug("Removed headless=True and added --headless=new launch arg")
    LOGGER.debug("prepared playwright context kwargs")
    return playwright_context_kwargs


def _patch_extension_file_with_key(extension_dir: str, api_key: str) -> None:
    with open(extension_dir + "/script.js") as f:
        script = f.read()
    script = patch_extension_script_with_key(script, api_key)
    with open(extension_dir + "/script.js", "w") as f:
        _ = f.write(script)
    LOGGER.debug("patched extension file with api key")

def patch_extension_script_with_key(script: str, api_key: str) -> str:
    script = script.replace("return apiKey;", f"return \"{api_key}\";")
    script = script.replace("localStorage.getItem(\"sadCaptchaKey\");", "true;")
    LOGGER.debug("patched extension script with api key")
    return script
