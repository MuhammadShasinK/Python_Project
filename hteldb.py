import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        U_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR UNIQUE,
        Password VARCHAR,
        Role VARCHAR
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rooms(
        R_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Room_No INTEGER UNIQUE,
        Room_Type VARCHAR,
        Price REAL,
        Status VARCHAR
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings(
        B_id INTEGER PRIMARY KEY AUTOINCREMENT,
        U_id INTEGER,
        R_id INTEGER,
        Days INTEGER,
        Total_Amount REAL,
        Status VARCHAR,
        FOREIGN KEY(U_id) REFERENCES Users(U_id),
        FOREIGN KEY(R_id) REFERENCES Rooms(R_id)
    )
''')

cursor.execute('''
    SELECT * FROM Users WHERE Username=?
''', ("admin",))

admin = cursor.fetchone()

if not admin:
    cursor.execute('''
        INSERT INTO Users(Username, Password, Role)
        VALUES(?,?,?)
    ''', ("admin", "admin123", "admin"))

conn.commit()
conn.close()


def register():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == "" or password == "":
        print("Username and password cannot be empty")
        conn.close()
        return

    try:
        cursor.execute('''
            INSERT INTO Users(Username, Password, Role)
            VALUES(?,?,?)
        ''', (username, password, "customer"))

        conn.commit()
        print("Registration successful")

    except sqlite3.IntegrityError:
        print("Username already exists")

    conn.close()


def login():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute('''
        SELECT * FROM Users
        WHERE Username=? AND Password=?
    ''', (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        print("Login successful")
        return user
    else:
        print("Invalid username or password")
        return None


def addroom():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    try:
        room_no = int(input("Enter room number: "))
        room_type = input("Enter room type: ")
        price = float(input("Enter price per day: "))

        cursor.execute('''
            INSERT INTO Rooms(Room_No, Room_Type, Price, Status)
            VALUES(?,?,?,?)
        ''', (room_no, room_type, price, "Available"))

        conn.commit()
        print("Room added successfully")

    except ValueError:
        print("Invalid input")

    except sqlite3.IntegrityError:
        print("Room number already exists")

    conn.close()


def viewroom():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM Rooms
    ''')

    rooms = cursor.fetchall()

    if rooms:
        print("Rooms Found")

        for i in rooms:
            print(i)

    else:
        print("No rooms found")

    conn.close()


def findroom():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    try:
        room_id = int(input("Enter room id: "))

        cursor.execute('''
            SELECT * FROM Rooms
            WHERE R_id=?
        ''', (room_id,))

        room = cursor.fetchone()

        if room:
            print("Room found")
            print("Room Number:", room[1])
            print("Room Type:", room[2])
            print("Price:", room[3])
            print("Status:", room[4])

        else:
            print("No such room")

    except ValueError:
        print("Invalid room id")

    conn.close()


def updateroom():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    try:
        room_id = int(input("Enter room id: "))

        cursor.execute('''
            SELECT * FROM Rooms
            WHERE R_id=?
        ''', (room_id,))

        room = cursor.fetchone()

        if room:
            room_no = int(input("Enter room number: "))
            room_type = input("Enter room type: ")
            price = float(input("Enter price per day: "))

            cursor.execute('''
                UPDATE Rooms
                SET Room_No=?, Room_Type=?, Price=?
                WHERE R_id=?
            ''', (room_no, room_type, price, room_id))

            conn.commit()
            print("Room Updated")

        else:
            print("Room not found")

    except ValueError:
        print("Invalid input")

    except sqlite3.IntegrityError:
        print("Room number already exists")

    conn.close()


def deleteroom():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    try:
        room_id = int(input("Enter room id: "))

        cursor.execute('''
            SELECT * FROM Rooms
            WHERE R_id=?
        ''', (room_id,))

        room = cursor.fetchone()

        if room:
            ch = input("Are you sure you want to delete the room(y/n): ").lower()

            if ch == "y":
                cursor.execute('''
                    DELETE FROM Rooms
                    WHERE R_id=?
                ''', (room_id,))

                conn.commit()
                print("Room Deleted")

            else:
                print("Room Not Deleted")

        else:
            print("Room not found")

    except ValueError:
        print("Invalid room id")

    except sqlite3.IntegrityError:
        print("Room cannot be deleted")

    conn.close()


def bookroom(user_id):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    try:
        room_id = int(input("Enter room id: "))
        days = int(input("Enter number of days: "))

        cursor.execute('''
            SELECT * FROM Rooms
            WHERE R_id=?
        ''', (room_id,))

        room = cursor.fetchone()

        if room:

            if room[4] == "Available":

                total = room[3] * days

                cursor.execute('''
                    INSERT INTO Bookings(
                        U_id, R_id, Days, Total_Amount, Status
                    )
                    VALUES(?,?,?,?,?)
                ''', (user_id, room_id, days, total, "Active"))

                cursor.execute('''
                    UPDATE Rooms
                    SET Status=?
                    WHERE R_id=?
                ''', ("Booked", room_id))

                conn.commit()

                print("Room booked successfully")
                print("Total amount:", total)

            else:
                print("Room is already booked")

        else:
            print("Room not found")

    except ValueError:
        print("Invalid input")

    conn.close()


def viewbooking(user_id):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Bookings.B_id,
               Rooms.Room_No,
               Rooms.Room_Type,
               Bookings.Days,
               Bookings.Total_Amount,
               Bookings.Status
        FROM Bookings
        JOIN Rooms
        ON Bookings.R_id=Rooms.R_id
        WHERE Bookings.U_id=?
    ''', (user_id,))

    bookings = cursor.fetchall()

    if bookings:
        print("Booking Records Found")

        for i in bookings:
            print(i)

    else:
        print("No booking records found")

    conn.close()


def cancelbooking(user_id):
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    try:
        booking_id = int(input("Enter booking id: "))

        cursor.execute('''
            SELECT * FROM Bookings
            WHERE B_id=? AND U_id=?
        ''', (booking_id, user_id))

        booking = cursor.fetchone()

        if booking:

            if booking[5] == "Active":

                cursor.execute('''
                    UPDATE Bookings
                    SET Status=?
                    WHERE B_id=?
                ''', ("Cancelled", booking_id))

                cursor.execute('''
                    UPDATE Rooms
                    SET Status=?
                    WHERE R_id=?
                ''', ("Available", booking[2]))

                conn.commit()

                print("Booking cancelled successfully")

            else:
                print("Booking already cancelled")

        else:
            print("Booking not found")

    except ValueError:
        print("Invalid booking id")

    conn.close()


def viewallbooking():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Bookings.B_id,
               Users.Username,
               Rooms.Room_No,
               Rooms.Room_Type,
               Bookings.Days,
               Bookings.Total_Amount,
               Bookings.Status
        FROM Bookings
        JOIN Users
        ON Bookings.U_id=Users.U_id
        JOIN Rooms
        ON Bookings.R_id=Rooms.R_id
    ''')

    bookings = cursor.fetchall()

    if bookings:
        print("Booking Records Found")

        for i in bookings:
            print(i)

    else:
        print("No booking records found")

    conn.close()


def adminmenu():
    while True:
        print("\n----- ADMIN MENU -----")
        print("1. Add Room")
        print("2. View Rooms")
        print("3. Find Room")
        print("4. Update Room")
        print("5. Delete Room")
        print("6. View Bookings")
        print("7. Logout")

        ch = input("Choose an option: ")

        if ch == "1":
            addroom()

        elif ch == "2":
            viewroom()

        elif ch == "3":
            findroom()

        elif ch == "4":
            updateroom()

        elif ch == "5":
            deleteroom()

        elif ch == "6":
            viewallbooking()

        elif ch == "7":
            break

        else:
            print("Invalid Option")


def customermenu(user_id):
    while True:
        print("\n----- CUSTOMER MENU -----")
        print("1. View Rooms")
        print("2. Find Room")
        print("3. Book Room")
        print("4. View My Bookings")
        print("5. Cancel Booking")
        print("6. Logout")

        ch = input("Choose an option: ")

        if ch == "1":
            viewroom()

        elif ch == "2":
            findroom()

        elif ch == "3":
            bookroom(user_id)

        elif ch == "4":
            viewbooking(user_id)

        elif ch == "5":
            cancelbooking(user_id)

        elif ch == "6":
            break

        else:
            print("Invalid Option")


def main():
    print("Welcome to Hotel Booking System")

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        ch = input("Choose an option: ")

        if ch == "1":
            register()

        elif ch == "2":
            user = login()

            if user:

                if user[3] == "admin":
                    adminmenu()

                elif user[3] == "customer":
                    customermenu(user[0])

        elif ch == "3":
            print("Thank you for using Hotel Booking System")
            break

        else:
            print("Invalid Option")


main()