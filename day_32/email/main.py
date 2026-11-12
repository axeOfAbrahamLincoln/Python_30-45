import smtplib

my_email = "kormociadam@gmail.com"
password = "faob bdps hpbg gwzn"

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(my_email, password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="csaba.kormoci@gmail.com",
        msg="Subject:Hello\n\nHello, ha ezt a sort olvasod akkor sikerult emailt kuldenem abbol a programbol amit en irtam",
    )
