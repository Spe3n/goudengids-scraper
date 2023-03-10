import requests
import lxml
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.goudengids.nl/"

headers = {
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

business_links = []

for x in range(1,2):
    r = requests.get(f"https://www.goudengids.nl/nl/zoeken/sanitair/{x}")
    soup = BeautifulSoup(r.content, "lxml")
    business_list = soup.find_all("div", class_="relative")
    for item in business_list:
        for link in item.find_all("a", href=True):
            business_links.append(baseurl + link["href"])

#testlink = "https://www.goudengids.nl/nl/bedrijf/Amsterdam/L119708784/Cees+Pronk+%7C+Own+Inspiration+Studio/"
for link in business_links:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")

    bedrijfsnaam = (soup.find('h1', itemprop="name"))
    straat = (soup.find('span', {"data-yext" : "address"}))
    postcode = (soup.find('span', {"data-yext" : "postal-code"}))
    plaatsnaam = (soup.find('span', {"data-yext" : "city"}))
    telefoon = (soup.find('a', class_="filled-yellow-btn rounded-full hover:bg-yellow-200 t-c"))
    emailadres = (soup.find("a", class_="outline-btn rounded-full t-c"))
    website = (soup.find('span', itemprop="url"))
    bedrijfsrecords = {
        "bedrijfsnaam" : bedrijfsnaam,
        "straat" : straat,
        "postcode" : postcode,
        "plaatsnaam" : plaatsnaam,
        "telefoon" : telefoon,
        "emailadres" : emailadres,
        "website" : website,
    }

    business_links.append(bedrijfsrecords)
    print('Saving: ', bedrijfsrecords)

df = pd.DataFrame(business_links)
df.to_csv('records.csv')
df.to_excel('records.xlsx')
print('save to file')

df = pd.DataFrame(business_links, columns=["bedrijfsnaam", "straat", "postcode", "plaatsnaam", "telefoon", "emailadres", "website",])
df.to_csv('recordlist.csv')

print(bedrijfsrecords)