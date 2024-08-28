                 
                       #Library Management System


import mysql.connector #Importing Mysqlconnector library

#Establishing the Database connection
mydb= mysql.connector.connect(
host='localhost',
user='u0_a256',
password='12345',
charset='utf8mb4',
collation='utf8mb4_general_ci',
port=3306)

mycursor= mydb.cursor()
print( """
_________________________________________________________

           Welcome To Library Management System

_________________________________________________________
""" )

# Creating Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS library")
mycursor.execute("USE library")

# Creating Tables
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS available_books(
        id INT,
        name VARCHAR(25),
        subject VARCHAR(25),
        quantity INT
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS issued(
        id INT,
        name VARCHAR(25),
        subject VARCHAR(25),
        s_name VARCHAR(25),
        s_class VARCHAR(25)
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS login(
        user VARCHAR(25),
        password VARCHAR(25)
    )
""")

# Commit changes
mydb.commit()

flag= 0
mycursor.execute("SELECT * FROM login")
for i in mycursor : #()
    flag= 1
if flag== 0 :
    mycursor.execute("INSERT INTO login VALUES('user','1234')")
    mydb.commit()

#############Loops///Main working#############

while True :
    print("""
 1.Login
 2.Exit    
    
    """)    
    ch= int(input(" Enter your choice :"))   
    if ch== 1 :
        pas=input(" Enter password :")
        mycursor.execute("SELECT * FROM login")        
        for i in mycursor : #var1,var2=(x,y)
            t_user,t_pas= i                          
        if pas== t_pas :
            print("""
 Login Successfully...
            """)
            loop1 = 'n'
            while loop1== 'n' :
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
                
                ch= int(input(" Enter your choice :"))
                

#Adding New Books
                if ch== 1 :
                    loop2= 'y'
                    while loop2== 'y' :
                        print(" All Information are mandatory to be filled !! ")
                        idd= int(input("""
 Enter book id : """))
                        name= input(" Enter book name : ")
                        subject= input(" Enter subject : ")
                        quan= int(input(" Enter quantity : "))
                        
                        mycursor.execute("INSERT INTO available_books VALUES (%s, %s, %s, %s)", (idd, name, subject, quan))
                        mydb.commit()
                        
                        print(" Data Insterted Successfully...")
                        loop2= input(""" 
 Do you want to add another book ?(y/n) : """).lower()                    
                    loop1= input(" Do you want to logout ? (y/n) : ").lower()
                        
                
 #Removing a Book              
                elif ch== 2 :
                    idd= int(input(" Enter Id to remove book : "))
                    mycursor.execute("SELECT * FROM available_books")
                    flag= 0
                    for i in mycursor :
                        t_id,t_name,t_subject,t_quan= i
                        if t_id== idd :
                            flag= 1
                    if flag== 1 :
                        mycursor.execute("DELETE FROM available_books WHERE id = %s", (idd,))
                        mydb.commit()
                        print(" Data Successfully Deleted...")
                    
                    else :
                        print (" Wrong Input... ")
                 
                
#Issuing a Book to student                
                elif ch== 3 :
                    loop2= 'y'
                    while loop2== 'y' :
                            idd=int(input(" Enter Book ID : "))
                            s_name=input(" Enter Student Name : ")
                            s_class=input(" Enter Student Class : ")
                            mycursor.execute("SELECT  * FROM available_books WHERE id= %s", (idd,))
                            
                            flag= 0
                            for i in mycursor :
                                t_id,t_name,t_subject,t_quan= i 
                                flag= 1
                                
                            if flag== 1 :
                               if t_quan>= 1 :
                                  quan= t_quan - 1
                                  mycursor.execute("INSERT INTO issued VALUES (%s,%s,%s,%s,%s)",(idd,t_name,t_subject,s_name,s_class))
                                  mycursor.execute("UPDATE available_books SET quantity = %s WHERE id = %s", (quan, idd))
                                  mydb.commit()
                                  print(" Successfully issued...")
                                  loop2= input(" Do you want to issue more books ?(y/n) : ").lower()
                              
                               else :
                                  print(" Book not available...")
                              
                            else :
                                print(" Invalid Input...")
                                                  
                    loop1= input(" Do you want to log out ?(y/n) : ").lower()
                        
                    
#Returning a Book                 
                elif ch == 4 :
                    loop2 = 'y'
                    while loop2 == 'y' :
                        idd = int(input(" Enter Book ID : "))
                        s_name = input(" Enter Student Name : ")
                        s_class = input(" Enter Student Class : ")
                        
                        mycursor.execute("SELECT * FROM issued")
                        flag = 0
                        for i in mycursor:
                            t_id, t_name, t_subject, t_s_name, t_s_class = i
                            flag= 1
                        if flag== 1 :
                            mycursor.execute("SELECT * FROM available_books WHERE id = %s", (idd,))
                            for i in mycursor:
                                t_id, t_name, t_subject, t_quan = i
                            quan = t_quan + 1
                            mycursor.execute("DELETE FROM issued WHERE id = %s AND s_name = %s AND s_class = %s", (idd, s_name, s_class))
                            mycursor.execute("UPDATE available_books SET quantity = %s WHERE id = %s", (quan, idd))
                            mydb.commit()
                            print(" Successfully returned...")
                            loop2 = input(" Do you want to return more books? (y/n) : ").lower()
                
                        else:
                            print(" Not issued yet...")
                
                    loop1 = input(" Do you want to logout? (y/n) : ").lower()
                                
                         
#Viewing Available Books                       
                elif ch== 5 :
                    mycursor.execute("SELECT * FROM available_books")
                    print(" ID | NAME | SUBJECT | QUANTITY ")
                    for i in mycursor :
                        a,b,c,d= i
                        print(f" {a} | {b} | {c} | {d} ")
                        
                   
#Viewing Issued Books                
                elif ch== 6 :
                    mycursor.execute("SELECT * FROM issued")
                    print(" ID | SUBJECT | S_NAME | S_CLASS")
                    for i in mycursor :
                        a2,b2,c2,d2,e2= i
                        print(f" {a2} | {b2} | {c2} | {d2} | {e2}")
                    
                    
#Logging Out                  
                elif ch== 7 :
                    break                                         
   
        else :
            print(" Wrong Password...")        
    
    elif ch== 2 :
         break
         
 
#________________________________________________________

    # End of program...
    
    
    # Developed on Android version 8.1.0
    # Ram and Rom : 2 GB and 16GB
    # Processor : Qualcomm Snapdragon 450 Octa Core
    # IDE : Termux And Pydroid Applications
    # Database Server : Maria DB
     
     
    # Thank you for reviewing this code...
     

#________________________________________________________    
       
         
     
        
            
                    
    
  