import csv
import asyncio
import nest_asyncio
from pyppeteer import launch
#from pyppeteer_stealth import stealth

SELECTOR = '#root > div.css-ynz9y9 > div:nth-child(2) > div > div.css-1633bsf > div > div.css-1pcha61 > div > div.css-1633bsf > div > table > tbody>tr'
OLD_ARRAY = []
NEW_ARRY = []

async def launch_webpage():
    # browser = await launch(headless=True)
    # browser = await launch(headless=True, executablePath='/usr/bin/chromium-browser')
    browser = await launch(headless=True, executablePath='/usr/bin/chromium-browser', args=['--no-sandbox'])
    page = await browser.newPage()
    #await stealth(page)
    #await page.goto('https://play.pakakumi.com/')
    try:
        await page.goto('https://play.pakakumi.com/')
    except pyppeteer.errors.PageError as e:
        print(f"Page navigation failed: {e}")
    await page.waitForSelector(SELECTOR)
    tr_elements = await page.querySelectorAll(SELECTOR)
    
    with open('output/pakakumi_odds.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        OLD_ARRAY.extend(NEW_ARRY)
        NEW_ARRY.clear()
        for tr_element in tr_elements:
            text_content = await page.evaluate('(trElement) => trElement.textContent', tr_element)
            NEW_ARRY.append(text_content.replace('x___',''))
        set1 = set(NEW_ARRY)
        set2 = set(OLD_ARRAY)
        new_odds = list(set1.difference(set2))
        print("Writing to CSV ...")
        for odd in new_odds:
            csv_writer.writerow(odd)
        print("Done")
    
    return browser
async def main(runs):
    while runs > 0:
        print(f'{runs-1} Remaining...')
        browser = await launch_webpage()
        await asyncio.sleep(45)
        await browser.close()
        runs = runs-1

nest_asyncio.apply()
new_loop = asyncio.new_event_loop()
asyncio.get_event_loop_policy().set_event_loop(new_loop)
new_loop.run_until_complete(main(runs=10000))
