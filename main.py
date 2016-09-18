import cv2
import numpy as np
import time
from threading import Thread

cap = cv2.VideoCapture(1) # If it doesn't work, try parsing 1 instead 0

# Program states
EXIT = False
TAKE_PICTURE = False
START_RECORDING = False
STOP_RECORDING = False
GRAY = False
RGB = False

command = ''

def help_screen():
    print("\n### HELP ###")
    print(">> startrec - Start recording")
    print(">> stoprec - Stop recording")
    print(">> takepic - Take picture")
    print(">> gray - Gray mode")
    print(">> quitgray - Exit gray mode")
    print(">> rgb - RGB mode")
    print(">> quitrgb - Exit RGB mode")
    print(">> exit - Exit the program\n")

def shut_down():
    cap.release()
    cv2.destroyAllWindows()

def take_picture(name, picture):
    cv2.imwrite(name, picture)

def command_line():
    global TAKE_PICTURE, EXIT, START_RECORDING, STOP_RECORDING, GRAY, RGB

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
        elif command == 'gray':
            GRAY = True
        elif command == 'quitgray':
            GRAY = False
        elif command == 'rgb':
            RGB = True
        elif command == 'quitrgb':
            RGB = False
            

def frame_loading():
    global TAKE_PICTURE, EXIT, START_RECORDING, STOP_RECORDING, GRAY, RGB

    # Command line thread
    command_line_thread = Thread(target=command_line)
    command_line_thread.daemon = True
    command_line_thread.start()

    out_normal = cv2.VideoWriter('video_normal.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))  
    # If you want you can un-comment 2 lines below to record 3 videos, but it will only record 2 of them
    # and there is possibility that one of them will be shorter, for best performance leave just normal recording
    # Also un-comment out.write and out.release in main loop if you want to record in more than 1 mode
    #out_gray = cv2.VideoWriter('video_gray.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))  
    #out_rgb = cv2.VideoWriter('video_rgb.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))  

    font = cv2.FONT_HERSHEY_COMPLEX

    # Main loop
    while not EXIT:
        ret, frame = cap.read()  
        
        currentTime = time.strftime("%H %M %S")
        cv2.putText(frame, currentTime, (0,40), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Normal mode', frame)  

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        
        if GRAY:
            cv2.imshow('Gray mode', gray)
        elif not GRAY:
            cv2.destroyWindow('Gray mode')

        if RGB:
            cv2.imshow('RGB mode', rgb)
        elif not RGB:
            cv2.destroyWindow('RGB mode')

        if TAKE_PICTURE:
            take_picture('slika_normal.png', frame)
            take_picture('slika_gray.png', gray)
            take_picture('slika_rgb.png', rgb)
            TAKE_PICTURE = False
        elif START_RECORDING:              
            out_normal.write(frame)
            #out_gray.write(gray)
            #out_rgb.write(rgb)
        elif STOP_RECORDING:
            out_normal.release()
            #out_gray.release()
            #out_rgb.release()
            STOP_RECORDING = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            shut_down()
            break

frame_loading()