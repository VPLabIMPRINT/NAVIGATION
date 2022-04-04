from tkinter.ttk import *
import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
import numpy as np

global width,height 
global lf                                      #creating global              variable
global cap1,cap2,cap3,cap4,cap5,cap6
global interval 

width = 533
height = 300
interval = 30
cap1 = cv2.VideoCapture("20201210_101221.mp4")
cap2 = cv2.VideoCapture("20201207_225737.mp4")
cap3 = cv2.VideoCapture("20201207_225737.mp4")
cap4 = cv2.VideoCapture("20201210_101221.mp4")
cap5 = cv2.VideoCapture("20201207_225737.mp4")
cap6 = cv2.VideoCapture("20201210_101221.mp4")

def extract_frame(cap):
    if not cap.isOpened():                             #checks for the opening of camera
        print("cant open the camera")
    flag, frame = cap.read()
    frame = cv2.resize(frame,(width, height))
    if flag is None:
        print("Major error!")
    elif flag:
        global last_frame
        last_frame = frame.copy()
    return last_frame


def show_vid1():  
    lf = extract_frame(cap1)
    pic = cv2.cvtColor(lf, cv2.COLOR_BGR2RGB)     #we can change the display color of the frame gray,black&white here
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain1.imgtk = imgtk
    lmain1.configure(image=imgtk)
    lmain1.after(interval, show_vid1)

def show_vid2():
    lf = extract_frame(cap2)
    pic = cv2.cvtColor(lf, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain2.imgtk = imgtk
    lmain2.configure(image=imgtk)
    lmain2.after(interval, show_vid2)

def show_vid3():
    lf = extract_frame(cap3)
    pic2 = cv2.cvtColor(lf, cv2.COLOR_BGR2RGB)
    img2 = Image.fromarray(pic2)
    img2tk = ImageTk.PhotoImage(image=img2)
    lmain3.img2tk = img2tk
    lmain3.configure(image=img2tk)
    lmain3.after(interval, show_vid3)

def show_vid4():
    lf = extract_frame(cap4)
    pic2 = cv2.cvtColor(lf, cv2.COLOR_BGR2RGB)
    img2 = Image.fromarray(pic2)
    img2tk = ImageTk.PhotoImage(image=img2)
    lmain4.img2tk = img2tk
    lmain4.configure(image=img2tk)
    lmain4.after(interval, show_vid4)

def show_vid5():
    lf = extract_frame(cap5)
    pic2 = cv2.cvtColor(lf, cv2.COLOR_BGR2RGB)
    img2 = Image.fromarray(pic2)
    img2tk = ImageTk.PhotoImage(image=img2)
    lmain5.img2tk = img2tk
    lmain5.configure(image=img2tk,text="Segmentation Output",compound="bottom",font=('Calibri',15))
    lmain5.after(interval, show_vid5)

def show_vid6():
    lf = extract_frame(cap6)
    pic2 = cv2.cvtColor(lf, cv2.COLOR_BGR2RGB)
    img2 = Image.fromarray(pic2)
    img2tk = ImageTk.PhotoImage(image=img2)
    lmain6.img2tk = img2tk
    lmain6.configure(image=img2tk)
    lmain6.after(interval, show_vid6)

if __name__ == '__main__':
    root=tk.Tk()                           #assigning root variable        for Tkinter as tk
    lmain1 = tk.Label(master=root)
    lmain2 = tk.Label(master=root)
    lmain3 = tk.Label(master=root)
    lmain4 = tk.Label(master=root)
    lmain5 = tk.Label(master=root)
    lmain6 = tk.Label(master=root)

    # in_text = tk.Text("")
    # lmain.Frame= Frame(width=768, height=576)
    # framex.grid(column=3,rowspan=2,padx=5, pady=5)
    lmain1.pack()
    lmain2.pack()
    lmain3.pack()
    lmain4.pack()
    lmain5.pack()
    lmain6.pack()

    lmain1.place(x=0,y=20)
    lmain2.place(x=width,y=20)
    lmain3.place(x=2 * width,y=20)
    lmain4.place(x= 0,y=height + 40)
    lmain5.place(x=width,y=height + 40)
    lmain6.place(x= 2*width,y=height + 40)

    root.title("Navigation GUI")            #you can give any title
    root.geometry("1600x900") #size of window , x-axis, yaxis
    
    show_vid1()
    show_vid2()
    show_vid3()
    show_vid4()
    show_vid5()
    show_vid6()
    
    root.mainloop()                                  #keeps the application in an infinite loop so it works continuosly
    cap1.release()
    cap2.release()
    cap3.release()
    cap4.release()
    cap5.release()
    cap6.release()