import mysql.connector as mycon

print("BANK MANAGEMENT")

# Establishing connection to the database
try:
    mydb = mycon.connect(
        host="localhost",
        user="root",
        passwd="tiger"
    )
    cur = mydb.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS Bank")
    cur.execute("USE Bank")

    # Creating required tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Account (
            acno CHAR(5) PRIMARY KEY,
            Name VARCHAR(30),
            dob VARCHAR(12),
            city CHAR(20),
            mobileno CHAR(10),
            Balance INT(7)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Banktrans (
            acno CHAR(5),
            amount INT(7),
            dot DATE,
            ttype CHAR(1),
            FOREIGN KEY (acno) REFERENCES Account(acno)
        )
    """)
    mydb.commit()

    while True:
        print("\n1. Create account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Display account details")
        print("5. Display all transactions")
        print("6. Display all Accounts info")
        print("7. Exit")
        
        ch = int(input("Enter your choice: "))
        
        if ch == 1:
            print("All the information prompted are mandatory to be filled")
            acno = input("Enter account number: ")
            Name = input("Enter your name: ") 
            dob = input("Enter your D.O.B.: ")
            city = input("Enter city name: ") 
            mn = input("Enter mobile no.: ")
            Balance = 0
            cur.execute(
                "INSERT INTO Account (acno, Name, dob, city, mobileno, Balance) VALUES (%s, %s, %s, %s, %s, %s)",
                (acno, Name, dob, city, mn, Balance)
            )
            mydb.commit()
            print("Account is successfully created!!\n")

        elif ch == 2:
            acno = input("Enter account number: ")
            dp = int(input("Enter amount to be deposited: "))
            dot = input("Enter date of Transaction (YYYY-MM-DD): ")
            ttype = "d"
            cur.execute(
                "INSERT INTO Banktrans (acno, amount, dot, ttype) VALUES (%s, %s, %s, %s)",
                (acno, dp, dot, ttype)
            )
            cur.execute(
                "UPDATE Account SET Balance = Balance + %s WHERE acno = %s",
                (dp, acno)
            )
            mydb.commit()
            print("Money has been deposited successfully!!\n")

        elif ch == 3:
            acno = input("Enter account number: ")
            wd = int(input("Enter amount to be withdrawn: "))
            dot = input("Enter date of transaction (YYYY-MM-DD): ")
            ttype = "w"
            cur.execute(
                "INSERT INTO Banktrans (acno, amount, dot, ttype) VALUES (%s, %s, %s, %s)",
                (acno, wd, dot, ttype)
            )
            cur.execute(
                "UPDATE Account SET Balance = Balance - %s WHERE acno = %s",
                (wd, acno)
            )
            mydb.commit()
            print("Money has been withdrawn successfully!!\n")

        elif ch == 4:
            acno = input("Enter account number: ")
            cur.execute("SELECT * FROM Account WHERE acno = %s", (acno,))
            for i in cur:
                print(i)
            print()

        elif ch == 5:
            cur.execute("SELECT * FROM Banktrans")
            for x in cur:
                print(x)
            print()

        elif ch == 6:
            cur.execute("SELECT * FROM Account")
            for x in cur:
                print(x)
            print()

        elif ch == 7:
            print("Have A Good Day, Sir :):)")
            break
        
        else:
            print("Invalid choice, please try again.")

except mycon.Error as err:
    print(f"Error: {err}")
finally:
    if 'mydb' in locals() and mydb.is_connected():
        mydb.close()
        print("MySQL connection is closed")
