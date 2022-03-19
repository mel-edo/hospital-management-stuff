'''CS class 12th Project

Members:-
1) Raunak
2) Saurabh

Title:- Hospital Management system

'''

import mysql.connector as c

db_user = input("Enter database username:- ")
db_password = input("Enter database password:- ")

con = c.connect(host="localhost", user=db_user, password=db_password)

cur = con.cursor(buffered=True)

# Creating the database and the tables
# Going to make 3 tables, Patients, Doctors, Services in the hospital

cur.execute("create database if not exists hospital")
cur.execute("use hospital")

cur.execute("create table if not exists Patients(PatientID int AUTO_INCREMENT PRIMARY KEY, Name varchar(50), Age int, Gender varchar(20), Phone char(10), Bloodgroup varchar (10))")

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

    cur.execute("insert into Patients (Name, Age, Gender, Phone, Bloodgroup) values((%s), (%s), (%s), (%s), (%s))", (name, age, gender, phone, blood))

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
    timeslot = input("Enter doctors timeslot (Morning, Afternoon, Evening, Night (Case-Sensitive)):- ")

    # Inserting the doctors information into the table

    cur.execute("insert into Doctors (Name, Specialization, RoomNo, Phone, Timeslot) values((%s), (%s), (%s), (%s), (%s))", (name, specialization, roomNo, phone, timeslot))

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

    cur.execute("insert into Services (Services, RoomNo) values((%s), (%s))", (name, roomNo))

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
        print()
        print("The following doctors are available in this timeslot:-\n(DoctorID, Name, RoomNo, Specialization)")
        print()
        cur.execute(f"select DoctorID, Name, RoomNo, Specialization from Doctors where Timeslot='{timeslot}'")

        data = cur.fetchall()
        for a in data:
            print(a)  # Prints the name of the available doctors
        cur.execute(f"select DoctorID from Doctors where Timeslot='{timeslot}'")

        print()

        d_id = input("Enter DoctorID of whom you want an appointment with:- ")

        try:
            appointments[d_id] += [p_id]    # Adds the patient to associate with the doctors key
        except:
            appointments[d_id] = [p_id]

        print()
        print("Your appointment has been set in your preffered timeslot!")
        print()

def appointment_doctor():

    d_id = input("Enter your id:-")

    if d_id not in appointments:
        print("You have no appointments currently!")

    else:
        print("You have appointments with the following people in your timeslot:-")
        print()
        ids = appointments[d_id]  # Storing the id's of the patients in this list
        print("(PatientID, Name, Age, Gender, Phone, Bloodgroup)")
        for i in ids:
            cur.execute(f"select * from Patients where PatientID = {i}")
            print(cur.fetchone())
        print()

def list_doc():

    # Listing all the doctors along with their specialization, RoomNo and their timeslot

    cur.execute("select Name, RoomNo, Specialization, Timeslot from Doctors order by Timeslot")
    print("Name, RoomNo, Specialization, Timeslot")

    for a in cur.fetchall():
        print(a)
    print()

def list_serv():

    # Listing all the services along with their RoomNo

    cur.execute("select Services, RoomNo from Services")
    print("Name, RoomNo")
    for a in cur.fetchall():
        print(a)
    print()

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

        print("Do you want to update current data or delete data?")
        up_del = int(input("Enter 1 or 2 (default is 1):- "))

        if up_del == 2:  # Deleting data case

            print("Do you want to delete specific content from row or entire row?")

            delw = int(input("Enter 1 or 2 (default is 1):- "))

            if delw == 2:
                cur.execute(f"delete from Doctors where DoctorID = {row}")
                con.commit()

                print("Given row was deleted!")

            else:
                cur.execute(f"update Doctors set '{col}' = NULL where DoctorID = {row}")
                con.commit()

                print("Given value in the row was deleted!")

        else:  # Updating data case

            upd = input("Enter new value you want to enter:- ")

            if col == "RoomNo":
                cur.execute(f"update Doctors set {col} = {int(upd)} where DoctorID = {row}")
                con.commit()

                print("Given row was updated!")

            else:
                cur.execute(f"update Doctors set {col} = '{upd}' where DoctorID = {row}")
                con.commit()

                print("Given row was updated!")

    elif modify_ch == 3:  # Services case

        row = int(input("Enter service's ID whose info you want to modify?:- "))

        col = input("Which column do you want to modify?:- ")

        print("Do you want to update current data or delete data?")
        up_del = int(input("Enter 1 or 2 (default is 1):- "))

        if up_del == 2:  # Deleting data case

            print("Do you want to delete specific content from row or entire row?")

            delw = int(input("Enter 1 or 2 (default is 1):- "))

            if delw == 2:
                cur.execute(f"delete from Services where ServiceID = {row}")
                con.commit()

                print("Given row was deleted!")

            else:
                cur.execute(f"update Services set {col} = NULL where ServiceID = {row}")
                con.commit()

                print("Given value in the row was deleted!")

        else:  # Updating data case

            upd = input("Enter new value you want to enter:- ")

            if col == "RoomNo":
                cur.execute(f"update Services set {col} = {int(upd)} where ServiceID = {row}")
                con.commit()

                print("Given row was updated!")

            else:
                cur.execute(f"update Services set {col} = '{upd}' where ServiceID = {row}")
                con.commit()

                print("Given row was updated!")

    else:  # Patients case

        row = int(input("Enter Patient's ID whose info you want to modify?:- "))

        col = input("Which column do you want to modify?:- ")

        print("Do you want to update current data or delete data?")
        up_del = int(input("Enter 1 or 2 (default is 1):- "))

        if up_del == 2:  # Deleting data case

            print("Do you want to delete specific content from row or entire row?")

            delw = int(input("Enter 1 or 2 (default is 1):- "))

            if delw == 2:
                cur.execute(f"delete from Patients where PatientID = {row}")
                con.commit()

                print("Given row was deleted!")

            else:
                cur.execute(f"update Patients set {col} = NULL where PatientID = {row}")
                con.commit()

                print("Given value in the row was deleted!")

        else:  # Updating data case

            upd = input("Enter new value you want to enter:- ")

            if col == "Age":
                cur.execute(f"update Patients set {col} = {int(upd)} where PatientID = {row}")
                con.commit()

                print("Given row was updated!")

            else:
                cur.execute(f"update Patients set {col} = '{upd}' where PatientID = {row}")
                con.commit()

                print("Given row was updated!")

# Main loop

while True:
    print("--------------------------------")
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
