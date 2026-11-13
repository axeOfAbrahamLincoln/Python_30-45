import pandas as pd
import datetime as dt
import random
import smtplib

# Sender email address.
my_email = "kormociadam@gmail.com"

# Load the Gmail app password from a local file. This password is not shared with GitHub.
with open("password.txt") as password_file:
    password = password_file.read().strip()


birthday_person = []

birthday_dataset = pd.read_csv("birthdays.csv")
birthdays_list = birthday_dataset.to_dict(orient="records")


today = dt.date.today()
month_today = today.month
day_today = today.day


for person in birthdays_list:
    if month_today == person["month"] and day_today == person["day"]:
        birthday_person.append(person)

if birthday_person != []:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        for person in birthday_person:
            with open(f"letter_templates/letter_{random.randrange(1,4)}.txt", mode="r") as letter_file:
                birthday_letter = letter_file.read().replace("[NAME]", person["name"])
            connection.sendmail(
                from_addr=my_email,
                to_addrs=person["email"],
                msg=f"Subject:Happy Birthday\n\n{birthday_letter}".encode("utf-8"),
            )
