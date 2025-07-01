import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from airflow.models import Variable

def scrape_institutions(pages_per_run=10):
    # Ambil halaman terakhir yang sudah discape
    current_page = int(Variable.get('sinta_scraper_current_page', default_var=1))
    page_start = current_page
    page_end = current_page + pages_per_run - 1

    # Target URL
    url = 'https://sinta.kemdikbud.go.id/affiliations'

    # Prepare storage
    data = []

    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))


    # Loop through multiple pages (example: 5 pages)
    for page in range(page_start, page_end+1):
        print(f'Scraping page {page}...')
        try:
            response = s.get(f'https://sinta.kemdikbud.go.id/affiliations?page={page}', timeout=60) # Added timeout
            response.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find institution containers (adjust selector as needed)
            institutions = soup.find_all('div', class_='list-item')

            for institution in institutions:
                # Ambil id
                profile_id_tag = institution.find('div', class_='profile-id')
                profile_id = profile_id_tag.get_text(strip=True) if profile_id_tag else '-'
                id_number = profile_id.split(' | ')[0].split(': ')[1]
                code_number = profile_id.split(' | ')[1].split(': ')[1]

                # Ambil affiliate name
                name_tag = institution.find('div', class_='affil-name')
                name = name_tag.get_text(strip=True) if name_tag else '-'

                # Ambil abbreviation
                abbrev_tag = institution.find('div', class_='affil-abbrev')
                abbrev = abbrev_tag.get_text(strip=True) if abbrev_tag else '-'

                # Ambil location
                loc_tag = institution.find('div', class_='affil-loc')
                location = loc_tag.get_text(strip=True) if loc_tag else '-'

                # Ambil stats department and authors
                stats_tag = institution.find_all('span', class_='num-stat')
                stats_dept = stats_tag[0].get_text(strip=True).split()[0] if len(stats_tag) > 0 else '-'
                stats_dept_number = re.findall(r'\d+', stats_dept)[0]
                stats_authors = stats_tag[1].get_text(strip=True).split()[0] if len(stats_tag) > 1 else '-'
                stats_authors_number = re.findall(r'\d+', stats_authors)[0]

                # Sinta score 3 yrs
                scores = institution.find_all('div', class_='pr-num')
                score_3yr = scores[0].get_text(strip=True) if len(scores) > 0 else '-'
                score_overall = scores[1].get_text(strip=True) if len(scores) > 1 else '-'

                data.append({
                    'id': id_number,
                    'code': code_number,
                    'affiliate_name': name,
                    'abbreviation': abbrev,
                    'location': location,
                    'num_department': stats_dept_number,
                    'num_authors': stats_authors_number,
                    'SINTA_score_3yr': score_3yr,
                    'SINTA_score_overall': score_overall
                })

            time.sleep(20)  # Politeness delay
        except requests.exceptions.RequestException as e:
            print(f"Error scraping page {page}: {e}")
            continue # Continue to the next page even if one fails

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(f'/usr/local/airflow/include/sinta_affiliations_pages_{page_start}_{page_end}.csv', index=False)
    print(f'Scraping pages {page_start} to {page_end} completed!')

    # Update Variable untuk next batch
    Variable.set('sinta_scraper_current_page', str(page_end + 1))