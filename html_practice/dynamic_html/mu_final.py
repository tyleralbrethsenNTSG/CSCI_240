#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, json

app = Flask(__name__)

with open('/home/tyleralbrethsen/CSCI_240/html_practice/dynamic_html/mu_secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCred']

@app.route('/', methods=['GET'])
def index():
    return render_template("mu_base_crud.html")

@app.route('/members', methods=['GET'])
def showPeople():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a PersonID 'GET' variable, use this to refine the query
    personID = request.args.get('PersonID')
    first = request.args.get('FirstName')
    last = request.args.get('LastName')

    if personID is not None:
        mycursor.execute("""SELECT Person.PersonId, FirstName, LastName, USAU_Number from Person 
                         join PersonCommittee on Person.PersonID = PersonCommittee.PersonID
                         join Committee on Committee.CommitteeID = PersonCommittee.CommitteeID
                         where Committee.CommitteeID = %s""", (personID,))
        all_members = mycursor.fetchall()
        
        mycursor.execute("""SELECT Committee.Name from Committee
                         where Committee.CommitteeID = %s""", (personID,))
        committeeName = mycursor.fetchone()
        pageTitle = f"Showing all members of the {committeeName}"
    
    elif first is not None and last is not None:
        mycursor.execute(''' SQL INSERT STATEMENT HERE ''')
    
    
    else:
        mycursor.execute("SELECT PersonID, FirstName, LastName, USAU_Number from Person")
        pageTitle = "Showing all Missoula Ultimate members"
        all_members = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('mu_person_list.html', personList = all_members, pageTitle = pageTitle)


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
        return redirect(url_for('showPeople'))

    mycursor = connection.cursor()
    mycursor.execute("select * from Person where PersonID=%s;", (id,))
    _, existingFirst, existingLast, existingUSAU = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('mu_person_update.html', id=id, existingFirst=existingFirst, existingLast=existingLast, existingUSAU=existingUSAU)



@app.route('/committees', methods=['GET'])
def showCommittees():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a PersonID 'GET' variable, use this to refine the query
    personID = request.args.get('PersonID')
    if personID is not None:
        mycursor.execute("""SELECT Committee.CommitteeID, Committee.Name, Person.FirstName, Person.LastName, PersonCommittee.CommitteePosition from Person 
                         join PersonCommittee on Person.PersonID = PersonCommittee.PersonID
                         join Committee on Committee.CommitteeID = PersonCommittee.CommitteeID
                         where Person.PersonID = %s""", (personID,))
        all_committees = mycursor.fetchall()

        mycursor.execute("""SELECT Person.FirstName, Person.LastName from Person
                         where Person.PersonID = %s""", (personID,))
        memberFirst, memberLast = mycursor.fetchone()
        pageTitle = f"Showing all committees containing {memberFirst} {memberLast}"
    else:
        mycursor.execute("SELECT CommitteeID, Committee.Name from Committee")
        pageTitle = "Showing all Missoula Ultimate committees"
        all_committees = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('mu_committee_list.html', committeeList = all_committees, pageTitle = pageTitle)

@app.route("/updateCommittee")
def updateCommittee():
    connection = mysql.connector.connect(**creds)

    id = request.args.get('CommitteeID')
    name = request.args.get('Name')
    if id is None:
        return "Error, id not specified"
    elif id is not None and name is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Committee set Name=%s where CommitteeID=%s", (id, name))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showCommittee'))

    mycursor = connection.cursor()
    mycursor.execute("select * from Committee where CommitteeID=%s;", (id,))
    _, existingName = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('mu_committee_update.html', id=id, existingName=existingName)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")