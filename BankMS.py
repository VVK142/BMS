import mysql.connector
import bcrypt,sys

db= mysql.connector.connect(host='localhost',user='root',password='', database='BMS')
myc=db.cursor()
myc.execute('CREATE DATABASE IF NOT EXISTS BMS')
myc.execute("CREATE TABLE IF NOT EXISTS Admin(AID int NOT NULL AUTO_INCREMENT, AdName varchar(255), Official_Position varchar(255), Email varchar(255), PASSWORD varchar(255), PRIMARY KEY (AID))")
myc.execute('CREATE TABLE IF NOT EXISTS Customers(CID int NOT NULL AUTO_INCREMENT, AccountNumber int, CName varchar(255), Address varchar(255), Balance float, PASSWORD varchar(255), PRIMARY KEY(CID))')
# myc.execute('CREATE TABLE IF NOT EXISTS PassWord_Admin(AID int NOT NULL, Salt varchar(255),FOREIGN KEY (AID) REFERENCES Admin(AID))')
myc.execute('CREATE TABLE IF NOT EXISTS PassWord_Customer(CID int NOT NULL, Salt varchar(255), FOREIGN KEY (CID) REFERENCES Customers(CID))')

def menu():
    print("***   Banking System   ***")
    print("1: Add Admin")
    print("2: Move to Banking System")
    print("3: Exit")
    m=int(input("Enter your Choice: "))
    if m==1:
        print("***   Add Admin to Banking System   ***")
        id=int(input("Enter the Admin ID: "))
        Name=input("Enter the Admin Name: ")
        offp=input("Enter the Admin's Official position: ")
        email=input("Enter the Admin email id: ")
        pw=input("Enter the Admin password: ")
        # # pw=Admin123
        # # converting password to array of bytes 
        # bytes = pw.encode('utf-8') 
        # # generating the salt 
        # salt = bcrypt.gensalt() 
        # # Hashing the password 
        # pw1 = bcrypt.hashpw(bytes, salt) 
        # print(pw1)
        # print(type(pw1))
        myc.execute("INSERT INTO Admin (AID,AdName,Official_Position,Email,PASSWORD) VALUES(%s,%s,%s,%s,%s)",(id,Name,offp,email,pw))
        # myc.execute("INSERT INTO PassWord_Admin (AID, salt) Values(%s,%s)",(id,salt))
        db.commit()
        print("New Admin added Successfully")
    elif m==2:
        print( " ***  Bank Management System Menu  *** ") 
        main_menu()
    elif m==3: 
        print("Thankyou for using our services.")
        sys.exit()

def main_menu():
    
    print(" 1: Admin Login")
    print(" 2: Customer Login")
    print(" 3: Exit")
    x=int(input("Enter your Choice: "))
    if x==1:
        print("***   Welcome to Admin Panel!!!   ***")
        id=int(input("Enter the Admin ID: "))
        myc.execute("SELECT * FROM Admin WHERE AID=%s ",[id])
        for x in myc:
            pw2=x[4]
            print("old P: ",pw2)
            print(type(pw2))
        # myc.execute("SELECT * FROM PassWord_Admin WHERE AID=%s ",[id])
        # for x in myc:
        #     s=x[1]
        pwd=input("Enter the Admin Password: ")
        if pwd==pw2:
            print("Password Matching!")
            print("***   Admin Panel   ***")
            admin_menu()
        else:
            # print(type(result),result,userBytes,type(userBytes))
            print("Incorrect Password. Please check your Password")
            main_menu()

    elif x==2:
        print("***   Welcome!!!   ***")
        print("***   Customer Panel   ***")
        acc=int(input("\nEnter your Account Number: "))
        myc.execute("SELECT * FROM Customers WHERE AccountNumber=%s" ,[acc])
        se=myc.fetchone()
        ps=input("Enter your Password: ")
        if ps==se[5]:
            customer_menu(se[0])
        else:
            print("Incorrect Password!")
        main_menu()


    elif x==3:
        print("Thankyou for using the Banking Services. \n See You Again!!")
        sys.exit()
    else:
        print("Invalid Choice")
        main_menu()

def admin_menu():
    print("1. Create Account")
    print("2. Update Account")
    print("3. Delete Account")
    print("4. Search Account")
    print("5. View all Accounts")
    print("6. Log out")
    ad= int(input("Enter your Choice: "))
    if ad==1:
        
        Acc=int(input("Enter the Customer's Account Number: "))
        name=input("Enter the Customer's Name: ")
        add=input("Enter the Customer's Address: ")
        bal=float(input("Enter the Customer's Account Balance: "))
        pasw=input("Enter the Customer's Password: ")
        myc.execute("INSERT INTO Customers(AccountNumber , CName , Address , Balance , PASSWORD) VALUES (%s,%s,%s,%s,%s)",(Acc,name,add,bal,pasw))
        db.commit()
        print("New Account created successfully")
        admin_menu()
    elif ad==2:
        cid=int(input("Enter the Customer ID of the account to be updated: "))
        myc.execute("SELECT * FROM Customers WHERE CID=%s" ,[cid])
        se=myc.fetchone()
        print (se)
        print("Select the option you want to edit ")
        print("1: Name ")
        print("2: Address ")
        print("3: Password")
        print("4: Account Number")
        opt=int(input("Select option: "))
        if opt==1:
            name=input("Enter the name: ")
            myc.execute("UPDATE Customers SET CName = %s WHERE CID = %s",[name,cid])
            db.commit()
            admin_menu()
        elif opt==2:
            add=input("Enter the Address: ")
            myc.execute("UPDATE Customers SET Address = %s WHERE CID = %s",[add,cid])
            db.commit()
            admin_menu()
        elif opt==3:
            pas=input("Enter the Password: ")
            myc.execute("UPDATE Customers SET PASSWORD = %s WHERE CID = %s",[pas,cid])
            db.commit()
            admin_menu()
        elif opt==4:
            acc=int(input("Enter the Account Number: "))
            myc.execute("UPDATE Customers SET AccountNumber = %s WHERE CID = %s",[acc,cid])
            db.commit()
            admin_menu()
        else:
            print("Invalid Option")
            admin_menu()
        
    elif ad==3:
        id= input("Enter the ID of the account to be deleted: ")
        myc.execute("SELECT * FROM Customers WHERE CID=%s" ,[id])
        se=myc.fetchone()
        print (se)
        print("Deleting Record...")
        myc.execute("DELETE FROM Customers WHERE CID=%s",[id])
        db.commit()
        print("Customer Account is successfully Deleted")
        admin_menu()

    elif ad==4:
        
        search_word=input("Enter the ID/Name of the customer to be searched: ")
        print("Searching....")
        myc.execute("SELECT * FROM Customers WHERE CID=%s OR CName=%s" ,(search_word,search_word))
        se=myc.fetchone()
        if se is None:
                  print("No such Account in this Bank")
        else:
                  print("Account Number is: ",se[1])
                  print("Customer Name is: ",se[2])
                  print("The Current Balance is: ",se[4])
        admin_menu()
                  
    elif ad==5:
        print("\nAll Customer Accounts!\n")
        myc.execute("Select * FROM Customers")
        for x in myc:
            print("Account Number:",x[1],"    Name:",x[2],"    Balance:",x[4])
        admin_menu()

    elif ad==6:
        print("Succesfully logged out.")
        sys.exit()
    else:
        print("Invalid Choice.\n")
        admin_menu()

def customer_menu(id):
    myc.execute("SELECT * FROM Customers WHERE CID=%s" ,[id])
    se=myc.fetchone() 
    print ("\n  Welcome ",se[2])
    print("\n1. Check Balance Amount")
    print("2. Deposit Amount")
    print("3. Withdraw Amount")
    print("4. Fund Transfer")
    print("5. Change Password")
    print("6. Log out")
    ad= int(input("\nEnter your Choice: "))

    if ad==1:
        print("\n Your Current Balance is Rs.",se[4])
        customer_menu(se[0])

    elif ad==2:
        a= int(input("\n Enter the amount to be deposited: "))
        bal=se[4]+a
        print("\n Current Balance after deposit is: ",bal)
        myc.execute("UPDATE Customers SET Balance = %s WHERE CID = %s",[bal,id])
        db.commit()
        customer_menu(se[0])

    elif ad==3:
        a= int(input("\n Enter the amount to withdraw: "))
        if se[4]<=a:
            print("Insufficient amount in your Account")
        else:
            bal=se[4]-a
            print("\n Current Balance after withdrawal is: ",bal)
            myc.execute("UPDATE Customers SET Balance = %s WHERE CID = %s",[bal,id])
            db.commit()
        customer_menu(se[0])
                    
    elif ad==4:
        a= int(input("\n Enter the amount to be transfered: "))
        
        if se[4]<=a:
            print("Insufficient amount in your Account")
        else:
            bal=se[4]-a
            print("\n Current Balance after Fund transfer is: ",bal)
            myc.execute("UPDATE Customers SET Balance = %s WHERE CID = %s",[bal,id])
            db.commit()
            k=int(input("Enter the Account Number to which funds are to be transfered: "))
            myc.execute("SELECT * FROM Customers WHERE AccountNumber =%s" ,[k])
            fund=myc.fetchone() 
            newbal=fund[4]+a
            myc.execute("UPDATE Customers SET Balance = %s WHERE AccountNumber = %s",[newbal,k])
            db.commit()
            print("Amount transfered successfully")
        customer_menu(se[0])

    elif ad==5:
        newpass=input("Enter new Password: ")
        myc.execute("UPDATE Customers SET PASSWORD = %s WHERE CID = %s",[newpass,id])
        db.commit()
        print("Password Changed Successfully!\n")
        customer_menu(se[0])

    elif ad==6:
        print("Succesfully logged out")
        sys.exit()

    else:
        print("Invalid Choice.")
        customer_menu(se[0])
    
menu()


    
