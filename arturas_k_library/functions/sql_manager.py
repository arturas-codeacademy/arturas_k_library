import arturas_k_library.config as config
import arturas_k_library.functions.helper as helper
import arturas_k_library.modules.user as usr
import arturas_k_library.modules.book as bk

import pyodbc
import os
import sqlite3
import datetime as dt

def odbc():
    # conn = pyodbc.connect(
    #     "DRIVER={SQL Server};"
    #     "SERVER=DESKTOP-MSGFDHE\SQLEXPRESS;"
    #     "DATABASE=library;"
    # )

    # cursor = conn.cursor()

    # cursor.execute("SELECT * FROM Hello")
    # for row in cursor.fetchall():
    #     print(row)

    # conn.close()

    # def init():
    #     conn = pyodbc.connect(
    #         "DRIVER={SQL Server};"
    #         "SERVER=DESKTOP-MSGFDHE\SQLEXPRESS;"
    #         "DATABASE=library;"
    #     )
    return

def create_tables():
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Books" (
            "isbn"	TEXT,
            "title"	TEXT NOT NULL,
            "author"	TEXT NOT NULL,
            "year"	INTEGER NOT NULL,
            "details"	TEXT,
            "genre"	TEXT,
            "quantity" INTEGER NOT NULL,
            PRIMARY KEY("isbn")
    );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Users" (
            "card_number"	TEXT,
            "first_name"	TEXT NOT NULL,
            "last_name"	TEXT NOT NULL,
            "password"	TEXT NOT NULL,
            PRIMARY KEY("card_number")
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Borrowed" (
            "card_number"	TEXT NOT NULL,
            "isbn"	TEXT NOT NULL,
            "borrowed"	DATE,
            FOREIGN KEY("card_number") REFERENCES "Users"("card_number"),
            FOREIGN KEY("isbn") REFERENCES "Books"("isbn")
        );
    ''')
    connection.commit()
    connection.close()

def delete_tables():
    connection = sqlite3.connect(config.db_name)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Library;")
    cursor.execute("DROP TABLE IF EXISTS Borrowed;")
    cursor.execute("DROP TABLE IF EXISTS Overdue;")
    cursor.execute("DROP TABLE IF EXISTS Users;")
    cursor.execute("DROP TABLE IF EXISTS Books;")
    connection.commit()
    connection.close()
    
def init():
    if check():
        read_from_library()
    else:
        create_tables()
        print("Įveskite iBibliotekos administratorių:")
        name    = input(" Vardas: ")
        last    = input(" Pavardė: ")
        pasword = input(" Slaptažodis: ")
        config.lib.add_user(usr.User("admin", name, last, pasword))
        print("Ar importuoti testinią biblioteką?")
        imp_lib = input(" (taip/ne) -> ")
        if (imp_lib=="taip"):
            helper.import_to_class()
        write_to_library()

def write_to_library():
    for book in config.lib.books:
        add_book_to_db(book)
    for user in config.lib.users:
        add_user_to_db(user)
        if (len(user.borrowed_books)>0):
            add_user_borrowed_to_db(user)

def add_book_to_db(book):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO Books (isbn, title, author, year, details, genre, quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(insert_query, (book.isbn, 
                                      book.title, 
                                      book.author, 
                                      book.year, 
                                      book.details, 
                                      book.genre, 
                                      book.quantity
                                      ))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
        
def add_user_to_db(user):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO Users (card_number, first_name, last_name, password)
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(insert_query, (user.card_number, 
                                      user.first_name, 
                                      user.last_name, 
                                      user.user_pasword
                                      ))
        conn.commit()
        
def add_user_borrowed_to_db(user) :
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        for book in user.borrowed_books:
            insert_query = '''
            INSERT INTO Borrowed (card_number, isbn, borrowed)
            VALUES (?, ?, ?)
            '''
            cursor.execute(insert_query, (user.card_number, 
                                        book[0].isbn, 
                                        dt.datetime.strftime(book[1],"%Y-%m-%d")
                                        ))
        conn.commit() 
    update_book_quantity(book[0].isbn,book[0].quantity)

def read_from_library():
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
        
        if len(books):
            cursor.execute("SELECT * FROM Users")
            for key,row_book in enumerate(books):
                config.lib.add_book(bk.Book(row_book[1], 
                                            row_book[2], 
                                            row_book[3], 
                                            row_book[4], 
                                            row_book[5], 
                                            row_book[0], 
                                            row_book[6]))
        users = cursor.fetchall()
        if len(users):
            for key,row_user in enumerate(users):
                user = usr.User("", row_user[1], row_user[2], row_user[3], row_user[0])
                config.lib.add_user(user)
                cursor.execute(f"SELECT * FROM Borrowed WHERE card_number=?", (row_user[0],))
                books = cursor.fetchall()
                for key, row_book in enumerate(books):
                    book = config.lib.get_book_by_isbn(row_book[1])
                    user.borrowed_books.append((book,dt.datetime.strptime(row_book[2],"%Y-%m-%d")))

def delete_book_from_db(isbn):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Borrowed WHERE isbn=?",(isbn,))
        result = cursor.fetchall()
        if len(result) > 0:
            return False
        else:
            cursor.execute("DELETE FROM Books WHERE isbn = ?", (isbn,))
            if cursor.rowcount > 0:
                return True
            else:
                return False
        
def delete_books_from_db(year):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE year < ?", (year,))
        return cursor.rowcount

def delete_user_borrowed_from_db(isbn, card_number):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Borrowed WHERE isbn=? and card_number=?", (isbn,card_number))
        return cursor.rowcount

def update_book_quantity(isbn,quantity):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Books SET quantity = ? WHERE isbn = ?",(quantity, isbn))
        return cursor.rowcount
           
def add_user_info_to_db(card_number, first_name, last_name, password):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO Users (card_number, first_name, last_name, password)
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(insert_query, (card_number, 
                                      first_name, 
                                      last_name, 
                                      password
                                      ))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
        
def add_book_to_user(card_number, isbn, borrowed):
    with sqlite3.connect(config.db_name) as conn:
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO Borrowed (card_number, isbn, borrowed)
        VALUES (?, ?, ?)
        '''
        cursor.execute(insert_query, (card_number, 
                                      isbn, 
                                     borrowed 
                                      ))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
        
def delete_reset():
    delete_tables()
    create_tables()

def check():
    with sqlite3.connect(config.db_name) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT * FROM Users')
        except:
            return False
        else:
            if(len(cursor.fetchall())==0):
                return False
            else:
                return True
    
if(__name__=="__main__"):
    delete_tables()
    