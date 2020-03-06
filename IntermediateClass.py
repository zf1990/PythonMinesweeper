#By Zhou Fang and Priyanka Muttaraju
#SEIS 603 - 02
#Final Project - Beginner class constructor and methods
#Due date: May 6, 2019

from tkinter import *
from tkinter import messagebox
import random
from tkinter import PhotoImage


class Intermediate:

    def __init__(self, master):

        #Importing Tile Icons
        self.tile_clicked = PhotoImage(file="tile_clicked.gif")
        self.tile_mine = PhotoImage(file="tile_mine.gif")
        self.tile_flag = PhotoImage(file="tile_flag.gif")
        self.tile_wrong = PhotoImage(file="tile_wrong.gif")
        self.tile_plain = PhotoImage(file = "tile_plain.gif")


        # importing number icons
        self.tile_number = [] #Creating a list for item 1-8
        for x in range(0, 8):
            self.tile_number.append(PhotoImage(file="tile_" + str(x+1) + ".gif"))

        #Creating the frame
        statusBar = Frame(master) #Creating a status bar.
        statusBar.pack(side = BOTTOM)

        frame = Frame(master)
        frame.pack(side = TOP)

        #Creating a welcome to beginner
        welcomeLabel = Label(frame, text = "Welcome to Intermediate Minesweeper", fg = "blue")
        welcomeLabel.grid(row = 0, column = 0, columnspan = 16)

        self.totalMine = 40
        self.flags = 0 #Number of flags user put up
        self.correct_flags = 0 #Number of flags user put up correctly
        self.clicked = 0 #Number of tiles revealed that's not a mine
        self.MineLabel = Label(statusBar, text = "Total Mine: " + str(self.totalMine))
        self.MineLabel.pack(side = LEFT)
        self.flagLabel = Label(statusBar, text = "Flagged: " + str(self.flags))
        self.flagLabel.pack(side = RIGHT)


       #Placing mines.  The number x will serve as Tile ID.

        mines = 40
        mineStatus = [] #Python does not have a built-in array function... List can be used instead then
        for x in range(0,216):
            if random.randrange(256) <= 39 and mines>0:
                #Trying to distribute mines roughly evently.  Since there are 10 mines and 81 Tiles, the probability of a random mine would be 10/81 as represented here.
                mineStatus.append(True)
                mines = mines - 1
            else:
                mineStatus.append(False)
        for x in range(216,256): #Placing the rest of mines in the bottom tiles if there are still more mines to place.
            if mines > 0:
                mineStatus.append(True)
                mines=mines-1
            else:
                mineStatus.append(False)


        # create buttons
        self.buttons = dict({}) #Create a dictionary of linked list.
        self.mines = 0

        cordX = 1
        cordY = 0 #Remember that the first row (row 0) is occupied by the welcome to minesweeper label


        for TileID in range(0,256): # 16x16 tiles with buttons
            # 0 = Creating buttons and its properties
            # 1 = Mine Status to check whether this is a mine.  True = Mine, False = Not a mine
            # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged #Creating the status for the buttons in place.
            # 3 = button id #Same thing
            # 4 = [cordX, cordY] coordinates in the grid
            # 5 = nearby mines, 0 by default, calculated after placement in grid

            if (TileID-16) % 16 == 0: #To start a new row.  The entire size would be 9x9
                cordY = cordY + 1
                cordX = 0

            self.buttons[TileID] = [Button(frame, image = self.tile_plain), mineStatus[TileID], 0, TileID, [cordX, cordY], 0] #Positive x and y direction going right and down respectively from top left corner
            self.buttons[TileID][0].bind('<Button-1>', self.left_click_dummy(TileID)) #Left Click action listener
            self.buttons[TileID][0].bind('<Button-3>', self.right_click_dummy(TileID)) #Right click action listener
            cordX += 1


        #Placing the buttons on the screen
        for TileID in self.buttons:
            self.buttons[TileID][0].grid(row=self.buttons[TileID][4][1], column=self.buttons[TileID][4][0])

        #Checking for mines
        for a in range(0,256): #Where a is equivalent to Button ID aka button widget.
            closeByMine = 0 #Initializing variables.
            dummylist = self.getAdjacentCells(a) #Stores the index of list of nearby indexes
            for b in dummylist: #Go through the nearby tiles
                closeByMine += self.mineCheck(b) #add mines if there is any

            self.buttons[a][5] = closeByMine #store the value to the button object.
    #end of constructor

    def left_click_dummy(self, x): #Test code
        return lambda Button: self.left_click(self.buttons[x])

    def right_click_dummy(self, x):
        return lambda Button: self.right_click(self.buttons[x])

    def mineCheck(self,TileID):
        if self.buttons[TileID][1] == True:
            return 1 #return 1 to be added if there is a mine
        else:
            return 0 #Not a mine, return 0

    def left_click(self,button_data): #Methods for when left mouse button is clicked.

        if button_data[1] == True:
            for a in self.buttons: #Go through every tile and reveal unchecked mines and the tiles that are flagged wrong
                if self.buttons[a][1] != True and self.buttons[a][2] == 2: #It is not a mine, but it was flagged
                    self.buttons[a][0].config(image = self.tile_wrong) #Change the images and letting users know they were wrong.
                elif self.buttons[a][1] == True and self.buttons[a][2] == 0: #It's mine but unflagged.
                    self.buttons[a][0].config(image = self.tile_mine) #Display the mines
            self.lostGame() #Telling the user they lost.  GG

        elif button_data[5] != 0 and button_data[2] != 1: #Unclick cells that does not have no mines surrounding thems
            num = button_data[5] #Store the number of nearby mines in num
            button_data[0].config(image = self.tile_number[num-1]) #Display the image accordingly
            button_data[2] = 1 #Change status to clicked
            self.clicked += 1 #add 1 to the tally
            button_data[0].unbind('<Button-1>')
            button_data[0].unbind('<Button-2>')
        else: #if the cell is not a mine and does not have mines surround it.
            quene = [button_data[3]] #Using a quene to determine how big of an area to open and initialzing the quene
            queneChecker = [button_data[3]] #This list is almost the same as quene except it never pops any item.  Used to check for duplicates and prevents infinite loop
            button_data[2] = 1 #Change the status to be clicked
            button_data[0].config(image = self.tile_clicked) #Change the tile image
            button_data[0].unbind('<Button-1>')
            button_data[0].unbind('<Button-2>')
            self.clicked+=1 #Change the tally
            while len(quene) != 0:
                surroundList = self.getAdjacentCells(quene[0]) #get surround tile index numbers
                for item in surroundList:
                    if self.buttons[item][5] == 0:
                        if item in queneChecker: #If the item has already been in the quene.  No need to add it again.
                            pass
                        else:
                            queneChecker.append(item)
                            quene.append(item)
                            self.buttons[item][0].config(image=self.tile_clicked) #Show blank cells
                            self.buttons[item][0].unbind('<Button-1>')
                            self.buttons[item][0].unbind('<Button-2>')
                    else:
                        num = self.buttons[item][5]
                        self.buttons[item][0].config(image=self.tile_number[num-1])  # Display the image accordingly
                        self.buttons[item][0].unbind('<Button-1>')
                        self.buttons[item][0].unbind('<Button-2>')
                        self.clicked += 1
                quene.pop(0)
            self.clicked += len(queneChecker)
        self.checkStatus()

    def right_click(self,button_data): #Methods for when right mouse button is clicked.
        if button_data[2] == 0: #If the tile was not marked
            button_data[0].config(image=self.tile_flag)
            button_data[2] = 2
            button_data[0].unbind('<Button-1>') #invalidate anymore clicks
            self.flags += 1
            self.update_flaglabel()
            # if a mine
            if button_data[1] == 1:
                self.correct_flags += 1
                self.checkStatus()

        # if flagged, unflag
        elif button_data[2] == 2:
            button_data[0].config(image=self.tile_plain)
            button_data[2] = 0
            button_data[0].bind('<Button-1>', self.left_click_dummy(button_data[3]))
            # if a mine
            if button_data[1] == 1:
                self.correct_flags -= 1
            self.flags -= 1

    def checkStatus(self):
        if self.correct_flags == 40:
            self.wonGame()

    def update_flaglabel(self):
        self.flagLabel.config(text = "Flags: "+ str(self.flags))

    def lostGame(self):
        global root
        messagebox.showinfo("GG, you lost","Oops, you hit a mine.")
        root.quit()

    def wonGame(self):
        messagebox.showinfo("GG, you won!","Good job, you got all the mines!")
        global root
        root.quit() #Close the Window

    def getAdjacentCells(self, TileID):
        adjacentIDList = []
        if TileID == 0:
            adjacentIDList = [1,16,17]
            return adjacentIDList
        elif TileID == 15:
            adjacentIDList = [14, 31, 30]
        elif TileID == 240:
            adjacentIDList = [224, 225, 241]
        elif TileID == 255:
            adjacentIDList = [254, 239, 238]
        elif TileID > 0 and TileID < 15: #Top Row
            num1 = TileID - 1 #Check left, right, bottom left, bottom, bottom right
            num2 = TileID + 1
            num3 = TileID + 15
            num4 = TileID + 16
            num5 = TileID + 17
            adjacentIDList=[num1,num2,num3,num4,num5]
        elif TileID%16 == 0: #Left column,
            num1 = TileID + 1 #check right, top, top right, bottom, bottom right
            num2 = TileID - 16
            num3 = TileID - 15
            num4 = TileID + 16
            num5 = TileID + 17
            adjacentIDList = [num1,num2,num3,num4,num5]
        elif (TileID+1)%16 == 0: #Right Column
            num1 = TileID - 1 #Check left, top, top left, bottom, bottom left
            num2 = TileID - 16
            num3 = TileID - 17
            num4 = TileID + 16
            num5 = TileID + 15
            adjacentIDList = [num1,num2,num3,num4,num5]
        elif TileID > 240 and TileID < 255: #Bottom Row
            num1 = TileID - 1 #Check left, right, top left, top, top right
            num2 = TileID + 1
            num3 = TileID - 17
            num4 = TileID - 16
            num5 = TileID - 15
            adjacentIDList = [num1, num2, num3, num4, num5]
        else:
            num1 = TileID - 1 #Check left, right, top left, top, top right, bottom left, bottom, bottom right
            num2 = TileID + 1
            num3 = TileID - 17
            num4 = TileID - 16
            num5 = TileID - 15
            num6 = TileID + 15
            num7 = TileID + 16
            num8 = TileID + 17
            adjacentIDList = [num1, num2, num3, num4, num5, num6, num7, num8]
        return adjacentIDList
#Ending Class

def main():
    global root
    # create Tk widget
    root = Tk()
    # set program title
    root.title("Intermediate Minesweeper")
    root.geometry("350x350")
    minesweeper = Intermediate(root)
    # run event loop
    root.mainloop()

main()