"""Utility functions for scraping articles from the web."""

from langchain_community.document_loaders import WebBaseLoader
from newspaper import Article


def scrape(url: str) -> str:
    """
    Scrape an article from the web.

    Args:
        url (str): url of the article to scrape

    Returns:
        str: text of the article
    """
    loader = WebBaseLoader(url)
    data = loader.load()
    return data[0].page_content
