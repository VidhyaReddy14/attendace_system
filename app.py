from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Connect to database
def get_db_connection():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create students table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            name TEXT NOT NULL,
            total_classes INTEGER NOT NULL,
            attended_classes INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():

    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students
    )


# Add student
@app.route("/add", methods=["POST"])
def add_student():

    roll_no = request.form["roll_no"]
    name = request.form["name"]

    total_classes = int(
        request.form["total_classes"]
    )

    attended_classes = int(
        request.form["attended_classes"]
    )

    # Validation
    if total_classes <= 0:
        return "Total classes must be greater than 0."

    if attended_classes < 0:
        return "Attended classes cannot be negative."

    if attended_classes > total_classes:
        return "Attended classes cannot be greater than total classes."

    # Save student
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO students
        (roll_no, name, total_classes, attended_classes)
        VALUES (?, ?, ?, ?)
    """, (
        roll_no,
        name,
        total_classes,
        attended_classes
    ))

    conn.commit()
    conn.close()

    return redirect("/")


# Delete student
@app.route("/delete/<int:id>")
def delete_student(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# Edit student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = get_db_connection()

    # When Update button is pressed
    if request.method == "POST":

        roll_no = request.form["roll_no"]
        name = request.form["name"]

        total_classes = int(
            request.form["total_classes"]
        )

        attended_classes = int(
            request.form["attended_classes"]
        )

        # Validation
        if total_classes <= 0:
            conn.close()
            return "Total classes must be greater than 0."

        if attended_classes < 0:
            conn.close()
            return "Attended classes cannot be negative."

        if attended_classes > total_classes:
            conn.close()
            return "Attended classes cannot be greater than total classes."

        # Update student
        conn.execute("""
            UPDATE students
            SET roll_no = ?,
                name = ?,
                total_classes = ?,
                attended_classes = ?
            WHERE id = ?
        """, (
            roll_no,
            name,
            total_classes,
            attended_classes,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    # Get student information
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit.html",
        student=student
    )


# Start application
if __name__ == "__main__":

    create_table()

    app.run(debug=True)