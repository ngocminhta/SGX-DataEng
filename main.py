import json
from datetime import datetime, timedelta
import requests
import os
import logging

global date
logging.basicConfig(filename='log_SGX.log', format='%(asctime)s: %(levelname)s \t %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def readDateHistory():
    global date
    with open('dateHistory.json', 'r') as f:
        date = json.load(f)


def lastBusinessDay():
    today = datetime.today()
    diff = 1
    if today.weekday() == 0:
        diff = 3
    elif today.weekday() == 6:
        diff = 2
    else:
        diff = 1
    return (today - timedelta(days=diff)).strftime('%Y-%m-%d')


def nextBusinessDay(curdate):
    nextBuzDay = datetime.strptime(curdate, '%Y-%m-%d') + timedelta(days=1)
    while nextBuzDay.weekday() in (5, 6):
        nextBuzDay += timedelta(days=1)
    return nextBuzDay.strftime('%Y-%m-%d')


def downloadNewDate(lastDate, cur):
    lastBuzDay = lastBusinessDay()

    i = date[lastDate] + 1
    while True:
        try:
            cvDate = str(i)
            URL = "https://links.sgx.com/1.0.0/derivatives-historical/" + cvDate + "/WEBPXTICK_DT.zip"
            response = requests.get(URL)
            header = response.headers.get('Content-Disposition')
            curdate = None

            if header[-4:] == '.zip':
                curdate = header[-12:-8] + '-' + header[-8:-6] + '-' + header[-6:-4]
            elif header[-4] == '.tic':
                curdate = header[-16:-12] + '-' + header[-12:-10] + '-' + header[-10:-8]
            elif header[-3] == '.gz':
                curdate = header[-11:-7] + '-' + header[-7:-5] + '-' + header[-5:-3]
            elif header[-4] == '.txt':
                curdate = header[-16:-12] + '-' + header[-12:-10] + '-' + header[-10:-8]

            date[curdate] = i
            logging.info('Updating new date...\t %s', curdate)

            with open('dateHistory.json', 'w') as f2:
                json.dump(date, f2)

            if curdate >= lastBuzDay:
                break
        except:
            continue
        i += 1


def downloadSpecificDay(directory):
    # Create folder
    cvDate = str(date[directory])
    if cvDate == '':
        return

    logging.info('--- Downloading the date %s', directory)
    files = ["/WEBPXTICK_DT.zip", "/TickData_structure.dat", "/TC.txt", "/TC_structure.dat"]
    URLpart = "https://links.sgx.com/1.0.0/derivatives-historical/"

    for file in files:
        response = requests.get(URLpart + cvDate + file)
        header = response.headers.get('Content-Disposition')
        logging.info('Downloading...\t %s', file[1:])
        if not os.path.exists(directory):
            os.mkdir(directory)
        open(directory + file, "wb").write(response.content)
        logging.info('File downloaded.\t %s', file[1:])

    if not checkFile(directory):
        downloadSpecificDay(directory)


def downloadRangeDay(start, end):
    currday = start
    while currday <= end:
        try:
            downloadSpecificDay(currday)
        except:
            logging.error("The date %s is not a working day!", currday)
        currday = nextBusinessDay(currday)


def getDate():
    global date
    cur = input('Type the day you want to download (yyyy-mm-dd):\n')
    if cur > list(date)[-1]:
        downloadNewDate(list(date)[-1], cur)
    return cur


def getDateRange():
    global date
    start = input('Type the starting day you want to download (yyyy-mm-dd):\n')
    end = input('Type the final day you want to download (yyyy-mm-dd):\n')
    if end > list(date)[-1]:
        downloadNewDate(list(date)[-1], end)
    return start, end


def checkFile(curday):
    curfiles = os.listdir(curday)
    files = ["WEBPXTICK_DT.zip", "TickData_structure.dat", "TC.txt", "TC_structure.dat"]
    for file in curfiles:
        if file not in files:
            return False
    return True


if __name__ == '__main__':
    readDateHistory()
    print('--------- SGX File Downloader ---------')
    while True:
        print("""Please choose one:
        1 - Download the most recent business day.
        2 - Download a specific business day.
        3 - Download a range of business days.\n""")
        choice = input('Your choice is: ')
        if choice == '1':
            try:
                downloadSpecificDay(lastBusinessDay())
            except:
                print('Your date you typed is not valid. Please try again.')
                downloadSpecificDay(lastBusinessDay())
        elif choice == '2':
            try:
                downloadSpecificDay(getDate())
            except:
                print('Your date you typed is not valid. Please try again.')
                downloadSpecificDay(getDate())
        elif choice == '3':
            start, end = getDateRange()
            downloadRangeDay(start, end)
        checkEnd = input("Do you want to download another day? (Y/N)\n")
        if checkEnd == "N" or checkEnd == "n":
            break
