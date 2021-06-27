import pandas as pd
import requests
from io import StringIO


apikeyfile=open("API_key.txt", "r") #requires API key from Elexon stored in API_key.txt file, or change apikey variable to string of Elexon API key
apikey=apikeyfile.read()


curr_date=pd.Timestamp.now()
curr_date_str=pd.Timestamp.now().strftime("%Y-%m-%d")
prev_date_str=(curr_date-pd.Timedelta("1D")).strftime("%Y-%m-%d")

def elexon_request_test(url:str):
    """
    Tests elexon url
    :param url: Elexon REST API url to be tested
    :return: status code for API request
    """
    req=requests.get(url)
    print(req.status_code)
    # print(req.headers)
    print(req.headers["Content-Type"])
    # print(req.text)
    return req.status_code



def elexon_request_simple(url:str):
    """
    Returns pandas DataFrame from Elexon URL request
    :param url: Elexon REST API endpoint
    :return: pandas DataFrame
    """
    elexon_df=pd.read_csv(url, header=[4])
    elexon_df.dropna(inplace=True)
    return elexon_df

def elexon_request_checked(url:str):
    """
    Returns pandas DataFrame from Elexon URL response having checked response is CSV format
    :param url: Elexon REST API endpoint
    :return: data from Elexon if in correct format (CSV) else raises error
    """
    req=requests.get(url)
    if req.headers["Content-Type"]!='text/csv;charset=UTF-8':
        raise TypeError("Request did not return csv format for url: "+url)
    else:
        elexon_df=pd.read_csv(StringIO(req.text), header=[4])
        elexon_df.dropna(inplace=True)
    return elexon_df

def url_gen(series_code:str="B1770", period:int=1, api_key:str=apikey, date_str:str=prev_date_str):
    """
    Generates url to get csv data from Elexon API (v1), tested on series B1770 and B1780
    :param series_code: name of series, full reference available at https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/
    :param period: integer from 1 to 48, corresponding to each half-hourly period in a day
    :param api_key: API key for Elexon portal
    :param date_str: date in form YYYY-MM-DD
    :return: url for Elexon REST API to obtain data in csv format
    """
    url="https://api.bmreports.com/BMRS/"+series_code+"/v1?APIKey="+api_key+"&SettlementDate="+date_str+"&Period="+str(period)+"&ServiceType=csv"
    return url


def main():

    B1770dflist=[elexon_request_checked(url_gen(series_code="B1770", period=i, api_key=apikey)) for i in range(1,49)]
    B1770df=pd.concat(B1770dflist)
    # B1770df.to_csv("B1770df.csv")
    B1770df["imbal_direction"]=B1770df["PriceCategory"].replace({"Insufficient balance":"DEFICIT", "Excess balance":"SURPLUS"}) # create imbalance column corresponding to values in B1780


    B1780dflist=[elexon_request_checked(url_gen(series_code="B1780", period=i, api_key=apikey)) for i in range(1,49)]
    B1780df=pd.concat(B1780dflist)
    # B1780df.to_csv("B1780df.csv")
    # print(B1770df.info())
    # print(B1780df.info())
    vol_pricedf=pd.merge(B1780df, B1770df, how="left",
                         left_on=["Settlement Date", "Settlement Period", "Imbalance Quantity Direction"],
                         right_on=["SettlementDate", "SettlementPeriod", "imbal_direction"])
    vol_pricedf["abs_imbal_quantity"]=vol_pricedf["Imbalance Quantity (MAW)"].abs()
    vol_pricedf["imbal_cost"]=vol_pricedf["abs_imbal_quantity"]*vol_pricedf["ImbalancePriceAmount"]
    total_imbal_vol=vol_pricedf["abs_imbal_quantity"].sum()
    total_imbal_cost=vol_pricedf["imbal_cost"].sum()
    imbal_cost_per_unit=total_imbal_cost/total_imbal_vol
    print("Daily total imbalance cost for {date} = {imb_cost}".format(date=prev_date_str,imb_cost=total_imbal_cost))
    print("Daily imbalance unit rate for {date} = {imb_rate}".format(date=prev_date_str,imb_rate=imbal_cost_per_unit))

    vol_pricedf["SettlementDate"]=pd.to_datetime(vol_pricedf["SettlementDate"], format="%Y-%m-%d")
    vol_pricedf["settle_period_start_dt"]=vol_pricedf["SettlementDate"]+pd.Timedelta("30m")*(vol_pricedf["SettlementPeriod"]-1)
    vol_pricedf["settle_period_end_dt"]=vol_pricedf["SettlementDate"]+pd.Timedelta("30m")*vol_pricedf["SettlementPeriod"]
    vol_pricedf["vol_rolling_sum_hr"]=vol_pricedf.rolling(pd.Timedelta("60m"),on="settle_period_start_dt").sum()["abs_imbal_quantity"] #hourly rolling imbalance volume
    max_hr_vol=vol_pricedf["vol_rolling_sum_hr"].max()
    max_vol_rows=vol_pricedf[vol_pricedf["vol_rolling_sum_hr"]==max_hr_vol].reset_index()
    max_imbal_period_end_list=[max_vol_rows.at[i,"settle_period_end_dt"] for i in range(len(max_vol_rows))]
    print("Maximum hourly imbalance volume for {date} was {vol:.2f} "
          "in the hour between {start} and {end}".format(date=prev_date_str,
                                                         vol=max_hr_vol,
                                                         start=(max_imbal_period_end_list[0]-pd.Timedelta("60m")).strftime("%H:%M"),
                                                         end=max_imbal_period_end_list[0].strftime("%H:%M")))


    # vol_pricedf.to_csv("vol_pricedf.csv")



if __name__ == "__main__":
    main()