import os
from desktop.data.database import Database
import matplotlib.pyplot as plt

class ReportGenerator:
    def __init__(self, db: Database):
        self.db = db

    def generate_course_report(self, user_id, report_path='course_report.txt'):
        courses = self.db.get_all_courses(user_id)
        total_courses = len(courses)
        completed_courses = sum(1 for course in courses if course[4] == "Completed")
        in_progress_courses = sum(1 for course in courses if course[4] == "In Progress")
        not_started_courses = total_courses - completed_courses - in_progress_courses

        with open(report_path, 'w') as report_file:
            report_file.write(f"Total Courses: {total_courses}\n")
            report_file.write(f"Completed Courses: {completed_courses}\n")
            report_file.write(f"In Progress Courses: {in_progress_courses}\n")
            report_file.write(f"Not Started Courses: {not_started_courses}\n")

        print(f"Report saved to {report_path}")

        self.generate_course_chart(completed_courses, in_progress_courses, not_started_courses)

    def generate_course_chart(self, completed, in_progress, not_started):
        labels = 'Completed', 'In Progress', 'Not Started'
        sizes = [completed, in_progress, not_started]
        colors = ['gold', 'yellowgreen', 'lightcoral']
        explode = (0.1, 0, 0)  # explode 1st slice

        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.savefig('course_chart.png')
        plt.show()

if __name__ == "__main__":
    db = Database("courses.db")
    user_id = 1  # Replace with the actual user ID
    report_generator = ReportGenerator(db)
    report_generator.generate_course_report(user_id)
    db.close()