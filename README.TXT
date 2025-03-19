# School Management System

## Overview

This project implements a simple school management system using Python and pandas. It leverages CSV files for persistent storage of data such as employees, students, attendance, class schedules, and lesson plans. The system provides functions for adding, updating, and removing records, as well as generating analytical reports with visualizations.

## Features

- **Employee Management:**  
  Add, update, and remove employee records. Employees are assigned roles (admin, teacher, or staff) based on their position.
  
- **Student Management:**  
  Add, update, remove, and import student records. Student marks and class assignments can also be managed.
  
- **Attendance Management:**  
  Mark attendance for students by class and date. Attendance records can be later used to generate reports.
  
- **Class Scheduling:**  
  Create and update class schedules including class details, dates, duration, and maximum number of students. Assign teachers to specific classes and dates.
  
- **Lesson Plans:**  
  Create and update lesson plans with details such as subject, learning objectives, and assessments.
  
- **Reports and Analysis:**  
  Generate analysis reports for classes that include:
  - Attendance statistics (e.g., attendance rate and standard deviation).
  - Student marks statistics (e.g., average marks, standard deviation).
  - Visualizations of attendance trends, marks distribution, and grade breakdown.

- **CSV Data Persistence:**  
  All data is stored in CSV files located in a dedicated `csv` folder, making it easy to back up or edit data externally.

## File Structure

- **csv/**  
  Directory containing CSV files for:
  - `employees.csv`
  - `students.csv`
  - `attendance.csv`
  - `schedules.csv`
  - `lesson_plan.csv`

- **reports/**  
  Directory where analysis report plots and summary images are saved (created automatically if it does not exist).

- **school.py**  
  The main Python script containing the `School` class and all its methods.

## Dependencies

- [Python 3.x](https://www.python.org/downloads/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)

You can install the required packages using pip:

```bash
pip install requirements.txt
