# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/5/27
# @File     : test.py
# @Software : PyCharm
import httpx
import asyncio


async def get():
    headers = {
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        # "cookie": "x5sec=7b22617365727665722d6c617a6164613b32223a226532653739386330366466313465656132633265393339316566633665336561434f507175345547454c2b5975504c396f643677574443633463657941773d3d227d; hng=MY|en-MY|MYR|458; hng.sig=3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0",
        "pragma": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }

    async with httpx.AsyncClient(http2=True, proxies="http://127.0.0.1:8888", verify=False) as client:
        response = await client.get('https://www.lazada.com.my/shop-electronic-cigarettes/?ajax=true&page=5', headers=headers)
        print(response.http_version)  # "HTTP/1.0", "HTTP/1.1", or "HTTP/2".
        print(response.text)


if __name__ == '__main__':
    asyncio.run(get())
