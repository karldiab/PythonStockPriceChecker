import urllib.request
import json
import sys

STOCKSLIST = "FavoriteStocks.txt"

#Opens external file containing the user's favorite stocks. If the file
#doesn't exist, it is created
def openFavStocks():
    global favStocks
    try:
        favStocks = open(STOCKSLIST, 'r+')
    #
    except IOError as e:
        print(e)
        favStocks = open(STOCKSLIST, 'wb')
        favStocks.close()
        favStocks = open(STOCKSLIST, 'r+')
    displaySelectedStocks()

#Display selected stock tickers
def displaySelectedStocks():
    favStocks.seek(0)
    readStocks = favStocks.read()
    if len(readStocks) == 0:
        readStocks = "None"
    print("Selected Stock Tickers:", readStocks)

#closes external favorite stocks file
def closeFavStocks():
    global favStocks
    favStocks.close()

##Takes in a list of stock tickers and fetches pricing info about them via JSON API. Then converts the data to
##dictionary form as global var stockInfo
def fetchStockInfo():
    global stockInfo
    url = "http://marketdata.websol.barchart.com/getQuote.json?key=a32e7f4a6e5ab0861c20381159572eae&symbols="
    for item in stocks:
        url += item + ','
    #remove extra ',' at the end of url
    url = url[:-1]
    response = urllib.request.urlopen(url)
    responseString = response.read().decode("utf-8")
    stockInfo = json.loads(responseString)

#Ensures each requested ticker is valid. Compares the requested tickers (global var stocks) to what
#stocks were returned by the info API and removes the stocks not found. Mutates global variable stocks
#so it only contains the stock tickers the API found info for. Prints which invalid stocks were removed.
def checkForInvalidTicker():
    global stocks
    global stockInfo
    validStocks = []
    for item in stocks:
        for i in stockInfo["results"]:
            if i["symbol"] == item:
                validStocks.append(item)
    for item in stocks:
        if item not in validStocks:
            print(item, "not found. Removing from stocks list.")
    stocks = validStocks

##Reads user's stocks from the external file and puts them into a list. Fetches info for those
##stocks and ensures info was found for every requested stock. Prints the information for each
##requested stock
def displayStockInfo():
    global stocks
    favStocks.seek(0)
    stocksString = favStocks.read()
    if len(stocksString) == 0:
        print("No Stocks entered.")
    else:
        stocks = stocksString.split(' ')
        fetchStockInfo()
        checkForInvalidTicker()
        for i in stockInfo["results"]:
            print()
            print("Symbol:", i["symbol"])
            print("Name:", i["name"])
            print("Last Price:", i["lastPrice"])
            print("Open:", i["open"])
            print("High:", i["high"])
            print("Low:", i["low"])
            print("Close:", i["close"])
            print("Exchange:", i["exchange"])


#Shows menu user can choose from
def getChoice():
    validOptions = ["1","2","3","4"]
    print("Options:")
    print("1 - Fetch info for selected tickers")
    print("2 - Add a ticker")
    print("3 - Remove a ticker")
    print("4 - Quit")
    option = input("Select an option: ")
    #input validation
    while option not in validOptions:
        errorMsg = "Invalid option. The only valid choices are "
        for i in validOptions:
            errorMsg += i + ' '
        option = input(errorMsg)
    return option
def addStock():
    stockToAdd = input("Enter Stock Symbol: ")
    #Go to end of faveStocks
    favStocks.seek(0,2)
    favStocks.write(' ' + stockToAdd.upper())
    print(stockToAdd.upper(), "added.")
    displaySelectedStocks()
##STILL NOT WORKING
def removeStock():
    displaySelectedStocks()
    stockToRemove = input("Enter Stock to Remove: ")
    while stockToRemove.upper() not in stocks or stockToRemove.upper() != "QUIT":
        stockToRemove = input("Stock not in list. Enter a stock in the list or 'quit' to return to main menu.")
    if stockToRemove.upper() == "QUIT":
        return 0


#Runs the main program
def runTheShow():
    openFavStocks()
    while 1:
        choice = getChoice()
        if choice == "1":
            displayStockInfo()
        elif choice == "2":
            addStock()
        elif choice == "3":
            print()
            #removeStock()
        elif choice == "4":
            break
    closeFavStocks()

runTheShow()