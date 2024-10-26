import json
import os
import uuid
import pygame
class Seat:
    def __init__(self, position):
        self.position = position
        self.is_booked = False

class SeatEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Seat):
            return {
                'position': obj.position,
                'is_booked': obj.is_booked
            }
        return super().default(obj)

class Movie:
    def __init__(self, movie_id, title, genre, language, duration, ticket_price, hall, seat_matrix):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.language = language
        self.duration = duration
        self.ticket_price = ticket_price
        self.hall = hall
        self.seat_matrix = seat_matrix
        self.bookings = []

class Theater:
    def __init__(self):
        self.movies = []

    def add_movie(self, movie):
        self.movies.append(movie)

    def display_movies(self):
        print("Available Movies:")
        if self.movies == None:
            print("No movies Available")
        for movie in self.movies:
            print("---------------------------------")
            print("              ",movie.title,"              ")
            print("---------------------------------")
            print("Movie ID       : ",movie.movie_id)
            print("Movie Name     : ",movie.title)
            print("Movie Genre    : ",movie.genre)
            print("Movie Language : ",movie.language)
            print("Movie Duration : ",movie.duration)
            print("Ticket Price   : ",movie.ticket_price)
            print("Movie Hall     : ",movie.hall)
            print("---------------------------------")
            Customer.display_seat_matrix(self,movie)
            print("---------------------------------")
            print("---------------------------------")
            print()
            print()

    def get_movie(self, movie_id):
        for movie in self.movies:
            if movie.movie_id == movie_id:
                return movie
        return None

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_movie(self, theater):
        movie_id = str(uuid.uuid4())[:8]  # Generate a unique movie ID
        title = input("Enter movie title: ")
        genre = input("Enter movie genre: ")
        language = input("Enter movie language: ")
        duration = input("Enter movie duration: ")
        ticket_price = float(input("Enter ticket price: "))
        hall = input("Enter hall number: ")
        seat_matrix = self.create_seat_matrix()
        
        movie = Movie(movie_id, title, genre, language, duration, ticket_price, hall, seat_matrix)
        theater.add_movie(movie)
        print(f"Movie '{title}' added successfully.")

    def create_seat_matrix(self):
        rows = int(input("Enter the number of rows: "))
        cols = int(input("Enter the number of seats per row: "))
        return [[Seat(f"{chr(65 + r)}{c + 1}") for c in range(cols)] for r in range(rows)]

class Customer:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance
        self.bookings = []

    def add_cash(self, amount):
        self.balance += amount
        print(f"Balance added successfully. \nCurrent balance: ${self.balance:.2f}")

    def display_seat_matrix(self, movie):
        print(f"Seat Matrix for {movie.title}:")
        for row in movie.seat_matrix:
            for seat in row:
                if seat.is_booked:
                    print("XX", end=" ")
                else:
                    print(seat.position, end=" ")
            print()
            
    def book_tickets(self, movie, num_tickets):
        total_cost = num_tickets * movie.ticket_price
        print("Your Current balance : ",self.balance)
        print("Amount Required to book tickets : ",total_cost)
        self.display_seat_matrix(movie)
        selected_seats = input("Enter the positions of the seats (comma-separated): ").split(',')
        
        if self.balance >= total_cost:
            booking_id = str(uuid.uuid4())[:8]  # Generate a unique booking ID
            print(f"Selected Movie: {movie.title}")
            print(f"Available Balance: ${self.balance:.2f}")
            
            for seat_position in selected_seats:
                for row in movie.seat_matrix:
                    for seat in row:
                        if seat.position == seat_position and not seat.is_booked:
                            seat.is_booked = True

            self.balance -= total_cost
            booking = {'booking_id': booking_id, 'movie_title': movie.title, 'num_tickets': num_tickets, 'selected_seats': selected_seats}
            movie.bookings.append(booking)
            self.bookings.append(booking)
            print(f"Tickets booked successfully for '{movie.title}'.")
            print(f"Booking ID: {booking_id}")
            print(f"Remaining balance: ${self.balance:.2f}")
            self.display_seat_matrix(movie) 
        else:
            print("Insufficient funds. Please add cash.")

    def cancel_ticket(self, booking_id, theater):
        for movie in theater.movies:
            for booking in movie.bookings:
                if booking['booking_id'] == booking_id:
                    for seat_position in booking['selected_seats']:
                        for row in movie.seat_matrix:
                            for seat in row:
                                if seat.position == seat_position:
                                    seat.is_booked = False

                    print(f"Ticket with Booking ID {booking_id} canceled for '{movie.title}'.")
                    self.balance += booking['num_tickets'] * movie.ticket_price
                    print(f"Refund processed. Current balance: ${self.balance:.2f}")
                    movie.bookings.remove(booking)
                    self.bookings.remove(booking)
                    return

        print("Invalid Booking ID.")

def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, cls=SeatEncoder)  # Use the custom encoder

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return {}

def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    user = Customer(username, password)
    users.append(user)
    save_data(USERS_FILE, [vars(u) for u in users])
    print("Registration successful.")
    pygame.time.delay(1000)
    os.system('cls')

def register_admin():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    admin = Admin(username, password)
    admins.append(admin)
    save_data(ADMINS_FILE, [vars(a) for a in admins])
    print("Admin registration successful.")
    pygame.time.delay(1000)
    os.system('cls')

# Main program
THEATER_FILE = "theater.json"
ADMINS_FILE = "admins.json"
USERS_FILE = "users.json"

# Load existing theater, admins, and users data
theater_data = load_data(THEATER_FILE)
admin_data = load_data(ADMINS_FILE)
user_data = load_data(USERS_FILE)

# Create or load theater
theater = Theater()
if theater_data:
    for movie_data in theater_data:
        seat_matrix = [[Seat(seat_info['position']) for seat_info in row] for row in movie_data['seat_matrix']]
        movie = Movie(movie_data['movie_id'], movie_data['title'], movie_data['genre'], movie_data['language'], movie_data['duration'], movie_data['ticket_price'], movie_data['hall'], seat_matrix)
        movie.bookings = movie_data['bookings']
        theater.add_movie(movie)

# Create or load admins
admins = []
if admin_data:
    for admin_info in admin_data:
        admin = Admin(admin_info['username'], admin_info['password'])
        admins.append(admin)

# Create or load users
users = []
if user_data:
    for user_info in user_data:
        user = Customer(user_info['username'], user_info['password'], user_info['balance'])
        user.bookings = user_info['bookings']
        users.append(user)

while True:
    print("\n---------------------------")
    print("Movie Ticket Booking System")
    print("---------------------------")
    print("1. Admin - Login")
    print("2. Admin - Register")
    print("3. Customer - Login")
    print("4. Customer - Register")
    print("5. Exit")
    print("---------------------------")
    choice = input("Enter your choice : ")

    if choice == '1':
        pygame.time.delay(1000)
        os.system('cls')
        admin_username = input("Enter admin username: ")
        admin_password = input("Enter admin password: ")
        admin = next((a for a in admins if a.username == admin_username and a.password == admin_password), None)
        if admin:
            print("Login Successful !!")
            while True:
                pygame.time.delay(1000)
                os.system('cls')
                print("Welcome ",admin_username," , to movie ticket booking sytem .")
                print("\n--------------")
                print("Admin Menu")
                print("--------------")
                print("1. Add Movie")
                print("2. View Movies")
                print("3. Logout")
                print("--------------")
                admin_choice = input("Enter your choice : ")

                if admin_choice == '1':
                    pygame.time.delay(1000)
                    os.system('cls')
                    admin.add_movie(theater)
                    save_data(THEATER_FILE, [vars(m) for m in theater.movies])
                elif admin_choice == '2':
                    pygame.time.delay(1000)
                    os.system('cls')
                    theater.display_movies()
                    print("Click any key to go back")
                    a = input()
                elif admin_choice == '3':
                    pygame.time.delay(1000)
                    os.system('cls')
                    print("Logging out.")
                    pygame.time.delay(1000)
                    os.system('cls')
                    break
                else:
                    pygame.time.delay(1000)
                    os.system('cls')
                    print("Invalid choice. Please enter 1, 2, or 3.")

    elif choice == '2':
        pygame.time.delay(1000)
        os.system('cls')
        register_admin()

    elif choice == '3':
        pygame.time.delay(1000)
        os.system('cls')
        customer_username = input("Enter your username: ")
        customer_password = input("Enter your password: ")
        user = next((u for u in users if u.username == customer_username and u.password == customer_password), None)
        if user:
            print("Logged in sucessfully!!")
            while True:
                pygame.time.delay(1000)
                os.system('cls')
                print("Welcome ",customer_username," , to movie ticket booking sytem .")
                print("\n----------------")
                print("Customer Menu")
                print("----------------")
                print("1. Add Cash")
                print("2. Book Tickets")
                print("3. View Bookings")
                print("4. Cancel Ticket")
                print("5. Check Balance")
                print("6. Logout")
                print("----------------")
                customer_choice = input("Enter your choice : ")

                if customer_choice == '1':
                    pygame.time.delay(1000)
                    os.system('cls')
                    print("Available Balance : $",user.balance)
                    amount = float(input("Enter the amount to add: "))
                    user.add_cash(amount)
                    save_data(USERS_FILE, [vars(u) for u in users])
                elif customer_choice == '2':
                    pygame.time.delay(1000)
                    os.system('cls')
                    theater.display_movies()
                    movie_id = input("Enter the movie ID you want to watch: ")
                    movie = theater.get_movie(movie_id)
                    if movie:
                        num_tickets = int(input("How many tickets do you want to book? "))
                        user.book_tickets(movie, num_tickets)
                        save_data(USERS_FILE, [vars(u) for u in users])
                    else:
                        print("Invalid Movie ID.")
                elif customer_choice == '3':
                    pygame.time.delay(1000)
                    os.system('cls')
                    print("Your Bookings:")
                    for index, booking in enumerate(user.bookings, start=1):
                        print(f"{index}. Movie: {booking['movie_title']}, Tickets: {booking['num_tickets']}, Seats: {', '.join(booking['selected_seats'])}, Booking ID: {booking['booking_id']}")
                        print("Click any key to go back")
                        a = input()
                elif customer_choice == '4':
                    pygame.time.delay(1000)
                    os.system('cls')
                    booking_id = input("Enter the Booking ID to cancel: ")
                    user.cancel_ticket(booking_id, theater)
                    save_data(USERS_FILE, [vars(u) for u in users])
                elif customer_choice == '5':
                    pygame.time.delay(1000)
                    os.system('cls')
                    print("Available Balance : $",user.balance)
                    print("Click any key to go back")
                    a = input()
                elif customer_choice == '6':
                    pygame.time.delay(1000)
                    os.system('cls')
                    print()
                    print("Logging out.")
                    pygame.time.delay(1000)
                    os.system('cls')
                    break
                else:
                    pygame.time.delay(1000)
                    os.system('cls')
                    print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

    elif choice == '4':
        pygame.time.delay(1000)
        os.system('cls')
        register_user()

    elif choice == '5':
        pygame.time.delay(1000)
        os.system('cls')
        print("Exiting. Thank you for using the Movie Ticket Booking System!")
        pygame.time.delay(1000)
        os.system('cls')
        break

    else:
        pygame.time.delay(1000)
        os.system('cls')
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")




