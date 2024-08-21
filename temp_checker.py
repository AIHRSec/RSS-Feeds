from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import configparser
import subprocess

# runs the vcgencmd command to get the current temperature of the device
result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)

# extracts the temperature value
temp_str = result.stdout.strip()
temp_value = temp_str.split('=')[1].split("'")[0]

# convert the extracted value to a float
temperature = float(temp_value)
threshold_temp = float(65.0)

# compare the temperature to the threshold
if temperature < threshold_temp:
   exit()
else:
    # variables misc variable for email
    subject_name = "WARNING: High Temperature"

    # load email configuration from the config file
    config = configparser.ConfigParser()
    config.read("config.ini")

    smtp_server = config["email"]["smtp_server"]
    smtp_port = int(config["email"]["smtp_port"])
    sender_email = config["email"]["sender_email"]
    recipient_email = config["email"]["recipient_email"]
    password = config["email"]["password"]
    recipient_emails = config["email"]["recipient_email"].split(', ') # needed for multiple recipients
    first_email = recipient_emails[0]  # pulls first email only 
    # uncomment the line below for multiple recipients and comment the line above
    # recipient_emails_str = ', '.join(recipient_emails) # needed for multiple recipients

    # create a multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = first_email
    # uncomment the line below for multiple recipients and comment the line above
    #message['To'] = recipient_emails_str
    message['Subject'] = subject_name
    

    # Add message body
    body = ("The temperature is " + str(temperature) + "°C, which is higher than the threshold of " + str(threshold_temp) + "°C")
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start TLS encryption
        # Login to the SMTP server
        server.login(sender_email, password)
        # Send email
        server.send_message(message)
        print("Email sent successfully")
