import requests
from bs4 import BeautifulSoup
import pandas as pd

# Requesting the page (USYD Table A cores)
url = 'https://www.sydney.edu.au/handbooks/science/subject_areas_ae/tableA_core.shtml'
page = requests.get(url)

if page.status_code == 200:
    # Session lists
    uos_sem_1 = []
    uos_sem_2 = []
    uos_S1CIJA = []  

    # Replacing all break tags for separation
    html = page.text.replace('<br>', '|br|')
    content = BeautifulSoup(html, 'html5lib')

    for heading in content.find_all('td'):
        cell = heading.text.strip()

        # Saving relevant unit name
        if len(cell.split('|br|')[0]) == 8:
            unit_name = cell.split('|br|')[0]
        
        else:
            # Adding unit into sessions
            for date in cell.split('|br|'):
                if date == "Semester 1":
                    uos_sem_1.append(unit_name)
                
                if date == "Semester 2":
                    uos_sem_2.append(unit_name)
                
                if date == "Intensive January":
                    uos_S1CIJA.append(unit_name)

else:
    print("Error! Page not found")
    exit()