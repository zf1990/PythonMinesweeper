#By Zhou Fang and Priyanka Muttaraju
#SEIS 603 - 02
#Final Project - Beginner class constructor and methods
#Due date: May 6, 2019

from tkinter import *
from tkinter import messagebox
import random


class Begin:

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
        welcomeLabel = Label(frame, text = "Welcome to Beginner Minesweeper", fg = "blue")
        welcomeLabel.grid(row = 0, column = 0, columnspan = 9)

        self.totalMine = 10
        self.flags = 0 #Number of flags user put up
        self.correct_flags = 0 #Number of flags user put up correctly
        self.clicked = 0 #Number of tiles revealed that's not a mine
        self.MineLabel = Label(statusBar, text = "Total Mine: " + str(self.totalMine))
        self.MineLabel.pack(side = LEFT)
        self.flagLabel = Label(statusBar, text = "Flagged: " + str(self.flags))
        self.flagLabel.pack(side = RIGHT)


       #Placing mines.  The number x will serve as grid ID.

        mines = 10
        mineStatus = [] #Python does not have a built-in array function... List can be used instead then
        for x in range(0,71):
            if random.randrange(81) <= 9 and mines>0:
                #Trying to distribute mines roughly evently.  Since there are 10 mines and 81 Tiles, the probability of a random mine would be 10/81 as represented here.
                mineStatus.append(True)
                mines = mines - 1
            else:
                mineStatus.append(False)
        for x in range(71,81): #Placing the rest of mines in the bottom tiles if there are still more mines to place.
            if mines > 0:
                mineStatus.append(True)
                mines=mines-1
            else:
                mineStatus.append(False)


        # create buttons
        self.buttons = dict({}) #Create a dictionary of linked list.
        self.mines = 0

        cordX = 0
        cordY = 1 #Remember that the first row (row 0) is occupied by the welcome to minesweeper label


        for TileID in range(0,81): # 9x9 tiles with buttons
            # 0 = Creating buttons and its properties
            # 1 = Mine Status to check whether this is a mine.  True = Mine, False = Not a mine
            # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged #Creating the status for the buttons in place.
            # 3 = button id #Same thing
            # 4 = [cordX, cordY] coordinates in the grid
            # 5 = nearby mines, 0 by default, calculated after placement in grid

            if (TileID-9) % 9 == 0: #To start a new row.  The entire size would be 9x9
                cordX = cordX + 1
                cordY = 0

            self.buttons[TileID] = [Button(frame, width = 2, height = 1), mineStatus[TileID], 0, TileID, [cordX, cordY], 0] #Positive x and y direction going right and down respectively from top left corner
            self.buttons[TileID][0].bind('<Button-1>', lambda button1: self.left_click(TileID)) #Left Click action listener
            self.buttons[TileID][0].bind('<Button-3>', lambda button2: self.right_click(TileID)) #Right click action listener
            self.buttons[TileID][0].bind('<Button-2>', lambda button2: self.middle_click(TileID))  # Right click action listener
            cordY += 1


        #Placing the buttons on the screen
        for TileID in self.buttons:
            self.buttons[TileID][0].grid(row=self.buttons[TileID][4][0], column=self.buttons[TileID][4][1])

        #Checking for mines
        for a in range(0,81): #Where a is equivalent to Button ID aka button widget.
            closeByMine = 0 #Initializing variables.
            if self.mineCheck(a): #If the index is a mine, we do not need to go on any longer
               pass
            elif (a==0): #Top left corner cell
                closeByMine = self.mineCheck(1) + self.mineCheck(9) + self.mineCheck(10)
                #right + bottom + botright
            elif (a==8): #Top right Cell
                closeByMine = self.mineCheck(7) + self.mineCheck(17) + self.mineCheck(16) #left, bottom, botleft
                #left + bottom + botLeft
            elif (a==72): #Bottom left cell
                closeByMine = self.mineCheck(73) + self.mineCheck(63) + self.mineCheck(64)
                # right, top, topright
            elif (a==80): #Bottom right corner cell
                closeByMine = self.mineCheck(79) + self.mineCheck(71) + self.mineCheck(70)
                # left, top, topleft
            elif (a>0 and a<8): #top row cells
                closeByMine = self.mineCheck(a-1) + self.mineCheck(a+1) + self.mineCheck(a+8) + self.mineCheck(a+9) + self.mineCheck(a+10)
                #left + right + botLeft + bottom + botRight
            elif (a%9==0): #Left column of cells that are not corner cells
                closeByMine = self.mineCheck(a-9) + self.mineCheck(a-8) + self.mineCheck(a+1) + self.mineCheck(a+9) + self.mineCheck(a+10)
                #Top + top right + right + bottom + bottom right
            elif ((a+1)%9 == 0): #Right Column of cells that are not corner cells
                closeByMine = self.mineCheck(a-9) + self.mineCheck(a-10) + self.mineCheck(a-1) + self.mineCheck(a+9) + self.mineCheck(a+8)
            elif(a>72 and a<80): #Bottom row
                closeByMine = self.mineCheck(a - 9) + self.mineCheck(a - 10) + self.mineCheck(a - 8) + self.mineCheck(a + 1) + self.mineCheck(a - 1)
                #Top + Top left + top right + right + left
            else:
                closeByMine = self.mineCheck(a - 9) + self.mineCheck(a - 10) + self.mineCheck(a - 1) + self.mineCheck(a + 9) + self.mineCheck(a + 8) + self.mineCheck(a + 1) + self.mineCheck(a - 8) + self.mineCheck(a + 10)
                #Top + Topleft + left + bottom + bottom left + right + topright + bottom right
            self.buttons[a][5] = closeByMine #Setting the value in the dictionary.
    #end of constructor

    # def left_click_dummy(self, x): Test code
    #     return lambda Button: self.left_click(x)
    #
    # def right_click_dummy(self, x):
    #     return lambda Button: self.right_click(x)

    def mineCheck(self,TileID):
        if self.buttons[TileID][1] == True:
            return 1 #return 1 to be added if there is a mine
        else:
            return 0 #Not a mine, return 0

    def left_click(self,TileID): #Methods for when left mouse button is clicked.
        isMine = self.mineCheck(TileID)

        if self.clicked == 81 - self.totalMine and isMine == 0:
            self.wonGame()

        if isMine == 1:
            for a in self.buttons: #Go through every tile and reveal unchecked mines and the tiles that are flagged wrong
                if self.buttons[a][1] != True and self.buttons[a][2] == 2: #It is not a mine, but it was flagged
                    self.buttons[a][0].config(image = self.tile_wrong, width = 2, height = 1) #Change the images and letting users know they were wrong.
                elif self.buttons[a][1] == True and self.buttons[a][2] == 0: #It's mine but unflagged.
                    self.buttons[a][0].config(image=self.tile_mine, width = 2, height = 1) #Display the mines
            self.lostGame()

        elif self.buttons[TileID][5] != 0:
            num = self.buttons[TileID][5]
            self.buttons[TileID][0].config(image = self.tile_number[num-1], width = 2, height = 1) #Display the image accordingly
            self.buttons[TileID][2] = 1
            self.clicked += 1
        else: #if the cell is blank
            quene = [TileID] #Using a quene to determine how big of an area to open and initialzing the quene
            queneChecker = [TileID]
            self.buttons[quene[0]][2] = 1 #Change the status to be clicked
            self.buttons[TileID][0].config(image = self.tile_clicked, width = 2, height = 1)
            self.clicked+=1
            while len(quene) != 0:
                surroundList = self.getAdjacentCells(quene[0])
                for item in surroundList:
                    if self.buttons[item][5] == 0:
                        if item in queneChecker:
                            pass
                        else:
                            queneChecker.append(item)
                            quene.append(item)
                            self.clicked += 1

                    else:
                        num = self.buttons[item][5]
                        self.buttons[item][0].config(image=self.tile_number[num-1], width = 2, height = 1)  # Display the image accordingly
                        self.clicked += 1
                quene.pop(0)


    def right_click(self,TileID): #Methods for when right mouse button is clicked.
        if self.buttons[TileID][2] == 0:
            self.buttons[TileID][0].config(image=self.tile_flag, width = 2, height = 1)
            self.buttons[TileID][2] = 2
            self.buttons[TileID][0].unbind('<Button-1>')
            # if a mine
            if self.buttons[TileID][1] == 1:
                self.correct_flags += 1
            self.flags += 1
            self.update_flaglabel()
        # if flagged, unflag
        elif self.buttons[TileID][2] == 2:
            self.buttons[TileID][0].config(image=self.tile_plain, width = 2, height = 1)
            self.buttons[TileID][2] = 0
            self.buttons[TileID][0].bind('<Button-1>', self.left_click(self.buttons[TileID][3]))
            # if a mine
            if self.buttons[TileID][1] == 1:
                self.correct_flags -= 1
            self.flags -= 1

    def update_flaglabel(self):
        self.flagLabel.config(text = "Flags: "+ str(self.flags))
    def middle_click(self,TileID):
        surroundingTiles = self.getAdjacentCells(TileID)
        for i in surroundingTiles:
            self.left_click(i)

    def lostGame(self):
        messagebox.showinfo("Oops, you clicked on the mine.")
        global master
        master.destory() ##Close the Window

    def wonGame(self):
        messagebox.showinfo("Good job, you got all the mines!")
        global master
        master.destory() ##Close the Window

    def getAdjacentCells(self, TileID):
        adjacentIDList = []
        if TileID == 0:
            adjacentIDList = [1,9,10]
            return adjacentIDList
        elif TileID == 8:
            adjacentIDList = [7, 17, 16]
        elif TileID == 72:
            adjacentIDList = [73, 63, 64]
        elif TileID == 80:
            adjacentIDList = [79, 71, 70]
        elif TileID > 0 and TileID < 8: #Top Row
            num1 = TileID - 1
            num2 = TileID + 1
            num3 = TileID + 8
            num4 = TileID + 9
            num5 = TileID + 10
            adjacentIDList=[num1,num2,num3,num4,num5]
        elif TileID%9 == 0: #Left column
            num1 = TileID + 1
            num2 = TileID - 9
            num3 = TileID - 8
            num4 = TileID + 9
            num5 = TileID + 10
            adjacentIDList = [num1,num2,num3,num4,num5]
        elif (TileID+1)%9 == 0: #Right Column
            num1 = TileID - 1
            num2 = TileID - 9
            num3 = TileID -10
            num4 = TileID + 9
            num5 = TileID + 8
            adjacentIDList = [num1,num2,num3,num4,num5]
        elif TileID > 72 and TileID < 81: #Bottom Row
            num1 = TileID - 1
            num2 = TileID + 1
            num3 = TileID - 8
            num4 = TileID - 9
            num5 = TileID - 10
            adjacentIDList = [num1, num2, num3, num4, num5]
        else:
            num1 = TileID - 1
            num2 = TileID + 1
            num3 = TileID - 8
            num4 = TileID - 9
            num5 = TileID - 10
            num6 = TileID + 8
            num7 = TileID + 9
            num8 = TileID + 10
            adjacentIDList = [num1, num2, num3, num4, num5, num6, num7, num8]
        return adjacentIDList

def main():
    global root
    # create Tk widget
    root = Tk()
    # set program title
    root.title("Minesweeper")
    # create game instance
    minesweeper = Begin(root)
    # run event loop
    root.mainloop()


if __name__ == "__main__":
    main()