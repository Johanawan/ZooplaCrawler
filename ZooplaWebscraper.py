from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('https://www.zoopla.co.uk/for-sale/property/london/')
bs = BeautifulSoup(html, 'html.parser')

house_info = {}


class ZooplaWebScraper():

    # Makes the variable house_list_finder global to be accessed by all the functions
    global house_list_finder
    house_list_finder = bs.find_all('li', id=re.compile(r'listing.[0-9]+'))
    


    # This function gets the names of all the houses on Zoopla
    def get_names(self):

        # Creates an empty list that will store the names of the houses
        names = []

        # Loops through all the house listings one by one using a regular expression to identify the different listing_<id>
        for listing in house_list_finder:

            # Gathers the html code of the tags we want for our scraping
            html_names = listing.find('h2', {'class': 'listing-results-attr'}).find('a')

            # Gets the text of the html code
            raw_names = html_names.get_text()

            # Appends the text to a list
            names.append(raw_names)

        return names



    # This function will get the price of the houses listed on Zoopla
    def get_price(self):

        # Creates an empty list with the raw list prices E.G. £200,000Guide Price, £300,000Offer Over
        list_price_raw = []  

        # Find the code where all the houses are listed on the Zoopla website.
        for listing in house_list_finder:    

            # Finds an <a> while the list above^ that has the class="listing-results-price"
            price = listing.find('a', {"class": "listing-results-price"}) 

            # Creates variable raw_list_price that gets the prices and removes the whitespace.
            raw_list_price = price.get_text(strip=True)   

            # Puts the string in raw_list_price into a list call list_price_raw
            list_price_raw.append(raw_list_price)

        # Creates an empty list called list_price. This will remove the Guide Price & Offer Over from the price.
        list_price = []
    
        # Creates a loop to check if each html price has Guide Price or Offer Overs attached to it. 
        for list in list_price_raw:
            match = re.sub(r'\£?[a-zA-Z]*\s[a-zA-Z]*', '', list)
            
            list_price.append(match)
        
        return list_price
    


    def get_url(self):
    
        # Create an empty variable that stores the slug (part after .com/(slug)).
        house_slug = []
        
        for listing in house_list_finder:

            url = listing.find('a', {"class": "listing-results-price"}, href=True)

            house_slug.append(url['href'])

        # Creates an empty list called house_url that stores the entire url path.
        house_url = [] 
        
        # A loop that goes through each slug adds www.zoopla.co.uk to it.
        for slug in house_slug:
            house_url.append('https://www.zoopla.co.uk' + slug)

        return house_url



    # This function gets all the addresses on Zoopla
    def get_address(self):

        # Creates an empty list for the address to go into
        address = []

        # Loops through each listing in the page.
        for listing in house_list_finder:
            
            # Finds the html line where it stores the address within listing-results-address
            html_address = listing.find('a', {'class': 'listing-results-address'})

            # Cuts out the html to only include the text
            raw_address = html_address.get_text()

            # Attaches raw_address to the empty list: address
            address.append(raw_address)

        return address 



    # This function gets the number of bedrooms from Zoopla
    def get_bedrooms(self):

        bedrooms = []

        # Finds all the listings_<id> using a regular expression
        for listing in bs.find_all('li', id=re.compile(r'listing.[0-9]+')):
            
            # Finds this code <span class="num-icon num-beds" title="2 bedrooms"><span class="interface"></span>2</span> and stores it in html_bedroom
            try:
                html_bedrooms = listing.find('h3', {'class': 'listing-results-attr'}).find('span', {'class': 'num-beds'})
            except AttributeError:
                html_bedrooms = '0'

            # Extracts the text in the span tags or return 0 if it doesn't exist.
            try:
                no_of_bedrooms = html_bedrooms.get_text(strip=True)
            except AttributeError:
                no_of_bedrooms = '0'

            # Updates the empty list with number of bedrooms
            bedrooms.append(no_of_bedrooms)

        return bedrooms 



    # This function gets the agent of all the houses on Zoopla
    def get_agent(self):

        # Creates an empty list that will store the agent of the houses
        agent = []

        # Loops through all the house listings one by one using a regular expression to identify the different listing_<id>
        for listing in bs.find_all('li', id=re.compile(r'listing.[0-9]+')):

            # Gathers the html code of the tags we want for our scraping
            html_agent = listing.find('div', {'class': 'agent_logo'}).find('img', alt=True)

            # Gets the text of the html code
            raw_agent = html_agent['alt']

            # Appends the text to a list
            agent.append(raw_agent)

        return agent



    # This function gets the description of all the houses on Zoopla
    def get_description(self):

        # Creates an empty list that will store the description of the houses
        description = []

        # Loops through all the house listings one by one using a regular expression to identify the different listing_<id>
        for listing in bs.find_all('li', id=re.compile(r'listing.[0-9]+')):

            # Gathers the html code of the tags we want for our scraping
            html_description = listing.find('p')

            # Gets the text of the html code
            raw_description = html_description.get_text(strip=True)

            # Appends the text to a list
            description.append(raw_description)

        return description



    # This function gets the listing_date of all the houses on Zoopla
    def get_listing_date(self):

        # Creates an empty list that will store the listing_date of the houses
        listing_date = []

        # Loops through all the house listings one by one using a regular expression to identify the different listing_<id>
        for listing in bs.find_all('li', id=re.compile(r'listing.[0-9]+')):

            # Gathers the html code of the tags we want for our scraping
            html_listing_date = listing.find('p', {'class': 'top-half'}).find('small')

            # Gets the text of the html code
            raw_listing_date = html_listing_date.get_text(strip=True)

            # Uses a regular expression to find the date in the string.
            find_date_match = re.search(r'\dth\s[A-Za-z]+\s20[0-9]+', raw_listing_date).group(0)

            # Adds "Listed on: " to the date.
            add_listed_on = "Listed on: " + find_date_match

            # Appends the text to a list
            listing_date.append(add_listed_on)

        return listing_date



# ZooplaWebScraper()
test = ZooplaWebScraper()

house_names_list = test.get_names()
house_price_list = test.get_price()
house_url_list = test.get_url()
house_address_list = test.get_address()
house_bedrooms_list = test.get_bedrooms()
house_agent_list = test.get_agent()
house_description_list = test.get_description()
house_listing_date_list = test.get_listing_date()



# Combining the lists into a nested dictionary
for i in range(len(house_price_list)):
  house_info["house{}".format(i+1)] = {
      "names": house_names_list[i],
      "price": house_price_list[i], 
      "url": house_url_list[i], 
      "address": house_address_list[i],
      "bedrooms": house_bedrooms_list[i],
      "agent": house_agent_list[i],
      "description": house_description_list[i],
      "listing-date": house_listing_date_list[i],
      }
  
print(house_info)