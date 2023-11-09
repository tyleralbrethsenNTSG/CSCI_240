# Reference 09-showingConnection
# Do not hard code credentials: use secrets.json and fetchall

import mysql.connector, os, json


with open('/home/tyleralbrethsen/CSCI_240/html_practice/dynamic_html/mu_secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCred']


connection = mysql.connector.connect(**creds)

mycursor = connection.cursor()
mycursor.execute("select * from Person")
myresult = mycursor.fetchall()

print(f"{myresult=}")

print("In the Person table, we have the following items:")
for row in myresult:
    print(row)

mycursor.close()
connection.close()
