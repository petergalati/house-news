from bs4 import BeautifulSoup
import requests
import json
import schedule
import time


def get_house_data():
    URL = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=POSTCODE%5E104931&maxBedrooms=8&minBedrooms=7&radius=1.0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.content, 'html5lib')
    houses = soup.find_all("div", class_="l-searchResult is-list")
    for house in houses:
        address = house.find("address", class_="propertyCard-address").get_text().strip()

        link = house.find("a", class_="propertyCard-link")["href"]

        # distance from queens building
        distance = house.find("div", class_="propertyCard-distance").get_text().strip().replace("from station", "").strip()

        print(address)
        print(link)
        print(distance)

        house_data = {
            "address": address,
            "link": link,
            "distance": distance
        }

        json_house_data = json.dumps(house_data, indent=4)

        with open("houses.json", "a") as f:
            f.write(json_house_data + "\n")

schedule.every(10).minutes.do(get_house_data)
while True:
    schedule.run_pending()
    time.sleep(1)