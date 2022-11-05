import sqlite3

def pass_check():
    print("-------------------------------------------------------------")
    print("  -    --    -   ----   -      ----   ----   --    --   ----")
    print("   -  -  -  -    ----   -      -      -  -   - -  - -   ----")
    print("    --    --     ----   ----   ----   ----   -  --  -   ----")
    print("-------------------------------------------------------------")
    print("-------------------WELCOME TO DATABASE-----------------------")
    print("ENTER USER ID: ",end='')
    user_id=input()
    print("-------------------------------------------------------------")
    conn = sqlite3.connect('user.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS user(user_id,user_name,password) ''')
    cur.execute('SELECT * FROM user WHERE user_id')
    row = cur.fetchall()
    conn.commit()
    cur.close()
    a="YES"
    count=0
    for i in row:
        if (i[0]==user_id):
            print("CONNECTING TO UserID:",user_id)
            print("-------------------------------------------------------------")
            while (a):
                if(count==4):
                    break
                count+=1
                print("Enter UserName: ",end='')
                user_name=input()
                if(i[1]==user_name):
                    a="NO"
                    print("USER NAME FOUND")
                    print("-------------------------------------------------------------")
                    password_db=i[2]
                    break
                elif(count==3):
                    print("ERROR:USER NAME OR USER ID NOT FOUND.")
                    print("EXITING...")
                    break
                else:
                    print("ERROR:USER NAME OR USER ID NOT FOUND.\n PRESS Q TO QUIT \n PRESS C TO TRY AGAIN")
                    choice=input()
                    if(choice=='Q' or choice=='q'):
                        print("-------------------------------------------------------------")
                        print("EXITING...")
                        break
                    elif(choice=='C' or choice=='c'):
                        print("RECONNECTING...")
                        print("-------------------------------------------------------------")
                        print(3-count,"ATTEMPS LEFT")
                        continue
                    else:
                        for j in range(2):
                            print("-------------------------------------------------------------")
                            print("Please Enter a proper selection")
                            print(" PRESS Q TO QUIT \n PRESS C TO TRY AGAIN")
                            choice=input()
                            if(choice=='Q' or choice=='q'):
                                print("-------------------------------------------------------------")
                                print("EXITING...")
                                break
                            elif(choice=='C' or choice=='c'):
                                print("RECONNECTING...")
                                print("-------------------------------------------------------------")
                                print(3-count,"ATTEMPS LEFT")
                                continue
                        break

    if(a=="NO"):
        print("ENTER PASSWORD: ",end='')
        password=input()
        if(password==password_db):
            print("PASSWORD ACCEPTED")
            print("-------------------------------------------------------------")
            print("LOGGING YOU IN")
        else:
            print("WRONG PASSWORD TRY AGAIN")
            for j in range(3):
                print("-------------------------------------------------------------")
                print("ENTER PASSWORD: ",end='')
                password=input()
                if(password==password_db):
                    print("PASSWORD ACCEPTED")
                    print("LOGGING YOU IN")
                    break
                print("WRONG PASSWORD TRY AGAIN",(3-j-1),"ATTEMPS LEFT")

    if(a=="YES"):
        print("Enter Valid Data")
        return False
    return True

def add(num):
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS registered_vehicles(state TEXT,ran TEXT,plateno TEXT,address TEXT,vehicle_holder_name TEXT,Model_name TEXT,Manufacturer TEXT,Vehicle_color TEXT) ''')
    row = cur.fetchone()
    st=num[:4]
    ra=num[4:6]
    pn=num[6:]
    print("Enter Vehicle holders name: ",end='')
    name=input()
    print("Enter Vehicle manufacturer name: ",end='')
    ma_name=input()
    print("Enter model name: ",end='')
    mo_name=input()
    print("Enter Vehicle colour: ",end='')
    v_color=input()
    print("Enter address: ",end='')
    addre=input()
    cur.execute('''INSERT INTO registered_vehicles(state,ran,plateno,address,vehicle_holder_name,Model_name,Manufacturer,Vehicle_color) VALUES(?,?,?,?,?,?,?,?)''',(st,ra,pn,addre,name,mo_name,ma_name,v_color))
    print("Successfully entered data")
    conn.commit()
    cur.close()
def dele(num):
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    st=num[:4]
    ran=num[4:6]
    plno=num[6:]
    try:
        cur.execute('''DELETE FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
    except:
        print("Vehicle number not found!!!")
    conn.commit()
    cur.close()

def det(num):
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    st=num[:4]
    ran=num[4:6]
    plno=num[6:]
    try:
        cur.execute('''SELECT vehicle_holder_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Name of the vehicle holder:",row[0])
        cur.execute('''SELECT address FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Adress of owner:",row[0])
        cur.execute('''SELECT Model_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Name of the model:",row[0])
        cur.execute('''SELECT Manufacturer FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Vehicle Manufacturer:",row[0])
        cur.execute('''SELECT Vehicle_color FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Vehicle Colour:",row[0])
    except:
        print("Vehicle number not found!!!")
    conn.commit()
    cur.close()

def upd(num):
    st=num[:4]
    ran=num[4:6]
    plno=num[6:]
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    try:
        cur.execute('''SELECT vehicle_holder_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Name of the vehicle holder:",row[0])
        cur.execute('''SELECT address FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Adress of owner:",row[0])
        cur.execute('''SELECT Model_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Name of the model:",row[0])
        cur.execute('''SELECT Manufacturer FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Vehicle Manufacturer:",row[0])
        cur.execute('''SELECT Vehicle_color FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Vehicle Colour:",row[0])
        print("-------------------------------------------------------------")
        print("-------------------------------------------------------------")
        print("1.Change vehicle holder name")
        print("2.Change Address of Owner")
        print("3.Change Name of the model")
        print("4.Change vehicle manufacturer name")
        print("5.Change vehicle colour")
        print("Press the corresponding numbers for changing: ",end='')
        n=int(input())
        print("-------------------------------------------------------------")
        print("-------------------------------------------------------------")
        if(n==1):
            print("Enter new vehicle holder name to be updated: ",end='')
            to_update=input()
            cur.execute('''SELECT vehicle_holder_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Old owner name: ",row[0])
            print("UPDATING...")
            cur.execute('''UPDATE registered_vehicles SET vehicle_holder_name=(?) WHERE state=(?) AND ran=(?) AND plateno=(?)''',(to_update,st,ran,plno))
            conn.commit()
            cur.execute('''SELECT vehicle_holder_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Updated owner name: ",row[0])

        elif(n==2):
            print("Enter new address to be updated: ",end='')
            to_update=input()
            cur.execute('''SELECT address FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Old Adress of owner:",row[0])
            print("UPDATING...")
            cur.execute('''UPDATE registered_vehicles SET address=(?) WHERE state=(?) AND ran=(?) AND plateno=(?)''',(to_update,st,ran,plno))
            conn.commit()
            cur.execute('''SELECT address FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Updated address: ",row[0])

        elif(n==3):
            print("Enter new model name to be updated: ",end='')
            to_update=input()
            cur.execute('''SELECT Model_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Old model name:",row[0])
            print("UPDATING...")
            cur.execute('''UPDATE registered_vehicles SET Model_name=(?) WHERE state=(?) AND ran=(?) AND plateno=(?)''',(to_update,st,ran,plno))
            conn.commit()
            cur.execute('''SELECT Model_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Updated model name: ",row[0])

        elif(n==4):
            print("Enter new vehicle manufacturer name to be updated: ",end='')
            to_update=input()
            cur.execute('''SELECT Manufacturer FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Old model name:",row[0])
            print("UPDATING...")
            cur.execute('''UPDATE registered_vehicles SET Manufacturer=(?) WHERE state=(?) AND ran=(?) AND plateno=(?)''',(to_update,st,ran,plno))
            conn.commit()
            cur.execute('''SELECT Manufacturer FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Updated manufacturer name: ",row[0])

        elif(n==5):
            print("Enter new vehicle colour to be updated: ",end='')
            to_update=input()
            cur.execute('''SELECT Vehicle_color FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Old model name:",row[0])
            print("UPDATING...")
            cur.execute('''UPDATE registered_vehicles SET Vehicle_color=(?) WHERE state=(?) AND ran=(?) AND plateno=(?)''',(to_update,st,ran,plno))
            conn.commit()
            cur.execute('''SELECT Vehicle_color FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
            row = cur.fetchone()
            print("Updated Vehicle color: ",row[0])

        else:
            print("Enter a valid selection.\n TRY AGAIN")
    except:
        print("Vehicle number not found")
    cur.close()

def track(num):
    conn = sqlite3.connect('rx.sqlite')
    cur = conn.cursor()
    st=num[:4]
    ran=num[4:6]
    plno=num[6:]
    print("-------------------------------------------------------------")
    print("-------------------------------------------------------------")
    try:
        cur.execute('''SELECT vehicle_holder_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Name of the vehicle holder:",row[0])
        cur.execute('''SELECT address FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Adress of owner:",row[0])
        cur.execute('''SELECT Model_name FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Name of the model:",row[0])
        cur.execute('''SELECT Manufacturer FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Vehicle Manufacturer:",row[0])
        cur.execute('''SELECT Vehicle_color FROM registered_vehicles WHERE state=(?) AND ran=(?) AND plateno=(?)''',(st,ran,plno))
        row = cur.fetchone()
        print("Vehicle Colour:",row[0])
        conn.commit()
        cur.close()
    except:
        print("Vehicle number not found in registered list!!!")
    print("-------------------------------------------------------------")
    print("-------------------------------------------------------------")
    try:
        st=num[:2]
        dist=num[2:4]
        ran=num[4:6]
        plno=num[6:]
        conn = sqlite3.connect('rx.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT time FROM number_plate WHERE state=(?) AND dist=(?) AND ran=(?) AND plateno=(?)''', (st,dist,ran,plno))
        row=cur.fetchall()
        for i in row:
            i=str(i)
            print("Detected at date:",i[2:12],end='  ')
            print(" at time:",i[13:24])
        cur.close()
        if(row):
            print("-------------------------------------------------------------")
        else:
            print("Vehicle is not detected till now")
    except:
        print("Vehicle is not detected till now")
    print("-------------------------------------------------------------")
    print("-------------------------------------------------------------")


def func():
    print("Enter the number of the operations listed below")
    print("1.Register a new vehicle")
    print("2.Delete an existing vehicle")
    print("3.Check details of an existing vehicle")
    print("4.Update details of an existing vehicles")
    print("5.Track a vehicle")
    print("Your choice: ",end='')
    try:
        fchoice=int(input())
    except:
        print("Enter a valid choice")
        func()
    if(fchoice==1):#Registering new vehicle
        num=' '
        while(len(num)!=10):
            print("Enter the Vehicle number of length 10: ",end=' ')
            num=input()
            if(len(num)!=10):
                print("To exit press Q  || To try again press ENTER \nEnter choice:")
                num=input()
                if (num=='q' or num=='Q'):
                    return None
        add(num)

    elif(fchoice==2):#Delete an existing vehicle
        num=' '
        while(len(num)!=10):
            print("Enter the Vehicle number of length 10: ",end=' ')
            num=input()
            if(len(num)!=10):
                print("to exit press q Enter a valid number:")
                num=input()
                if (num=='q' or num=='Q'):
                    return None
        dele(num)

    elif(fchoice==3):#Check details of an existing vehicle
        num=' '
        while(len(num)!=10):
            print("Enter the Vehicle number of length 10: ",end=' ')
            num=input()
            if(len(num)!=10):
                print("to exit press q Enter a valid number:")
                num=input()
                if (num=='q' or num=='Q'):
                    return None
        det(num)

    elif(fchoice==4):#Update details of an existing vehicles
        num=' '
        while(len(num)!=10):
            print("Enter the Vehicle number of length 10: ",end=' ')
            num=input()
            if(len(num)!=10):
                print("to exit press q Enter a valid number:")
                num=input()
                if (num=='q' or num=='Q'):
                    return None
        upd(num)

    elif(fchoice==5):#Track a vehicle
        num=' '
        while(len(num)!=10):
            print("Enter the Vehicle number of length 10: ",end=' ')
            num=input()
            if(len(num)!=10):
                print("to exit press q Enter a valid number:")
                num=input()
                if (num=='q' or num=='Q'):
                    return None
        track(num)

    else:
        print("Enter valid number")

while(1):
    if(pass_check()):
        func()
    print("-------------------------------------------------------------")
    print("PRESS Q AND ENTER IF YOU WANT TO EXIT THE APPLICATION OR PRESS ENTER TO CONTINUE: ",end='')
    choice=input()
    print("Pressed ",choice)
    if(choice=='Q' or choice=='q'):
        print("-------------------------------------------------------------")
        print("EXITING...")
        break
    print("-------------------------------------------------------------")
    print("-------------------------------------------------------------")
    print("------------------Moving you to login page-------------------")
    print("-------------------------------------------------------------")
    print("-------------------------------------------------------------")
