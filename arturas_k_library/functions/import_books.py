from arturas_k_library.modules import book as bk

import random

def import_to_class(lib):
    books = [
        ("Gyvas vabzdžių pasaulis", "Paltanavičius, Selemonas ", "2024","Vilnius: Alma littera", "Kids", "9786090157923", 3),
        ("Migruojantys paukščiai", "Norvaišaitė-Aleliūnienė, Ignė", "2024","Vilnius : Svajonių knygos", "Novel", "9786090309391", 1),
        ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "New York: Charles Scribner's Sons", "Novel", "9780743273565",10),
        ("1984", "George Orwell", 1949, "London: Secker & Warburg", "Dystopian", "9780451524935",10),
        ("To Kill a Mockingbird", "Harper Lee", 1960, "New York: J.B. Lippincott & Co.", "Novel", "9780061120084",10),
        ("Pride and Prejudice", "Jane Austen", 1813, "London: T. Egerton", "Romance", "9780141439518",10),
        ("The Catcher in the Rye", "J.D. Salinger", 1951, "Boston: Little, Brown and Company", "Novel", "9780316769488",10),
        ("Moby Dick", "Herman Melville", 1851, "Harper & Brothers", "Adventure", "9781503280786",10),
        ("War and Peace", "Leo Tolstoy", 1869, "The Russian Messenger", "Historical Fiction", "9780199232765",10),
        ("The Odyssey", "Homer", "8th century BC", "Ancient Greece: Various", "Epic Poetry", "9780140268867",10),
        ("Jane Eyre", "Charlotte Brontë", 1847, "London: Smith, Elder & Co.", "Gothic Fiction", "9780142437209",10),
        ("The Hobbit", "J.R.R. Tolkien", 1937, "London: George Allen & Unwin", "Fantasy", "9780007487293",10),
        ("Fahrenheit 451", "Ray Bradbury", 1953, "Simon & Schuster", "Dystopian", "9781451673319",10),
        ("Brave New World", "Aldous Huxley", 1932, "Chatto & Windus", "Dystopian", "9780060850524",10),
        ("The Grapes of Wrath", "John Steinbeck", 1939, "The Viking Press", "Historical Fiction", "9780143039433",10),
        ("The Picture of Dorian Gray", "Oscar Wilde", 1890, "Lippincott's Monthly Magazine", "Philosophical Fiction", "9780141439570",10),
        ("Wuthering Heights", "Emily Brontë", 1847, "Thomas Newby", "Gothic Fiction", "9780141439556",10),
        ("The Adventures of Huckleberry Finn", "Mark Twain", 1884, "Charles L. Webster And Company", "Adventure", "9780142437179",10),
        ("The Chronicles of Narnia", "C.S. Lewis", 1950, "Geoffrey Bles", "Fantasy", "9780066238500",10),
        ("The Old Man and the Sea", "Ernest Hemingway", 1952, "Charles Scribner's Sons", "Novel", "9780684832507",10),
        ("One Hundred Years of Solitude", "Gabriel García Márquez", 1967, "Harper & Row", "Magical Realism", "9780060883286",10),
        ("The Bell Jar", "Sylvia Plath", 1963, "Heinemann", "Autobiographical Novel", "9780060834024",10),
        ("Tumo knygos", "Andrius Tapinas", 2013, "Alma littera", "Adventure", "9786094412130",10),
        ("Broliai", "Romualdas Granauskas", 1991, "Vaga", "Novel", "9789986116061",10),
        ("Laumė", "Vytautas V. Landsbergis", 1994, "Vaga", "Fairy Tale", "9789986118904",10),
        ("Aukso pieva", "Maironis", 1935, "Vaga", "Poetry", "9789986112306",10),
        ("Baltaragis", "B. Brazdžionis", 1947, "Alauda", "Novel", "9789986082002",10),
        ("Knyga apie save", "Raimondas Černiauskas", 2018, "Tyto alba", "Autobiography", "9786098225569",10),
        ("Gimtinė", "Kazys Binkis", 1934, "Naujoji Romuva", "Novel", "9789986119992",10),
        ("Rūpintojėlis", "Tomas Venclova", 1994, "Baltos lankos", "Poetry", "9789986116617",10),
        ("Kanklių skambėjimas", "Sigutis Jaunius", 2008, "Lietuvos rašytojų sąjunga", "Novel", "9786098122380",10),
        ("Bėgantis žmogus", "Dainius Gintalas", 2012, "Alma littera", "Adventure", "9786090114279",10),
        ("Tarp pilkų debesų", "T. Ivanauskas", 2015, "Knygų sodas", "Drama", "9786090105659",10),
        ("Saulė ir jūra", "Gintaras Grajauskas", 2007, "Tyto alba", "Poetry", "9789986118529",10),
        ("Daugiau nei draugai", "Kęstutis Ziemelis", 2003, "Tyto alba", "Romance", "9789986162195",10),
        ("Vėjų gūsiuose", "Silvija Lukošiūtė", 2019, "Alma littera", "Adventure", "9786090303520",10),
        ("Karaimui 100", "Ona Baublytė", 2005, "Kraštotyros muziejus", "Historical Fiction", "9789986184827",10),
        ("Gera moteris", "Julija Vysniauskaitė", 1991, "Alma littera", "Novel", "9789986171919",10),
        ("Nebaigtas romanas", "A. Šlepikas", 2014, "Tyto alba", "Novel", "9786094470825",10),
        ("Pasakos knyga", "M. Vaitiekūnas", 2000, "Alma littera", "Children's", "9786090347852",10),
        ("Pikčiurna", "Eglė Rakauskaitė", 2011, "Alma littera", "Poetry", "9786090241367",10),
        ("Rudenio lapai", "V. Mačernis", 1997, "Vaga", "Poetry", "9789986112306",10),
        
        # Baigiame su likusiomis lietuviškomis knygomis
        ("Žvilgsnis į save", "Raimondas Jankauskas", 2004, "Knygų sodas", "Autobiography", "9786090801029",10),
        ("Mėnesienos pasaka", "Vaiva R. Murauskienė", 2020, "Alma littera", "Children's", "9786090514291",10),
        ("Amžinasis Sūnus", "K. Dineika", 2016, "Aukso pieva", "Historical Fiction", "9786090420043",10),
        ("Sielos balzamas", "K. B. Lauras", 2015, "Tyto alba", "Drama", "9786090349827",10),
        ("Pasaulio pradžia", "Evelina Daciūtė", 2021, "Alma littera", "Children's", "9786090499653",10),
        ("Knyga apie mus", "Vaiva M. Šlekytė", 2013, "Alma littera", "Romance", "9786090501234",10),
        ("Paslaptis", "M. G. Raulinaitis", 2005, "Vaga", "Adventure", "9789986156262",10),
        ("Pradžia", "L. Gaidys", 2020, "Tyto alba", "Drama", "9786090415053",10),
        ("Tamsa", "R. Kasparavičius", 2008, "Alma littera", "Novel", "9786090303286",10),
        ("Žvaigždžių vakaras", "A. Šeškevičius", 2019, "Aukso pieva", "Fantasy", "9786090407836",10)
    ]
    random.shuffle(books)
    
    for book in books:
       lib.add_book(bk.Book(book[0], book[1], book[2], book[3], book[4], book[5], random.randint(1,book[6])))