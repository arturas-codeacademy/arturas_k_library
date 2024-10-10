class Library:
    def __init__(self):
        self.users = []
        self.books = []
    
    def add_user(self, User):
        self.users.append(User)
    
    def add_book(self, Book):
        self.books.append(Book)

    def remove_book(self, isbn):
        pass
    
    def __repr__(self) -> str:
        tmp_str = "\nBibliotekos informacija!\n\n"
        
        tmp_str += "Vartotojai:\n"
        if self.users:
            for user in self.users:
                tmp_str += f"  - {str(user)}\n" 
        else:
            tmp_str += "  - Nėra įvesta vartotojų!\n"
        
        tmp_str += "Knygos:\n"
        if self.books:
            for book in self.books:
                tmp_str += f"  - {str(book)}\n"
        else:
            tmp_str += "  - Nėra įvesta knygų!\n"
            
        return tmp_str
    
    def get_books_list(self):
        book_list=[]
        for i in self.books:
            book_list.append(i.get_book_info())
        return list(book_list)
    
    def get_count(self):
        return len(self.books)