import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime
import dateparser


class NewsScraper:
    """News article scraper that extracts content from various news websites"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 30
    
    def scrape_article(self, url):
        """
        Scrape a single news article from URL
        
        Args:
            url (str): URL of the news article
            
        Returns:
            dict: Article data including title, content, date, source
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            article_data = {
                'url': url,
                'source': self._extract_source(url),
                'title': self._extract_title(soup),
                'content': self._extract_content(soup),
                'published_date': self._extract_date(soup),
                'scraped_at': datetime.utcnow(),
                'author': self._extract_author(soup),
                'tags': self._extract_tags(soup)
            }
            
            # Clean and validate
            if not article_data['title'] or not article_data['content']:
                return None
                
            return article_data
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def _extract_source(self, url):
        """Extract source name from URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
                
            # Map known Thai news sources
            source_mapping = {
                'thairath.co.th': 'Thairath',
                'kapook.com': 'Kapook',
                'bangkokpost.com': 'Bangkok Post',
                'nationthailand.com': 'The Nation Thailand',
                'khaosod.co.th': 'Khaosod',
                'matichon.co.th': 'Matichon',
                'manager.co.th': 'Manager',
                'thaipbs.or.th': 'Thai PBS',
                'sanook.com': 'Sanook',
                'dailynews.co.th': 'Daily News'
            }
            
            return source_mapping.get(domain, domain)
            
        except Exception:
            return 'Unknown'
    
    def _extract_title(self, soup):
        """Extract article title"""
        # Try various selectors for title
        selectors = [
            'h1',
            '.headline',
            '.title',
            '.article-title',
            '.post-title',
            'h1.entry-title',
            '[property="og:title"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.get('content'):  # og:title case
                    return element.get('content').strip()
                else:
                    return element.get_text().strip()
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
            
        return None
    
    def _extract_content(self, soup):
        """Extract main article content"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
            element.decompose()
        
        # Try various selectors for content
        content_selectors = [
            '.article-content',
            '.entry-content',
            '.post-content',
            '.content',
            '.article-body',
            '[property="articleBody"]',
            '.story-body',
            '.news-content'
        ]
        
        content_text = ""
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    content_text += element.get_text() + "\n"
                break
        
        # If no specific content area found, try to extract from paragraphs
        if not content_text.strip():
            paragraphs = soup.find_all('p')
            content_text = '\n'.join([p.get_text() for p in paragraphs if len(p.get_text().strip()) > 50])
        
        # Clean up content
        content_text = re.sub(r'\s+', ' ', content_text).strip()
        content_text = re.sub(r'\n\s*\n', '\n\n', content_text)
        
        return content_text if len(content_text) > 100 else None
    
    def _extract_date(self, soup):
        """Extract published date"""
        # Try various meta tags and selectors
        date_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="publishdate"]',
            'meta[name="date"]',
            'time[datetime]',
            '.publish-date',
            '.date',
            '.article-date'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                date_str = element.get('content') or element.get('datetime') or element.get_text()
                if date_str:
                    parsed_date = dateparser.parse(date_str)
                    if parsed_date:
                        return parsed_date
        
        return None
    
    def _extract_author(self, soup):
        """Extract author information"""
        author_selectors = [
            'meta[name="author"]',
            '.author',
            '.byline',
            '.article-author',
            '[rel="author"]'
        ]
        
        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                author = element.get('content') or element.get_text()
                if author:
                    return author.strip()
                    
        return None
    
    def _extract_tags(self, soup):
        """Extract article tags/categories"""
        tags = []
        
        # Try various selectors for tags
        tag_selectors = [
            '.tags a',
            '.categories a',
            '.tag',
            '.category',
            'meta[name="keywords"]'
        ]
        
        for selector in tag_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    if element.name == 'meta':
                        tag_text = element.get('content', '')
                        tags.extend([tag.strip() for tag in tag_text.split(',') if tag.strip()])
                    else:
                        tag_text = element.get_text().strip()
                        if tag_text:
                            tags.append(tag_text)
                break
        
        return list(set(tags))  # Remove duplicates
    
    def scrape_multiple_articles(self, urls):
        """
        Scrape multiple articles
        
        Args:
            urls (list): List of URLs to scrape
            
        Returns:
            list: List of article data dictionaries
        """
        articles = []
        for url in urls:
            article = self.scrape_article(url)
            if article:
                articles.append(article)
        
        return articles
