from flask import Flask, render_template, request, jsonify
import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

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
    sender_email = "twinkledevwanshi93@gmail.com"  # Replace with your email
    sender_password = "fjof hfah knql fseb"        # Replace with your email password or app password
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.form.get('email')
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address."}), 400

    otp = generate_otp()
    otp_store[email] = otp
    send_otp_email(email, otp)
    return jsonify({"message": "OTP sent successfully!"}), 200

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = request.form.get('email')
    otp = request.form.get('otp')

    if email not in otp_store:
        return jsonify({"error": "No OTP generated for this email."}), 400

    if otp_store[email] == otp:
        del otp_store[email]  # Clear OTP after successful verification
        return jsonify({"message": "OTP verified successfully!"}), 200
    else:
        return jsonify({"error": "Invalid OTP."}), 400

if __name__ == "__main__":
    app.run(debug=True)
