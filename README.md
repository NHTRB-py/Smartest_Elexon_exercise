# Elexon_scrape

This repo contains Python code to scrape data from Elexon's REST API 

Notes: 
- There doesn't seem to be a way to obtain more than one period per API call to the Elexon API
- I could not find documentation stating a limit to how many API calls or the frequency of API calls which can be made to the Elexon API, so there is no sleep/wait function implemented here
- All information required to call the API is contained in the URL, so a simple solution was to call pandas read_csv rather than use a HTTP library such as requests or httplib2. I have included a solution with requests to raise more informative errors if data are not available
- Units are not stated in the documentation, have been taken from https://www.bmreports.com/bmrs/?q=balancing/aggregatedimbalance and https://www.bmreports.com/bmrs/?q=balancing/imbalanceprice
