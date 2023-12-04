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
    else:
        mycursor.execute("SELECT PersonID, FirstName, LastName, USAU_Number from Person")
        pageTitle = "Showing all Missoula Ultimate members"
        all_members = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('mu_person_list.html', personList = all_members, pageTitle = pageTitle)

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
                         where Person.PersonID = %s""", (PersonID,))
        all_committees = mycursor.fetchall()

        mycursor.execute("""SELECT Person.FirstName, Person.LastName from Person
                         where Person.PersonID = %s""", (personID,))
        memberFirst = mycursor.fetchone()[0]
        memberLast = mycursor.fetchone()[1]
        pageTitle = f"Showing all committees containing {memberFirst} {memberLast}"
    else:
        mycursor.execute("SELECT CommitteeID, Committee.Name from Committee")
        pageTitle = "Showing all Missoula Ultimate committees"
        all_committees = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('mu_committee_list.html', committeeList = all_committees, pageTitle = pageTitle)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")