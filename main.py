import streamlit as st
import pandas as pd
import random
from typing import List

# Set page configuration
st.set_page_config(page_title="SABEEM UNIVERSITY Management System", layout="wide")

# ---------- Supporting Classes ----------
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

class Student(Person):
    def __init__(self, name: str, age: int, department: str, subjects: List[str], instructors: List[str] = None):
        super().__init__(name, age)
        self.roll_number = self.generate_roll_number()
        self.department = department
        self.courses = subjects
        self.instructors = instructors if instructors else []
        self.fees_paid = False
        self.attendance = 0.0

    def generate_roll_number(self):
        return f"S-{random.randint(1000, 9999)}"

class Instructor(Person):
    def __init__(self, name: str, age: int, subject: str, salary: float):
        super().__init__(name, age)
        self.subject = subject
        self.salary = salary
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

class Course:
    def __init__(self, name: str, code: str, instructor: Instructor = None):
        self.name = name
        self.code = code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        self.students.append(student)

class Department:
    def __init__(self, name: str):
        self.name = name
        self.students = []
        self.instructors = []
        self.courses = []

    def add_student(self, student):
        self.students.append(student)

    def add_instructor(self, instructor):
        self.instructors.append(instructor)

    def add_course(self, course):
        self.courses.append(course)

# ---------- Initialize Session State ----------
for key in ["students", "instructors", "courses", "departments"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ---------- Sidebar Navigation ----------
st.sidebar.image("ums.png", width=150)
section = st.sidebar.selectbox("\U0001F4C2 Navigate", [
    "Home", "Department", "Students", "Instructors", "Courses", "Classes", "Search"
])

# ---------- Home Page ----------
if section == "Home":
    st.markdown("""
        <style>
        .typewriter {
            display: inline-block;
            overflow: hidden;
            border-right: 2px solid rgba(0,0,0,0.75);
            white-space: nowrap;
            animation: typing 3.5s steps(40, end), blink-caret 0.5s step-end infinite;
            font-size: 36px;
            font-weight: bold;
            color: black;
            font-family: 'Segoe UI', sans-serif;
        }
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: rgba(0,0,0,0.5); }
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("ums.png", width=200)

    st.markdown("<h1 class='typewriter'>\U0001F393 WELCOME TO SABEEM UNIVERSITY</h1>", unsafe_allow_html=True)

# ---------- Department Section ----------
elif section == "Department":
    st.header("\U0001F3EB University Departments")
    new_dept = st.text_input("Add a new department")
    if st.button("\u2795 Add Department"):
        if new_dept and new_dept not in [d.name for d in st.session_state.departments]:
            st.session_state.departments.append(Department(new_dept))
            st.success(f"Department '{new_dept}' added successfully!")
        elif not new_dept:
            st.error("Department name cannot be empty.")
        else:
            st.warning("This department already exists.")

    if st.session_state.departments:
        st.markdown("### \U0001F4CB List of Departments")
        col1, col2 = st.columns(2)
        for i, d in enumerate(st.session_state.departments):
            (col1 if i % 2 == 0 else col2).success(f"\u2705 {d.name}")

# ---------- Instructor Section ----------
elif section == "Instructors":
    st.header("\U0001F468‍\U0001F3EB Add Instructor")
    dept_names = [d.name for d in st.session_state.departments]

    with st.form("add_instructor"):
        name = st.text_input("Instructor Name")
        subject = st.text_input("Subject")
        salary = st.number_input("Salary", min_value=0.0)
        department = st.selectbox("Department", dept_names)
        submitted = st.form_submit_button("Add Instructor")

        if submitted and name and subject and department:
            instructor = Instructor(name, 30, subject, salary)
            for dept in st.session_state.departments:
                if dept.name == department:
                    dept.add_instructor(instructor)
            st.session_state.instructors.append(instructor)
            st.success(f"Instructor {name} added to {department}.")

    st.subheader("\U0001F4CB All Instructors")
    for d in st.session_state.departments:
        if d.instructors:
            st.markdown(f"### \U0001F4DA {d.name}")
            for i in d.instructors:
                st.markdown(f"- {i.name} (Subject: {i.subject}, Salary: {i.salary})")

# ---------- Courses Section ----------
elif section == "Courses":
    st.header("\U0001F4DA Add Course")
    dept_names = [d.name for d in st.session_state.departments]
    with st.form("add_course"):
        name = st.text_input("Course Title")
        code = st.text_input("Course Code")
        department = st.selectbox("Department", dept_names)
        submitted = st.form_submit_button("Add Course")
        if submitted and name and code:
            course = Course(name, code)
            for dept in st.session_state.departments:
                if dept.name == department:
                    dept.add_course(course)
            st.session_state.courses.append(course)
            st.success(f"Course {name} added to {department}.")

    st.subheader("\U0001F4CB All Courses")
    for d in st.session_state.departments:
        if d.courses:
            st.markdown(f"### \U0001F3EB {d.name}")
            for c in d.courses:
                st.markdown(f"- {c.name} ({c.code})")

# ---------- Students Section ----------
elif section == "Students":
    if st.session_state.departments:
        dept_names = [d.name for d in st.session_state.departments]
        with st.form("Add Student"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=16, max_value=100)
            department = st.selectbox("Department", dept_names)
            fees_paid = st.checkbox("Fees Paid")
            attendance = st.slider("Attendance (%)", 0.0, 100.0, 75.0)

            selected_dept = next(d for d in st.session_state.departments if d.name == department)
            subjects = st.multiselect("Subjects", [c.name for c in selected_dept.courses])
            submitted = st.form_submit_button("Add Student")

            if submitted and name and age:
                student = Student(name, age, department, subjects)
                student.fees_paid = fees_paid
                student.attendance = attendance
                selected_dept.add_student(student)
                st.session_state.students.append(student)
                st.success(f"Student {student.get_name()} (Roll: {student.roll_number}) added to {department} successfully!")

    else:
        st.warning("No departments available. Please add a department first.")

# ---------- Search Section (Unified for Student & Instructor) ----------
elif section == "Search":
    st.header("🔍 Search Profiles")

    # Safety check: initialize session lists if not present
    if "students" not in st.session_state:
        st.session_state.students = []
    if "instructors" not in st.session_state:
        st.session_state.instructors = []

    # Debugging aid
    st.write("🛠️ Debug - Student Names:", [s.get_name() for s in st.session_state.students])
    st.write("🛠️ Debug - Instructor Names:", [i.get_name() for i in st.session_state.instructors])

    search_option = st.selectbox("Search for", ["Student", "Instructor"])
    query = st.text_input("Enter name, roll number, or subject").strip()

    if search_option == "Student" and query:
        found = False
        for s in st.session_state.students:
            if query.lower() in s.get_name().lower() or query.lower() == s.roll_number.lower():
                found = True
                st.subheader(f"🎓 Profile of {s.get_name()} ({s.roll_number})")
                st.write(f"**Name:** {s.get_name()}")
                st.write(f"**Age:** {s.age}")
                st.write(f"**Department:** {s.department}")
                st.write(f"**Fees Paid:** {'Yes' if s.fees_paid else 'No'}")
                st.write(f"**Attendance:** {s.attendance}%")
                st.write("**Courses:**")
                for course in s.courses:
                    st.write(f" - {course}")
        if not found:
            st.error("Student not found.")

    elif search_option == "Instructor" and query:
        found = False
        for i in st.session_state.instructors:
            if query.lower() in i.get_name().lower() or query.lower() in i.subject.lower():
                found = True
                st.subheader(f"👨‍🏫 Profile of {i.get_name()}")
                st.write(f"**Name:** {i.get_name()}")
                st.write(f"**Age:** {i.age}")
                st.write(f"**Subject:** {i.subject}")
                st.write(f"**Salary:** {i.salary}")
                st.write("**Courses:**")
                for course in i.courses:
                    st.write(f" - {course.name} (Code: {course.code})")
        if not found:
            st.error("Instructor not found.")

# CLASS SECTION

# Initialize session_state for classes
if "classes" not in st.session_state:
    st.session_state.classes = []

elif section == "Classes":
        st.title("📘 Manage Classes")

        tab1, tab2, tab3 = st.tabs(["➕ Add Class", "📋 View Classes", "🔍 Search Class"])

        # TAB 1: Add Class
        with tab1:
            st.subheader("Add a New Class")
            class_name = st.text_input("Class Name")
            department = st.text_input("Department")
            instructor = st.text_input("Instructor")
            time_slot = st.text_input("Time Slot")

            if st.button("Add Class"):
                class_data = {
                    "name": class_name,
                    "department": department,
                    "instructor": instructor,
                    "time": time_slot
                }
                st.session_state.classes.append(class_data)
                st.success("✅ Class added successfully!")

        # TAB 2: View All Classes
        with tab2:
            st.subheader("All Classes")
            if st.session_state.classes:
                st.table(st.session_state.classes)
            else:
                st.info("No classes available yet.")

        # TAB 3: Search Class
        with tab3:
            st.subheader("Search Class by Name")
            search_query = st.text_input("Enter class name to search")
            if search_query:
                results = [cls for cls in st.session_state.classes if search_query.lower() in cls["name"].lower()]
                if results:
                    st.table(results)
                else:
                    st.warning("No matching class found.")
