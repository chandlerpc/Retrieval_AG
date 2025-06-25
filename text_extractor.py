import requests
from bs4 import BeautifulSoup

def scrape_webpage(url):
    """
    Fetches a Wikipedia article, extracts text from <p> tags within the main
    content area, and saves it to a text file.

    Args:
        url (str): The URL of the Wikipedia article.

    Returns:
        str: The extracted article text, or None if the request fails.
    """
    # Hard-code the URL as requested
    url = "https://en.wikipedia.org/wiki/Nissan_Skyline_GT-R"
    
    try:
        response = requests.get(url)
        # Check for successful request
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main content div
            content_div = soup.find('div', class_='mw-parser-output')
            
            if content_div:
                # Extract text from all paragraph tags
                paragraphs = content_div.find_all('p')
                article_text = '\n\n'.join([p.get_text() for p in paragraphs])
                
                # Write the result to the output file
                with open("Selected_Document.txt", "w", encoding="utf-8") as f:
                    f.write(article_text)
                
                print("Successfully scraped and saved the article to Selected_Document.txt")
                return article_text
            else:
                print("Failure: Could not find the main content div.")
                return None
        else:
            print(f"Failure: HTTP status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failure: An error occurred during the request: {e}")
        return None

def main():
    """Main function to run the scraper."""
    scrape_webpage(url="https://en.wikipedia.org/wiki/Nissan_Skyline_GT-R")

if __name__ == '__main__':
    main()