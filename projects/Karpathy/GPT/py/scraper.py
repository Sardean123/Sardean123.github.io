import requests
from bs4 import BeautifulSoup
import time
import json
import os
from urllib.parse import urljoin
import re

class DrSeussScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.books = []
        self.poems = []
        self.output_dir = "dr_seuss_texts"
        
    def create_output_directory(self):
        """Create directory for storing scraped texts"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def scrape_by_title(self, book_titles):
        """Scrape Dr. Seuss texts by book titles"""
        for title in book_titles:
            print(f"Searching for: {title}")
            # Clean title for search
            search_title = re.sub(r'[^\w\s]', '', title).replace(' ', '+')
            
            # Search for the book
            search_url = f"https://www.google.com/search?q={search_title}+dr+seuss+text+online"
            
            try:
                response = requests.get(search_url, headers=self.headers)
                response.raise_for_status()
                time.sleep(2)  # Be polite to servers
                
                # Parse the search results
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all search result links
                search_results = soup.find_all('div', class_='g')  # Google search result container
                
                for result in search_results:
                    # Extract the link from each search result
                    link_element = result.find('a')
                    if link_element and 'href' in link_element.attrs:
                        url = link_element['href']
                        
                        # Filter for relevant links (avoid ads, secondary links, etc.)
                        if self.is_relevant_link(url, title):
                            print(f"Found relevant link: {url}")
                            
                            # Try to scrape the content from this link
                            text = self.scrape_text_from_url(url)
                            
                            if text:
                                self.books.append({
                                    'title': title,
                                    'text': text,
                                    'source': url
                                })
                                print(f"Successfully scraped: {title}")
                                break  # Move to next book after finding one good source
                    
                    time.sleep(1)  # Small delay between processing results
                    
            except requests.RequestException as e:
                print(f"Error searching for {title}: {e}")
            
    def is_relevant_link(self, url, title):
        """Check if a URL is likely to contain the book text"""
        # Skip Google's own links and ads
        if 'google.com' in url or 'doubleclick' in url:
            return False
            
        # Look for common text-hosting domains
        relevant_domains = [
            'archive.org',
            'gutenberg.org',
            'openlibrary.org',
            'pdfbooks.co',
            'pdfdrive.com',
            'textfiles.com'
        ]
        
        for domain in relevant_domains:
            if domain in url:
                return True
                
        # Check if the URL likely contains the book title
        clean_title = re.sub(r'[^\w\s]', '', title).lower()
        clean_url = re.sub(r'[^\w\s]', '', url).lower()
        
        title_words = clean_title.split()
        url_words = clean_url.split()
        
        # If at least half the title words are in the URL, it's probably relevant
        matching_words = sum(1 for word in title_words if word in url_words)
        
        return matching_words >= len(title_words) / 2
        
    def scrape_text_from_url(self, url):
        """Extract text content from a URL"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Different strategies for different sites
            if 'gutenberg.org' in url:
                # Project Gutenberg usually has a link to plain text
                text_link = soup.find('a', href=lambda x: x and x.endswith('.txt'))
                if text_link:
                    text_url = 'https://www.gutenberg.org' + text_link['href']
                    text_response = requests.get(text_url, headers=self.headers)
                    return text_response.text
                    
            elif 'archive.org' in url:
                # Internet Archive might have text view
                text_div = soup.find('div', class_='page')
                if text_div:
                    return text_div.get_text()
                    
            else:
                # Generic text extraction
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                    
                # Get text content
                text = soup.get_text()
                
                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                # Verify this looks like a book (has minimum length)
                if len(text) > 1000:  # Arbitrary minimum length
                    return text
                    
            return None
            
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None
                
    def scrape_public_domain_poems(self):
        """Scrape publicly available Dr. Seuss poems"""
        # This would target sites that have legally posted poems
        public_sources = [
            "https://allpoetry.com/poems/by/Dr_Seuss",
            "https://www.poemsearcher.com/poetry/dr+seuss"
        ]
        
        for url in public_sources:
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract poems based on the site structure
                poems = soup.find_all('div', class_='poem')  # Example selector
                
                for poem in poems:
                    title = poem.find('h3', class_='title')
                    text = poem.find('div', class_='poem-text')
                    
                    if title and text:
                        self.poems.append({
                            'title': title.text.strip(),
                            'text': text.text.strip(),
                            'source': url
                        })
                        
                time.sleep(2)  # Be polite to servers
                
            except requests.RequestException as e:
                print(f"Error accessing {url}: {e}")
                
    def save_texts(self):
        """Save scraped texts to files"""
        # Save books
        books_file = os.path.join(self.output_dir, "dr_seuss_books.json")
        with open(books_file, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, indent=4)
            
        # Save poems
        poems_file = os.path.join(self.output_dir, "dr_seuss_poems.json")
        with open(poems_file, 'w', encoding='utf-8') as f:
            json.dump(self.poems, f, indent=4)
            
        # Create consolidated text file for training
        consolidated_file = os.path.join(self.output_dir, "dr_seuss_consolidated.txt")
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            for book in self.books:
                f.write(f"=== {book.get('title', 'Unknown')} ===\n\n")
                f.write(f"{book.get('text', '')}\n\n")
                f.write("="*50 + "\n\n")
                
            for poem in self.poems:
                f.write(f"=== {poem.get('title', 'Untitled')} ===\n\n")
                f.write(f"{poem.get('text', '')}\n\n")
                f.write("="*50 + "\n\n")
                
    def run(self):
        """Main execution function"""
        self.create_output_directory()
        
        # List of Dr. Seuss books
        book_titles = [
            "Green Eggs and Ham",
            "Cat in the Hat",
            "One Fish Two Fish Red Fish Blue Fish",
            "Oh the Places You'll Go",
            "Fox in Socks",
            "How the Grinch Stole Christmas",
            "Hop on Pop",
            "The Lorax",
            "Dr. Seuss's ABC",
            "Mr. Brown Can Moo! Can You?"
        ]
        
        # Scrape poems that might be in public domain or legally available
        self.scrape_public_domain_poems()
        
        # Save all collected texts
        self.save_texts()
        
        print(f"Scraping complete. Check {self.output_dir} for results.")

# Usage
if __name__ == "__main__":
    scraper = DrSeussScraper()
    scraper.run()