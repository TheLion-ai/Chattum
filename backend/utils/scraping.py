"""Utility functions for scraping articles from the web."""

from newspaper import Article


def scrape(url: str) -> str:
    """
    Scrape an article from the web.

    Args:
        url (str): url of the article to scrape

    Returns:
        str: text of the article
    """
    article = Article(url)
    article.download()
    article.parse()
    return article.text.encode("utf-8")
