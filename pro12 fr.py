import mysql.connector

def insert_course(cursor, connection):
    while True:
        course_id = int(input("Enter the course id: "))
        stream_name = input("Enter stream name: ")
        available_seats = int(input("Enter available seats: "))

        insert_query = """
        INSERT INTO course (courseid, streamname, availableseat)
        VALUES (%s, %s, %s)
        """

        cursor.execute(insert_query, (course_id, stream_name, available_seats))
        connection.commit()

        print("Course added successfully!")

        con = input("Do you want to insert more courses (y/n): ")
        if con.lower() != 'y':
            break


def view_students(cursor):
    cursor.execute("SELECT * FROM students")
    res = cursor.fetchall()

    print("\nStudent Details:")
    print("Student ID | Student Name | Course ID")

    for x in res:
        print(x)


def view_courses(cursor):
    print("\nSelect the search criteria:")
    print("1. Course ID")
    print("2. Stream Name")
    print("3. All Courses")

    ch = int(input("Enter your choice: "))

    if ch == 1:
        s = int(input("Enter course id: "))
        cursor.execute("SELECT * FROM course WHERE courseid = %s", (s,))
    elif ch == 2:
        s = input("Enter stream name: ")
        cursor.execute("SELECT * FROM course WHERE streamname = %s", (s,))
    elif ch == 3:
        cursor.execute("SELECT * FROM course")
    else:
        print("Invalid choice")
        return

    res = cursor.fetchall()

    print("\nCourse Details:")
    print("Course ID | Stream Name | Available Seats")

    for x in res:
        print(x)


def delete_course(cursor, connection):
    course_id = int(input("Enter the course id to delete: "))

    delete_query = "DELETE FROM course WHERE courseid = %s"

    cursor.execute(delete_query, (course_id,))
    connection.commit()

    print("Course deleted successfully!")


def book_seat(cursor, connection):
    while True:
        student_name = input("Enter student name: ")
        course_id = int(input("Enter course id: "))

        cursor.execute(
            "SELECT availableseat FROM course WHERE courseid = %s",
            (course_id,)
        )

        result = cursor.fetchone()

        if result:
            available_seats = result[0]

            if available_seats > 0:
                new_seat_count = available_seats - 1

                cursor.execute(
                    "UPDATE course SET availableseat = %s WHERE courseid = %s",
                    (new_seat_count, course_id)
                )

                cursor.execute(
                    "INSERT INTO students (studentname, courseid) VALUES (%s, %s)",
                    (student_name, course_id)
                )

                connection.commit()

                print(f"Seat booked successfully.")
                print(f"Remaining seats: {new_seat_count}")

            else:
                print("No seats available.")

        else:
            print("Course ID not found.")

        con = input("Do you want to book another seat? (y/n): ")

        if con.lower() != 'y':
            break


def main():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="omkleemkrishnaya"
    )

    if connection.is_connected():
        print("Connection successful")

    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS course")
    cursor.execute("USE course")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course(
        courseid INT PRIMARY KEY,
        streamname VARCHAR(30),
        availableseat INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        studentid INT PRIMARY KEY AUTO_INCREMENT,
        studentname VARCHAR(50),
        courseid INT,
        FOREIGN KEY(courseid) REFERENCES course(courseid)
    )
    """)

    while True:
        print("\n===== COURSE MANAGEMENT SYSTEM =====")
        print("1. Insert Course")
        print("2. View Courses")
        print("3. Delete Course")
        print("4. Book Seat")
        print("5. View Students")
        print("6. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            insert_course(cursor, connection)

        elif choice == 2:
            view_courses(cursor)

        elif choice == 3:
            delete_course(cursor, connection)

        elif choice == 4:
            book_seat(cursor, connection)

        elif choice == 5:
            view_students(cursor)

        elif choice == 6:
            break

        else:
            print("Invalid choice. Try again.")

    cursor.close()
    connection.close()

    print("MySQL connection closed.")


if __name__ == "__main__":
    main()