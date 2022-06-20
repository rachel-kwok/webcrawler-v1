import logging
from zipfile import Path
import requests
from bs4 import BeautifulSoup

# Basic config for logs
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

# Referenced non-scrapy crawler template:
# Bajo, A (2020) Web Crawling with Python [Source code]. 
# https://www.scrapingbee.com/blog/crawling-python/#:~:text=Web%20crawling%20is%20a%20component,new%20links%20to%20a%20queue.

class usyd_crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.uos_sem_1 = []     # Semester 1 UOS
        self.uos_sem_2 = []     # Semester 2 UOS
        self.uos_S1CIJA = []    # Intensive Jan UOS
        self.uos_S1CIFE = []    # Intensive Feb UOS
        self.uos_S1CIJN = []    # Intrensive Jun UOS
        self.uos_S2CIJL = []    # Intensive Jul UOS
        self.uos_S2CINO = []    # Intensive Nov UOS
        self.uos_S2CIDE = []    # Intensive Dec UOS 
        self.urls_to_visit = urls
    
    def clean_url(self, url):
        page = requests.get(url)
        
        # Replacing all break tags for separation
        html = page.text.replace('<br>', '|br|')
        return html
    
    def add_unit(self, unit, session):
        if unit not in session:
            session.append(unit)

    def extract(self, html):
        content = BeautifulSoup(html, 'html5lib')
        for table_descrip in content.find_all('td'):
            cell = table_descrip.text.strip()

            # Obtaining unit name
            if len(cell.split('|br|')[0]) == 8:
                unit_name = cell.split('|br|')[0]
            
            else:
                # Adding unit into relevant sessions
                for date in cell.split('|br|'):
                    if date.startswith("Semester 1"):
                        self.add_unit(unit_name, self.uos_sem_1)
                    
                    if date.startswith("Semester 2"):
                        self.add_unit(unit_name, self.uos_sem_2)
                    
                    if date.startswith("Intensive"):
                        if date.endswith("January"):
                            self.add_unit(unit_name, self.uos_S1CIJA)

                        if date.endswith("February"):
                            self.add_unit(unit_name, self.uos_S1CIFE)
                        
                        if date.endswith("June"):
                            self.add_unit(unit_name, self.uos_S1CIJN)
                        
                        if date.endswith("July"):
                            self.add_unit(unit_name, self.uos_S2CIJL)
                        
                        if date.endswith("November"):
                            self.add_unit(unit_name, self.uos_S2CINO)
                        
                        if date.endswith("December"):
                            self.add_unit(unit_name, self.uos_S2CIDE)
                        
    def crawl(self, url):
        html = self.clean_url(url)
        self.extract(html)
        soup = BeautifulSoup(html, 'html5lib')
        for link in soup.find_all('a'):
            path = link.get('href')

            if path is not None:
                if path.startswith('/') and path.endswith("table.shtml") or path.endswith("tab.shtml"):
                    path = "https://www.sydney.edu.au" + path

                    if path not in self.visited_urls and path not in self.urls_to_visit:
                        self.urls_to_visit.append(path)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')

            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'BRUH FAILED: {url}')
            finally:
                self.visited_urls.append(url)
        
        print("Crawl complete! Reporting:")
        print(str(len(self.visited_urls)) + " visited URLs")
        print(str(len(self.uos_sem_1)) + " Semester 1 units")
        print(str(len(self.uos_sem_2)) + " Semester 2 units")
        print(str(len(self.uos_S1CIJA)) + " Intensive Jan units")
        print(str(len(self.uos_S1CIFE)) + " Intensive Feb units")
        print(str(len(self.uos_S1CIJN)) + " Intensive Jun units")
        print(str(len(self.uos_S2CIJL)) + " Intensive Jul units")
        print(str(len(self.uos_S2CINO)) + " Intensive Nov units")
        print(str(len(self.uos_S2CIDE)) + " Intensive Dec units")
            
if __name__ == '__main__':
    crawl = usyd_crawler(urls=['https://www.sydney.edu.au/handbooks/science/subject_areas_ae/tableA_overview.shtml'])
    crawl.run()