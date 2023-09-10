import sqlite3

# Read the file and copy content to a list
stephen_king_adaptations_list = []
with open("stephen_king_adaptations.txt", "r") as file:
    stephen_king_adaptations_list = file.readlines()

# Establish connection with SQLite database
conn = sqlite3.connect("stephen_king_adaptations.db")
cursor = conn.cursor()

# Create table in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
        movieID INTEGER PRIMARY KEY,
        movieName TEXT NOT NULL,
        movieYear INTEGER,
        imdbRating REAL
    )
''')

# Clear the table before inserting new data
cursor.execute("DELETE FROM stephen_king_adaptations_table")

# Insert data from list into the table
for line in stephen_king_adaptations_list:
    movie_details = line.strip().split(",")
    cursor.execute('''
        INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
        VALUES (?, ?, ?)
    ''', (movie_details[1], movie_details[2], movie_details[3]))


conn.commit()


while True:
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")
    choice = input("Enter your choice: ")

    if choice == "1":

        movie_name = input("Enter the movie name: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
        result = cursor.fetchone()
        if result:
            print("Movie found!")
            print("Movie Name:", result[1])
            print("Movie Year:", result[2])
            print("IMDB Rating:", result[3])
        else:
            print("No such movie exists in our database")

    elif choice == "2":

        movie_year = input("Enter the movie year: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
        result = cursor.fetchall()
        if result:
            print("Movies released in", movie_year)
            for row in result:
                print("Movie Name:", row[1])
                print("Movie Year:", row[2])
                print("IMDB Rating:", row[3])
        else:
            print("No movies were found for that year in our database")

    elif choice == "3":

        movie_rating = input("Enter the minimum movie rating: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (movie_rating,))
        result = cursor.fetchall()
        if result:
            print("Movies with rating at or above", movie_rating)
            for row in result:
                print("Movie Name:", row[1])
                print("Movie Year:", row[2])
                print("IMDB Rating:", row[3])
        else:
            print("No movies at or above that rating were found in the database")

    elif choice == "4":

        break

    print()


conn.close()
