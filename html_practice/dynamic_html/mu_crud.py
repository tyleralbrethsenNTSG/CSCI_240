#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, json


app = Flask(__name__)

with open('/home/tyleralbrethsen/CSCI_240/html_practice/dynamic_html/mu_secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCred']

@app.route('/', methods=['GET'])
def showPerson():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a FirstName, LastName, and USAU_Number 'GET' variable, insert the new value into the database
    newFirst = request.args.get('FirstName')
    newLast = request.args.get('LastName')
    newUSAU = request.args.get('USAU_Number')
    if newFirst is not None and newLast is not None and newUSAU is not None:
        mycursor.execute("INSERT into Person (FirstName, LastName, USAU_Number) values (%s, %s, %s)", (newFirst, newLast, newUSAU))
        connection.commit()
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('PersonID')
        mycursor.execute("DELETE from Person where PersonID=%s", (deleteID,))
        connection.commit()

    # Fetch the current values of the Person table
    mycursor.execute("Select * from Person")
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('mu_person_list.html', collection=myresult)

@app.route("/updatePerson")
def updatePerson():
    connection = mysql.connector.connect(**creds)

    id = request.args.get('PersonID')
    first = request.args.get('FirstName')
    last = request.args.get('LastName')
    usau = request.args.get('USAU_Number')
    if id is None:
        return "Error, id not specified"
    elif first is not None and last is not None and usau is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Person set FirstName=%s, LastName=%s, USAU_Number=%s where PersonID=%s", (first, last, usau, id))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showPerson'))

    mycursor = connection.cursor()
    mycursor.execute("select * from Person where PersonID=%s;", (id,))
    _, existingFirst, existingLast, existingUSAU = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('mu_person_update.html', id=id, existingFirst=existingFirst, existingLast=existingLast, existingUSAU=existingUSAU)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")