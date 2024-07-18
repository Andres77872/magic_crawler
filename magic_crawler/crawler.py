import os
from bs4 import BeautifulSoup
import ssl
import urllib.request
import aiohttp
import html2text

ssl._create_default_https_context = ssl._create_unverified_context

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': os.environ['CRAWLER_PROXY'],
         'https': os.environ['CRAWLER_PROXY']}))

ua = 'magic-llm https://arz.ai'


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

    # Extract text content, preserving tags for html2text to convert
    cleaned_html = str(soup)

    return cleaned_html


def convert_html_to_markdown(html_content):
    # Clean the HTML content
    cleaned_html = clean_html(html_content)

    # Convert the cleaned HTML to Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    markdown_content = h.handle(cleaned_html)

    return {
        'markdown': markdown_content,
        'text': cleaned_html
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


async def extract_text_from_url_crawler_local(url):
    headers = {
        'User-Agent': ua,
        'token-access': os.environ['CRAWLER_TOKEN_ACCESS']
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post('https://crawler.arz.ai/',
                                    data={'url': url, 'timeout': 2}) as response:
                html = await response.read()
                return {
                    'raw': html.decode(),
                    **convert_html_to_markdown(html)
                }
        except Exception as e:
            print(f"Error fetching {url}: {e}")


async def extract_text_from_url_crawler_pro(url):
    headers = {
        'User-Agent': ua
    }

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, proxy=os.environ['CRAWLER_PROXY'], ssl=False) as response:
            print(response)
            data = await response.read()
            return {
                'raw': data.decode(),
                **convert_html_to_markdown(data)
            }
