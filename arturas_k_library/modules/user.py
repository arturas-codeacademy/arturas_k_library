import time
import random
import string

from datetime import datetime, timedelta

class User:
    def __init__(self, 
                 role: str, 
                 first_name: str, 
                 last_name: str, 
                 user_pasword: str = None) -> None:
        
        self.card_number = self.generate_numeric_user_id(role)
        if (user_pasword==None):
            self.user_pasword = self.generate_password()
        else:
            self.user_pasword = user_pasword
        self.first_name = first_name
        self.last_name = last_name
        
        self.borrowed_books = []
        self.overdue_books = []
        
        print(self.get_new_user())
    
    def generate_numeric_user_id(self, role: str = "reader" ):
        timestamp = str(int(time.time() * 1000))
        if (role=="reader"):
            return f"18{timestamp}"
        elif(role=="admin"):
            return f"01{timestamp}"
        else:
            return f"00{timestamp}"
    
    def generate_password(self,length=8):
        characters = string.ascii_letters + string.digits 
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def get_library_role(self):
        #User ID: 181728543955507
        #       role|timestamp 
        # 18 - reader, 01 - admin, 00 - guest
        role = self.card_number[0:2]
        if (role=="18"):
            return "reader"
        elif(role=="01"):
            return "admin"
        else:
            return "guest"
        
    def get_new_user(self):
        result =  f"Naujas vartotojas sistemoje:\n"
        result += f" ID: {self.card_number}\n"
        result += f" Vardas: {self.first_name}\n"
        result += f" Pavardė: {self.last_name}\n"
        result += f" Slaptažodis: {self.user_pasword}\n"
        result += f" Rolė: {self.get_library_role()}\n"
        return result
    
    def __str__(self):
        result =  f"  - Skaitytojo informacija sistemoje:\n"
        result += f"     ID: {self.card_number}\n"
        result += f"     Vardas: {self.first_name}\n"
        result += f"     Pavardė: {self.last_name}\n"
        
        if (len(self.overdue_books)>0):
            result += "!"*80+"\n"
            result += "     - DĖMESIO, turi vėluojančių knygų:\n"
            for book in enumerate(self.overdue_books):
                result += f"      {book[0]+1}. {book[1]}\n"
            result += "!"*80+"\n"
        
        if (len(self.borrowed_books)>0):
            result += "     - Paimtos knygos:\n"
            for book in enumerate(self.borrowed_books):
                result += f"      {book[0]+1}. {book[1][0]}\n"

        return result
   
    def __repr__(self):
        return f"ID: {self.card_number}, {self.first_name}, {self.get_library_role()}" 
    
    def borrow_book(self, book, borrow_days):
        if self.has_overdue_books():
            return f"\n{self.first_name}, turi vėluojančią knygą, todėl negali pasiimti naujų knygų."
            
        if book.quantity > 0:
            book.quantity -= 1
            due_date = datetime.now() + timedelta(days=borrow_days)
            self.borrowed_books.append((book, due_date))
            return f"{self.first_name} paėmė knygą: {book.title}. Grąžinimo data: {due_date}"
        else:
            return f"Knyga {book.title} neturi laisvų egzempliorių."
            
    def check_overdue_books(self, simulate_date=None):
        if (simulate_date!=None):
            try:
                check_date = datetime.strptime(simulate_date, "%Y-%m-%d")
            except:
                datetime.now()
        else:
            check_date = datetime.now()
        self.overdue_books = [
            book for book, due_date in self.borrowed_books
            if check_date > due_date
        ]
        if self.overdue_books:
            result  = f"Skaitovas: {self.first_name} {self.first_name}\n"
            result += f"Sąrašas vėluojančių knygų:\n"
            result += ', '.join([f"{book.title} - {book.author}" for book in self.overdue_books])
            return result
        else:
            return f"Skaitytojas {self.first_name} {self.last_name} neturi vėluojančių knygų."
        
    
    def has_overdue_books(self):
        self.check_overdue_books()
        return len(self.overdue_books) > 0