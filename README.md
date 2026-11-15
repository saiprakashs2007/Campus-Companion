# 🎓 Campus Companion
### An Integrated Student Academic and Productivity Management System

Campus Companion is a desktop-based student productivity application developed using **Python and Tkinter**. It provides a centralized platform for students to organize their academic activities, manage daily tasks, monitor attendance, calculate academic performance, and maintain their student profiles.

The application features a modern dark-themed graphical user interface designed to make academic management simple, organized, and accessible.

---

## ✨ Features

### 1. Dashboard
- Displays an overview of academic activities.
- Shows total subjects.
- Displays average attendance percentage.
- Tracks pending tasks.
- Displays current semester SGPA.
- Shows the timetable for the current day.

### 2. Timetable Management
- Add, update and delete classes.
- Organize classes by day and time.
- Store subject names, timings and classroom details.

### 3. Task Manager
- Add academic tasks and assignments.
- Set deadlines and priorities.
- Update and delete tasks.
- Mark tasks as completed.
- Filter tasks by All, Pending and Completed status.

### 4. Attendance Tracker
- Add and manage subjects.
- Record total classes and attended classes.
- Automatically calculate attendance percentages.
- Identify subjects below the 75% attendance threshold.
- Calculate additional consecutive classes required to reach 75%.

### 5. CGPA Calculator
- Add subjects with credits and grade points.
- Calculate Semester Grade Point Average (SGPA).
- Calculate cumulative CGPA using previous semester SGPA and credits.
- Update and delete subject records.

### 6. Student Profile
- Store student information.
- Maintain name, roll number, department, program, academic year, section and email address.
- Update profile details through the graphical interface.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Tkinter | Graphical User Interface |
| ttk | GUI widgets and tables |
| Python OOP | Modular application design |
| Lists and Dictionaries | Runtime data management |

---

## 📁 Project Structure

```text
CampusCompanion/
├── main.py
├── app.py
├── README.md
├── ui/
│   ├── __init__.py
│   ├── theme.py
│   └── components.py
├── pages/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── timetable.py
│   ├── tasks.py
│   ├── attendance.py
│   ├── cgpa.py
│   ├── profile.py
│   └── placeholder.py
├── logic/
│   ├── __init__.py
│   ├── timetable_logic.py
│   ├── task_logic.py
│   ├── attendance_logic.py
│   └── cgpa_logic.py
└── assets/
```

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10 or later
- Visual Studio Code or another Python-supported IDE
- Tkinter support

### Step 1: Clone the Repository

```bash
git clone https://github.com/saiprakashs2007/Campus-Companion.git
```

### Step 2: Navigate to the Project Folder

```bash
cd Campus-Companion
```

### Step 3: Run the Application

```bash
python main.py
```

The Campus Companion desktop application will launch.

---

## 🧠 Application Architecture

The project follows a modular architecture that separates the graphical interface from application logic.

- **main.py:** Application entry point.
- **app.py:** Handles the main window, sidebar navigation and integration of modules.
- **ui/:** Contains reusable interface components and theme configurations.
- **pages/:** Contains the graphical interfaces for individual modules.
- **logic/:** Contains the core operations and calculations for each module.

Shared manager objects allow data to remain accessible across different pages while the application is running.

---

## 📊 Key Calculations

### Attendance Percentage

\[
Attendance = \frac{Attended\ Classes}{Total\ Classes}\times100
\]

The application uses a 75% attendance threshold.

### Semester Grade Point Average (SGPA)

\[
SGPA = \frac{\sum(Credit \times Grade\ Point)}{\sum Credits}
\]

### Cumulative Grade Point Average (CGPA)

\[
CGPA = \frac{\sum(SGPA \times Semester\ Credits)}{\sum Semester\ Credits}
\]

---

## ⚠️ Current Limitations

- Data is stored temporarily in memory using Python lists and dictionaries.
- All records are reset when the application is closed.
- No external database or cloud storage is currently integrated.
- The application is designed as a desktop-based productivity system.

---

## 🚀 Future Enhancements

- Database integration using SQLite or MySQL.
- Permanent storage of student records and academic information.
- Assignment deadline notifications and reminders.
- Graphical attendance and academic performance analytics.
- Export attendance and CGPA reports as PDF files.
- Improved timetable visualization and scheduling.

---

## 👥 Team Members

| S. No. | Name | Roll Number |
|---|---|---|
| 1 | [Member 1] | [Roll Number] |
| 2 | [Member 2] | [Roll Number] |
| 3 | [Member 3] | [Roll Number] |

---

## 🎯 Project Objective

The primary objective of Campus Companion is to develop a simple, user-friendly academic management application that brings essential student productivity tools together in one place.

By combining timetable management, task organization, attendance monitoring, academic performance calculation and student profile management, the project aims to improve students' academic organization and productivity.

---

**Developed as an academic team project using Python and Tkinter.**