import cv2
import numpy as np
from threading import Thread

cap = cv2.VideoCapture(1) # If it doesn't work, try parsing 1 instead 0

EXIT = False
TAKE_PICTURE = False
START_RECORDING = False
STOP_RECORDING = False
command = ''

def help_screen():
    print("\n### HELP ###")
    print(">> startrec - Start recording")
    print(">> stoprec - Stop recording")
    print(">> takepic - Take picture")
    print(">> exit - Exit the program\n")

def shut_down():
    cap.release()
    cv2.destroyAllWindows()

def take_picture(name, picture):
    cv2.imwrite(name, picture)

def command_line():
    global TAKE_PICTURE, EXIT, START_RECORDING, STOP_RECORDING

    while True:
        command = input("> ")

        if command == 'help':
            help_screen()
        elif command == 'exit': 
            print("Exiting the program...")
            EXIT = True
            shut_down()
        elif command == 'takepic':
            print("Taking picture...")
            TAKE_PICTURE = True
        elif command == 'startrec':
            print("Recording started...")
            START_RECORDING = True
        elif command == 'stoprec':
            print("Recording stopped.")
            STOP_RECORDING = True
            START_RECORDING = False
            

def frame_loading():
    global TAKE_PICTURE, EXIT, START_RECORDING, STOP_RECORDING

    # Command line thread
    command_line_thread = Thread(target=command_line)
    command_line_thread.daemon = True
    command_line_thread.start()

    out = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))  

    # Main loop
    while not EXIT:
        ret, frame = cap.read()  
        cv2.imshow('frame', frame)            

        if TAKE_PICTURE:
            take_picture('slika.png', frame)
            TAKE_PICTURE = False
        elif START_RECORDING:              
            out.write(frame)
        elif STOP_RECORDING:
            print("staloo")
            out.release()
            STOP_RECORDING = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            shut_down()
            break


frame_loading()