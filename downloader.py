import json
import os
import asyncio
import aiohttp
import requests
from datetime import datetime

class downloader:
    def __init__(self, params):
        self._url = 'https://api.lolicon.app/setu/v2'
        self._params = params

    def get_url(self, params):
        r = requests.get(self._url, params=params)
        content = json.loads(r.content)
        return content["data"]

    async def download(self, picture):
        try:
            if os.path.exists(f"./pictures/{picture['pid']}.{picture['ext']}"): return print(f"圖片: {picture['pid']}.{picture['ext']}已存在")
            print(f"正在下載圖片: {picture['pid']}.{picture['ext']}")
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=180)) as session:
                async with session.get(picture["urls"]["original"]) as r:
                    with open(f'./pictures/{picture["pid"]}.{picture["ext"]}', 'wb') as fd:
                        fd.write(await r.read())
            print(f"下載圖片: {picture['pid']}.{picture['ext']} 完成")
        except:
            print(f"下載圖片: {picture['pid']}.{picture['ext']} 失敗")
            os.remove(f'./pictures/{picture["pid"]}.{picture["ext"]}')

    def start(self):
        if not os.path.exists("./pictures"): os.mkdir("./pictures")
        try:
            pictures = self.get_url(self._params)
            print(f"總共獲取到 {len(pictures)} 張圖片")
            time_start = round(datetime.now().timestamp())

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = [asyncio.ensure_future(self.download(picture), loop=loop) for picture in pictures]
            loop.run_until_complete(asyncio.wait(tasks))

            time_end = round(datetime.now().timestamp())
            input(f"下載所有圖片完成, 耗時: {time_end - time_start} 秒, 按任意鍵退出...")
        except KeyboardInterrupt:
            print("已取消下載")
        except Exception as e:
            print(f"發生未知錯誤: {e}")

if __name__ == "__main__":
    print("""
        歡迎使用Pixiv圖片下載器\n
    """)

    keyword = input("關鍵詞: ")

    r18 = input("是否 R18 (y/n): ")
    if r18.lower() == "y": r18 = 1
    else : r18 = 0

    ai = input("是否包含Ai作品 (y/n): ")
    if ai.lower() == "y": ai = 1
    else : ai = 0

    num = int(input("獲取數量: "))
    if num > 20: 
        print(f"數量過多，將只下載20張圖片")
        num = 20

    params = [
        ("keyword", keyword),
        ("r18", r18),
        ("excludeAI", ai),
        ("num", num)
    ]

    download_picture = downloader(params)
    download_picture.start()
    
