import smtplib
import random
import re
import tkinter as tk
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp(length=6):
    """
    Generates a random OTP of the specified length.
    """
    return ''.join(random.choices('0123456789', k=length))

def send_otp_email(receiver_email, otp):
    """
    Sends the generated OTP to the specified email address.
    """

    # Email credentials and settings
    sender_email = "repalce with your gmail id"  # Replace with your email
    sender_password = "use application password"        # Replace with your email password or app password
    subject = "Your OTP Code"

    # Create email content
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    body = f"Your One-Time Password (OTP) is: {otp}\n\nPlease use this code to complete your action."
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"OTP sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send OTP. Error: {e}")

def is_valid_email(email):
    """
    Validates the email address format.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Store OTPs for email addresses
otp_store = {}

def start_gui():
    def send_otp():
        email = email_entry.get()
        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        otp = generate_otp()
        otp_store[email] = otp
        send_otp_email(email, otp)
        messagebox.showinfo("Success", "OTP sent successfully!")

    def verify_otp():
        email = email_entry.get()
        otp = otp_entry.get()

        if email not in otp_store:
            messagebox.showerror("Error", "No OTP generated for this email.")
            return

        if otp_store[email] == otp:
            del otp_store[email]  # Clear OTP after successful verification
            messagebox.showinfo("Success", "OTP verified successfully!")
        else:
            messagebox.showerror("Error", "Invalid OTP.")

    root = tk.Tk()
    root.title("OTP System")

    tk.Label(root, text="Email Address:").grid(row=0, column=0, padx=10, pady=10)
    email_entry = tk.Entry(root, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="OTP:").grid(row=1, column=0, padx=10, pady=10)
    otp_entry = tk.Entry(root, width=30)
    otp_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(root, text="Send OTP", command=send_otp).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(root, text="Verify OTP", command=verify_otp).grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
