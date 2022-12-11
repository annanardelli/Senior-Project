import requests
from bs4 import BeautifulSoup
import csv
import time
import mysql.connector

drugId = []
name = []
bioLink = []

with open("/Users/jaquelinmontes/Desktop/Senior Project/biochem.csv", 'r') as file:
    csvreader = csv.reader(file, delimiter=',', skipinitialspace=True)
    for row in csvreader:
        drugId.append(row[0])
        name.append(row[1])
        bioLink.append(row[2])


def getSummary(page):
    try:
        id = page.find(id="summary")
        dd = id.next_element
        summary = dd.next_element.text
        return (summary)
    except AttributeError as err:
        print(err)
        return None


def getBrand(page):
    try:
        brand = page.find(id="brand-names")
        dd = brand.next_element
        result = dd.next_element.text
        return (result)
    except AttributeError as err:
        print(err)
        return None


def getGeneric(page):
    try:
        gen = page.find(id="generic-name")
        dd = gen.next_element
        result = dd.next_element.text
        return (result)
    except AttributeError as err:
        print(err)
        return None


def getType(page):
    try:
        dType = page.find(id="type")
        dd = dType.next_element
        result = dd.next_element.text
        return (result)
    except AttributeError as err:
        print(err)
        return None


def getGroups(page):
    try:
        id = page.find(id="groups")
        dd = id.next_element
        result = dd.next_element.text
        return (result)
    except AttributeError as err:
        print(err)
        return None


def getState(page):
    try:
        id = page.find(id="state")
        dd = id.next_element
        result = dd.next_element.text
        return (result)
    except AttributeError as err:
        print(err)
        return None


def getWeight(page):
    try:
        id = page.find(id="weight")
        dd = id.next_element
        weight = dd.next_element
        return (weight.text)
    except AttributeError as err:
        print(err)
        return None


def getExperimentalPro(page):
    try:
        id = page.find(id="experimental-properties")
        dd = id.next_element
        table = dd.next_element
        td = table.find_all("td")
        exList = []
        index = 0
        for data in td:
            index += 1
            if index % 3 == 0:
                continue
            else:
                exList.append(data.text)
        return (exList)
    except AttributeError as err:
        print(err)
        return (None)


def getPredictedPro(page):
    try:
        id = page.find(id="predicted-properties")
        dd = id.next_element
        table = dd.next_element
        td = table.find_all("td")
        preProp = []
        index = 0
        for data in td:
            index += 1
            if index % 3 == 0:
                continue
            else:
                preProp.append(data.text)
        return (preProp)
    except AttributeError as err:
        print(err)
        return (None)


def main():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Gonzalez#1222",
        db="pharm_db")
    cursor = db.cursor()

    for i in range(981, 983):
        drug = name[i]
        url = bioLink[i]
        page = requests.get(url)
        result = BeautifulSoup(page.text, "html.parser")

        sum = getSummary(result)
        weight = getWeight(result)
        genName = getGeneric(result)
        brandName = getBrand(result)
        ty = getType(result)
        drugGroup = getGroups(result)
        st = getState(result)
        ex = getExperimentalPro(result)
        pre = getPredictedPro(result)
        time.sleep(5)

        update_drug = ("Update DailymedDrug set summary = %s, netWeight = %s, biochemicalDataSummaryLink =%s, genericName =%s,"
                       "brandNames = %s, type=%s, drugGroup=%s, state =%s where drugID = %s;")
        data_drug = (sum, weight, bioLink[i], genName, brandName, ty,
                     drugGroup, st, drugId[i])
        cursor.execute(update_drug, data_drug)

        index1 = index2 = 0
        try:
            for x in range(0, len(ex)-1, 2):
                add_ex_prop = ("Insert into ExperimentalProperties(drugID, expPropertyNo, propertyName, propertyValue) "
                               "VALUES(%s,%s,%s,%s)")
                prop_data = (drugId[i], index1, ex[x], ex[x+1])
                index1 += 1
                cursor.execute(add_ex_prop, prop_data)

            for x in range(0, len(pre)-1, 2):
                add_pre_prop = ("Insert into PredictedProperties(drugID, predPropertyNo, propertyName, propertyValue)"
                                "VALUES(%s,%s,%s,%s)")
                prop_data = (drugId[i], index2, pre[x], pre[x+1])
                index2 += 1
                cursor.execute(add_pre_prop, prop_data)

            time.sleep(10)
        except TypeError as err:
            print(err)
            continue

        print("Done with index: " + str(i))

    db.commit()
    cursor.close()
    db.close()
    print("Done Execution")


if __name__ == "__main__":
    main()
