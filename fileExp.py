from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label
from tkinter import messagebox
import os
import signal
import cv2
import subprocess
import threading
import sys


pid = 0


def closeAll():
    if pid != 0:

        # print(pid)

        #_ = os.kill(int(pid), signal.SIGKILL)
        #sys.exit(1)
        #os.system('ps')

        os.system('pkill -9 python')
        # os.system('ps')

        cv2.destroyAllWindows()
        cv2.waitKey(1)
        root.destroy()
    else:
        root.destroy()


class Example(Frame):

    def __init__(self,width,height,master):
        super().__init__(master)
    
        self.initUI()
        self.width = width
        self.height = height

    def use_webcam(self):
        self.fname = '/webcam'
        self.label_file_explorer.configure(text='Folder selected: Using Webcam Input'
                )
        self.button_explore.config(state=tk.DISABLED)
        self.submit_choices['state'] = 'normal'

    def browseFiles(self):
        self.fname = filedialog.askdirectory(initialdir='/',
                title='Select a Folder containing input images')

        flag = 0
        print(self.fname)
        for file in os.listdir(self.fname):
            if file.endswith('.jpg'):
                flag = 1
                break
        if flag == 0:
            messagebox.showerror('Error',
                                 'Selected folder does not contain any jpg images'
                                 )
        else:
            self.label_file_explorer.configure(text='Folder selected: '
                    + self.fname.split("/")[-1])
            self.submit_choices['state'] = 'normal'
            self.use_webcam['state'] = tk.DISABLED

    def getchoices(self):
        # inp = self.input.get()
        # seg = self.seg.get()
        # depth = self.depth.get()
        # SFD = self.SFD.get()
        # ASFDS = self.ASFDS.get()
        out = self.out.get()
        obj = self.obj.get()
        cgl = self.cgl.get()
        # summation = inp + seg + depth + out + SFD + ASFDS + obj
        # if summation < 2 or summation > 6:
        #     messagebox.showerror('Error',
        #                          'kindly make sure that the number of outputs selected is between 2 and 6'
        #                          )
        # else:
        global pid
    #         proc = subprocess.Popen('python show_windows.py '
    #                                 + self.fname + ' ' + str(inp) + ' '
    #                                 + str(seg) + ' ' + str(depth) + ' '
    #                                 + str(SFD) + ' ' + str(ASFDS) + ' '
    #                                 + str(out) + ' ' + str(obj) + ' '
				# + str(width) + ' ' + str(height),
                                    # shell=True)
        proc = subprocess.Popen('python show_windows.py '
                                + self.fname.replace(' ','\ ') + ' ' 
                                + str(out) + ' ' + str(obj) + ' ' + str(cgl) + ' '
			+ str(width) + ' ' + str(height),
                                shell=True)
        
        pid = proc.pid

        # messagebox.showerror("Error","Select atleast two checkboxes")

    def initUI(self):
        self.master.title('IMPRINT Demo - Navigation using RGB Camera GUI : VPLAB, Dept. of CS&E, IIT Madras')
        self.master.title('Demo : VPLAB, Dept. of CS&E, IIT Madras')
        self.master.geometry('{}x{}+0+0'.format(width,height))
        self.font_style = "Calibri"
        self.font_size = 13
        # self.master.pack(side="top")

        self.pack(fill=X)

        frame1 = Frame(self, relief='raised')
        frame1.pack(fill=X)

        self.label_file_explorer = Label(frame1,
                text='Selected Folder: -',font=(self.font_style, self.font_size))

        self.label_file_explorer.pack(side=LEFT, padx=5, pady=5)

        self.use_webcam = Button(frame1, text='Use Webcam Input',
                                 command=self.use_webcam,font=(self.font_style, self.font_size))

        self.use_webcam.pack(side=RIGHT, padx=5, pady=5)

        self.button_explore = Button(frame1,
                text='Browse Folders to select Input folder',
                command=self.browseFiles,font=(self.font_style, self.font_size))

        self.button_explore.pack(side=RIGHT, padx=5, pady=5)

        frame2 = Frame(self, relief='raised')
        frame2.pack(fill=X)

        l = Label(frame2, text='Choose what to display:',font=(self.font_style, self.font_size))
        l.pack(side=LEFT, padx=5, pady=5)

        

        # self.input = IntVar()
        # self.input_check = Checkbutton(frame2, text=' Input',
        #         variable=self.input,font=(self.font_style, self.font_size))
        # self.input_check.pack(side=LEFT, padx=10, pady=5)

        # self.seg = IntVar()
        # self.seg_check = Checkbutton(frame2, text=' Segmentation',
        #         variable=self.seg,font=(self.font_style, self.font_size))
        # self.seg_check.pack(side=LEFT, padx=10, pady=5)

        # self.depth = IntVar()
        # self.depth_check = Checkbutton(frame2, text=' Depth Map',
        #         variable=self.depth,font=(self.font_style, self.font_size))
        # self.depth_check.pack(side=LEFT, padx=10, pady=5)

        # self.SFD = IntVar()
        # self.SFD_check = Checkbutton(frame2, text=' SFD',
        #         variable=self.SFD,font=(self.font_style, self.font_size))
        # self.SFD_check.pack(side=LEFT, padx=10, pady=5)

        # self.ASFDS = IntVar()
        # self.ASFDS_check = Checkbutton(frame2, text=' ASFDS',
        #         variable=self.ASFDS,font=(self.font_style, self.font_size))
        # self.ASFDS_check.pack(side=LEFT, padx=10, pady=5)

        self.out = IntVar()
        self.out_check = Checkbutton(frame2, text=' Maximal Freespace Direction',
                variable=self.out,font=(self.font_style, self.font_size))
        self.out_check.pack(side=LEFT, padx=10, pady=5)

        self.obj = IntVar()
        self.obj_check = Checkbutton(frame2, text=' Object Detection',
                variable=self.obj,font=(self.font_style, self.font_size))
        self.obj_check.pack(side=LEFT, padx=10, pady=5)

        self.cgl = IntVar()
        self.cgl_check = Checkbutton(frame2, text=' Covert Geo-Location (CGL) Detection',
                variable=self.cgl,font=(self.font_style, self.font_size))
        self.cgl_check.pack(side=LEFT, padx=10, pady=5)
        self.cgl_check['state'] = tk.DISABLED

        self.submit_choices = Button(frame2, text='Start Demo',
                command=lambda : \
                threading.Thread(target=self.getchoices).start(),
                state=tk.DISABLED,font=(self.font_style, self.font_size))

        self.submit_choices.pack(side=RIGHT, padx=5, pady=5)

        # frame25 = Frame(self, relief='raised')
        # frame25.pack(fill=X)

        self.frame3 = Frame(self, relief='raised')
        self.frame3.pack(fill=BOTH, expand=True)


        # self.lm = tk.Label(master=frame25,
        #                    text="Click on 'start the demo' to get started with the demo"
        #                    )
        # self.lm.pack(pady=10)

root = tk.Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

app = Example(width,height,master=root)

# app.pack(side="top")
# menubar = Menu(root)
# choosefolder = Menu(menubar, tearoff=0)
# choosefolder.add_command(label="Choose Input Folder", command=app.browseFiles)
# menubar.add_cascade(label="Choose Folder", menu=choosefolder)
# root.config(menu=menubar)

root.protocol('WM_DELETE_WINDOW', closeAll)
root.mainloop()

