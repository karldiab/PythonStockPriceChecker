import urllib.request
import json
import sys

STOCKSLIST = "FavoriteStocks.txt"

#Opens external file containing the user's favorite stocks. If the file
#doesn't exist, it is created
def openFavStocks():
    global favStocksFile
    try:
        favStocksFile = open(STOCKSLIST, 'r+')
    except IOError as e:
        print(e)
        favStocksFile = open(STOCKSLIST, 'wb').close()
        favStocksFile = open(STOCKSLIST, 'r+')


#Display selected stock tickers. Also puts favStockFile contents into global string favStocks
def displaySelectedStocks():
    global favStocks
    favStocksFile.seek(0)
    favStocks = favStocksFile.read()
    if len(favStocks) == 0:
        print("No stocks entered.")
    else:
        #Remove excess white space if present
        tempStocks = favStocks.split(' ')
        favStocks = ""
        for item in tempStocks:
            if len(item) > 0:
                favStocks += item + " "
        #Remove final space
        favStocks = favStocks[:-1]
        print("Selected Stock:", favStocks)

#closes external favorite stocks file
def closeFavStocks():
    favStocksFile.close()
#Syncs the external stocks file to the favStocks string kept in memoryls
def updateStocksFile():
    favStocksFile.close()
    open(STOCKSLIST, "w").close()
    openFavStocks()
    favStocksFile.write(favStocks)
    
##Takes in a list of stock tickers and fetches pricing info about them via JSON API. Then converts the data to
##dictionary form as global var stockInfo
def fetchStockInfo():
    global stockInfo
    url = "http://marketdata.websol.barchart.com/getQuote.json?key=a32e7f4a6e5ab0861c20381159572eae&symbols="
    for item in stocks:
        url += item + ','
    #remove extra ',' at the end of url
    url = url[:-1]
    print("\nFetching data from the internet...")
    response = urllib.request.urlopen(url)
    responseString = response.read().decode("utf-8")
    stockInfo = json.loads(responseString)

#Ensures each requested ticker is valid. Compares the requested tickers (global var stocks) to what
#stocks were returned by the info API and removes the stocks not found. Mutates global variable stocks
#so it only contains the stock tickers the API found info for. Prints which invalid stocks were removed.
def checkForInvalidTicker():
    global favStocks
    favStocks = ""
    validStocks = []
    for item in stocks:
        for i in stockInfo["results"]:
            if i["symbol"] == item:
                validStocks.append(item)
    for item in stocks:
        if item not in validStocks:
            print(item, "not found. Removing from stocks list.")
        else:
            favStocks += item + ' '
    updateStocksFile()

##Reads user's stocks from the external file and puts them into a list. Fetches info for those
##stocks and ensures info was found for every requested stock. Prints the information for each
##requested stock.
def displayStockInfo():
    global stocks
    if len(favStocks) == 0:
        print("No Stocks entered.")
        stocks = []
    else:
        stocks = favStocks.split(' ')
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
    print()


#Shows menu user can choose from
def getChoice():
    validOptions = ("1","2","3","4")
    print("Options:")
    print("1 - Fetch info for selected stock")
    print("2 - Add a stock")
    print("3 - Remove a stock")
    print("4 - Quit")
    option = input("Select an option: ")
    #input validation
    while option not in validOptions:
        errorMsg = "Invalid option. The only valid choices are "
        for i in validOptions:
            errorMsg += i + ' '
        option = input(errorMsg)
    return option
#Adds a stock to end of file. Does no validation
def addStock():
    stockToAdd = input("\nEnter Stock Symbol: ")
    #Go to end of faveStocks
    favStocksFile.seek(0,2)
    favStocksFile.write(' ' + stockToAdd.upper())
    print(stockToAdd.upper(), "added.")
#Removes stockToRemove from file.
#Precondition: stockToRemove must be in the favStocks string
def removeStock(stockToRemove):
    global favStocks
    favStocks = favStocks.replace(stockToRemove,"")
    print(stockToRemove, "removed.")
    updateStocksFile()
#Prompts the user for which stock they want removed. Ensures the entered stock
#is actually in favStocks string
def removeStocksPrompt():
    print("\nCurrently entered stocks:")
    displaySelectedStocks()
    stockToRemove = input("Enter stock to remove or 'quit' to return to main menu: ")
    while stockToRemove.upper() not in favStocks and stockToRemove.upper() != "QUIT":
        stockToRemove = input("Stock not in list. Enter a stock in the list or 'quit' to return to main menu: ")
    if stockToRemove.upper() == "QUIT":
        return 0
    removeStock(stockToRemove.upper())


#Runs the main program
def runTheShow():
    openFavStocks()
    while 1:
        displaySelectedStocks()
        choice = getChoice()
        if choice == "1":
            displayStockInfo()
        elif choice == "2":
            addStock()
        elif choice == "3":
            removeStocksPrompt()
        elif choice == "4":
            break
    closeFavStocks()

runTheShow()