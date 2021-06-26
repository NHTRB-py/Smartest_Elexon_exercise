import pandas as pd
import requests


apikey="bqridit944a4wev"
curr_date=pd.Timestamp.now()
curr_date_str=pd.Timestamp.now().strftime("%Y-%m-%d")
prev_date_str=(curr_date-pd.Timedelta("1D")).strftime("%Y-%m-%d")

def elexon_request_test(url:str):
    """
    Tests elexon url
    :param url: elexon REST API url to be tested
    :return: status code for API request
    """
    req=requests.get(url)
    print(req.status_code)
    return req.status_code



def elexon_request(url:str):
    elexon_df=pd.read_csv(url, header=[4])
    elexon_df.dropna(inplace=True)
    return elexon_df

def url_gen(series_code:str="B1770", period:int=1, api_key:str=apikey, date_str:str=prev_date_str):
    """
    Generates url to get csv data from elexon API (v1), tested on sreies B1770 and B1780
    :param series_code: name of series, full reference available at https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/
    :param period: integer from 1 to 48, corresponding to each half-hourly period in a day
    :param api_key: API key for Elexon portal
    :param date_str: 
    :return: url to csv
    """
    url="https://api.bmreports.com/BMRS/"+series_code+"/v1?APIKey="+apikey+"&SettlementDate="+prev_date_str+"&Period="+str(period)+"&ServiceType=csv"
    return url


def main():
    B1770dflist=[elexon_request(url_gen(series_code="B1770", period=i)) for i in range(1,49)]
    # print(B1770dflist)
    B1770df=pd.concat(B1770dflist)
    print(B1770df)
    B1780dflist=[elexon_request(url_gen(series_code="B1780", period=i)) for i in range(1,49)]
    # print(B1780dflist)
    B1780df=pd.concat(B1780dflist)
    print(B1780df)



if __name__ == "__main__":
    main()