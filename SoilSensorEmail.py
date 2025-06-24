
import RPi.GPIO as GPIO
import time
import logging
import smtplib
from email.mime.text import MIMEText
import json
from datetime import datetime
import schedule

# Configure logging for essential information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define sensor digital output pin (D0)
SENSOR_PIN = 20

# Configure pin as input
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Email configuration
MAIL_CONFIG = {
    "email_sender": "lyn228239@gmail.com",
    "email_receiver": "1779271568@qq.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}

# SMTP timeout duration (seconds)
SMTP_TIMEOUT = 30

def load_email_password():
    """Load email password from config.js"""
    try:
        with open('config.js', 'r') as file:
            config = json.load(file)
            return config["email_password"]
    except Exception as e:
        logger.error(f"Failed to load email password: {str(e)}")
        raise

def generate_email_html(sensor_value):
    """Generate HTML email content based on sensor value"""
    background_color = "#FF4D4D" if sensor_value == 1 else "#4CAF50"
    status_text = "Please Water Your Plant! 🌱💧" if sensor_value == 1 else "Soil is Moist, No Watering Needed! 🌿"
    emoji = "🚨" if sensor_value == 1 else "✅"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Soil Moisture Reminder</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: {background_color}; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                        <tr>
                            <td style="background-color: {background_color}; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Soil Moisture Alert {emoji}</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 20px; text-align: center;">
                                <h2 style="color: #333333; margin: 0 0 20px 0;">{status_text}</h2>
                                <p style="color: #555555; font-size: 16px; line-height: 1.5;">
                                    Hello Plant Lover! 🌼<br>
                                    Your plant's soil moisture was checked at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.<br>
                                    <strong>{'Urgent: Your plant needs water!' if sensor_value == 1 else 'Your plant is happy and well-hydrated.'}</strong><br>
                                    Keep nurturing your green friend! 🌳
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; color: #777777;">
                                <p>Automated message from your Soil Moisture Monitoring System</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html_content

def send_watering_email(sensor_value):
    """Send watering reminder email with HTML content"""
    try:
        MAIL_CONFIG["email_password"] = load_email_password()
        
        # Set email content
        subject = "Soil Moisture Reminder"
        html_content = generate_email_html(sensor_value)
        
        # Create email message
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = MAIL_CONFIG["email_sender"]
        msg['To'] = MAIL_CONFIG["email_receiver"]

        # Connect and send email
        with smtplib.SMTP(MAIL_CONFIG["smtp_server"], MAIL_CONFIG["smtp_port"], timeout=SMTP_TIMEOUT) as server:
            server.starttls()
            server.login(MAIL_CONFIG["email_sender"], MAIL_CONFIG["email_password"])
            server.send_message(msg)

        logger.info(f"Email sent: {'Water needed' if sensor_value == 1 else 'No water needed'}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def read_and_notify():
    """Read sensor and send email notification"""
    try:
        sensor_value = GPIO.input(SENSOR_PIN)
        status = "moist" if sensor_value == 0 else "dry"
        logger.info(f"Soil is {status}")
        send_watering_email(sensor_value)
    except Exception as e:
        logger.error(f"Error reading sensor: {str(e)}")

def main():
    """Main function: Schedule sensor readings and email notifications"""
    try:
        # Schedule tasks at 8 AM, 12 PM, 4 PM, and 8 PM
        schedule.every().day.at("08:00").do(read_and_notify)
        schedule.every().day.at("12:00").do(read_and_notify)
        schedule.every().day.at("16:00").do(read_and_notify)
        schedule.every().day.at("20:00").do(read_and_notify)
        logger.info("Scheduled sensor readings at 8 AM, 12 PM, 4 PM, and 8 PM")

        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
    except Exception as e:
        logger.error(f"Program error: {str(e)}")
    finally:
        GPIO.cleanup()
        logger.info("GPIO cleanup completed")

if __name__ == "__main__":
    logger.info("Starting soil moisture monitoring program")
    main()

