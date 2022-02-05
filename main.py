'''CS class 12th Project

Members:-
1) Raunak
2) Saurabh

Title:- Patient information system

(no. of people registered, vaccine takers, no. of shots, which one is it etc.)

Program should be able to:-
-search all records of patients
-track info of patients
-add, update, remove patient data and medicine data
-report generation for patients
-transactions
-report generation of patients

Adding project synopsis for easy access here:-
https://docs.google.com/document/d/1UYbQPDa1fvAXFaGIU2_KWfl-VtuCvlOuH5WvQmfIf68/edit?usp=sharing

'''

import mysql.connector as c
db_user = input("Enter database username:- ")
db_password = input("Enter database password:- ")
con = c.connect(host="localhost", user=db_user, password=db_password)
cur = con.cursor()

# Creating the database and the tables
# Going to make 3 tables, Patients, Doctors, Services in the hospital

cur.execute("create database if not exists hospital")
cur.execute("use hospital")

cur.execute("create table if not exists Patients(PatientID int PRIMARY KEY, Name varchar(50), Age int, Gender varchar(20), Phone int, Bloodgroup varchar (10))")

cur.execute("create table if not exists Doctors(DoctorID int PRIMARY KEY, Name varchar(50), Specialization varchar(50), RoomNo int)")

cur.execute("create table if not exists Services(ServiceID int PRIMARY KEY, Services varchar(50))")

# Main loop

while True:

    print("Hospital Management system:-\n")

    print("1) Register(patient)\n2) Make an Appointment(patient) \n3) Check Appointments(docotor)\n4) List of doctors\n5) List of services\n6) Edit Data\n7) Exit")

    ch = int(input("Enter one of the numbers(1-7) above to proceed:- "))
    print()

    if ch not in range(1, 8):
        print("Please enter from one of the numbers in the range!\n")
        continue

    else:
        if ch == 7:
            print("Thank you for using our program :praydge:")

            break
