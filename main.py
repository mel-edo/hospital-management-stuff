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

# NOTE TO CONTRIBUTORS:- I have replaced aadhar no. for patientID

import mysql.connector as c

db_user = input("Enter database username:- ")
db_password = input("Enter database password:- ")

con = c.connect(host="localhost", user=db_user, password=db_password)

cur = con.cursor()

# Creating the database and the tables
# Going to make 3 tables, Patients, Doctors, Services in the hospital

cur.execute("create database if not exists hospital")
cur.execute("use hospital")

cur.execute("create table if not exists Patients(PatientID int AUTO_INCREMENT PRIMARY KEY, Name varchar(50), Age int, Gender varchar(20), Phone int, Bloodgroup varchar (10))")

cur.execute("create table if not exists Doctors(DoctorID int AUTO_INCREMENT PRIMARY KEY, Name varchar(50), Specialization varchar(50), RoomNo int, Phone int)")

cur.execute("create table if not exists Services(ServiceID int AUTO_INCREMENT PRIMARY KEY, Services varchar(50), RoomNo int)")

def register_patient():

    # Asking for details of patients to be inserted into the patients table

    name = input("Enter patient's name:- ")
    age = int(input("Enter patient's age:- "))
    gender = input("Enter patient's gender:- ")
    phone = int(input("Enter patient's phone no.:- "))
    blood = input("Enter patient's blood group:- ")

    # Inserting the patient's information into the table

    cur.execute("insert into Patients (Name, Age, Gender, Phone, Bloodgroup) values({}, {}, {}, {}, {})").format(name, age, gender, phone, blood)

    con.commit()

    cur.execute("select * from Patients order by desc")

    return cur.fetchone()

def register_doctor():

    # Asking for details of doctors to be inserted into the doctors table

    name = input("Enter doctors name:- ")
    specialization = input("Enter doctors specialization:- ")
    phone = int(input("Enter doctors phone no.:- "))
    roomNo = int(input("Enter doctors RoomNo:- "))

    # Inserting the doctors information into the table

    cur.execute("insert into Doctors (Name, Specialization, RoomNo, Phone) values({}, {}, {}, {})").format(name, specialization, roomNo, phone)

    con.commit()

    cur.execute("select * from Doctors order by desc")

    return cur.fetchone()

def appointment_patient():
    pass

def appointment_doctor():
    pass

def list_doc():

    # Listing all the doctors along with their specialization and RoomNo

    cur.execute("select Name, RoomNo, Specialization from Doctors")

    return cur.fetchall()

def list_serv():

    # Listing all the services along with their RoomNo

    cur.execute("select Services, RoomNo from Services")

    return cur.fetchall()

def modify():

    # Modifying either patients,doctors or services info

    print("Which data do you want to modify?\n")

    print("1) Patients\n2) Doctors\n3) Services")
    modify_ch = int(input("Enter one of the numbers(1-3) above to proceed (Default is Patients):- "))
    print("--------------------------------")

    if modify_ch == 2:  # Doctors case
        pass

    elif modify_ch == 3:  # Services case
        pass

    else:  # Patients case
        pass

# Main loop

while True:

    print("Hospital Management system:-\n")

    print("1) Register(patient)\n2) Register(doctor)\n3) Make an Appointment(patient)\n4) Check Appointments(doctor)\n5) List of doctors\n6) List of services\n7) Edit Data\n8) Exit")

    ch = int(input("Enter one of the numbers(1-8) above to proceed:- "))
    print("--------------------------------")
    print()

    if ch not in range(1, 9):
        print("Please enter from one of the numbers in the range!\n")
        continue

    else:
        if ch == 7:
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
            appointment_patient()

        elif ch == 4:
            appointment_doctor()

        elif ch == 5:
            list_doc()

        elif ch == 6:
            list_serv()

        elif ch == 7:
            modify()
