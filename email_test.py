import smtplib

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("your_email_address", "your_app_password")
    print("Logged in successfully!")
    server.quit()
except Exception as e:
    print("SMTP test failed:", e)
