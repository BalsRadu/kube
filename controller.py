from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from connection import ConnectWindow  # import the ConnectWindow class
from joystick import JoystickWindow  # import the JoystickWindow class
from serial_wrapper import SerialWrapper  # import the SerialWrapper class
from follower import LineFollowerWindow  # import the LineFollowerWindow class
import qdarkstyle
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Robot Controller")

        # Create a central widget and set a layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Apply dark theme
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

        # Connect button
        self.connect_button = QPushButton("Connect to Robot", self)
        self.connect_button.clicked.connect(self.connect_to_robot)
        layout.addWidget(self.connect_button)

        # Joystick control button
        self.joystick_button = QPushButton("Joystick Control", self)
        self.joystick_button.clicked.connect(self.joystick_control)
        layout.addWidget(self.joystick_button)

        # Line follower mode button
        self.line_follower_button = QPushButton("Line follower mode", self)
        self.line_follower_button.clicked.connect(self.line_follower)
        layout.addWidget(self.line_follower_button)

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Serial connection object
        self.serialWrapper = SerialWrapper()

    def connect_to_robot(self):
        # Open the Connect page here
        self.connect_window = ConnectWindow(self.serialWrapper)
        self.connect_window.show()

    def joystick_control(self):
        # Open the Joystick Control page here
        self.joystick_window = JoystickWindow(self.serialWrapper)
        self.joystick_window.show()

    def line_follower(self):
        # Open the Line Follower Control page here
        self.line_follower_window = LineFollowerWindow(self.serialWrapper)
        self.line_follower_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
