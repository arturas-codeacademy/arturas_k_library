import time
import random
import string

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
    
    def __repr__(self):
       return f"ID: {self.card_number}, {self.first_name}, {self.get_library_role()}" 