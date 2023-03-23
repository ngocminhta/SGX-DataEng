# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from urllib.request import urlopen, urlretrieve
import cgi
import requests
import os

def downloadFile():
    # Create folder
    directory = getDate()
    #os.mkdir(directory)
    # cvDate = str(5380)
    # files = ["/WEBPXTICK_DT.zip", "/TickData_structure.dat", "/TC.txt", "/TC_structure.dat"]
    # URLpart = "https://links.sgx.com/1.0.0/derivatives-historical/"
    #
    # for file in files:
    #     response = requests.get(URLpart + cvDate + file)
    #     header = response.headers.get('Content-Disposition')
    #     open(directory + file, "wb").write(response.content)

    for i in range(2709,5380):
        try:
            cvDate = str(i)
            URL = "https://links.sgx.com/1.0.0/derivatives-historical/" + cvDate + "/WEBPXTICK_DT.zip"
            response = requests.get(URL)
            header = response.headers.get('Content-Disposition')
            open(directory + "/filename", "a").write(header + "\n")
        except:
            open(directory + "/filename", "a").write("No data found!" + "\n")

def getDate():
    print('Type the day you want to download in format yyyy-mm-dd:')
    date = input()
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:])
    return date

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    downloadFile()
    # try:
    #     getDate()
    # except:
    #     print('Your date you typed is not valid. Please try again.')
    #     getDate()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
