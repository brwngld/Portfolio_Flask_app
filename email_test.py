import smtplib

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("amegben@gmail.com", "xkatfvyyhdgjdjye")
    print("Logged in successfully!")
    server.quit()
except Exception as e:
    print("SMTP test failed:", e)
