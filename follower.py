from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout
from pyqtgraph import PlotWidget, plot, BarGraphItem
from PyQt5 import QtCore
import pyqtgraph as pg
import random
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor

class LineFollowerWindow(QMainWindow):
    def __init__(self, serialWrapper):
        super(LineFollowerWindow, self).__init__()

        self.setWindowTitle("Line Follower Mode")

        layout = QGridLayout()

        # Buttons
        self.stop_robot_button = QPushButton("Stop Robot")
        self.start_robot_turbine_button = QPushButton("Start Robot With Turbine")
        self.start_robot_no_turbine_button = QPushButton("Start Robot Without Turbine")
        self.calibrate_button = QPushButton("Calibrate")

        self.stop_robot_button.clicked.connect(self.stop_robot)
        self.start_robot_turbine_button.clicked.connect(self.start_robot_turbine)
        self.start_robot_no_turbine_button.clicked.connect(self.start_robot_no_turbine)
        self.calibrate_button.clicked.connect(self.calibrate)

        # Graphs
        self.left_motor_graph = PlotWidget()
        self.right_motor_graph = PlotWidget()

        # Sensor blocks
        self.sensor_blocks = [QLabel() for _ in range(8)]
        for block in self.sensor_blocks:
            block.setStyleSheet("background-color: red")

        # Add widgets to the layout
        layout.addWidget(self.stop_robot_button, 0, 0)
        layout.addWidget(self.start_robot_turbine_button, 0, 1)
        layout.addWidget(self.start_robot_no_turbine_button, 0, 2)
        layout.addWidget(self.calibrate_button, 0, 3)
        layout.addWidget(self.left_motor_graph, 1, 0, 1, 4)
        layout.addWidget(self.right_motor_graph, 2, 0, 1, 4)
        for i, block in enumerate(self.sensor_blocks):
            layout.addWidget(block, 3, i)

        # Set the layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.left_motor_graph.setYRange(-1, 1)
        self.right_motor_graph.setYRange(-1, 1)

        # Serial connection object
        self.serialWrapper = serialWrapper

        self.serialWrapper.connection.timeout = 2  # 2 seconds


        # Initial data for motor graphs
        self.left_motor_data = [0 for _ in range(10)]
        self.right_motor_data = [0 for _ in range(10)]

        # BarGraphItem for motor graphs
        self.left_motor_graph_item = BarGraphItem(x=range(len(self.left_motor_data)), height=self.left_motor_data, width=1)
        self.right_motor_graph_item = BarGraphItem(x=range(len(self.right_motor_data)), height=self.right_motor_data, width=1)
        
        # Add BarGraphItems to the graphs
        self.left_motor_graph.addItem(self.left_motor_graph_item)
        self.right_motor_graph.addItem(self.right_motor_graph_item)

        # Initialize timer for receiving serial data
        self.timer = QTimer()
        self.timer.timeout.connect(self.serial_data_event_loop)
        self.timer.start(10)  # in ms, adjust as needed


    def stop_robot(self):
        self.send_command("follower,stop_robot;")

    def start_robot_turbine(self):
        self.send_command("follower,start_follower_turbine;")

    def start_robot_no_turbine(self):
        self.send_command("follower,start_follower_no_turbine;")

    def calibrate(self):
        self.send_command("follower,calibrate;")

    def send_command(self, command):
        if self.serialWrapper.connection:
            try:
                # Write only if the connection is not busy
                if self.serialWrapper.connection.out_waiting == 0:
                    self.serialWrapper.connection.write(command.encode())
            except Exception as e:
                print(f"Error writing to serial port: {str(e)}")
        else:
            print("Not connected to any device")

    def serial_data_event_loop(self):
        if self.serialWrapper.connection:
            while self.serialWrapper.connection.in_waiting:
                try:
                    incoming_serial_data = self.serialWrapper.connection.readline().decode('utf-8').strip()
                    print(incoming_serial_data)
                    if incoming_serial_data.startswith("motor,"):
                        # Update motor graphs
                        _, left_motor, right_motor = incoming_serial_data.split(',')
                        self.update_graphs(float(left_motor), float(right_motor.split(';')[0]))
                    elif incoming_serial_data.startswith("sensor,"):
                        # Update sensor blocks
                        _, sensor = incoming_serial_data.split(',')
                        self.update_sensor_blocks(int(sensor.split(';')[0]))
                    else:
                        # Print any other incoming data
                        print(incoming_serial_data)
                except Exception as e:
                    print(f"Error reading from serial port: {str(e)}")


    def update_graphs(self, left_motor, right_motor):
        self.left_motor_data = self.left_motor_data[1:] + [left_motor]
        self.right_motor_data = self.right_motor_data[1:] + [right_motor]

        self.left_motor_graph_item.setOpts(height=self.left_motor_data)
        self.right_motor_graph_item.setOpts(height=self.right_motor_data)

    def update_sensor_blocks(self, sensor_data):
        for block in self.sensor_blocks:
            block.setStyleSheet("background-color: red")
        
        self.sensor_blocks[sensor_data].setStyleSheet("background-color: green")


    def showEvent(self, event):
        # This function is called when the window is shown
        # Send the "follower;" message to the Arduino
        if self.serialWrapper.connection:
            try:
                self.serialWrapper.connection.write("follower;".encode())
                    
                # Wait for confirmation from the Arduino
                input = self.serialWrapper.connection.readline().decode('utf-8').strip()
                print(input)
                if input != "confirm_follower;":
                    print("Confirmation not received from Arduino")
            except Exception as e:
                print(f"Error writing to serial port: {str(e)}")
        else:
            print("Not connected to any device")

    def closeEvent(self, event):
        # This function is called when the window is closed
        # Send the "stop_following;" message to the Arduino
        if self.serialWrapper.connection:
            try:
                self.serialWrapper.connection.write("stop_following;".encode())
                    
                # Wait for confirmation from the Arduino
                input = self.serialWrapper.connection.readline().decode('utf-8').strip()
                print(input)
                if input != "confirm_stop_following;":
                    print("Confirmation not received from Arduino")
            except Exception as e:
                print(f"Error writing to serial port: {str(e)}")
            
        # Hide the window
        event.ignore()
        self.hide()

