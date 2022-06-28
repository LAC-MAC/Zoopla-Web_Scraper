import requests
from bs4 import BeautifulSoup
import re
import json
import math

class Property:
  def __init__(self, id, address, price, numOfBeds, summary, agent):
    self.id = id
    self.address = address
    self.price = price
    self.numOfBeds = numOfBeds
    self.summary = summary
    self.agent = agent


def parseJson(soup, propertyList):
    results = soup.findAll('script', id="__NEXT_DATA__")

    for i in results:
       
        jObj = json.loads(i.getText())

    #print(json.dumps(jObj, indent = 4, sort_keys=True))

    numberOfResults = jObj["props"]["pageProps"]["initialProps"]["analyticsTaxonomy"]["searchResultsCount"]

    #print(numberOfResults)

    featuredProps =jObj["props"]["pageProps"]["initialProps"]["featuredProperties"]
    
    #print(json.dumps(featuredProps, indent=4))
    
    regularProps = jObj["props"]["pageProps"]["initialProps"]["regularListingsFormatted"]

    #print(json.dumps(jObj, indent=4))

    #print(len(regularProps))

    bed = 0
    for i in featuredProps:

        for j in i["features"]:
            if j["iconId"] == "bed":
                bed = j["content"]


        prop = Property(i['listingId'], i['address'], i['price'], bed, i['title'], i["branch"]["name"])
        propertyList.append(prop)

    for i in regularProps:

        for j in i["features"]:
            if j["iconId"] == "bed":
                bed = j["content"]


        prop = Property(i['listingId'], i['address'], i['price'], bed, i['title'], i["branch"]["name"])
        propertyList.append(prop)

    return numberOfResults


def printMatches(numOfBeds, desPrice):
    index = 0

    for i in propertyList:
        price = re.search(r'£(.*?)pcm', i.price).group(1)

        price = int(price.replace(',', ''))

       
    
        if i.numOfBeds >= numOfBeds and int(price) <= desPrice:
            index = index+1
            print("---------------------------")
            print(i.id)
            print(i.address)
            print(i.numOfBeds)
            print(i.price, "\n")

            print(i.summary, "\n")
            print(i.agent, "\n")
        

    print("Total Number Of Results: ", index)


baseURL = "https://www.zoopla.co.uk/to-rent/property/glasgow-city-centre/?page_size=25&price_frequency=per_month&view_type=list&q=Glasgow%20City%20Centre%2C%20Glasgow&radius=3&results_sort=newest_listings&search_source=refine"

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'
}


r = requests.get(baseURL)

soup = BeautifulSoup(r.content, 'lxml')


propertyList = []

numOfResult = parseJson(soup, propertyList)


numberOfPages = math.ceil( numOfResult/ 25)


for i in range(numberOfPages-1):
    index = (i+2)

    
    baseURL = "https://www.zoopla.co.uk/to-rent/property/glasgow-city-centre/?page_size=25&price_frequency=per_month&q=Glasgow%20City%20Centre%2C%20Glasgow&radius=3&results_sort=newest_listings&search_source=refine&pn={p}".format(p =index)

    r = requests.get(baseURL)

    soup = BeautifulSoup(r.content, 'lxml')

    parseJson(soup, propertyList)




printMatches(4, 2000)



















