# Elexon_scrape

This repo contains Python code in Elexon_Scrape_Analyse.py to scrape data from Elexon's REST API and print a message displaying daily total imbalance cost and daily imbalance unit rate for the previous day, and the hour which had the greatest imbalance volume. The code also saves charts of the imbalance prices, volume and cost throughout the previous day.


Notes: 
- There doesn't seem to be a way to obtain more than one period per API call to the Elexon API.
- I could not find documentation stating a limit to how many API calls or the frequency of API calls which can be made to the Elexon API, so there is no sleep/wait function implemented here.
- All information required to call the API is contained in the URL, so a simple solution was to call pandas read_csv rather than use a HTTP library such as requests or httplib2. I have included a solution with requests to raise more informative errors if data are not available.
- Units are not stated in the documentation, have been taken from https://www.bmreports.com/bmrs/?q=balancing/aggregatedimbalance and https://www.bmreports.com/bmrs/?q=balancing/imbalanceprice.

Extensions
- Add charts/analysis comparing the previous day to recent or longer term history such as histograms for the prices/volumes to give a visual representation of how this day compares to (for example) the last 7 days.
- Analyse seasonality: check if particular hours in the day or particular days of the week exhibit similar behaviours
- Adjust  code to run in parallel using asyncio
