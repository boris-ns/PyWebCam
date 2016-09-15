import cv2
import numpy as np
from threading import Thread

cap = cv2.VideoCapture(0) # If it doesn't work, try parsing 1 instead 0
EXIT = False
TAKE_PICTURE = False
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
    global TAKE_PICTURE, EXIT

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

def frame_loading():
    global TAKE_PICTURE, EXIT

    command_line_thread = Thread(target=command_line)
    command_line_thread.daemon = True
    command_line_thread.start()

    while not EXIT:
        ret, frame = cap.read()  
        cv2.imshow('frame', frame)            

        if TAKE_PICTURE:
            take_picture('slika.png', frame)
            TAKE_PICTURE = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            shut_down()
            break


frame_loading()