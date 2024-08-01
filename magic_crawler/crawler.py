from bs4 import BeautifulSoup
import html2text
from markdownify import MarkdownConverter

global_user_agent = 'magic-llm https://arz.ai'


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
