import serial

class SerialWrapper:
    def __init__(self, com_port='COM13', baud_rate=9600):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.connection = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = serial.Serial(self.com_port, self.baud_rate)
                print(f"Connected to {self.com_port}")
            except Exception as e:
                print(f"Error connecting to {self.com_port}: {str(e)}")

    def disconnect(self):
        if self.connection is not None:
            try:
                self.connection.close()
                print(f"Disconnected from {self.com_port}")
                self.connection = None
            except Exception as e:
                print(f"Error disconnecting: {str(e)}")
        else:
            print("Not connected to any device")
