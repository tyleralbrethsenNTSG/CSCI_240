#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, json

app = Flask(__name__)

with open('/home/tyleralbrethsen/CSCI_240/html_practice/dynamic_html/mu_secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCred']

# Simple Index Page with a couple of hyperlinks
@app.route('/', methods=['GET'])
def index():
    return render_template("mu_base_crud.html")

# Page that shows all members and adds new members (Create and Read)
@app.route('/members', methods=['GET', 'POST'])
def showPeople():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    first = request.args.get('FirstName')
    last = request.args.get('LastName')
    usau = request.args.get('USAU_Number')

    if first is not None and last is not None and usau is not None:
        mycursor.execute("INSERT INTO Person (FirstName, LastName, USAU_Number) VALUES ('%s', '%s', '%s');" % (first, last, usau))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showPeople'))
    
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('PersonID')
        mycursor.execute("DELETE from Person where PersonID = %s", (deleteID,))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showPeople'))
    
    else:
        mycursor.execute("SELECT PersonID, FirstName, LastName, USAU_Number FROM Person")
        pageTitle = "Missoula Ultimate"
        all_members = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('mu_person_list.html', personList = all_members, pageTitle = pageTitle)

# Page that shows all committees and adds new committees (Create and Read)
@app.route('/committees', methods=['GET'])
def showCommittees():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    newCommittee = request.args.get('Name')

    if newCommittee is not None:
        mycursor.execute("INSERT INTO Committee (Name) VALUES ('%s');" % (newCommittee))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showCommittees'))
    
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('CommitteeID')
        mycursor.execute("DELETE from Committee where CommitteeID = %s", (deleteID,))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showCommittees'))

    else:
        mycursor.execute("SELECT CommitteeID, Committee.Name FROM Committee")
        pageTitle = "Missoula Ultimate"
        all_committees = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('mu_committee_list.html', committeeList = all_committees, pageTitle = pageTitle)

# This page udates member information
@app.route("/updatePerson")
def updatePerson():
    connection = mysql.connector.connect(**creds)

    id = request.args.get('PersonID')
    first = request.args.get('FirstName')
    last = request.args.get('LastName')
    usau = request.args.get('USAU_Number')

    if id is None:
        return "Error, ID not specified"
    elif first is not None and last is not None and usau is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Person set FirstName = %s, LastName = %s, USAU_Number = %s where PersonID = %s", (first, last, usau, id))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showPeople'))

    mycursor = connection.cursor()
    mycursor.execute("select * from Person where PersonID=%s;", (id,))
    _, existingFirst, existingLast, existingUSAU = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('mu_person_update.html', id=id, existingFirst=existingFirst, existingLast=existingLast, existingUSAU=existingUSAU)

# This page updates Committee information
@app.route("/updateCommittee")
def updateCommittee():
    connection = mysql.connector.connect(**creds)

    id = request.args.get('CommitteeID')
    name = request.args.get('Name')

    if id is None:
        return "Error, ID not specified"
    elif id is not None and name is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Committee set Name = %s where CommitteeID = %s", (name, id))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showCommittees'))

    mycursor = connection.cursor()
    mycursor.execute("select * from Committee where CommitteeID=%s;", (id,))
    _, existingName = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('mu_committee_update.html', id=id, existingName=existingName)



if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")