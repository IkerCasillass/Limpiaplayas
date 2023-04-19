import functions2 as func
import serial, time


arduino = serial.Serial("COM7", 9600, timeout=1)


func.arduinoMessage("led1", arduino)