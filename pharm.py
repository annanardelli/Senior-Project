
import pandas as pd

product = []
data = pd.read_csv('products.txt', sep="~", header=None, skiprows=1)
data.columns = ["Ingredient", "DF Route", "Trade_Name", "Applicant", "Strength", "Appl_Type",
                "Appl_No", "Product_No", "TE_Code", "Approval_Date", "RLD", "RS", "Type", "Applicant_Full_Name"]
print(data.head())
print(data.iloc[1])

'''with open('products.txt', 'r', encoding="utf-8") as file:
    print("file is opened")
    lineNum = 1
    for line in file:
        while (lineNum < 6):
            content = file.readline()
            lineNum += 1
            content = content.split('\n')
            product.append(content)

            # print(product)

element = product[0]
print(element)
element = str(element)
print(element.split("~"))


file.close()'''
