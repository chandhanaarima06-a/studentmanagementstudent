
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

students = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Management System - V2</title>
    <style>
        body {
            font-family: Arial;
            max-width: 800px;
            margin: 40px auto;
            background: #f4f6f9;
        }
        h1 { color: #243b55; }
        form, .student {
            background: white;
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 8px;
        }
        input, button {
            padding: 9px;
            margin: 5px;
        }
        button { cursor: pointer; }
    </style>
</head>
<body>
    <h1>Student Management System - V2</h1>

    <h2>Add Student</h2>
    <form method="POST" action="/add">
        <input name="name" placeholder="Student name" required>
        <input name="department" placeholder="Department" required>
        <button type="submit">Add Student</button>
    </form>

    <h2>Student List</h2>

    {% for student in students %}
        <div class="student">
            <strong>ID:</strong> {{ student.id }}<br>

            <form method="POST" action="/edit/{{ student.id }}">
                <input name="name" value="{{ student.name }}" required>
                <input name="department"
                       value="{{ student.department }}" required>
                <button type="submit">Save Changes</button>
            </form>

            <form method="POST" action="/delete/{{ student.id }}">
                <button type="submit">Delete Student</button>
            </form>
        </div>
    {% else %}
        <p>No students added yet.</p>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, students=students)

@app.route("/add", methods=["POST"])
def add_student():
    global next_id

    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if name and department:
        students.append({
            "id": next_id,
            "name": name,
            "department": department
        })
        next_id += 1

    return redirect("/")

@app.route("/edit/<int:student_id>", methods=["POST"])
def edit_student(student_id):
    for student in students:
        if student["id"] == student_id:
            name = request.form["name"].strip()
            department = request.form["department"].strip()

            if name and department:
                student["name"] = name
                student["department"] = department

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
    app.run(host="0.0.0.0", port=5001, debug=True)