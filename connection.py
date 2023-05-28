
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class ConnectWindow(QMainWindow):
    def __init__(self, serialWrapper):
        super(ConnectWindow, self).__init__()
        
        self.setWindowTitle("Connect to Robot")
        
        layout = QVBoxLayout()
        
        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)
        layout.addWidget(self.connect_button)

        # Disconnect button
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect)
        layout.addWidget(self.disconnect_button)
        
        # Set the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        # Serial connection object
        self.serialWrapper = serialWrapper

    def connect(self):
        # Implement the function to connect via bluetooth here
        if self.serialWrapper.connection is None:
            try:
                self.serialWrapper.connection = serial.Serial(self.serialWrapper.com_port, 9600)
                print(f"Connected to {self.serialWrapper.com_port}")
            except Exception as e:
                print(f"Error connecting to {self.serialWrapper.com_port}: {str(e)}")
        else:
            print("Already connected")

    def disconnect(self):
        # Implement the function to disconnect here
        if self.serialWrapper.connection is not None:
            try:
                self.serialWrapper.connection.close()
                print(f"Disconnected from {self.serialWrapper.com_port}")
                self.serialWrapper.connection = None
            except Exception as e:
                print(f"Error disconnecting: {str(e)}")
        else:
            print("Not connected to any device")
            
    def closeEvent(self, event):
        # This function is called when the close button is clicked
        # Instead of closing the window, we simply hide it
        event.ignore()
        self.hide()
