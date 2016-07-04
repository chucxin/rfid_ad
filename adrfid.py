from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from functools import partial

class App:
    def __init__(self, master):
        # 所打开的文件名
        self.fileName = StringVar()
        # save alter
        self.status = StringVar()
        # is modified?
        self.isModified = False
        # just deleted?
        self.justDeleted = False
        # 当前打开的用户index
        self.curUserIndex = -1;
        # 文件中已整理好的数据
        self.listOfName = []
        self.listOfPhone = []
        self.listOfUid = []
        self.listOfArriveMsg = []
        self.listOfLeaveMsg = []

        # 正在显示的数据
        self.curName = StringVar(master)
        self.curName.trace("w", self.nameEntryModified)
        self.curPhone = StringVar()
        self.curPhone.trace("w", self.entryModified)
        # self.curUid = StringVar()
        self.curArriveMsg = StringVar()
        self.curArriveMsg.trace("w", self.entryModified)
        self.curLeaveMsg = StringVar()
        self.curLeaveMsg.trace("w", self.entryModified)
        self.curUid1 = StringVar()
        self.curUid1.trace("w", self.entryModified)
        self.curUid2 = StringVar()
        self.curUid2.trace("w", self.entryModified)
        self.curUid3 = StringVar()
        self.curUid3.trace("w", self.entryModified)
        self.curUid4 = StringVar()
        self.curUid4.trace("w", self.entryModified)

        # TOP
        self.topFrame = Frame(master, width=60)
        self.topFrame.grid(row=0, column=0, sticky=W+N+E+S)
            # Open File
        self.buttonOpenFile = Button(self.topFrame, padx=20, pady=8, text="Open", command=self.loadFile)
        self.buttonOpenFile.grid(row=0, column=0, columnspan=1, sticky=W+N+E+S)
        self.labelFileName = Label(self.topFrame, width=40, textvariable=self.fileName)
        self.labelFileName.grid(row=0, column=1, columnspan=1, ipadx=20, ipady=9, sticky=W)

        # MAIN
        self.mainFrame = Frame(master, width=60)
        self.mainFrame.grid(row=1, column=0, sticky=W+N+S+E)
            # MAIN > LEFT
        self.mainLeftFrame = Frame(self.mainFrame, width=10)
        self.mainLeftFrame.grid(row=0, column=0, sticky=W+N)
                # student list
        self.nameList = Listbox(self.mainLeftFrame, height=25)
        self.nameList.bind('<<ListboxSelect>>', self.selectList)
        self.nameList.grid(row=0, column=0, rowspan=15, sticky=W)
                # add & delete
        self.addDelFrame = Frame(self.mainLeftFrame)
        self.addDelFrame.grid(row=16, column=0, sticky=W+N)
                    # add
        self.addButton = Button(self.addDelFrame, width=4, height=2, text="Add", command=self.addUser)
        self.addButton.grid(row=0, column=0)
                    # delete
        self.deleteButton = Button(self.addDelFrame, width=4, height=2, text="Del", command=self.deleteUser)
        self.deleteButton.grid(row=0, column=1)

            # MAIN > RIGHT
        self.mainRightFrame = Frame(self.mainFrame, width=80)
        self.mainRightFrame.grid(row=0, column=1, sticky=W+N)
                # student information ###############################
                # Name
        self.nameTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Name:")
        self.nameTitle.grid(row=0, column=0, sticky=W)
        self.nameEntry = Entry(self.mainRightFrame, width=20, exportselection=0, textvariable=self.curName)
        self.nameEntry.grid(row=0, column=1, sticky=N+W)
                # Phone
        self.phoneTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Cellphone Number:")
        self.phoneTitle.grid(row=1, column=0, sticky=N+W)
        self.phoneEntry = Entry(self.mainRightFrame, width=20, exportselection=0, textvariable=self.curPhone)
        self.phoneEntry.grid(row=1, column=1, sticky=N+W)
                # UID
        self.uidTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="UID:")
        self.uidTitle.grid(row=2, column=0, sticky=N+W)
        self.uidFrame = Frame(self.mainRightFrame, width=40)
        self.uidFrame.grid(row=2, column=1, sticky=N+W)
        self.uidEntry1 = Entry(self.uidFrame, width=2, exportselection=0, textvariable=self.curUid1)
        self.uidEntry1.grid(row=0, column=0, sticky=N+W)
        self.uidEntry2 = Entry(self.uidFrame, width=2, exportselection=0, textvariable=self.curUid2)
        self.uidEntry2.grid(row=0, column=1, sticky=N+W)
        self.uidEntry3 = Entry(self.uidFrame, width=2, exportselection=0, textvariable=self.curUid3)
        self.uidEntry3.grid(row=0, column=2, sticky=N+W)
        self.uidEntry4 = Entry(self.uidFrame, width=2, exportselection=0, textvariable=self.curUid4)
        self.uidEntry4.grid(row=0, column=3, sticky=N+W)
                # Arrive Msg
        self.arriveMsgTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Message for Arriving: ")
        self.arriveMsgTitle.grid(row=3, column=0, columnspan=1, sticky=N+W)
        self.arriveMsgEntry = Entry(self.mainRightFrame, width=50, exportselection=0, textvariable=self.curArriveMsg)
        self.arriveMsgEntry.grid(row=3, column=1, columnspan=1, sticky=N+W)
                # Leave Msg
        self.leaveMsgTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Message for Leaving: ")
        self.leaveMsgTitle.grid(row=4, column=0, columnspan=1, sticky=N+W)
        self.leaveMsgEntry = Entry(self.mainRightFrame, width=50, exportselection=0, textvariable=self.curLeaveMsg)
        self.leaveMsgEntry.grid(row=4, column=1, columnspan=1, sticky=N+W)
                # Save to file
        self.saveButton = Button(self.mainRightFrame, text="Save", padx=20, pady=8, command=self.saveToFile)
        self.saveButton.grid(row=5, column=1, sticky=E+S)

        # BOTTOM
        self.bottomFrame = Frame(master, width=70, height=2)
        self.bottomFrame.grid(row=2, column=0, sticky=W)
            # bottom > LEFT
        self.bottomLeftLabel = Label(self.bottomFrame, width=40, height=2, anchor=W, textvariable=self.status)
        self.bottomLeftLabel.grid(row=0, column=0, sticky=W+N)

        # close alert
        master.protocol("WM_DELETE_WINDOW", partial(self.on_closing, master))


    # load file function
    def loadFile(self):
        fname = filedialog.askopenfilename(filetypes=(("RFID Files", "*.rfid"), ("All files", "*.*")))
        # file opened
        if fname:
            try:
                self.fileName.set(fname); # display filename
                # open the file in python
                myFile = open(fname, "r")
                fl = myFile.readlines() # read all lines of the file
                print(fl)
                myFile.close()
                # process the data in the file
                for i in range(len(fl)):
                    if (i+1) % 5 == 1: # name
                        self.listOfName.append(fl[i][:-1])
                    elif (i+1) % 5 == 2: # phone
                        self.listOfPhone.append(fl[i][:-1])
                    elif (i+1) % 5 == 3: # uid
                        uid = []
                        for ii in range(4):
                            uid.append(fl[i][ii*2:ii*2+2])
                        self.listOfUid.append(uid)
                        print(uid)
                    elif (i+1) % 5 == 4: # arrive msg
                        self.listOfArriveMsg.append(fl[i][:-1])
                    elif (i+1) % 5 == 0: # leave msg
                        self.listOfLeaveMsg.append(fl[i][:-1])

                # 放入左边名单
                for item in self.listOfName:
                    print(item)
                    self.nameList.insert(END, item)
                # self.nameList.bind('<<ListboxSelect>>', self.selectList)
                # self.nameList.grid(row=0, column=0, rowspan=15, sticky=W)

            except:
                messagebox.showerror("Open Source File", "Failed to read file")
            return

    # select from Listbox
    def selectList(self, *args):
        if self.justDeleted:
            self.nameList.delete(0)
            self.justDeleted = False

        print(self.nameList.get(0, END))

        isM = self.isModified
        print(self.curUserIndex)
        print(len(self.listOfName))
        # 保存前一个用户的数据 (放入全部文件数据)
        # if(self.curUserIndex >= 0 and self.curUserIndex < len(self.listOfName)):
        #     print("test")
        #     self.listOfName[self.curUserIndex] = self.nameEntry.get()
        #     self.listOfPhone[self.curUserIndex] = self.phoneEntry.get()
        #     self.listOfUid[self.curUserIndex] = [self.uidEntry1.get(), self.uidEntry2.get(), self.uidEntry3.get(), self.uidEntry4.get()]
        #     self.listOfArriveMsg[self.curUserIndex] = self.arriveMsgEntry.get()
        #     self.listOfLeaveMsg[self.curUserIndex] = self.leaveMsgEntry.get()
        print(self.nameList.curselection())
        self.curUserIndex = self.nameList.curselection()[0] # 取所点击的用户index
        # 显示当前用户的数据
        self.curName.set(self.listOfName[self.curUserIndex])
        self.curPhone.set(self.listOfPhone[self.curUserIndex])
        # self.curUid.set(self.listOfUid[self.curUserIndex])
        self.curArriveMsg.set(self.listOfArriveMsg[self.curUserIndex])
        self.curLeaveMsg.set(self.listOfLeaveMsg[self.curUserIndex])
        self.curUid1.set(self.listOfUid[self.curUserIndex][0])
        self.curUid2.set(self.listOfUid[self.curUserIndex][1])
        self.curUid3.set(self.listOfUid[self.curUserIndex][2])
        self.curUid4.set(self.listOfUid[self.curUserIndex][3])
        if not isM:
            self.status.set("")
            self.isModified = False

    # save to file
    def saveToFile(self):
        # update the current data to all data listOfLeaveMsg
        if(self.curUserIndex >= 0):
            self.listOfName[self.curUserIndex] = self.nameEntry.get()
            self.listOfPhone[self.curUserIndex] = self.phoneEntry.get()
            self.listOfUid[self.curUserIndex] = [self.uidEntry1.get(), self.uidEntry2.get(), self.uidEntry3.get(), self.uidEntry4.get()]
            self.listOfArriveMsg[self.curUserIndex] = self.arriveMsgEntry.get()
            self.listOfLeaveMsg[self.curUserIndex] = self.leaveMsgEntry.get()
        #
        dataToWrite = "";
        for i in range(0, len(self.listOfName), 1):
            dataToWrite += self.listOfName[i] + "\n"
            dataToWrite += self.listOfPhone[i] + "\n"
            for ii in range(4):
                dataToWrite += self.listOfUid[i][ii]
            dataToWrite += "\n"
            dataToWrite += self.listOfArriveMsg[i] + "\n"
            dataToWrite += self.listOfLeaveMsg[i] + "\n"

        print(dataToWrite)

        myFile = open(self.fileName.get(), "w")
        myFile.write(dataToWrite)
        self.status.set("Saved.")
        self.isModified = False
        myFile.close()

    # entry modified
    def entryModified(self, *args):
        self.isModified = True
        self.status.set("Modified...")
    def nameEntryModified(self, *args):
        self.isModified = True
        self.status.set("Modified...")
        # modify the name in name list at left
        self.nameList.delete(self.curUserIndex)
        self.nameList.insert(self.curUserIndex, self.nameEntry.get())

    # exit
    def on_closing(self, master):
        if self.isModified:
            if messagebox.askokcancel("Quit", "You haven't save your file. Do you want to quit?"):
                master.destroy()
        else:
            master.destroy()

    # add user
    def addUser(self):
        self.listOfName.append("")
        self.listOfPhone.append("")
        self.listOfUid.append(["","","",""])
        self.listOfArriveMsg.append("")
        self.listOfLeaveMsg.append("")
        # insert to name list
        self.nameList.insert(END, self.listOfName[len(self.listOfName) - 1])
        # 保存前一个用户的数据 (放入全部文件数据)
        if(self.curUserIndex >= 0):
            self.listOfName[self.curUserIndex] = self.nameEntry.get()
            self.listOfPhone[self.curUserIndex] = self.phoneEntry.get()
            self.listOfUid[self.curUserIndex] = [self.uidEntry1.get(), self.uidEntry2.get(), self.uidEntry3.get(), self.uidEntry4.get()]
            self.listOfArriveMsg[self.curUserIndex] = self.arriveMsgEntry.get()
            self.listOfLeaveMsg[self.curUserIndex] = self.leaveMsgEntry.get()
        self.curUserIndex = len(self.listOfName) - 1 # user index 为最新的
        # 显示当前用户的数据
        self.curName.set(self.listOfName[self.curUserIndex])
        self.curPhone.set(self.listOfPhone[self.curUserIndex])
        # self.curUid.set(self.listOfUid[self.curUserIndex])
        self.curArriveMsg.set(self.listOfArriveMsg[self.curUserIndex])
        self.curLeaveMsg.set(self.listOfLeaveMsg[self.curUserIndex])
        self.curUid1.set(self.listOfUid[self.curUserIndex][0])
        self.curUid2.set(self.listOfUid[self.curUserIndex][1])
        self.curUid3.set(self.listOfUid[self.curUserIndex][2])
        self.curUid4.set(self.listOfUid[self.curUserIndex][3])

    # delete user
    def deleteUser(self):
        # 从 全部数据 列表中删除
        self.listOfName.pop(self.curUserIndex)
        self.listOfPhone.pop(self.curUserIndex)
        self.listOfUid.pop(self.curUserIndex)
        self.listOfArriveMsg.pop(self.curUserIndex)
        self.listOfLeaveMsg.pop(self.curUserIndex)
        # update name list
        self.nameList.selection_clear(self.curUserIndex)
        self.nameList.delete(self.curUserIndex)
        self.justDeleted = True

        # self.nameList.delete(0, END)
        # for item in self.listOfName:
        #     print(item)
        #     self.nameList.insert(END, item)
        print(self.nameList.curselection())
        print(self.nameList.size())

        # print(self.nameList.curselection()[0])
        # 重设 当前所选用户为 -1
        self.curUserIndex = -1
        # reset current data
        self.curName.set("")
        self.curPhone.set("")
        self.curUid1.set("")
        self.curUid2.set("")
        self.curUid3.set("")
        self.curUid4.set("")
        self.curArriveMsg.set("")
        self.curLeaveMsg.set("")





root = Tk()
app = App(root)
root.mainloop()
