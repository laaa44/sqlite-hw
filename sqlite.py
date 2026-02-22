import sqlite3


db = sqlite3.connect("students.db")
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    studentID INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS course (
    courseID INTEGER PRIMARY KEY,
    courseName TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS registered_courses (
    studentID INTEGER,
    courseID INTEGER,
    FOREIGN KEY(studentID) REFERENCES student(studentID),
    FOREIGN KEY(courseID) REFERENCES course(courseID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    studentID INTEGER,
    courseID INTEGER,
    grade REAL,
    FOREIGN KEY(studentID) REFERENCES student(studentID),
    FOREIGN KEY(courseID) REFERENCES course(courseID)
)
""")


cursor.execute("DELETE FROM student")
cursor.execute("DELETE FROM course")
cursor.execute("DELETE FROM registered_courses")
cursor.execute("DELETE FROM grades")


cursor.execute("INSERT INTO student VALUES (1, 'Aya', 20)")
cursor.execute("INSERT INTO student VALUES (2, 'Dany', 21)")

# Courses
cursor.execute("INSERT INTO course VALUES (101, 'Database Systems')")
cursor.execute("INSERT INTO course VALUES (102, 'Computer Networks')")
cursor.execute("INSERT INTO course VALUES (103, 'Electronics I')")


cursor.execute("INSERT INTO registered_courses VALUES (1, 101)")
cursor.execute("INSERT INTO registered_courses VALUES (1, 102)")
cursor.execute("INSERT INTO registered_courses VALUES (2, 101)")
cursor.execute("INSERT INTO registered_courses VALUES (2, 103)")


cursor.execute("INSERT INTO grades VALUES (1, 101, 85.5)")
cursor.execute("INSERT INTO grades VALUES (1, 102, 90.0)")
cursor.execute("INSERT INTO grades VALUES (2, 101, 78.0)")
cursor.execute("INSERT INTO grades VALUES (2, 103, 82.0)")

db.commit()




print("Maximum grade per student:")
cursor.execute("""
SELECT s.studentID, s.name, c.courseName, g.grade
FROM grades g
JOIN student s ON g.studentID = s.studentID
JOIN course c ON g.courseID = c.courseID
WHERE g.grade = (
    SELECT MAX(grade)
    FROM grades
    WHERE studentID = g.studentID
)
""")
for row in cursor.fetchall():
    print(f"Student {row[1]} (ID {row[0]}) : Max Grade {row[3]} in {row[2]}")


print("\nAverage grade per student:")
cursor.execute("""
SELECT s.studentID, s.name, AVG(g.grade)
FROM grades g
JOIN student s ON g.studentID = s.studentID
GROUP BY s.studentID
""")
for row in cursor.fetchall():
    print(f"Student {row[1]} (ID {row[0]}) : Average Grade {row[2]:.2f}")


print("\nAll students with their registered courses and grades:")
cursor.execute("""
SELECT s.name, c.courseName, g.grade
FROM registered_courses rc
JOIN student s ON rc.studentID = s.studentID
JOIN course c ON rc.courseID = c.courseID
LEFT JOIN grades g ON rc.studentID = g.studentID AND rc.courseID = g.courseID
ORDER BY s.name, c.courseName
""")
for row in cursor.fetchall():
    print(f"{row[0]} : {row[1]} : {row[2]}")


db.close()
