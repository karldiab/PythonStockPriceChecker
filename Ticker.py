import urllib.request
import json


STOCKSLIST = "FavoriteStocks.txt"
NUMOFGUESSES = 7
#Opens external file containing the user's favorite stocks. If the file
#doesn't exist, it is created
def openFavStocks():
    global favStocks
    print("Loading favorite stocks from file", STOCKSLIST)
    try:
        favStocks = open(STOCKSLIST, 'r+')
    except (IOError):
        favStocks = open(STOCKSLIST, 'wb')
        favStocks.close()
        favStocks = open(STOCKSLIST, 'r+')
    readStocks = favStocks.read()
    if len(readStocks) == 0:
        readStocks = "None"
    print("Favorite stocks loaded:", readStocks)

#closes external favorite stocks file
def closeFavStocks():
    global favStocks
    favStocks.close()
##Takes in a list of stock tickers and fetches pricing info about them via JSON API. Then converts the data to
##dictionary form as global var stockInfo
def fetchStockInfo(stockList):
    global stockInfo
    url = "http://marketdata.websol.barchart.com/getQuote.json?key=a32e7f4a6e5ab0861c20381159572eae&symbols="
    for item in stockList:
        url += item + ','
    #remove extra ',' at the end of url
    url = url[:-1]
    print(url)
    response = urllib.request.urlopen(url)
    responseString = response.read().decode("utf-8")
    stockInfo = json.loads(responseString)
    #print(stockInfo['results'])


openFavStocks()
closeFavStocks()
fetchStockInfo(["IBM","GOOGL"])