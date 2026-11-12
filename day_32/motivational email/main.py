"""Password note: The Gmail app password is stored locally in the project and is not uploaded to GitHub. The password file is included in the .gitignore file so it stays private and secure."""

# Import the libraries needed to send an email and work with dates and random choices.
import smtplib
import random
import datetime as dt

# Read a random motivational quote from the text file so it can be included in the email body.
with open("motivational_quotes.txt", mode="r") as motivational_qoutes_list:
    random_quote = random.choice(motivational_qoutes_list.readlines())

# Sender email address.
my_email = "kormociadam@gmail.com"

# Load the Gmail app password from a local file. This password is not shared with GitHub.
with open("password.txt") as password_file:
    password = password_file.read().strip()


# Send the motivational email only on Thursday (weekday 3 in Python's datetime system).
if dt.datetime.now().weekday() == 3:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="kormociadam@gmail.com",
            msg=f"Subject:Motivation to you\n\n{random_quote}".encode("utf-8"),
        )
