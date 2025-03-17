import csv
import random

platforms = ["Udemy", "Zenva", "Coursera", "edX", "Pluralsight"]
statuses = ["Not Started", "In Progress", "Completed"]

with open("test_courses.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "title", "platform", "status", "progress", "notes"])
    for i in range(1, 1501):
        title = f"Course {i}"
        platform = random.choice(platforms)
        progress = random.randint(0, 100)
        status = "Completed" if progress == 100 else "In Progress" if progress > 0 else "Not Started"
        notes = f"Notes for course {i}" if random.random() > 0.5 else ""
        writer.writerow([i, title, platform, status, progress, notes])

print("Generated test_courses.csv with 1500 courses")