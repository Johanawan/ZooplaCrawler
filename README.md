# ZooplaCrawler

This is a Housing Webscraper that crawls www.Zoopla.com for housing data.

Modules used:
Pandas
BeautifulSoup
Requests
Regular Expressions

Stage 1: Extract relevant HTML tags that hold data such as: Names, Listing Dates, Prices, Addresses, Bedrooms, Agents, Descriptions, and Urls. 

Stage 2: Loop through each page on Zoopla and collect all data listed in Stage 1.

Stage 3: Transform into a data frame and create a CSV file. (You need to specify where you want it store on the code.

Features: Allows fitering by Property Type, Location, Price and Bedrooms.


Creates a nested dictionary with data extracted from Zoopla.
![Image of Unstructured Data](https://github.com/Johanawan/ZooplaCrawler/blob/master/images/Unstructured.JPG)

Turns the nested dictionary into a Pandas DataFrame
![Image of Structured Data](https://github.com/Johanawan/ZooplaCrawler/blob/master/images/Structured.JPG)

Saves the data into a CSV file.
![Image of CSV Data](https://github.com/Johanawan/ZooplaCrawler/blob/master/images/ExcelData.JPG)
