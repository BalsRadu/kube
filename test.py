import serial
import time

# Set up the serial line
# Replace 'COMX' with your Bluetooth device name or the correct COM port
serialPort = serial.Serial('COM13', 9600)

def send(data):
    serialPort.write(data.encode())

def receive():
    while True:
        if serialPort.in_waiting > 0:
            incoming_serial_data = serialPort.readline()
            print('Received data: ', incoming_serial_data.decode('utf-8'))

try:
    while True:
        print("Enter '1' to turn on the LED or '0' to turn off the LED")
        data = input()
        if data == '1' or data == '0':
            send(data)
            time.sleep(0.1)
            receive()

        else:
            print("Invalid input. Please enter '1' or '0'.")

except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serialPort.close()
    print("Serial port closed. Exiting Program")