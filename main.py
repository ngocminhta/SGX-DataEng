import json

import requests
import os
import logging

global date
def readDateHistory():
    global date
    with open('dateHistory.json', 'r') as f:
        date = json.load(f)

def downloadNewDate(lastDate, cur):
    for i in range(date[lastDate]+1,5383):
        try:
            cvDate = str(i)
            print(cvDate)
            URL = "https://links.sgx.com/1.0.0/derivatives-historical/" + cvDate + "/WEBPXTICK_DT.zip"
            response = requests.get(URL)
            header = response.headers.get('Content-Disposition')
            print(header[-4:])
            if header[-4:] == '.zip':
                name = header[-12:-8] + '-' + header[-8:-6] + '-' + header[-6:-4]
                print(name)
                date[name] = i
            elif header[-5:-1] == '.tic':
                date[header[-17:-13] + '-' + header[-13:-11] + '-' + header[-11:-9]] = i
            elif header[-4:-1] == '.gz':
                date[header[-12:-8] + '-' + header[-8:-6] + '-' + header[-6:-4]] = i
            elif header[-5:-1] == '.txt':
                date[header[-17:-13] + '-' + header[-13:-11] + '-' + header[-11:-9]] = i
        except:
            continue
    print(date)

def downloadFile():
    # Create folder
    directory = getDate()
    if not os.path.exists(directory):
        os.mkdir(directory)
    cvDate = str(date[directory])
    print(cvDate)
    files = ["/WEBPXTICK_DT.zip", "/TickData_structure.dat", "/TC.txt", "/TC_structure.dat"]
    URLpart = "https://links.sgx.com/1.0.0/derivatives-historical/"

    for file in files:
        response = requests.get(URLpart + cvDate + file)
        header = response.headers.get('Content-Disposition')
        open(directory + file, "wb").write(response.content)

    # get the date assigned to the file
    # for i in range(2709,5380):
    #     try:
    #         cvDate = str(i)
    #         URL = "https://links.sgx.com/1.0.0/derivatives-historical/" + cvDate + "/WEBPXTICK_DT.zip"
    #         response = requests.get(URL)
    #         header = response.headers.get('Content-Disposition')
    #         open(directory + "/filename", "a").write(header + "\n")
    #     except:
    #         open(directory + "/filename", "a").write("No data found!" + "\n")


def getDate():
    global date
    cur = input('Type the day you want to download in format yyyy-mm-dd:\n')
    if cur > list(date)[-1]:
        downloadNewDate(list(date)[-1],cur)
    return cur


if __name__ == '__main__':
    readDateHistory()
    while True:
        downloadFile()
        # try:
        #     downloadFile()
        # except:
        #     print('Your date you typed is not valid. Please try again.')
        #     downloadFile()
        checkEnd = input("Do you want to download another day? (Y/N)\n")
        if checkEnd == "N":
            break
