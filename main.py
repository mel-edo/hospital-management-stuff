'''CS class 12th Project

Members:-
1) Raunak
2) Saurabh

Title:- Patient information system

'''

import mysql.connector as c
import random

db_user = input("Enter database username:- ")
db_password = input("Enter database password:- ")

con = c.connect(host="localhost", user=db_user, password=db_password)

cur = con.cursor()

# Creating the database and the tables
# Going to make 3 tables, Patients, Doctors, Services in the hospital

cur.execute("create database if not exists hospital")
cur.execute("use hospital")

cur.execute("create table if not exists Patients(PatientID int AUTO_INCREMENT PRIMARY KEY, Name varchar(50), Age int, Gender varchar(20), Phone int, Bloodgroup varchar (10))")

cur.execute("create table if not exists Doctors(DoctorID int AUTO_INCREMENT PRIMARY KEY, Name varchar(50), Specialization varchar(50), RoomNo int, Phone char(10), Timeslot varchar(10))")

cur.execute("create table if not exists Services(ServiceID int AUTO_INCREMENT PRIMARY KEY, Services varchar(50), RoomNo int)")

appointments = {}

def register_patient():

    # Asking for details of patients to be inserted into the patients table

    name = input("Enter patient's name:- ")
    age = int(input("Enter patient's age:- "))
    gender = input("Enter patient's gender:- ")
    phone = int(input("Enter patient's phone no.:- "))
    blood = input("Enter patient's blood group:- ")

    # Inserting the patient's information into the table

    cur.execute("insert into Patients (Name, Age, Gender, Phone, Bloodgroup) values(%s, %s, %s, %s, %s)", (name, age, gender, phone, blood))

    con.commit()

    cur.execute("select * from Patients order by PatientID desc")
    print()
    print(cur.fetchone(), "has been registered!")
    print()

def register_doctor():

    # Asking for details of doctors to be inserted into the doctors table

    name = input("Enter doctors name:- ")
    specialization = input("Enter doctors specialization:- ")
    phone = int(input("Enter doctors phone no.:- "))
    roomNo = int(input("Enter doctors RoomNo:- "))
    timeslot = input("Enter doctors timeslot:- ")

    # Inserting the doctors information into the table

    cur.execute("insert into Doctors (Name, Specialization, RoomNo, Phone, Timeslot) values(%s, %s, %s, %s, %s)", (name, specialization, roomNo, phone, timeslot))

    con.commit()
    print()
    cur.execute("select * from Doctors order by DoctorID desc")
    print(cur.fetchone(), "has been registered!")
    print()

def register_service():

    # Asking for details of services

    name = input("Enter service name:- ")
    roomNo = int(input("Enter doctors RoomNo:- "))

    # Inserting data into table

    cur.execute("insert into Services (Services, RoomNo) values(%s, %s)", (name, roomNo))

    con.commit()
    print()
    cur.execute("select * from Services order by ServiceID desc")
    print(cur.fetchone(), "has been registered!")
    print()

def appointment_patient():

    p_id = int(input("Enter your id:- "))
    print("Which timeslot do you want to book a appointment in? (Morning, Afternoon, Evening, Night")
    timeslot = input("Enter one of the above:- ")  # Gets the timeslot in which patient wants to book

    if timeslot not in ("Morning", "Afternoon", "Evening", "Night"):
        print("Please enter a correct timeslot from one of the above!")

    else:
        print("The following doctors are available in this timeslot:-")
        cur.execute("select DoctorID, Name, RoomNo, Specialization from Doctors where Timeslot=%s", (timeslot))
        choices = []  # Adds all doctorIDs into this list for random selection

        a = 0
        while a is not None:
            a = cur.fetchone()
            print(a)
        cur.execute("select DoctorID from Doctors where Timeslot=%s", (timeslot))

        a = 0
        while a is not None:
            a = cur.fetchone()[0]
            choices.append(a)

        print("Do you want appointment with specific doctor? (y/n) (Default is n)")
        app = input("Enter your choice:- ")

        if app == "y":
            d_id = input("Enter DoctorID of whom you want an appointment with:- ")
            appointments[d_id] += [p_id]  # Adds the patient to associate with the doctors key
            print("Your appointment has been set in your preffered timeslot!")

        else:
            ch1 = random.choice(choices)
            appointments[ch1] += [p_id]
            print("Your appointment has been set in your preffered timeslot!")

def appointment_doctor():

    d_id = int(input("Enter your id:-"))
    print("You have appointments with the following people in your timeslot:-")
    print(appointments[d_id])

def list_doc():

    # Listing all the doctors along with their specialization, RoomNo and their timeslot

    cur.execute("select Name, RoomNo, Specialization, Timeslot from Doctors order by Timeslot")
    a = 0
    while a is not None:
        a = cur.fetchone()
        print(a)

def list_serv():

    # Listing all the services along with their RoomNo

    cur.execute("select Services, RoomNo from Services")

    a = 0
    while a is not None:
        a = cur.fetchone()
        print(a)

def modify():

    # Modifying either patients,doctors or services info
    # Modification means either updating current data or deleting current data (adding data takes place in register function)

    print("Which data do you want to modify?\n")
    print("1) Patients\n2) Doctors\n3) Services")

    modify_ch = int(input("Enter one of the numbers(1-3) above to proceed (Default is Patients):- "))
    print("--------------------------------")

    if modify_ch == 2:  # Doctors case

        row = int(input("Enter doctor's ID whose info you want to modify?:- "))

        col = input("Which column do you want to modify?:- ")
        cur.execute("select %s from Doctors where DoctorID=%s", (col, row))
        old = cur.fetchone()[0]

        print("Do you want to update current data or delete data?")
        up_del = int(input("Enter 1 or 2 (default is 1):- "))

        if up_del == 2:  # Deleting data case

            print("Do you want to delete specific content from row or entire row?")

            delw = int(input("Enter 1 or 2 (default is 1):- "))

            if delw == 2:
                cur.execute("delete from Doctors where DocotorID = %s", (row))
                con.commit()

                return "Given row was deleted!"

            else:
                cur.execute("update Doctors set %s = NULL where DoctorID = %s", (old, row))
                con.commit()

                return "Given value in the row was deleted!"

        else:  # Updating data case

            upd = input("Enter new value you want to enter")

            if col == "RoomNo":
                cur.execute("update Doctor set %s = %s where DoctorID = %s", (int(old), int(upd), row))
                con.commit()

                return "Given row was updated!"

            else:
                cur.execute("update Doctor set %s = %s where DoctorID = %s", (old, upd, row))
                con.commit()

                return "Given row was updated!"

    elif modify_ch == 3:  # Services case

        row = int(input("Enter service's ID whose info you want to modify?:- "))

        col = input("Which column do you want to modify?:- ")
        cur.execute("select %s from Services where ServiceID=%s", (col, row))
        old = cur.fetchone()[0]

        print("Do you want to update current data or delete data?")
        up_del = int(input("Enter 1 or 2 (default is 1):- "))

        if up_del == 2:  # Deleting data case

            print("Do you want to delete specific content from row or entire row?")

            delw = int(input("Enter 1 or 2 (default is 1):- "))

            if delw == 2:
                cur.execute("delete from Services where ServiceID = %s", (row))
                con.commit()

                return "Given row was deleted!"

            else:
                cur.execute("update Services set %s = NULL where ServiceID = %s", (old, row))
                con.commit()

                return "Given value in the row was deleted!"

        else:  # Updating data case

            upd = input("Enter new value you want to enter")

            if col == "RoomNo":
                cur.execute("update Services set %s = %s where ServiceID = %s", (int(old), int(upd), row))
                con.commit()

                return "Given row was updated!"

            else:
                cur.execute("update Services set %s = %s where ServiceID = %s"), (old, upd, row)
                con.commit()

                return "Given row was updated!"

    else:  # Patients case

        row = int(input("Enter Patient's ID whose info you want to modify?:- "))

        col = input("Which column do you want to modify?:- ")

        cur.execute("select %s from Patients where PatientID=%s", (col, row))
        print(cur.fetchall())

        print("Do you want to update current data or delete data?")
        up_del = int(input("Enter 1 or 2 (default is 1):- "))

        if up_del == 2:  # Deleting data case

            print("Do you want to delete specific content from row or entire row?")

            delw = int(input("Enter 1 or 2 (default is 1):- "))

            if delw == 2:
                cur.execute("delete from Patients where PatientID = %s", (row))
                con.commit()

                return "Given row was deleted!"

            else:
                cur.execute("update Patients set %s = NULL where PatientID = %s", (old, row))
                con.commit()

                return "Given value in the row was deleted!"

        else:  # Updating data case

            upd = input("Enter new value you want to enter:- ")

            if col == "Age":
                cur.execute("update Patients set %s = %s where PatientID = %s", (int(old), int(upd), row))
                con.commit()

                return "Given row was updated!"

            else:
                cur.execute("update Patients set %s = %s where PatientID = %s", (old, upd, row))
                con.commit()

                return "Given row was updated!"

# Main loop

while True:

    print("Hospital Management system:-\n")

    print("1) Register(patient)\n2) Register(doctor)\n3) Register(service)\n4) Make an Appointment(patient)\n5) Check Appointments(doctor)\n6) List of doctors\n7) List of services\n8) Edit Data\n9) Exit")

    ch = int(input("Enter one of the numbers(1-9) above to proceed:- "))
    print("--------------------------------")
    print()

    if ch not in range(1, 10):
        print("Please enter from one of the numbers in the range!\n")
        continue

    else:
        if ch == 9:
            print("Thank you for using our program!")
            print("--------------------------------")

            cur.close()

            con.close()

            break

        elif ch == 1:
            register_patient()

        elif ch == 2:
            register_doctor()

        elif ch == 3:
            register_service()

        elif ch == 4:
            appointment_patient()

        elif ch == 5:
            appointment_doctor()

        elif ch == 6:
            list_doc()

        elif ch == 7:
            list_serv()

        elif ch == 8:
            modify()
