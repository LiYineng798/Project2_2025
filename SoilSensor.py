
import RPi.GPIO as GPIO
import time
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define sensor digital output pin (D0)
SENSOR_PIN = 20

# Configure pin as input
GPIO.setup(SENSOR_PIN, GPIO.IN)

def read_soil_sensor():
    """Read the digital output of the soil moisture sensor"""
    try:
        while True:
            # Read digital output value (0 means wet, 1 means dry)
            sensor_value = GPIO.input(SENSOR_PIN)
            if sensor_value == 0:
                logger.info("Soil is moist")
            else:
                logger.info("Soil is dry, needs watering")
            # Read every second
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Program terminated")
    finally:
        # Clean up GPIO settings
        GPIO.cleanup()

if __name__ == "__main__":
    logger.info("Starting to read soil moisture sensor")
    read_soil_sensor()

