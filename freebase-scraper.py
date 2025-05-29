import requests
import os
from datetime import date
from bs4 import BeautifulSoup
from pathlib import Path

#συναρτηση για να επιλεξει ο χρηστης τι γλωσσα θελει το προογραμμα να τρεξει. (ΔΟΥΛΕΥΕΙ!!!)
def language():
    while True:
            lang = input("Choose language (eng/gr): ").lower()
            if lang == 'gr':
                return lang
            elif lang == 'eng':
                return lang
            else:
                print("Please choose between (eng/gr).")

langchoice = language()

#συναρτηση που ρωταει τον χρηστη ποια σελιδα θελει να τραβηξει. αν ο χρηστης γραψει κατι λαθος, του ξαναζητα τα στοιχεια σε λουπα.
def askuserpage():
    while True:
        try:
            if langchoice == 'gr':
                page_number = int(input("Ποια σελίδα θέλεις να κατεβάσεις (1-50); : "))
                if 1 <= page_number <= 50:
                    return page_number
                else:
                    print("Λαθος αριθμος σελιδας. Δοκιμασε ξανα")
        except ValueError:
            print("Πρεπει να βαλεις αριθμο. Δοκιμασε ξανα.")
        try:
            if langchoice == 'eng':
                page_number = int(input("Which page would you like to scrape (1-50)? : "))
                if 1 <= page_number <= 50: #αν η page_number (to input δηλαδη) ειναι αναμεσα στο 1-50 (δηλαδη ειναι εγκκυρο) τοτε επεστρεψε την τιμη στην συναρτηση page_number
                    return page_number
                else: #αλλιως αν ειναι  εκτοσ του 1-50, δηλαδη σελιιδα που δεν υπαρχει, γραψε οοτι ειναι λαθος ο αριθμος.
                    print("Wrong page number Try again.")
        except ValueError: #αν καποιος αντι για αριθμο (integer) βαλει καποιο αλλο data type, βγαλε error.
            print("You need to insert a number. Try again.")

number = askuserpage() #η μεταβλητη number ειναι το νουμερο που διαλεξε ο χρηστης στη συναρτηση askuserpage
url = f"https://books.toscrape.com/catalogue/page-{number}.html" #το νουμεροο του χρηστη μπαινει στο σημειο του url για να δουλεψει. χρηση f-string για να βαλω μεταβλητεσ μεσα στο string
response = requests.get(url) #κανει αιτημα get στην ιστοσελιδα γιια να παρειι το html
response.encoding = 'utf-8'  # Επιβεβαίωσε σωστό encoding, ωστε να βγαζει χαρακτηρεσ οπως (€, £) χωρις bugs.
soup = BeautifulSoup(response.text, 'html.parser') #παιρνει την απαντηση response και την "καθαριζει" ωστε να μπορουμε να ψαξουμε για διαφορα tags (h2,h3,a) πολυ πιο ευκολα..


# πωσ τυπωνει
def printresults():

    books = soup.find_all('article', class_='product_pod') #ψαχνει στο ητμλ ολα τα article tags me class product_pod (δηλαδη τον καθε τιτλο)v

    for book in books: #λουπα, περναει απο καθε βιβλιο ΕΝΑ ΕΝΑ
        title = book.h3.a['title'] #μπαινει στηη λιστα book και ψαχνει μεσα στο h3 για ενα a , δηλαδη το τιτλο
        price = book.find('p', class_='price_color').text #παλι, ψαχνειι για <p> me class pricecolor, για να παρει την τιμη.
        rating = book.find('p', class_='star-rating')['class'][1] #και τοο ιδιο εδω με τη κλαση starratinng, παιρνει τη λιστα τησ κλασησ πχ ['star-rating', 'Three'], και παιρνει μονο το 2ο στοιχειο τησ λιστασ με το [1], δηλαδη την αξιολογηση με γραμματα ('three')πχ
        if langchoice == 'gr':
            print(f"Τιτλος: {title} | Τιμη: {price} | Αξιολογηση: {rating}")
        if langchoice == 'eng':
            print(f"Title: {title} | Price: {price} | Rating: {rating}")

def saveresults():

    books = soup.find_all('article', class_='product_pod') #ψαχνει στο ητμλ ολα τα article tags me class product_pod (δηλαδη τον καθε τιτλο)

    basepath = Path.home() / "Documents" / "scraperdata" #ο φακελος μεσα στα documents του χρηστη, σε οτιδηποτε λειτουργικο και να ειναι.
    basepath.mkdir(parents=True, exist_ok=True) # αν δεν υπαρχει ο φακκελος αρχειων, δημιουργειται
    filename = f"result_{langchoice}_page{number}_{date.today()}.txt" #δημιουργια νεου αρχειου με ημερομηνια, τον αριθμο τησ σελιδας και τη γλωσσα.
    folderpath = basepath / filename #o φακελοσ που θα δημηουργηθει για τα αρχεια και το ΠΟΥ αποθηκκευονται!

    with open(folderpath, 'w', encoding='utf-8') as f:
        for book in books: #λουπα, περναει απο καθε βιβλιο ΕΝΑ ΕΝΑ
            title = book.h3.a['title'] #μπαινει στηη λιστα book και ψαχνει μεσα στο h3 για ενα a , δηλαδη το τιτλο
            price = book.find('p', class_='price_color').text #παλι, ψαχνειι για <p> me class pricecolor, για να παρει την τιμη.
            rating = book.find('p', class_='star-rating')['class'][1] #και τοο ιδιο εδω με τη κλαση starratinng, παιρνει τη λιστα τησ κλασησ πχ ['star-rating', 'Three'], και παιρνει μονο το 2ο στοιχειο τησ λιστασ με το [1], δηλαδη την αξιολογηση με γραμματα ('three')πχ
            if langchoice == 'gr':
                f.write(f"Τιτλος: {title} | Τιμη: {price} | Αξιολογηση: {rating}\n")
            if langchoice == 'eng':
                f.write(f"Title: {title} | Price: {price} | Rating: {rating}\n")
    if langchoice == 'gr':
        print(f"Το αρχειο αποθηκευτηκε σε: {folderpath}")
    if langchoice == 'eng':
        print(f"File saved at: {folderpath}")

#λουπα για να ρωταει τον χρηστη αν θελει να αποθηκευσει η να προβαλει τα στοιχεια
while True:
    if langchoice == 'gr':
        choice = input("Θες να προβαλεις τα αποτελεσματα ή να τα αποθηκευσεις σε ενα αρχειο; (view/save): ").lower()
        if choice == "save":
            saveresults()
            break
        elif choice == "view":
            printresults()
            break
        else:
            print("Μη εγκυρη καταχωρηση.")

    if langchoice == 'eng':
        choice = input("Do you want to view the results or save them in a file? (view/save): ").lower()
        if choice == "save":
            saveresults()
            break
        elif choice == "view":
            printresults()
            break
        else:
            print("Wrong input.")