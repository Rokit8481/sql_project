import sqlite3

class StudentCourseManager:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def add_student(self):
        name = input("Ім'я студента: ")
        age = int(input("Вік: "))
        major = input("Спеціальність: ")
        self.cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
        self.conn.commit()
        print("Студента додано!")

    def add_course(self):
        course_name = input("Ім'я курсу: ")
        instructor = input("Викладач: ")
        self.cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
        self.conn.commit()
        print("Курс додано!")

    def show_students(self):
        self.cursor.execute("SELECT * FROM students")
        students = self.cursor.fetchall()
        print("\nСписок студентів:")
        for s in students:
            print(f"ID: {s[0]}, Ім'я: {s[1]}, Вік: {s[2]}, Спеціальність: {s[3]}")

    def show_courses(self):
        self.cursor.execute("SELECT * FROM courses")
        courses = self.cursor.fetchall()
        print("\nСписок курсів:")
        for c in courses:
            print(f"ID: {c[0]}, Назва: {c[1]}, Викладач: {c[2]}")

    def register_student_to_course(self):
        try:
            student_id = int(input("ID студента: "))
            course_id = int(input("ID курсу: "))
            self.cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
            self.conn.commit()
            print("Студента зареєстровано на курс!")
        except sqlite3.IntegrityError:
            print("Такий запис вже існує або ID некоректні.")

    def show_students_in_course(self):
        course_id = int(input("Введіть ID курсу: "))

        self.cursor.execute("SELECT course_name FROM courses WHERE course_id = ?", (course_id,))
        course = self.cursor.fetchone()

        if not course:
            print("Курс з таким ID не знайдено.")
            return

        course_name = course[0]

        self.cursor.execute('''
            SELECT students.id, students.name
            FROM students
            JOIN student_courses ON students.id = student_courses.student_id
            WHERE student_courses.course_id = ?
        ''', (course_id,))
        results = self.cursor.fetchall()

        if results:
            print(f"\nСтуденти, зареєстровані на курс \"{course_name}\":")
            for r in results:
                print(f"ID: {r[0]}, Ім'я: {r[1]}")
        else:
            print(f"На курс \"{course_name}\" ще ніхто не зареєстрований.")

    def run(self):
        while True:
            print("\n1. Додати нового студента")
            print("2. Додати новий курс")
            print("3. Показати список студентів")
            print("4. Показати список курсів")
            print("5. Зареєструвати студента на курс")
            print("6. Показати студентів на конкретному курсі")
            print("7. Вийти")

            choice = input("Оберіть опцію (1-7): ")

            match choice:
                case "1":
                    self.add_student()
                case "2":
                    self.add_course()
                case "3":
                    self.show_students()
                case "4":
                    self.show_courses()
                case "5":
                    self.register_student_to_course()
                case "6":
                    self.show_students_in_course()
                case "7":
                    print("До побачення!")
                    break
                case _:
                    print("Некоректний вибір. Будь ласка, введіть число від 1 до 7.")

        self.conn.close()

if __name__ == "__main__":
    manager = StudentCourseManager()
    manager.run()
