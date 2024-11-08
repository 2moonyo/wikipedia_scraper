import requests
import json
from bs4 import BeautifulSoup
import re
def get_first_paragraph(session, wikipedia_url):
   #   [insert your code]
   
   wiki = session.get(wikipedia_url)
   text_file = wiki.text
   soup = BeautifulSoup(text_file, "html.parser")
   first_paragraph = []
   paragraphs = soup.find_all("p")
   for paragraph in paragraphs:
      text = paragraph.get_text(strip=True)
      if text:
         text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
         text = re.sub(r'(\d{4})\s*–\s*(\d{4})', r'\1 – \2', text)
         text = re.sub(r'\s+([.,])', r'\1', text)
         first_paragraph = text             
   #   return first_paragraph
         return first_paragraph
      
# <25 lines
session = requests.Session()
def get_leaders(session):
    root_url = "https://country-leaders.onrender.com"
    countries_url = "countries"
    cookie_url = "cookie"
    leaders_url = "leaders"
    
    cookies_response = session.get(f"{root_url}/{cookie_url}")
    cookies = cookies_response.cookies
    
    countries_list_response = session.get(f"{root_url}/{countries_url}", cookies=cookies)
    countries_list = countries_list_response.json()

    leaders_per_country = {}
    for c_code in countries_list:
        cookies = session.get(f"{root_url}/{cookie_url}").cookies
        params = {f"country":c_code}
        received = session.get(f"{root_url}/{leaders_url}", cookies=cookies, params=params)
        
        try:
            leaders = received.json()
            if isinstance(leaders, list):
                leaders_per_country[c_code] = []
                for leader in leaders:
                    leader_names = {"first_name": leader.get("first_name"),
                                   "last_name": leader.get("last_name")}
                    wikipedia_url = leader.get("wikipedia_url")
                    leader_names["first_paragraph"] = get_first_paragraph(session ,wikipedia_url) if wikipedia_url else "No Wikipedia URL available"         
                    leaders_per_country[c_code].append(leader_names)
            else:
                print(f"Incorrect c-code and leaders {c_code}: {leaders}")
        except ValueError:
            print(f"No country_code {c_code}")
    return leaders_per_country


def save(leaders_per_country):
    with open("leaders.json", "w") as json_file:
        json.dump(leaders_per_country, json_file)

leaders_info = get_leaders(session)
save(leaders_info)