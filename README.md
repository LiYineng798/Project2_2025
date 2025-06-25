# Raspberry Pi Soil Moisture Monitoring System

## Project Introduction

This project aims to design, build, and test a Raspberry Pi-based device for monitoring soil moisture in plants. The system monitors soil moisture by connecting a soil moisture sensor (FC-28) and sends email notifications when the moisture level falls below a set threshold.

The project is managed using the Scrum agile framework, employing sprint cycles and burndown charts to track progress and ensure efficient project delivery.

## Hardware Requirements

*   Raspberry Pi (any model)
*   Soil Moisture Sensor (FC-28)
*   Connecting Wires (Dupont wires, etc.)
*   Power Adapter (for Raspberry Pi)

## Steps to Run the Script

1.  **Hardware Connection:**
   *   Connect the FC-28 soil moisture sensor to the Raspberry Pi's GPIO pin (Port P20).
2.  **Software Installation:**
   *   Install the necessary Python library, `RPi.GPIO`, on the Raspberry Pi.
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip
   pip3 install RPi.GPIO
   ```
3.  **Email Configuration:**
   *   Configure the email sending parameters in the Python script, including the sender's email address, password, and recipient's email address.
   *   Configure the 'config.js' file in the same directory.
4.  **Run Script:**
   *   Copy the project code to the Raspberry Pi.
   *   Run the main script using Python.
   ```bash
   python3 main.py
   ```
5.  **Automatic Execution:**
   *   Once the program is enabled, the system will automatically detect soil moisture and send emails on a scheduled basis.
   *   Additionally, the system will output info to the terminal for later inspection.

## Project Features

*   **Real-time Monitoring:** Real-time monitoring of soil moisture.
*   **Email Notification:** Automatic email notifications when soil moisture falls below a set threshold.
*   **Configurability:** Flexible configuration of moisture thresholds and email sending parameters.
*   **Easy Deployment:** Simple deployment, easy to use in various environments.
*   **Scrum-based Agile Development:** Project management using the Scrum framework to ensure an efficient development process.

## Scrum Agile Development

This project is developed using the Scrum agile framework, specifically including:

*   **Sprint Cycle:** Two-week sprint cycle.
*   **Burndown Chart:** Tracking sprint progress using a burndown chart.

## Objectives

*   Apply agile principles and use the Scrum framework to plan and execute the project.
*   Complete the hardware connection and software development of the Raspberry Pi and soil moisture sensor.
*   Implement the function of automatically detecting soil moisture and sending email notifications 4 times a day.
