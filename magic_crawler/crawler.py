import os
from bs4 import BeautifulSoup
import ssl
import urllib.request
import aiohttp
import html2text
from markdownify import MarkdownConverter

ssl._create_default_https_context = ssl._create_unverified_context

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': os.environ['CRAWLER_PROXY'],
         'https': os.environ['CRAWLER_PROXY']}))

ua = 'magic-llm https://arz.ai'


class MagicCrawlerParser(object):
    HTML2TEXT = 'html2text'
    MARKDOWNINFY = 'markdownify'


def clean_html(html_content) -> str:
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    # Remove all <script> and <style> tags
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Remove common unnecessary elements
    unnecessary_selectors = [
        'header', 'footer', 'nav', 'aside', '.ads', '.advertisement',
        '.footer', '.header', '.nav', '.sidebar', '.toc'
    ]
    for selector in unnecessary_selectors:
        for element in soup.select(selector):
            element.decompose()

    return soup


def convert_html_to_markdown(html_content, clean: bool = True, parser: str = 'html2text'):
    # Clean the HTML content
    if clean:
        cleaned_html = clean_html(html_content)
    else:
        cleaned_html = BeautifulSoup(html_content, 'html.parser')
    # Convert the cleaned HTML to Markdown
    if parser == MagicCrawlerParser.HTML2TEXT:
        h = html2text.HTML2Text()
        h.ignore_links = False
        markdown_content = h.handle(str(cleaned_html))
    elif parser == MagicCrawlerParser.MARKDOWNINFY:
        markdown_content = MarkdownConverter().convert_soup(cleaned_html)
    else:
        raise ValueError('parser must be html2text or markdownify')

    return {
        'markdown': m if type(m := markdown_content) is str else str(m),
        'text': str(cleaned_html)
    }


async def extract_text_from_url_crawler_jina(url):
    headers = {
        'User-Agent': ua,
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


async def extract_text_from_url_crawler_local(url,
                                              headers=None,
                                              cookies=None,
                                              **kwargs):
    async with aiohttp.ClientSession(headers={
        'User-Agent': ua,
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


async def extract_text_from_url_crawler_pro(url, **kwargs):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.get(url,
                               headers={
                                   'User-Agent': ua
                               },
                               proxy=os.environ['CRAWLER_PROXY'],
                               ssl=False) as response:
            data = await response.read()
            return {
                'raw': data.decode(),
                **convert_html_to_markdown(data, **kwargs)
            }
