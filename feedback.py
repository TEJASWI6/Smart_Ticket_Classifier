import csv
from datetime import datetime


def save_feedback(user, feedback):
    # Save feedback to a CSV file
    with open('feedback.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), user, feedback])

