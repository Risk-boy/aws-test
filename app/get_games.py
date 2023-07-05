import asyncio
import aiohttp
from app.config import get_secret


class GetGames:
    LOL_API = "https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5"
    API_KEY = get_secret("API_KEY")
    
    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result

    def unit_url(self, tier, division, start):
        return {
            "url": f"{self.LOL_API}/{tier}/{division}?page={start}",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://developer.riotgames.com",
                "X-Riot-Token": self.API_KEY
            }
        }

    async def search(self, tier, division, total_page):
        apis = [self.unit_url(tier, division, i + 1) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[GetGames.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)
            return result

    def run(self, tier, division, total_page):
        return asyncio.get_event_loop().run_until_complete(self.search(tier, division, total_page))


if __name__ == "__main__":
    scraper = GetGames()
    # print(scraper.run("DIAMOND", "I", 1))
    
