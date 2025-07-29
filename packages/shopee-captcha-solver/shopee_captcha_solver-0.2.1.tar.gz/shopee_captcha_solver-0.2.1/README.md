# Shopee Captcha Solver API
This project is the [SadCaptcha Shopee Captcha Solver](https://www.sadcaptcha.com/shopee-captcha-solver?ref=shopeeghclientrepo) API client.
The purpose is to make integrating SadCaptcha into your Selenium, Playwright, or Async Playwright app as simple as one line of code.
Instructions for integrating with Selenium, Playwright, and Async Playwright are described below in their respective sections.

The end goal of this tool is to solve every single Shopee captcha. 
Currently we are able to solve the crawling image and the puzzle slide:

<div align="center">
    <img src="https://sadcaptcha.b-cdn.net/shopee-image-crawl-captcha.png" width="200px" height="150px" alt="Shopee Captcha Solver">
    <img src="https://sadcaptcha.b-cdn.net/shopee-puzzle-slide-captcha.png" width="200px" height="150px" alt="SHopee Captcha Solver">
</div>

The Crawling Image challenge is the one where there is a puzzle piece that travels in an unpredictable trajectory, and there are two possible locations where the solution may be.
This often shows up at login.
The puzzle slide is just a simple challenge that asks you to move the piece to the correct location.
    
## Requirements
- Python >= 3.10
- **If using Nodriver** - Google chrome installed on system. This is the recommended method.
- **If using Selenium** - Selenium properly installed and in `PATH`
- **If using Playwright** - Playwright must be properly installed with `playwright install`
- **Stealth plugin** - You should use the appropriate `stealth` plugin for whichever browser automation framework you are using.
    - For Selenium, you can use [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
    - For Playwright, you can use [playwright-stealth](https://pypi.org/project/playwright-stealth/)

## Installation
This project can be installed with `pip`. Just run the following command:
```
pip install shopee-captcha-solver
```

## Nodriver Client (Recommended)
Nodriver is the latest advancement in undetected automation technology, and is the recommended method for using SadCaptcha. 
Import the function `make_nodriver_solver`
This function will create an noddriver instance patched with the Shopee Captcha Solver chrome extension.
The extension will automatically detect and solve the captcha in the background, and there is nothing further you need to do.

```py
from shopee_captcha_solver.launcher import make_nodriver_solver

async def main():
    launch_args = ["--headless=chrome"] # If running headless, use this option, or headless=new
    api_key = "YOUR_API_KEY_HERE"
    # NOTE: Keyword arguments passed to make_nodriver_solver() are directly passed to nodriver.start()!
    driver = await make_nodriver_solver(api_key, browser_args=launch_args) # Returns nodriver browser 
    # ... [The rest of your code that accesses shopee goes here]
    # Now shopee captchas will be automatically solved!
```
All keyword arguments passed to `make_nodriver_solver()` are passed directly to `nodriver.start()`.

## Selenium Client 
Import the function `make_undetected_chromedriver_solver`.
This function will create an undetected chromedriver instance patched with the Shopee Captcha Solver chrome extension.
The extension will automatically detect and solve the captcha in the background, and there is nothing further you need to do.

```py
from shopee_captcha_solver import make_undetected_chromedriver_solver
from selenium_stealth import stealth
from selenium.webdriver import ChromeOptions
import undetected_chromedriver as uc

chrome_options = ChromeOptions()
# chrome_options.add_argument("--headless=chrome") # If running headless, use this option

api_key = "YOUR_API_KEY_HERE"
driver = make_undetected_chromedriver_solver(api_key, options=options) # Returns uc.Chrome instance
stealth(driver) # Add stealth if needed
# ... [The rest of your code that accesses shopee goes here]

# Now shopee captchas will be automatically solved!
```
You may also pass `ChromeOptions` to `make_undetected_chromedriver_solver()`, as well as keyword arguments for `uc.Chrome()`.

## Playwright Client
Import the function `make_playwright_solver_context`.
This function will create a playwright BrowserContext instance patched with the Shopee Captcha Solver chrome extension.
The extension will automatically detect and solve the captcha in the background, and there is nothing further you need to do.

```py
from shopee_captcha_solver import make_playwright_solver_context
from playwright.sync_api import sync_playwright

# Need this arg if running headless
launch_args = ["--headless=chrome"] 

api_key = "YOUR_API_KEY_HERE"
with sync_playwright() as p:
    context = make_playwright_solver_context(p, api_key, args=launch_args) # Returns playwright BrowserContext instance
    # ... [The rest of your code that accesses shopee goes here]

# Now shopee captchas will be automatically solved!
```
You may also pass keyword args to this function, which will be passed directly to playwright's call to `playwright.chromium.launch_persistent_context()`.
By default, the user data directory is a tempory directory that is deleted at the end of runtime.

## Async Playwright Client
Import the function `make_async_playwright_solver_context`.
This function will create an async playwright BrowserContext instance patched with the Shopee Captcha Solver chrome extension.
The extension will automatically detect and solve the captcha in the background, and there is nothing further you need to do.

```py
import asyncio
from playwright.async_api import async_playwright
from shopee_captcha_solver import make_async_playwright_solver_context

# Need this arg if running headless
launch_args = ["--headless=chrome"] 

async def main():
    api_key = "YOUR_API_KEY_HERE"
    async with async_playwright() as p:
        context = await make_async_playwright_solver_context(p, api_key, args=launch_args) # Returns playwright BrowserContext instance
        # ... [The rest of your code that accesses shopee goes here]

asyncio.run(main())

# Now shopee captchas will be automatically solved!
```
You may also pass keyword args to this function, which will be passed directly to playwright's call to `playwright.chromium.launch_persistent_context()`.
By default, the user data directory is a tempory directory that is deleted at the end of runtime.

## Contact
- Homepage: https://www.sadcaptcha.com/
- Email: greg@sadcaptcha.com
- Telegram @toughdata
