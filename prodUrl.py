import csv
import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
import mysql.connector

name = []
urls = []

with open("/Users/jaquelinmontes/Desktop/Senior Project/ProductsURL  - Sheet1.csv", 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    for row in csvreader:
        name.append(row[0])
        urls.append(row[1])
# data_frame = pd.DataFrame(list(zip(name, urls)), columns=[
 #   'Name', 'DailymedLink'])
# print(data_frame)


def bioChemLink(page):
    try:
        bioChem = page.find('a', id="anch_dj_98")
        link = bioChem['href']
        return (link)
    except AttributeError as err:
        print(err)
        return None
    except TypeError as err:
        print(err)
        return None

# --------------------------------------------------


def getDescriptionID(page):
    pattern = re.compile(".*(DESCRIPTION)")
    t = page.find_all('li')
    id = ''
    for item in t:
        if (item.find('a', text=pattern) != None):
            tag = item.find('a', text=pattern)
            if not tag.has_attr('id'):
                continue
            id = tag.attrs['id']
    return (id)

# --------------------------------------------------


def getInfo(page):
    pattern = re.compile(".*(DESCRIPTION)")
    text = ''
    identification = getDescriptionID(page)
    try:
        t = page.find_all('li')
        a = page.find('a', id=identification)
        parent = a.parent
        des = parent.find_all('p', text=True)
        for para in des:
            text += para.get_text()
        return (text)
    except AttributeError as err:
        print(err)
        return None


# --------------------------------------------------


def getActiveIng(page):
    skip = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28,
            31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70, 73, 76, 79, 82, 85,
            88, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118, 121, 124, 127, 130, 133, 136,
            139, 142]
    try:
        table = page.find('td', text="Active Ingredient/Active Moiety")
        active = []
        tr = table.parent
        tbody = tr.parent
        # print(tbody)
        td = tbody.find_all('td', {'class': 'formItem'})
        count = 0
        for item in td:
            text = item.get_text()
            active.append(text)
        finalAct = []
        for i in range(len(active)):
            if i in skip:
                continue
            else:
                finalAct.append(active[i])

        return (finalAct)
    except AttributeError as err:
        print(err)
        return None

# --------------------------------------------------


def getInactive(page):
    inactive = []
    try:
        table = page.find('td', text="Inactive Ingredients")
        tr = table.parent
        tbody = tr.parent
        td = tbody.find_all('td', {'class': 'formItem'})
        for item in td:
            text = item.get_text()
            inactive.append(text)
        return (inactive)
    except AttributeError as err:
        print(err)
        return None
# --------------------------------------------------


def getFormula(page):
    try:
        FigClass = page.find('div', {'class': 'Figure'})
        img = FigClass.find('img')
        chemFormula = img.attrs['src']
        return (chemFormula)
    except AttributeError as err:
        print(err)
        return None
    except TypeError as err:
        print(err)
        return None


def main():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Gonzalez#1222",
        db="pharm_db")
    cursor = db.cursor()

    for i in range(1832, 1864):
        drug = name[i]
        url = urls[i]
        page = requests.get(url)
        result = BeautifulSoup(page.text, "html.parser")
        # description = getInfo(result)
        try:
            formula = getFormula(result)
            inactiveIngredients = getInactive(result)
            activeIngredients = getActiveIng(result)
            biolink = bioChemLink(result)
            time.sleep(8)

            add_drug = ("Insert into DailymedDrug(drugID, DrugName, dailyMedLink, chemicalFormula, summary, netWeight, biochemicalDataSummaryLink, genericName, brandNames, type, drugGroup, state)"
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            data_drug = (i, drug, url, formula, 'null', 0,
                         biolink, 'null', 'null', 'null', 'null', 'null')
            cursor.execute(add_drug, data_drug)

            for x in range(0, len(inactiveIngredients)-1, 2):
                add_ingredients = ("Insert into Inactive (drugID, name, strength)"
                                   "VALUES(%s,%s,%s)")
                data_ingredients = (
                    i, inactiveIngredients[x], inactiveIngredients[x+1])
                cursor.execute(add_ingredients, data_ingredients)

            for x in range(0, len(activeIngredients)-1, 2):
                add_ingredients = ("Insert into ActiveIngredient (drugID, name, strength)"
                                   "VALUES(%s,%s,%s)")
                data_ingredients = (
                    i, activeIngredients[x], activeIngredients[x+1])
                cursor.execute(add_ingredients, data_ingredients)

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
