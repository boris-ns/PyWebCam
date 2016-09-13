import cv2
import numpy as np
from threading import Thread

cap = cv2.VideoCapture(0)
EXIT = False
command = ''

def help_screen():
    print("\n### HELP ###")
    print("> startrec - Start recording")
    print("> stoprec - Stop recording")
    print("> takepic - Take picture")
    print("> exit - Exit the program\n")

def command_line():
    while True:
        command = input("> ")

        if command == 'help':
            help_screen()
        elif command == 'exit': # TODO namesti exit da radi, problem je sto deo promena EXIT ne stigne do frame_loading
            EXIT = True
            print(EXIT)
        elif command == 'takepic': # TODO prosledi nekako frame
            cv2.imwrite('slika.png', frame)

def frame_loading():
    command_line_thread = Thread(target=command_line)
    command_line_thread.daemon = True
    command_line_thread.start()

    while True:
        ret, frame = cap.read()  
        cv2.imshow('frame', frame)            

        if cv2.waitKey(1) & 0xFF == ord('q') or EXIT:
            break


frame_loading()

cap.release()
cv2.destroyAllWindows()