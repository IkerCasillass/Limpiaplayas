# !usr/bin/python
# Standard imports
import cv2

import serial, time

# Serial communication
def arduinoMessage(cmd,arduino):

     arduino.write(cmd.encode())
     time.sleep(0.1) #wait for arduino to answer
     #answer=str(arduino.readline())
     #print(answer)
     #arduino.flushInput() #remove data after reading 
     
def main():

     # Arduino port
     arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
     # with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:

     #Webcam video
     vc = cv2.VideoCapture(0)
  
     
     #Main loop
     while True:
          ret, frame = vc.read()

          if ret == True:
              cv2.imshow("30fps",frame)
              vc.set(cv2.CAP_PROP_FPS, 30)
              
              #cv2.imshow("60fps",frame)
              #vc.set(cv2.CAP_PROP_FPS, 60)
			  
              arduinoMessage('B',arduino)
              #time.sleep(0.2)

               
              if cv2.waitKey(50) == 27:
                    break

     cv2.destroyAllWindows()


if __name__ == "__main__":
     main()
