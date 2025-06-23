
import RPi.GPIO as GPIO
import time
import logging
import smtplib
from email.mime.text import MIMEText
import json

# Configure logging for detailed debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set GPIO mode to BCM
logger.info("Setting GPIO mode to BCM")
GPIO.setmode(GPIO.BCM)

# Define sensor digital output pin (D0)
SENSOR_PIN = 20
logger.info(f"Configuring sensor pin: {SENSOR_PIN}")

# Configure pin as input
GPIO.setup(SENSOR_PIN, GPIO.IN)
logger.info(f"Pin {SENSOR_PIN} configured as input")

# Email configuration (password loaded from config.js)
MAIL_CONFIG = {
    "email_sender": "lyn228239@gmail.com",
    "email_receiver": "1779271568@qq.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}
logger.info("Email configuration initialized")

# SMTP timeout duration (seconds)
SMTP_TIMEOUT = 30
logger.info(f"SMTP timeout set to {SMTP_TIMEOUT} seconds")

def load_email_password():
    """Load email password from config.js"""
    logger.info("Attempting to load email password from config.js")
    try:
        with open('config.js', 'r') as file:
            logger.info("Successfully opened config.js")
            config = json.load(file)
            logger.info("Config file parsed successfully")
            password = config["email_password"]
            logger.info("Email password retrieved")
            return password
    except Exception as e:
        logger.error(f"Failed to load email password: {str(e)}")
        raise

def send_watering_email(sensor_value):
    """Send watering reminder email"""
    logger.info("Preparing to send watering reminder email")
    try:
        # Load email password
        logger.info("Loading email password")
        MAIL_CONFIG["email_password"] = load_email_password()
        logger.info("Email password loaded successfully")
        
        # Set email content based on sensor value
        logger.info(f"Preparing email content for sensor value: {sensor_value}")
        subject = "Soil Moisture Reminder"
        body = "Soil is moist, no watering needed" if sensor_value == 0 else "Soil is dry, needs watering"
        logger.info(f"Email subject: {subject}")
        logger.info(f"Email body: {body}")
        
        # Create email message
        logger.info("Creating MIMEText email message")
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = MAIL_CONFIG["email_sender"]
        msg['To'] = MAIL_CONFIG["email_receiver"]
        logger.info("Email headers configured")

        # Connect and send email
        logger.info(f"Connecting to SMTP server: {MAIL_CONFIG['smtp_server']}:{MAIL_CONFIG['smtp_port']}")
        with smtplib.SMTP(MAIL_CONFIG["smtp_server"], MAIL_CONFIG["smtp_port"], timeout=SMTP_TIMEOUT) as server:
            logger.info("Initiating STARTTLS")
            server.starttls()
            logger.info("Logging in to SMTP server")
            server.login(MAIL_CONFIG["email_sender"], MAIL_CONFIG["email_password"])
            logger.info("Sending email")
            server.send_message(msg)
            logger.info("Email sent successfully")

        logger.info("Watering reminder email sent successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def main():
    """Main function: Read sensor and send one email"""
    logger.info("Starting main function")
    try:
        # Read sensor value
        logger.info(f"Reading sensor value from pin {SENSOR_PIN}")
        sensor_value = GPIO.input(SENSOR_PIN)
        status = "Soil is moist" if sensor_value == 0 else "Soil is dry, needs watering"
        logger.info(f"Sensor reading: {status}")
        
        # Send email
        logger.info("Initiating email sending process")
        send_watering_email(sensor_value)
        logger.info("Email sending process completed")
    except Exception as e:
        logger.error(f"Program error: {str(e)}")
    finally:
        # Clean up GPIO settings
        logger.info("Cleaning up GPIO settings")
        GPIO.cleanup()
        logger.info("GPIO cleanup completed")

if __name__ == "__main__":
    logger.info("Starting soil moisture email reminder program")
    main()
    logger.info("Program execution completed")

