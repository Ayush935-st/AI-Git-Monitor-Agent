import smtplib

EMAIL = "ayush.srinivasan09@gmail.com"
PASSWORD = "hkjvhwzhgtcqrlbp"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, PASSWORD)
print("Login Successful!")
server.quit()