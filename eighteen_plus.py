import time
import asyncio
from pyppeteer.launcher import launch
from pyppeteer.element_handle import ElementHandle
from bs4 import BeautifulSoup as bs

url:str = "https://www.ozon.ru/category/vibratory-i-vibromassazhery-9051/"

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50"


#For not working methond
# ageCookieTemp:dict = {
#     'name':'adult_user_birthdate',
#     'value':'1986-02-13',
# }

# confirmCookieTemp:dict = {
#     'name':'is_adult_confirmed',
#     'value':'true',
# }
# cookieTemp:dict = {
#     'domain':'.ozone.ru',
#     'path': '/',
#     'expires': -1,
#     'httpOnly':False,
#     'secure': False,
#     'session':True
#     }


async def intercept(request):
    if any(request.resourceType == _ for _ in ('stylesheet', 'image', 'font')):
        await request.abort()
    else:
        await request.continue_()

async def main():
    browser = await launch({'headless': True, 'args': ['--no-sandbox'], })
    page = await browser.newPage()
    await page.setUserAgent(useragent)
    # await page.setRequestInterception(True)
    # page.on('request', lambda req: asyncio.ensure_future(intercept(req)))
    await page.goto(url)
    #Not working method
    # cookies = await page._client.send("Network.getAllCookies")
    # cookies['cookies'].append(ageCookieTemp | cookieTemp)
    # cookies['cookies'].append(confirmCookieTemp | cookieTemp)
    # await page.setCookie(*cookies['cookies'])
    # await page.reload()
    el:ElementHandle = await page.waitForSelector('input[name="birthdate"]')
    await el.type('13.02.1986')
    el = await page.waitForSelector("button")
    await el.click()
    
    await page.waitForSelector('a[class="k1o tile-hover-target"]') #Ожидание загрузки основной страницы
    #Для ожидания ждем загрузку какого-нибудь селектора, который есть только на главной странице
    html = await page.content() #Забираем контент
    await page.close()
    with open("res.html","w",encoding="utf8") as file:
        file.write(html)
    #Используем BeautifulSoup 4 для разбора страницы
    soup = bs(html,"lxml")
    hrefList = soup.find_all('a',class_='k1o tile-hover-target')
    for item in hrefList:
        print(f"link: https://ozon.ru{item.attrs['href']}")

if __name__ == "__main__":
    eLoop = asyncio.get_event_loop()
    eLoop.run_until_complete(main())    
    print("Done")