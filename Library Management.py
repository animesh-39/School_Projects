# Library Management System


import mysql.connector
from tabulate import tabulate

# Establishing the Database connection

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    charset='utf8mb4',
    collation='utf8mb4_general_ci',
    port=3306)

mycursor = mydb.cursor()
print("""
_________________________________________________________

           Welcome To Library Management System

_________________________________________________________
""")

# Creating Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS library")
mycursor.execute("USE library")

# Creating Tables
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS available_books(
        id INT PRIMARY KEY,
        name VARCHAR(256) NOT NULL,
        subject VARCHAR(256),
        quantity INT NOT NULL
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS issued(
        id INT,
        name VARCHAR(256),
        subject VARCHAR(256),
        s_name VARCHAR(256),
        s_class VARCHAR(256)
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS login(
        user VARCHAR(25),
        password VARCHAR(25)
    )
""")

mydb.commit()

flag = 0
mycursor.execute("SELECT * FROM login")
for i in mycursor:
    flag = 1
if flag == 0:
    mycursor.execute("INSERT INTO login VALUES('user','1234')")
    mydb.commit()


while True:
    print("""
 1.Login
 2.Exit    
    
    """)
    ch = int(input(" Enter your choice :"))
    if ch == 1:
        pas = input(" Enter password :")
        mycursor.execute("SELECT * FROM login")
        for i in mycursor:  # var1,var2=(x,y)
            t_user, t_pas = i
        if pas == t_pas:
            print("""Login Successfully...""")
            loop1 = 'n'
            while loop1 == 'n':
                print("""
_________________________________
    
    1. Add New Books
    2. Remove any Book
    3. Issue Book to Student
    4. Return Book
    5. View Available Books
    6. View Issued Books 
    7. Logout 
    
_________________________________
""")

                ch = int(input(" Enter your choice :"))

                # Adding New Books
                if ch == 1:
                    loop2 = 'y'
                    while loop2 == 'y':
                        print("All Information are mandatory to be filled !! ")
                        idd = int(input("Enter book id : "))
                        name = input("Enter book name : ")
                        subject = input("Enter subject : ")
                        quan = int(input("Enter quantity : "))

                        mycursor.execute("INSERT INTO available_books VALUES (%s, %s, %s, %s)",
                                         (idd, name, subject, quan))
                        mydb.commit()

                        print("Data Insterted Successfully...")
                        loop2 = input("Do you want to add another book ?(y/n) : ").lower()
                    loop1 = input("Do you want to logout ? (y/n) : ").lower()

                    if loop1 == 'y':
                        print("Logging out....")
                        break

                # Removing a Book
                elif ch == 2:
                    try:
                        idd = int(input("Enter ID to remove book: "))

                        mycursor.execute("SELECT * FROM available_books WHERE id = %s", (idd,))
                        book = mycursor.fetchone()

                        if book:
                            mycursor.execute("DELETE FROM available_books WHERE id = %s", (idd,))
                            mydb.commit()
                            print("Book deleted successfully!")
                        else:
                            print("No book exists with the given ID. Please check the ID and try again.")
                            loop2 = input("Do you want to remove another book? (y/n): ").lower()

                    except Exception as e:
                        print("An error occurred:", e)  # for debugging

                # Issuing a Book to student
                elif ch == 3:
                    loop2 = 'y'
                    while loop2 == 'y':

                        try:
                            idd = int(input("Enter Book ID : "))
                            s_name = input("Enter Student Name : ")
                            s_class = input("Enter Student Class : ")
                            mycursor.execute("SELECT * FROM available_books WHERE id = %s", (idd,))
                            book = mycursor.fetchone()

                            if book:
                                t_id, t_name, t_subject, t_quan = book

                                if t_quan >= 1:
                                    quan = t_quan - 1
                                    mycursor.execute("INSERT INTO issued VALUES (%s, %s, %s, %s, %s)",
                                                     (idd, t_name, t_subject, s_name, s_class))

                                    mycursor.execute("UPDATE available_books SET quantity = %s WHERE id = %s",
                                                     (quan, idd))
                                    mydb.commit()
                                    print("Book successfully issued.")

                                else:
                                    print("Book not available.")

                            else:
                                print("No book exists with the given ID. Please check the ID and try again.")

                        except ValueError:
                            print("Invalid input. Please enter a valid Book ID.")

                        loop2 = input("Do you want to issue more books? (y/n): ").lower()

                    loop1 = input("Do you want to log out? (y/n): ").lower()

                # Returning a Book

                elif ch == 4:
                    loop2 = 'y'
                    while loop2 == 'y':
                        idd = int(input("Enter Book ID : "))
                        s_name = input("Enter Student Name : ")
                        s_class = input("Enter Student Class : ")

                        mycursor.execute("SELECT * FROM issued WHERE id = %s AND s_name = %s AND s_class = %s",
                                         (idd, s_name, s_class))
                        issued_book = mycursor.fetchone()

                        if issued_book:
                            mycursor.execute("SELECT * FROM available_books WHERE id = %s", (idd,))
                            available_book = mycursor.fetchone()

                            if available_book:  # If the book exists in the available_books table
                                t_id, t_name, t_subject, t_quan = available_book
                                quan = t_quan + 1

                                mycursor.execute("DELETE FROM issued WHERE id = %s AND s_name = %s AND s_class = %s",
                                                 (idd, s_name, s_class))
                                mycursor.execute("UPDATE available_books SET quantity = %s WHERE id = %s", (quan, idd))
                                mydb.commit()

                                print("Successfully returned...")

                            else:
                                print("Book not found in available books table.")

                            loop2 = input("Do you want to return more books? (y/n): ").lower()

                        else:
                            print("This book is not issued to the given student or incorrect details provided.")

                    loop1 = input("Do you want to logout? (y/n): ").lower()

                # Viewing Available Books

                elif ch == 5:
                    mycursor.execute("SELECT * FROM available_books")
                    books = mycursor.fetchall()

                    if books:
                        headers = ["ID", "NAME", "SUBJECT", "QUANTITY"]
                        print(tabulate(books, headers=headers, tablefmt="grid"))

                    else:
                        print("No books available.")

                # Viewing Issued Books
                elif ch == 6:
                    mycursor.execute("SELECT * FROM issued")
                    issued_books = mycursor.fetchall()  # Fetch all rows
                    if issued_books:
                        headers = ["ID", "NAME", "SUBJECT", "S_NAME", "S_CLASS"]
                        print(tabulate(issued_books, headers=headers, tablefmt="grid"))
                    else:
                        print("No books have been issued.")


                # Logging Out
                elif ch == 7:
                    break

        else:
            print(" Wrong Password...")

    elif ch == 2:

        break

''' 
#_______________________________________________________#
                                                        |
End of program...                                       |
                                                        |
Operating System :   Android Oreo 8.1.0                 |
RAM              :    2 GB                              |
ROM              :    16GB                              |
Processor        :  Qualcomm Snapdragon 450 Octa Core   |
IDE              :   Termux & Pydroid                   |
Database Server  :   Maria DB                           |
                                                        |
Thank you for reviewing this code...                    | 
________________________________________________________#
'''