
# HTML to Markdown Crawler

This project provides a set of tools to extract and convert HTML content from URLs to Markdown format.
It includes functions to clean HTML, convert it to Markdown,
and retrieve content from different sources using asynchronous requests.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)

## Installation

To use this project, you need to install the required Python packages. You can do this using pip:

```bash
pip install beautifulsoup4 aiohttp html2text
```

## Usage

### Extracting Text from URLs

There are three methods provided to extract text from URLs using different crawlers.

```python
from magic_crawler import (extract_text_from_url_crawler_local,
                           extract_text_from_url_crawler_pro,
                           extract_text_from_url_crawler_jina)

url = 'https://example.com'
res = await extract_text_from_url_crawler_local(url)
print('MD', res['markdown'])

```

## Environment Variables

Ensure you set the following environment variables for the project to function correctly:

- `CRAWLER_PROXY`: Proxy URL to be used for HTTP and HTTPS requests.
- `CRAWLER_TOKEN_ACCESS_JINA`: Access token for Jina crawler.
- `CRAWLER_TOKEN_ACCESS`: Access token for the local crawler.
