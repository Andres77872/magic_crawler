import os
import aiohttp

from magic_crawler.crawler import global_user_agent, convert_html_to_markdown


async def extract_text_from_url_crawler_local(url,
                                              headers=None,
                                              cookies=None,
                                              **kwargs):
    async with aiohttp.ClientSession(headers={
        'User-Agent': global_user_agent,
        'token-access': os.environ['CRAWLER_TOKEN_ACCESS']
    }) as session:
        try:
            data = {
                'url': url,
                'timeout': 2
            }
            if headers is not None:
                data.update(headers)
            if cookies is not None:
                data.update(cookies)

            async with session.post('https://crawler.arz.ai/',
                                    data=data) as response:
                html = await response.read()
                return {
                    'raw': html.decode(),
                    **convert_html_to_markdown(html, **kwargs)
                }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
