from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

students = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Management System V3</title>
</head>
<body>
    <h1>Student Management System - V3</h1>

    <h2>Add Student</h2>
    <form action="/add" method="post">
        <input name="name" placeholder="Student Name" required>
        <input name="course" placeholder="Course" required>
        <button type="submit">Add Student</button>
    </form>

    <h2>Search Students</h2>
    <form action="/" method="get">
        <input name="search" placeholder="Search by name or ID"
               value="{{ search }}">
        <button type="submit">Search</button>
        <a href="/">Show All</a>
    </form>

    <h2>Student List</h2>

    {% for student in students %}
        <div>
            <p>
                ID: {{ student.id }} |
                Name: {{ student.name }} |
                Course: {{ student.course }}
            </p>

            <form action="/edit/{{ student.id }}" method="post">
                <input name="name" value="{{ student.name }}" required>
                <input name="course" value="{{ student.course }}" required>
                <button type="submit">Update</button>
            </form>

            <form action="/delete/{{ student.id }}" method="post">
                <button type="submit">Delete</button>
            </form>
        </div>
        <hr>
    {% else %}
        <p>No students found.</p>
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def home():
    search = request.args.get("search", "").strip().lower()

    if search:
        filtered_students = [
            student for student in students
            if search in student["name"].lower()
            or search == str(student["id"])
        ]
    else:
        filtered_students = students

    return render_template_string(
        HTML,
        students=filtered_students,
        search=request.args.get("search", "")
    )


@app.route("/add", methods=["POST"])
def add_student():
    global next_id

    name = request.form["name"].strip()
    course = request.form["course"].strip()

    students.append({
        "id": next_id,
        "name": name,
        "course": course
    })

    next_id += 1
    return redirect("/")


@app.route("/edit/<int:student_id>", methods=["POST"])
def edit_student(student_id):
    for student in students:
        if student["id"] == student_id:
            student["name"] = request.form["name"].strip()
            student["course"] = request.form["course"].strip()
            break

    return redirect("/")


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    global students

    students = [
        student for student in students
        if student["id"] != student_id
    ]

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)