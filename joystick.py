
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer

class JoystickWindow(QMainWindow):
    def __init__(self, serialWrapper):
        super(JoystickWindow, self).__init__()
        
        self.setWindowTitle("Joystick Control")
        
        layout = QVBoxLayout()
        
        # Joystick status label
        self.joystick_status = QLabel("Joystick disconnected")
        layout.addWidget(self.joystick_status)
        
        # Set the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Serial connection object
        self.serialWrapper = serialWrapper

        self.serialWrapper.connection.timeout = 2
        
        # Initialize pygame for joystick
        pygame.init()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)  # Get the first joystick
            self.joystick.init()


        # Initialize timer for pygame
        self.timer = QTimer()
        self.timer.timeout.connect(self.joystick_event_loop)
        self.timer.start(100)  # in ms, adjust as needed

        

    def joystick_event_loop(self):
        pygame.event.pump()  # to keep pygame in check with the OS
        if pygame.joystick.get_count() < 1:
            self.joystick_status.setText("Joystick disconnected")
            return
        
        self.joystick_status.setText("Joystick connected")
        
        # Do not initialize joystick here, it's done in __init__
        if pygame.event.get(pygame.JOYAXISMOTION):
            # Get the Y-axis values of the two analog sticks
            y1 = -1 * self.joystick.get_axis(1)
            y2 = -1 * self.joystick.get_axis(3)


            print(f"y1: {y1}, y2: {y2}")

            # If the values are beetwen -0.01 and 0.01, set them to 0
            if -0.01 < y1 < 0.01:
                y1 = 0
            if -0.01 < y2 < 0.01:
                y2 = 0

            # Send the joystick values to the Arduino
            data = f"joystick,{y1},{y2};"
            if self.serialWrapper.connection:
                try:
                    # Write only if the connection is not busy
                    if self.serialWrapper.connection.out_waiting == 0:
                        self.serialWrapper.connection.write(data.encode())
                except Exception as e:
                    print(f"Error writing to serial port: {str(e)}")
            else:
                print("Not connected to any device")

    def showEvent(self, event):
        # This function is called when the window is shown
        # Send the "joystick;" message to the Arduino
        if self.serialWrapper.connection:
            try:
                self.serialWrapper.connection.write("joystick;".encode())
                    
                # Wait for confirmation from the Arduino
                input = self.serialWrapper.connection.readline().decode('utf-8').strip()
                print(input)
                if input != "confirm_joystick;":
                    print("Confirmation not received from Arduino")
            except Exception as e:
                print(f"Error writing to serial port: {str(e)}")
        else:
            print("Not connected to any device")
    
    def closeEvent(self, event):
        # This function is called when the window is closed
        # Send the "exit;" message to the Arduino
        if self.serialWrapper.connection:
            try:
                self.serialWrapper.connection.write("exit;".encode())
                    
                # Wait for confirmation from the Arduino
                input = self.serialWrapper.connection.readline().decode('utf-8').strip()
                print(input)
                if input != "exit_confirmed;":
                    print("Confirmation not received from Arduino")
            except Exception as e:
                print(f"Error writing to serial port: {str(e)}")
            
        # Hide the window
        event.ignore()
        self.hide()

