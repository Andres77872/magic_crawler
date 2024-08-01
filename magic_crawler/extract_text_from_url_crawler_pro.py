import os
import ssl
import urllib.request
import aiohttp

from magic_crawler.crawler import global_user_agent, convert_html_to_markdown

ssl._create_default_https_context = ssl._create_unverified_context

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': os.environ['CRAWLER_PROXY'],
         'https': os.environ['CRAWLER_PROXY']}))


async def extract_text_from_url_crawler_pro(url, **kwargs):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.get(url,
                               headers={
                                   'User-Agent': global_user_agent
                               },
                               proxy=os.environ['CRAWLER_PROXY'],
                               ssl=False) as response:
            data = await response.read()
            return {
                'raw': data.decode(),
                **convert_html_to_markdown(data, **kwargs)
            }
