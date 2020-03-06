#By Zhou Fang & Priyanka Muttaraju
#SEIS 603 - 02
#Final Project
#Due date: May 6, 2019

from tkinter import *
import BeginClass
import Sample2


root = Tk()

root.title("Minesweeper")
root.geometry("600x600")


frame = Frame(root)
frame.pack(side = TOP)
Welcome = Label(frame, text="Welcome to Minesweeper")
Welcome.pack()

def Beginner():

    BeginClass.main()

def Intermediate():

    Sample2.main()

def Advanced():
    print("hello Ad")

button1 = Button(frame, text ="Beginner", fg ="blue", command = Beginner) #Creating buttons for levels
button2 = Button(frame, text ="Intermediate", fg ="blue", command = Intermediate)
button3 = Button(frame, text ="Advanced", fg ='blue', command = Advanced)


button1.pack(fill = X, pady = 50)
button2.pack(fill = X, pady = 50)
button3.pack(fill = X, pady = 50)

root.mainloop()