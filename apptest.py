import threading
import time
from datetime import datetime, date
import bisect
import csv
import os.path

startTime = datetime.now()
inputPump = 'Pump1'

def doWork(M, p, timeList):
    global inputPump

    print(M, p)
    if len(timeList) == 0:
        print("Empty")

    now = datetime.now()
    elapsedTime = now - startTime
    elapsedTimeMinutes = elapsedTime.total_seconds() / 60
    targetSleep = 0

    # Avoid small times or time less than the current time
    if timeList[0] < 0.5 or elapsedTimeMinutes > timeList[-1]:
        return

    if len(timeList) == 1:
        targetSleep = timeList[0] * 60
    else:
        minDist = timeList[-1]
        minDistIndex = 0
        for i, t in enumerate(timeList):
            if abs(elapsedTimeMinutes - t) < minDist:
                minDistIndex = i
                minDist = abs(elapsedTimeMinutes - t)
        if minDistIndex == len(timeList) - 1:
            return
        else:
            j = minDistIndex
            while timeList[j] < elapsedTimeMinutes:
                j = j + 1
                if j == len(timeList):
                    return
            targetSleep = (timeList[j] - elapsedTimeMinutes) * 60

    # Check periodically if the experiment is off
    period = 10
    while targetSleep > 0:
        if targetSleep <= period:
            time.sleep(targetSleep)
        else:
            time.sleep(period)
            print("Period ends")
        targetSleep = targetSleep - period

    currentPump = inputPump
    if currentPump == 'Pump1':
        inputPump = 'Pump3'
    else:
        inputPump = 'Pump1'

    print("Current time", (datetime.now() - startTime).total_seconds() / 60)  # Get time running in seconds
    print("Current pump", inputPump)

    workThread = threading.Thread(target=doWork, args=(M, 'plc', timeList))
    # workThread.setDaemon(True)
    workThread.start()


# workThread = threading.Thread(target=doWork, args=('M0', 'plc', lst))
# workThread.start()

def runDoWork(M):
    print("Running work")
    M = 'M0'
    fname='PumpToggleTimes_' + str(M)+'.csv'
    rows = []
    if os.path.isfile(fname):
        with open(fname, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
            rows = rows[0]
        if isinstance(row, list):
            try:
                if len(row) > 0:
                    timeList = [float(x) for x in row]
                    timeList.sort()
                    workThread = threading.Thread(target=doWork, args=(M, 'plc', timeList))
                    workThread.start()

            except:
                print("Unknown type")

# runDoWork('M0', [0.5001, 0.6, 0.7, 0.8])
# runDoWork('M0', "29")


# rows = []
# if os.path.isfile(fname):
#     with open(fname, 'r', encoding='utf-8-sig') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             rows.append(row)
#
#         print(rows)
#         rows = rows[0]

# runDoWork('M0', rows)
runDoWork('M0')