class Library:
    def __init__(self):
        self.users = []
        self.books = []
    
    def add_user(self, User):
        self.users.append(User)
    
    def add_book(self, Book):
        self.books.append(Book)

    def remove_single_book(self,isbn):
        book_to_remove = None
        for book in self.books:
            if book.isbn == isbn:
                book_to_remove = book
                break
        if book_to_remove:
            self.books.remove(book_to_remove)
            return (f"Knyga su ISBN {isbn} sėkmingai pašalinta.")
        else:
            return (f"Knygų su duutu ISBN {isbn} nėra.")
        
    def remove_old_books(self, year):
        try:
            year = int(year)
        except:
            return "Įvyko klaida, bandykite dar kartą!"
        before_count = self.get_count()
        self.books = [book for book in self.books if book.year > year]
        after_count = self.get_count()
        return f"Ištrinta {before_count-after_count}, pagal metus {year}"
    
    def __repr__(self) -> str:
        tmp_str = "\nBibliotekos informacija!\n\n"
        tmp_str += "Vartotojai:\n"
        if self.users:
            for user in self.users:
                tmp_str += f"{str(user)}\n" 
        else:
            tmp_str += "  - Nėra įvesta vartotojų!\n"
        tmp_str += "\nKnygos:\n"
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
    
    def search_books(self, title=None, author=None):
        results = []
        results = [book for book in self.books if title.lower() in book.title.lower() or author.lower() in book.author.lower()]
        if results:
            for book in results:
                return f"Rasta knyga: {book.title}, autorius: {book.author}, metai: {book.year}, žanras: {book.genre}, kiekis: {book.quantity}"
        else:
            return "Knyga nerasta."
    
    def get_book_by_isbn(self, isbn):
        if(len(isbn)!=13):
            return False
        books = list(filter(lambda book: isbn.upper() in str(book.isbn).upper(), self.books))
        if len(books)>0:
            return books[0] 
        return False

    def get_user_by_cn(self, card_number):
        if(len(card_number)!=15):
            return False
        users = list(filter(lambda user: card_number in user.card_number, self.users))
        if len(users)>0:
            return users[0] 
        return False

    def view_overdue_books(self):
        overdue_books = []
        for reader in self.users:
            reader.check_overdue_books()
            overdue_books.extend(reader.overdue_books)
        
        if overdue_books:
            print("\nVėluojančių knygų sąrašas:")
            for book in enumerate(overdue_books):
                print(f"{book[0]+1}. {book[1].title} - {book[1].author}")
        else:
            print("Nėra vėluojančių knygų!")
        return overdue_books
    
    def get_overdue_books(self):
        overdue_books = []
        for reader in self.users:
            reader.check_overdue_books()
            id_in = reader.card_number
            # print(reader.overdue_books)
            for book in reader.overdue_books:
                linst_in = book.get_list()
                overdue_books.append([id_in]+linst_in)
        return overdue_books

    def get_borrowed_books(self):
        borrowed_books = []
        for reader in self.users:
            id_in = reader.card_number
            for book in reader.borrowed_books:
                borrowed_books.append([id_in]+[book[1]]+book[0].get_list())
        return borrowed_books
    
    def get_user_list(self):
        user_list=[]
        for users in self.users:
            user_list.append(users.get_user_info())
        return user_list
        