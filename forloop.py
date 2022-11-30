import random
import tkinter
from tkinter import *
from tkinter import messagebox as mb
from  tkinter import ttk
from PIL import Image, ImageTk
import customtkinter
import requests
import json
import string
import time
from cryptography.fernet import Fernet
import os
import ast
from tkinter.filedialog import askopenfilename,asksaveasfilename


PATH = os.path.dirname(os.path.realpath(__file__))
class Quiz(customtkinter.CTk):
    APP_NAME = "QZZER"
    WIDTH = 900
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taken = 0
        self.upres=0
        #self.retake = False
        self.login_event()
    def clicked(self,event):
        print("Clicked On Frame")
    def date_time(self):
        self.datetim=''
        try:
            url = "https://www.worldtimeapi.org/api/timezone/Asia/Kolkata.txt"
            r = requests.get(url, allow_redirects=True)
            open('datetime.txt', 'wb').write(r.content)
            with open('datetime.txt', 'r') as f:
                x = f.readlines()[2]
                date = x[-33:][:-23]
                time = x[-22:][:-14]
            self.datetim = date + " " + time
        except requests.exceptions.ConnectionError as te:
            print("Can't Connect to time server")
        #dateti = datetime.strptime(datetim, '%y/%m/%d %H:%M:%S')
    def login_event(self):
        self.title(Quiz.APP_NAME)
        ico=Image.open(PATH + "/assets/ico.png")
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)
        self.geometry(f"{Quiz.WIDTH}x{Quiz.HEIGHT}")
        self.minsize(Quiz.WIDTH-200, Quiz.HEIGHT)
        #self.maxsize(Quiz.WIDTH+200, Quiz.HEIGHT)
        # self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.ltype=0
        self.frame = customtkinter.CTkFrame(master=self,
                                            width=Quiz.WIDTH - 100,
                                            height=Quiz.HEIGHT - 100,
                                            corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.label_1 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                              text="LOGIN", text_font=("Sketchzone", 20, "bold"), corner_radius=7)
        self.label_1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.entry_1 = customtkinter.CTkEntry(master=self.frame, corner_radius=1, width=200,text_font=("Cabin Sketch",10),
                                              placeholder_text="username")
        self.entry_1.place(relx=0.5, rely=0.42, anchor=tkinter.CENTER)
        self.entry_2 = customtkinter.CTkEntry(master=self.frame, corner_radius=1, width=200, show="*",text_font=("Cabin Sketch",10),
                                              placeholder_text="password")
        self.entry_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.button_2 = customtkinter.CTkButton(master=self.frame, text="Login", text_font=("Cabin Sketch", 10),
                                                corner_radius=1,command=lambda:self.login_db(),width=200, height=47)
        self.button_2.place(relx=0.5, rely=0.62, anchor=tkinter.CENTER)

        self.button_3 = customtkinter.CTkButton(master=self.frame, text="Sign Up",text_font=("Cabin Sketch",10),
                                                corner_radius=1, command=lambda:self.signup_open(), width=200,
                                                fg_color="#7FFFD4", text_color="#023020", hover_color="#50C878")
        self.button_3.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        try:
            self.taken=0
            with open("login",'r') as f:
                self.login_db()
                us = f.readlines()[0].strip()
                f.seek(0)
                ps = f.readlines()[1]
                self.entry_1.insert(0, us)
                self.entry_2.insert(0, ps)
                if self.ltype==1:
                    if us == str(self.entry_1.get()) and ps == str(self.entry_2.get()):
                            self.strt_scrn()
                else:
                    #self.entry_1.insert(0, us)
                    #self.entry_2.insert(0, ps)
                    self.login_db()
        except OSError as e:
            print("No Login File found")


        #one_lambda=lambda x : ""
        #self.entry_2.bind("<Return>", one_lambda(self) : self.login_db(self))
        #print("Login pressed - username:", self.entry_1.get(), "password:", self.entry_2.get())

    def login_db(self):
        try:
            number = 0
            self.username=self.entry_1.get()
            url = "https://qzzer-12e5.restdb.io/rest/login-details"

            headers = {
                'content-type': "application/json",
                'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers).text
            p_json=json.loads(response)
            for i in range(len(p_json)):
                if str(p_json[i]['username'])==str(self.entry_1.get()) and str(p_json[i]['password'])==str(self.entry_2.get()):
                    file=open("login",'w')
                    file.write(str(self.entry_1.get())+"\n")
                    file.write(str(self.entry_2.get()))
                    self.strt_scrn()
                    number = 1
                    break
            if number==0:
                self.label_Cau2 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                        text="Cannot Login, Try again with proper Credentials", text_color='#FFFF00',
                                                        text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
                self.label_Cau2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
                self.frame.after(1000, self.entry_1.delete(0, 'end'))
                self.frame.after(1000, self.entry_2.delete(0, 'end'))
                self.frame.after(4000, self.label_Cau2.destroy)
                #mb.showinfo("Invalid Login","Sign Up or try again")
                #print("invalid login")
            #if response[0]==self.entry_2.get():
            #    print(response[0])
            #dict=response.json()
            #print(dict)
        except requests.exceptions.ConnectionError as le:
            self.label_Cau2 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                     text="No Internet Connection",
                                                     text_color='#FFFF00',
                                                     text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
            self.label_Cau2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
            self.frame.after(4000, self.label_Cau2.destroy)
            self.ltype=1


    def signup_open(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
            self.label_2 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                  text="SIGN UP", text_font=("Sketchzone", 20, "bold"), corner_radius=7)
            self.label_2.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            self.entry_1u = customtkinter.CTkEntry(master=self.frame, corner_radius=1, width=200,text_font=("Cabin Sketch",10),
                                                  placeholder_text="username")
            self.entry_1u.place(relx=0.5, rely=0.32, anchor=tkinter.CENTER)

            self.entry_2u = customtkinter.CTkEntry(master=self.frame, corner_radius=1, width=200, show="*",text_font=("Cabin Sketch",10),
                                                  placeholder_text="password")
            self.entry_2u.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

            self.entry_3 = customtkinter.CTkEntry(master=self.frame, corner_radius=1, width=200,text_font=("Cabin Sketch",10),
                                                  placeholder_text="First Name")
            self.entry_3.place(relx=0.5, rely=0.48, anchor=tkinter.CENTER)
            self.entry_4 = customtkinter.CTkEntry(master=self.frame, corner_radius=1, width=200,text_font=("Cabin Sketch",10),
                                                  placeholder_text="Last Name")
            self.entry_4.place(relx=0.5, rely=0.56, anchor=tkinter.CENTER)

            self.button_2u= customtkinter.CTkButton(master=self.frame, text="Back",text_font=("Cabin Sketch",10),
                                                    corner_radius=1, command=self.login_event, width=200)
            self.button_2u.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
            self.button_3u = customtkinter.CTkButton(master=self.frame, text="Sign Up",text_font=("Cabin Sketch",10),
                                                    corner_radius=1, command=self.signup_db, width=200,height=47,
                                                    fg_color="#7FFFD4", text_color="#023020", hover_color="#50C878")
            self.button_3u.place(relx=0.5, rely=0.68, anchor=tkinter.CENTER)
        #print("Login pressed - username:", self.entry_1.get(), "password:", self.entry_2.get())

    def signup_db(self):
        try:
            url = "https://qzzer-12e5.restdb.io/rest/login-details"

            payload = json.dumps({"username": self.entry_1u.get(), "password": self.entry_2u.get(), "lname":self.entry_4.get(), "fname":self.entry_3.get()})
            headers = {
                'content-type': "application/json",
                'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                'cache-control': "no-cache"
            }

            response = requests.request("POST", url, data=payload, headers=headers)
            res=json.loads(response.text)
            print(res)
            re=""
            try:
                re=res['list'][0]['message'][0]
                print(re)
            except KeyError as ke:
                print("Signed Up Successfully")
                self.label_Cau = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                        text="Successfully Signed Up", text_color='#FFFF00',
                                                        text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
                self.label_Cau.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
                self.frame.after(1000,self.entry_1u.delete(0,'end'))
                self.frame.after(1000, self.entry_2u.delete(0,'end'))
                self.frame.after(1000, self.entry_3.delete(0,'end'))
                self.frame.after(1000, self.entry_4.delete(0,'end'))
                self.frame.after(4000, self.label_Cau.destroy)

            if(str(re)=="Already exists"):
                print("Username already taken")
                self.label_Cau = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                      text="Username Already Taken,Try another one",text_color='#FFFF00', text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
                self.label_Cau.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
                self.frame.after(1000, self.entry_1u.delete(0,'end'))
                self.frame.after(4000,self.label_Cau.destroy)
            if (str(re) == "Missing required field"):
                print("All Fields are mandatory")
                self.label_Cau1 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                        text="All Fields are mandatory", text_color='#FFFF00',
                                                        text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
                self.label_Cau1.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
                self.frame.after(4000, self.label_Cau1.destroy)
            #sp_json=json.loads(response)
        except requests.exceptions.ConnectionError as se:
            print("No Connetion, Can't sign up")
            self.label_Cau = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                    text="Can't Sign Up\nNo Internet Connection", text_color='#FFFF00',
                                                    text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
            self.label_Cau.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
            self.frame.after(1000, self.entry_1u.delete(0, 'end'))
            self.frame.after(1000, self.entry_2u.delete(0, 'end'))
            self.frame.after(1000, self.entry_3.delete(0, 'end'))
            self.frame.after(1000, self.entry_4.delete(0, 'end'))
            self.frame.after(4000, self.label_Cau.destroy)


    def strt_scrn(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        try:
            with open("pres.json", "r") as resf:
                res = resf.readline()
                dic = json.loads(res)
                self.username = dic["username"]
                self.correct = dic["score"]
                self.datetim = dic["datetime"]
                self.musername = dic["musername"]
                self.quizid = dic["quiz-id"]
                self.qlen = dic["qlen"]
                self.timetaken = dic["time-taken"]
                if dic["retake"] == 1:
                    self.retake = True
                else:
                    self.retake = False
                self.upresult()
                self.username = ""
                self.correct = 0
                self.datetim = ""
                self.musername = ''
                self.quizid = ''
                self.qlen = 0
        except OSError as pre:
            pass
        try:
            os.remove("pres.json")
        except OSError as pred:
            pass
        #self.retake = False
        image_size=200
        self.frame=customtkinter.CTkFrame(master=self, width=Quiz.WIDTH+200,
                                           height=Quiz.HEIGHT,
                                            corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.label_1 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                              text="QZZER", text_font=("Sketchzone", 40, "bold"), corner_radius=7)
        self.label_1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        self.label_srn = customtkinter.CTkLabel(master=self.frame, width=50, height=60,
                                              text=f"Logged in as\n{self.username}", text_font=("Cabin Sketch", 8, "roman"), corner_radius=7)
        self.label_srn.place(relx=0.8, rely=0.1, anchor=tkinter.CENTER)
        self.label_srn.after(5000,self.label_srn.destroy)
        mkQ_image = ImageTk.PhotoImage(
            Image.open(PATH + "/assets/mkQ.png").resize((image_size, image_size)))
        tkQ_image = ImageTk.PhotoImage(
            Image.open(PATH + "/assets/tkQ.png").resize((image_size, image_size)))
        r_image = ImageTk.PhotoImage(
            Image.open(PATH + "/assets/rimg.png").resize((image_size, image_size)))
        lo_image = ImageTk.PhotoImage(
            Image.open(PATH + "/assets/logO.png").resize((40, 40)))
        self.mk_button = customtkinter.CTkButton(master=self.frame, image=mkQ_image, text="Make Quiz",
                                                 text_font=("Cabin Sketch", 17, "bold"), width=400, height=70,
                                                 corner_radius=3, fg_color="gray40", hover_color="gray12",
                                                 command=lambda:self.mkQuiz())
        self.mk_button.place(relx=0.3, rely=0.36, anchor=tkinter.CENTER)
        self.tk_button = customtkinter.CTkButton(master=self.frame, image=tkQ_image, text="Take Quiz",
                                                 text_font=("Cabin Sketch", 17, "bold"), width=400, height=70,
                                                 corner_radius=3, fg_color="gray40", hover_color="gray12",
                                                 command=lambda: self.tkQuiz())
        self.tk_button.place(relx=0.7, rely=0.36, anchor=tkinter.CENTER)
        self.r_button = customtkinter.CTkButton(master=self.frame, image=r_image, text="Analyze Result",
                                                 text_font=("Cabin Sketch", 17, "bold"), width=400, height=70,
                                                 corner_radius=3, fg_color="gray40", hover_color="gray12",
                                                 command=lambda: self.anRes())
        self.r_button.place(relx=0.5, rely=0.77, anchor=tkinter.CENTER)
        self.lo_button = customtkinter.CTkButton(master=self.frame, image=lo_image, text="",
                                                text_font=("Helvetica", 17, "bold"), width=50, height=50,
                                                corner_radius=3, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.logut())
        self.lo_button.place(relx=0.87, rely=0.1, anchor=tkinter.CENTER)
        if self.taken!=0:
            self.upresult()
            self.taken=0
    def logut(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        os.remove("login")
        self.login_event()

    def mkQuiz(self):
        self.qfno=0
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        self.frame = customtkinter.CTkFrame(master=self, width=Quiz.WIDTH + 200,
                                            height=Quiz.HEIGHT,
                                            corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.label_1 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                              text="Make Quiz", text_font=("Sketchzone", 40, "bold"), corner_radius=7)
        self.label_1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        image_size=100
        open_img=ImageTk.PhotoImage(Image.open(PATH + "/assets/openf.png").resize((image_size,image_size)))
        back_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/bimg.png").resize((40, 40)))
        #reta_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/retake.png").resize((40, 40)))
        self.o_button = customtkinter.CTkButton(master=self.frame, image=open_img, text="Choose Text File\nand Generate Quiz File",
                                                 text_font=("Cabin Sketch", 17, "bold"), width=400, height=50,
                                                 corner_radius=3, fg_color="gray40", hover_color="gray12",
                                                 command=lambda: self.mkQuizf())
        self.o_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        #self.ret_button = customtkinter.CTkButton(master=self.frame, image=reta_img,
         #                                       text="Retake\nOption",
          #                                      text_font=("Cabin Sketch", 13, "bold"), width=40, height=40,
           #                                     corner_radius=3, fg_color="gray40", hover_color="gray12",
            #                                    command=lambda: self.ret_but())
        #self.ret_button.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)
        self.b_button = customtkinter.CTkButton(master=self.frame, image=back_img, text="",
                                                text_font=("Helvetica", 17, "bold"), width=50, height=50,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.strt_scrn())
        self.b_button.place(relx=0.87, rely=0.1, anchor=tkinter.CENTER)

    def ret_but(self):
        self.dialog = customtkinter.CTkInputDialog(master=None, text="Type \'y\'\nto Specify that the Quiz\ncan be retaken multiple times:\n\nType any other key to specify \nthat the quiz is not retakable\n\nGenerated Quizzes are not retakable by default", title="Is the Quiz retakable")
        self.ret_set()
        #print(type(dialog.get_input()))
    def ret_set(self):
        r = self.dialog.get_input().strip()
        print(r)
        if r == 'y' or r == 'Y':
            self.retake = True
        else:
            self.retake = False
        print(self.retake)
        #self.ret_button.destroy()
    def qidf(self):
        n=7
        self.qid=''.join(random.choices(string.ascii_uppercase + string.digits,k=n))
    def mkQuizf(self):
        # resultant dictionary
        #reta_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/retake.png").resize((40, 40)))
        #if self.qfno!=0:
         #   self.ret_button = customtkinter.CTkButton(master=self.frame, image=reta_img,
          #                                            text="Retake\nOption",
           #                                           text_font=("Cabin Sketch", 13, "bold"), width=40, height=40,
            #                                          corner_radius=3, fg_color="gray40", hover_color="gray12",
             #                                         command=lambda: self.ret_but())
            #self.ret_button.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)
        filename = askopenfilename()
        #print(filename[-4:])
        if filename[-4:] != '.txt':
            self.label_fnw = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                    text="You have to choose a \'.txt\' file ", text_color='#FFFF00',
                                                    text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
            self.label_fnw.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            self.frame.after(4000,self.label_fnw.destroy)
            return
        self.ret_but()
        if self.retake:
            reta=1
        else:
            reta=0
        print(reta)
        c = 0
        self.qidf()
        qd = [self.qid,self.username,reta]
        dictq = []
        dicto = []
        answer = []
        with open(filename) as fh:
            for line in fh:
                sno = ["qd","questions", "options", "answers"]
                desc = line.strip()
                if not desc.startswith(".") and c != 0:
                    if c1 == 1:
                        c1 = 2
                        dictq.append(desc)
                    elif c1 >= 2:
                        while c1 == 2:
                            answer.append(desc)
                            break
                        dico.append(desc)
                        c1 += 1
                else:
                    c += 1
                    c1 = 1
                    if c > 1:
                        dicto.append(dico)
                    dico = []
                    continue
            dict2 = dict(zip(sno, [qd,dictq, dicto, answer]))
        qstr = json.dumps(dict2, indent=1)
        print(qstr)
        self.encrpt(qstr)
        self.qfno=1

    def encrpt(self,qstr):
        key = b'CjqCzW0CZfmaMYuizKRmizo4GMkx3ane4dnnpiEo4eE='
        data = qstr
        fernet = Fernet(key)
        encrypted = fernet.encrypt(bytes(data, 'utf-8'))
        filename=asksaveasfilename()
        if filename=='':
            return
        with open(f"{filename}.qzr", 'wb') as f:
            f.write(encrypted)
        self.label_qidt = customtkinter.CTkLabel(master=self.frame, width=200, height=30,
                                                 text="The Quiz ID is", text_color='#FF0000',
                                                 text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
        self.label_qid = customtkinter.CTkLabel(master=self.frame, width=200, height=30,
                                                text=f"{self.qid}", text_color='#FFFF00',
                                                text_font=("Helvetica", 12, "bold"), corner_radius=7)
        self.label_qid.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
        self.label_qidt.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        return

    def tkQuiz(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        open_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/opent.png").resize((100, 100)))
        back_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/bimg.png").resize((40, 40)))
        self.frame = customtkinter.CTkFrame(master=self, width=Quiz.WIDTH + 200,
                                            height=Quiz.HEIGHT,
                                            corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.label_1 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                              text="Take Quiz", text_font=("Sketchzone", 40, "bold"), corner_radius=7)
        self.label_1.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        self.b_button = customtkinter.CTkButton(master=self.frame, image=back_img, text="",
                                                text_font=("Helvetica", 17, "bold"), width=50, height=50,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.strt_scrn())
        self.b_button.place(relx=0.87, rely=0.1, anchor=tkinter.CENTER)
        self.o_button = customtkinter.CTkButton(master=self.frame, image=open_img,
                                                text="Choose the Quiz File\nand Generate Quiz",
                                                text_font=("Cabin Sketch", 17, "bold"), width=400, height=50,
                                                corner_radius=3, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.tkQuizf())
        self.o_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    def tkQuizf(self):
        decrypted = self.decrpt()
        if decrypted == None:
            return
        dec = ast.literal_eval(decrypted.decode('utf-8'))
        questions=dec['questions']
        options=dec['options']
        answers=dec['answers']
        qidls=dec['qd']
        retak= dec['qd']
        if retak[2]==1:
            self.retake=True
        print(self.retake)
        self.musername=qidls[1]
        self.quizid=qidls[0]
        try:
            url = "https://qzzer-12e5.restdb.io/rest/results"

            headers = {
                'content-type': "application/json",
                'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers).text
            p_json = json.loads(response)
            print(response)
            for i in range(len(p_json)):
                if str(p_json[i]['quiz-id']) == self.quizid and str(p_json[i]['username']) == self.username:
                    print(p_json[i]["retake"])
                    if p_json[i]["retake"] == 0:
                        mb.showinfo("Already Attended",
                                    "You have already attended this Quiz\nContact The Quiz Master to attend it again")
                        return
                    else:
                        print("y")
                        url = f'https://qzzer-12e5.restdb.io/rest/results/{p_json[i]["_id"]}'

                        headers = {
                            'content-type': "application/json",
                            'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                            'cache-control': "no-cache"
                        }

                        response = requests.request("DELETE", url, headers=headers)

                        print(response.text)


        except requests.exceptions.ConnectionError as che:
            print("Can't Connect")

        self.qintrf(questions,options,answers)
        self.qlen=len(questions)
        #for value in decrypted

    def onlyAddR(self):
        url = "https://qzzer-12e5.restdb.io/rest/results"
        if self.retake == True:
            reta = 1
        else:
            reta = 0

        payload = json.dumps(
            {"username": self.username, "score": self.correct, "datetime": self.datetim,
             "musername": self.musername, "quiz-id": self.quizid, "time-taken": self.endT - self.startT,
             "retake": reta})
        headers = {
            'content-type': "application/json",
            'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)

    def qintrf(self,questions, options, answers):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        next_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/next.png").resize((100, 100)))
        back_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/bimg.png").resize((40, 40)))
        self.frame = customtkinter.CTkFrame(master=self, width=Quiz.WIDTH + 200,
                                            height=Quiz.HEIGHT,
                                            corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.correct=0
        self.ci =-1
        self.radVar = tkinter.StringVar()
        self.radVar.set("")
        c = 0
        for i in options:
            random.shuffle(options[c])
            c += 1
        self.n_button = customtkinter.CTkButton(master=self.frame, image=next_img, text="Take Quiz",
                                                text_font=("Cabin Sketch", 17, "bold"), width=50, height=50,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.dandC(questions,options,answers))
        self.n_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.b_button = customtkinter.CTkButton(master=self.frame, image=back_img, text="",
                                                text_font=("Helvetica", 17, "bold"), width=50, height=50,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.strt_scrn())
        self.b_button.place(relx=0.87, rely=0.1, anchor=tkinter.CENTER)

    def disp_Q(self,questions,options,answers):
        if self.ci==0:
            self.startT=time.time()
            self.date_time()
            print(self.startT)
        next_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/next.png").resize((50, 50)))
        back_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/bimg.png").resize((40, 40)))
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        if self.ci != len(questions):
            self.label_1 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                  text=questions[self.ci], text_font=("Cabin Sketch", 40, "bold"),
                                                  corner_radius=7)
            self.label_1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            self.aframe=customtkinter.CTkFrame(master=self.frame, width=Quiz.WIDTH-10,height=Quiz.HEIGHT-300,
                                               fg_color="#808080",corner_radius=2,border_width=2,border_color="#abab97")
            self.aframe.place(relx=.5004,rely=.6,anchor=tkinter.CENTER)
            ypos = 0.3
            inv = 0
            for aitem in options[self.ci]:
                customtkinter.CTkRadioButton(master=self.aframe,text_font=("Cabin Sketch",14,"bold"),text_color="#000000", text=options[self.ci][inv], variable=self.radVar,corner_radius=4,
                                             border_color="#ffffff",bg_color="#808080",value=options[self.ci][inv]).place(relx=0.3, rely=ypos, anchor="w")
                #print(type(self.radVar))
                ypos += 0.107
                inv += 1
            self.n_button = customtkinter.CTkButton(master=self.frame, image=next_img, text="Next",
                                                    text_font=("Cabin Sketch", 17, "bold"), width=50, height=50,
                                                    corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                    command=lambda: self.dandC(questions,options,answers))
            self.n_button.place(relx=0.5, rely=0.94, anchor=tkinter.CENTER)
            self.b_button = customtkinter.CTkButton(master=self.frame, image=back_img, text="",
                                                    text_font=("Helvetica", 17, "bold"), width=50, height=50,
                                                    corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                    command=lambda: self.afQesc())
            self.b_button.place(relx=0.87, rely=0.1, anchor=tkinter.CENTER)
            self.taken = 1
        else:
            self.endT=time.time()
            print(self.endT)
            print(self.endT-self.startT)
            self.timetaken=self.endT - self.startT
            self.strt_scrn()
            return
        #print(len(questions)+1)
        print(self.ci)
        #print(self.radVar.get())
        return
    def afQesc(self):
        self.endT = time.time()
        print(self.endT)
        print(self.endT - self.startT)
        self.timetaken = self.endT - self.startT
        self.strt_scrn()
    def dandC(self,questions,options,answers):
        self.checkC(answers)
        self.disp_Q(questions, options, answers)
    def checkC(self,answers):
        if self.ci!=-1:
            if (self.radVar.get() == answers[self.ci]):
                self.correct+=1
            else:
                #print(answers[self.ci])
                print("Not Correct")
            self.ci += 1
        else:
            self.ci+=1
            return
    def upresult(self):
        try:
            url = "https://qzzer-12e5.restdb.io/rest/results"

            headers = {
                'content-type': "application/json",
                'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers).text
            p_json = json.loads(response)
            print(response)
            for i in range(len(p_json)):
                if str(p_json[i]['quiz-id']) == self.quizid and str(p_json[i]['username']) == self.username:
                    if p_json[i]["retake"] == 0:
                        mb.showinfo("Already Attended",
                                    "You have already attended this Quiz\nContact The Quiz Master to attend it again")
                        return
                    else:
                        pass


        except requests.exceptions.ConnectionError as che:
            print("Can't Connect")

        mb.showinfo("RESULTS",f"You got {self.correct} answers right out of the total {self.qlen} questions")
        #print("invalid login")

        try:
            url = "https://qzzer-12e5.restdb.io/rest/results"
            if self.retake==True:
                reta=1
            else:
                reta=0
            print(self.username)
            payload = json.dumps({"username": self.username, "score": self.correct, "datetime": self.datetim,"musername":self.musername,"quiz-id":self.quizid,"time-taken":self.timetaken,"retake":reta})
            headers = {
                'content-type': "application/json",
                'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                'cache-control': "no-cache"
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            print(response.text)
        except requests.exceptions.ConnectionError as ce:
            #print(ce.response.text)
            try:
                file=open("pres.json","r")
            except OSError as oe:
                file=open("pres.json","w")
                print(self.retake)
                self.timetaken=self.endT-self.startT
                if self.retake==False:
                    pass
                dic={"username": self.username, "score": self.correct, "datetime": self.date_time(),"musername":self.musername,"quiz-id":self.quizid,"qlen":self.qlen,"time-taken":self.timetaken,"retake":self.retake }
                json.dump(dic,file)

    def decrpt(self):
        key = b'CjqCzW0CZfmaMYuizKRmizo4GMkx3ane4dnnpiEo4eE='
        filename = askopenfilename()
        if filename[-3:]!='qzr':
            self.label_tfw = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                    text="You have to choose a \'.qzr\' file ", text_color='#FFFF00',
                                                    text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
            self.label_tfw.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            self.label_tfw.after(4000, self.label_tfw.destroy)
            return
        with open(filename,'rb') as f:
            encrypted=f.read()
        fernet = Fernet(key)
        decrypted=fernet.decrypt(encrypted)
        return decrypted
        #with open('Equiz.json','wb') as qf:
        #    qf.write(decrypted)
    def anRes(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        self.bact=0
        back_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/bimg.png").resize((40, 40)))
        next_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/next.png").resize((50, 50)))
        self.b_button = customtkinter.CTkButton(master=self.frame, image=back_img, text="",
                                                text_font=("Helvetica", 17, "bold"), width=50, height=50,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.strt_scrn())
        self.b_button.place(relx=0.87, rely=0.1, anchor=tkinter.CENTER)
        self.label_anr = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                              text="Analyze Result", text_font=("Sketchzone", 40, "roman"), corner_radius=7)
        self.label_anr.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.entry_qid = customtkinter.CTkEntry(master=self.frame, corner_radius=1, width=215,
                                              text_font=("Cabin Sketch", 20),
                                              placeholder_text="Enter the Quiz ID")
        self.entry_qid.place(relx=0.5, rely=0.42, anchor=tkinter.CENTER)
        self.n_button = customtkinter.CTkButton(master=self.frame, image=next_img, text="",
                                                text_font=("Cabin Sketch", 17, "bold"), width=120, height=50,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",command=lambda:self.idC())
        self.n_button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)


    def idC(self):
        try:
            self.quizid = self.entry_qid.get()
            url = "https://qzzer-12e5.restdb.io/rest/results"

            headers = {
                'content-type': "application/json",
                'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers).text
            p_json = json.loads(response)
            print(response)
            ii = 0
            for i in range(len(p_json)):
                if str(p_json[i]['quiz-id']) == self.quizid and str(p_json[i]['musername']) == self.username:
                    self.bact = self.res(p_json)
                    self.resulto(p_json)
                    return
                else:
                    if str(p_json[i]['quiz-id']) == self.quizid:
                        ii=1
            if ii==0:
                self.label_Caut = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                         text="This Quiz has no attendees",
                                                         text_color='#FFFF00',
                                                         text_font=("Cabin Sketch", 10, "bold"),
                                                         corner_radius=7)
                self.label_Caut.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
                self.frame.after(4000, self.label_Caut.destroy)
            else:
                print("Not the Master")
                self.label_Caut = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                         text="You are not the Quiz master for this Quiz",
                                                         text_color='#FFFF00',
                                                         text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
                self.label_Caut.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
                self.frame.after(4000, self.label_Caut.destroy)


        except requests.exceptions.ConnectionError as are:
            print("Can't Connect")
            self.label_Cau2 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                     text="No Internet Connection",
                                                     text_color='#FFFF00',
                                                     text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
            self.label_Cau2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
            self.frame.after(4000, self.label_Cau2.destroy)


    def resulto(self,p_json):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        self.frame = customtkinter.CTkFrame(master=self, width=Quiz.WIDTH + 200,
                                            height=Quiz.HEIGHT,
                                            corner_radius=0)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        back_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/bimg.png").resize((40, 40)))
        v_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/view.png").resize((50, 50)))
        self.b_button = customtkinter.CTkButton(master=self.frame, image=back_img, text="",
                                                text_font=("Helvetica", 17, "bold"), width=50, height=50,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.anRes())
        self.b_button.place(relx=0.87, rely=0.1, anchor=tkinter.CENTER)
        self.label_anri = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                text="Analyze Result", text_font=("Sketchzone", 40, "roman"),
                                                corner_radius=7)
        self.label_anri.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
        if self.bact==1:
            self.v_button = customtkinter.CTkButton(master=self.frame, image=v_img, text="View All\nScores",
                                                    text_font=("Cabin Sketch", 17, "bold"), width=50, height=50,
                                                    corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                    command=lambda: self.resView(p_json))
            self.v_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        '''else:
            self.label_Cau2 = customtkinter.CTkLabel(master=self.frame, width=400, height=60,
                                                     text="No Internet Connection",
                                                     text_color='#FFFF00',
                                                     text_font=("Cabin Sketch", 10, "bold"), corner_radius=7)
            self.label_Cau2.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
            self.frame.after(4000, self.label_Cau2.destroy)
            self.ltype = 1'''

    def res(self,p_json):
        try:
            url = "https://qzzer-12e5.restdb.io/rest/login-details"

            headers = {
                'content-type': "application/json",
                'x-apikey': "bfa1088aaa5530a2628324f31064aa3d06a4f",
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers).text
            p_jsonl = json.loads(response)
            usernames=[]
            usernamesl=[]
            self.fnames=[]
            self.lnames=[]
            self.scor=[]
            self.tt=[]
            for i in p_json:
                if i['quiz-id']==self.quizid:
                    usernames.append(i['username'])
                    self.scor.append(i['score'])
                    self.tt.append(i['time-taken'])

            print(usernames)
            for i in p_jsonl:
                usernamesl.append(i['username'])
            print(usernamesl)
            for ni in range(len(usernames)):
                for ni2 in range(len(usernamesl)):
                    if usernamesl[ni2] == usernames[ni]:
                        self.fnames.append(p_jsonl[ni2]['fname'])
                        self.lnames.append(p_jsonl[ni2]['lname'])
            return 1
        except requests.exceptions.ConnectionError as le:
            return 0

    def resView(self,p_json):
        for widgets in self.frame.winfo_children():
            widgets.destroy()
        back_img = ImageTk.PhotoImage(Image.open(PATH + "/assets/bimg.png").resize((30, 30)))
        columns = ('first_name', 'last_name', 'score', 'time_taken')
        tree = ttk.Treeview(self.frame, columns=columns, show='headings',height=24)
        style=ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="#585858",foreground="#FFFFFF",rowheight=20,fieldbackground="#808080")
        style.map("Treeview",background=[('selected','#888888')])
        tree.heading('first_name', text='First Name')
        tree.heading('last_name', text='Last Name')
        tree.heading('score', text='Score')
        tree.heading('time_taken', text='Time taken')
        tree.grid(row=1, column=0,sticky=tkinter.NSEW)
        tree_scrolly = customtkinter.CTkScrollbar(self.frame, command=tree.yview)
        tree_scrolly.grid(row=1, column=1, sticky="ns")
        tree_scrollx = customtkinter.CTkScrollbar(self.frame,height=15, command=tree.xview)
        tree_scrollx.grid(row=2, column=0, sticky="ew")
        for i in range(len(self.fnames)):
            tree.insert(parent='', index='end', iid=i, text='',
                           values=(self.fnames[i], self.lnames[i],self.scor[i],self.tt[i]))
        self.ba_button = customtkinter.CTkButton(master=self, image=back_img, text="",
                                                text_font=("Helvetica", 17, "bold"), width=40, height=30,
                                                corner_radius=4, fg_color="gray40", hover_color="gray12",
                                                command=lambda: self.fback(p_json))
        self.ba_button.place(relx=0.87, rely=0.04, anchor=tkinter.CENTER)

    '''def sortScr(self,p_json):
        self.scor'''

    def fback(self,p_json):
        self.ba_button.destroy()
        self.resulto(p_json)
    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = Quiz()
    app.start()