class Book:
    def __init__(self, title: str, 
                 author: str, 
                 year: int, 
                 details: str, 
                 genre: str, 
                 isbn:str,
                 quantity:int):
        
        self.title = title
        self.author = author
        self.year = year
        self.details = details
        self.isbn =  isbn
        self.genre = genre
        self.quantity = quantity
    
    def __repr__(self):
        return f"ISBN: {self.isbn}, {self.title}, {self.author}, {self.year}, {self.genre}, {self.details}, {self.quantity}"

    def __str__(self):
        return f"ISBN: {self.isbn}, {self.title}, {self.author}, {self.year}"
   
    def get_book_info(self):
        return (str(self.isbn), str(self.title), str(self.author), str(self.year), str(self.details), str(self.genre))
    