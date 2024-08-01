import os
import aiohttp

from magic_crawler.crawler import global_user_agent


async def extract_text_from_url_crawler_jina(url):
    headers = {
        'User-Agent': global_user_agent,
        'token-access': os.environ['CRAWLER_TOKEN_ACCESS_JINA']
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(f'https://r.jina.ai/{url}') as response:
                markdown = await response.read()
                return {
                    'markdown': markdown
                }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
