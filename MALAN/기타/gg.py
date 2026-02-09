import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright


async def wait_locator(locator):
    await locator.first.wait_for()
    return await locator.all()


async def crawling(item_number, params):
    res = {}
    async with async_playwright() as p:
        # 브라우저 실행 (headless=False 로 하면 실제 창이 보임)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # 페이지 접속
        await page.goto(f"https://mapleland.gg/item/{item_number}?{params}")

        # 팝니다 삽니다 목록
        locator = page.locator(".bg-gray-200.rounded.p-2")
        # locator.text
        sell_n_buy = await wait_locator(locator)
        
        # 뒤에게 삽니다 목록
        buys = sell_n_buy[-1]
        locator = buys.locator(".dark\:text-gray-200")
        
        buy_items = await wait_locator(locator)
        
        for buy_item in buy_items:
            item_root = buy_item.locator(".px-1")
            
            price_n_time = item_root.locator(".text-sm.border-t.border-black\/10.dark\:border-white\/10")
            
            nickname =await item_root.locator("a.flex.items-center.gap-1").inner_text()
            price = await price_n_time.locator(".flex.justify-between.items-center>div").inner_text()
            ago = await price_n_time.locator(".flex.justify-between.items-center>span").inner_text()
            res[nickname] = {"price": int(price.replace(",", "")), "ago": ago}
        
        await browser.close()
    return res


if __name__ == "__main__": 
    # 아이템 코드 사전
    with open("item_gg/item_number.json", "r", encoding="utf8") as f:
        item_numbers = json.load(f)

    # 크롤링
    item_name = "장미꽃 귀고리"
    params = "lowPrice=&highPrice=9999999999&lowincDEX=5&highincDEX=5&lowTuc=&highTuc=0"
    wanted = 4500000
    
    item_number = item_numbers[item_name]
    new_data = asyncio.run(crawling(item_number, params))

    try:
        with open(f"item_gg/{item_name}.json", "r", encoding="utf8") as f:
            exists_data = json.load(f)["data"]
        
        for k in new_data.keys():
            # 새 데이터의 닉네임이 기존 데이터에 없거나, 같은 닉이어도 기존 가격과 달라졌으면 기록
            if (k not in exists_data) or (new_data[k]["price"] != exists_data[k]["price"]):
                print(f"{k} 가 수정됨: {new_data[k]}")
                exists_data[k] = new_data[k]

                if new_data[k]["price"] >= wanted:
                    print("목표에 도달", k, new_data[k]["price"])
                    # 카톡 보내기

        integration_data = exists_data
    except:
        print("파일이 존재안함")
        integration_data = new_data

    # 가격순으로 정렬
    integration_data = dict(
        sorted(
            integration_data.items(),
            key=lambda x: x[1]["price"],
            reverse=True
        )
    )

    json_data = {
        "기록시간":datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "data": integration_data,

    }
    with open(f"item_gg/{item_name}.json", "w", encoding="utf8") as f:
        json.dump(json_data, f, ensure_ascii = False)
