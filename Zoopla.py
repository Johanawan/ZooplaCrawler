from bs4 import BeautifulSoup           # pip install bs4=0.0.1
from urllib.request import urlopen      
import pandas as pd                     # pip install pandas=1.1.3
import re

house_info = {}

def zooplaScraping(base_url, page_number):

    html = urlopen(base_url)
    bs = BeautifulSoup(html, 'html.parser')
    # Finds the total number of pages to paginate into.
    try:
        total_pages = int(bs.find('div', {'id': 'content'}).find('div', {'class': 'paginate'}).find_all('a')[-2].get_text())
    except AttributeError:
        total_pages = 1   

    global zoopla_names, zoopla_prices, zoopla_urls, zoopla_addresses, zoopla_bedrooms, zoopla_agent, zoopla_description, zoopla_listing_date, zoopla_website_source
    # Create an empty list of variables
    zoopla_names = []
    zoopla_prices = []
    zoopla_urls = []
    zoopla_addresses = []
    zoopla_bedrooms = []
    zoopla_agents = []
    zoopla_descriptions = []
    zoopla_listing_dates = []
    zoopla_website_source = []

    # Loops through the pagination pages at the bottom of the listings
    while page_number <= total_pages:
        next_page = base_url + str(page_number)
        html = urlopen(next_page)
        bs = BeautifulSoup(html, "html.parser")
        page_number += 1

        # Gather the listings on the page
        bs_listings = bs.find_all('li', id=re.compile(r'listing.[0-9]+'))

        for listing in bs_listings:
            
            # Get names
            bs_name = listing.find('h2', {'class': 'listing-results-attr'}).find('a').get_text()
            zoopla_names.append(bs_name)

            # Get prices
            bs_price = listing.find('a', {"class": "listing-results-price"}).get_text(strip=True)
            match = re.sub(r'[a-zA-Z]*\s*[a-zA-Z]*', '', bs_price) # Use regular expressions to cut away extra text i.e. Guide Price, From, Offer Overs
            zoopla_prices.append(match)

            # Get urls
            bs_url = listing.find('a', {"class": "listing-results-price"}, href=True)
            zoopla_urls.append('https://www.zoopla.co.uk' + bs_url['href'])

            # Get addresses
            bs_address = listing.find('a', {'class': 'listing-results-address'}).get_text()
            zoopla_addresses.append(bs_address)

            # Get bedrooms
            try:
                bs_bedrooms = listing.find('h3', {'class': 'listing-results-attr'}).find('span', {'class': 'num-beds'}).get_text(strip=True)
            except AttributeError:
                bs_bedrooms = '0'
            zoopla_bedrooms.append(bs_bedrooms)

            # Get agent
            bs_agent = listing.find('div', {'class': 'agent_logo'}).find('img', alt=True)['alt']
            zoopla_agents.append(bs_agent)

            # Get description
            bs_description = listing.find('p').get_text(strip=True)
            zoopla_descriptions.append(bs_description)

            # TODO: Get listing date
            bs_listing_date = listing.find('p', {'class': 'top-half'}).find('small').get_text(strip=True)
            find_date = re.search(r'\d+[a-z]+\s[A-Za-z]+\s[0-9]+', bs_listing_date).group(0)
            zoopla_listing_dates.append(find_date)

            # Get Website Source
            zoopla_website_source.append("Zoopla")




    # Combining the lists into a nested dictionary
    for i in range(len(zoopla_names)):
        house_info["{}".format(i+1)] = {
            "Names": zoopla_names[i],
            "Listing Dates": zoopla_listing_dates[i],
            "Prices": zoopla_prices[i], 
            "Addresses": zoopla_addresses[i],
            "Bedrooms": zoopla_bedrooms[i],
            "Agents": zoopla_agents[i][12:],
            "Descriptions": zoopla_descriptions[i][],
            "Urls": zoopla_urls[i], 
            "Website Source": zoopla_website_source[i],
            }   

    # Put the dictionary into a pandas dataframe     
    df = pd.DataFrame.from_dict(house_info, orient='index')

    # Save the dataframe into a csv file in the specified location below
    df.to_csv(r'C:\\PythonProjects\websiteScrapers\\zoopla_dataframe.csv', header=True, encoding='utf-8-sig')

    return df


# Gets an input of the type of property
type = "property" #str(input(
#     """What type of property are you looking for: 
#     -Property (all)
#     -Houses
#     -Flats

# Answer: """
# ))

# Gets an input of the location the user would like to see
location = "balham"# str(input('Which location would you like to search: '))

# Gets the price the user is looking for
price_min = 200000# int(input("Minimum price you are looking for: "))
price_max = 1200000# int(input("Maxmimum price you are looking for: "))

# Gets the number of bedrooms the user is looking for
bedrooms_min = 5# int(input("Minimum number of bedrooms you are looking for: "))
bedrooms_max = 5# int(input("Maxmimum number of bedrooms you are looking for: "))

# base_url = "https://www.zoopla.co.uk/for-sale/property/balham/?identifier=balham&q=Balham&radius=0&pn="
base_url = "https://www.zoopla.co.uk/for-sale/{}/{}/?price_min={}&price_max={}&beds_min={}&beds_max={}&identifier={}&q={}&radius=0&pn=".format(type, location, price_min, price_max, bedrooms_min, bedrooms_max, location, location)

zooplaData = zooplaScraping(base_url, 1)

print(zooplaData)