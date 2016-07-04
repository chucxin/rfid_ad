from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
import pathlib
# for sqlite
import sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#
class App:
    def __init__(self, master):
        master.title("Administration of Informations of Students")
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
        # 要删除的用户 index
        # self.listOfDeletedIndex = []
        # 文件中已整理好的数据
        self.listOfName = []
        self.listOfPhone = []
        self.listOfUid = []
        self.listOfArriveMsg = []
        self.listOfLeaveMsg = []
        self.listOfId = []

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
        self.topFrame = Frame(master, width=60, padx=20, pady=10)
        self.topFrame.grid(row=0, column=0, sticky=W+N+E+S)
            # Open File
        self.buttonOpenFile = Button(self.topFrame, padx=20, pady=8, text="Open", command=self.loadFile)
        self.buttonOpenFile.grid(row=0, column=0, columnspan=1, sticky=W+N+E+S)
        self.labelFileName = Label(self.topFrame, width=40, textvariable=self.fileName)
        self.labelFileName.grid(row=0, column=1, columnspan=1, ipadx=20, ipady=9, sticky=W)

        # MAIN
        self.mainFrame = Frame(master, width=60, padx=20)
        self.mainFrame.grid(row=1, column=0, sticky=W+N+S+E)
            # MAIN > LEFT
        self.mainLeftFrame = Frame(self.mainFrame, width=10)
        self.mainLeftFrame.grid(row=0, column=0, sticky=W+N)
                # student list
        self.nameList = Listbox(self.mainLeftFrame, height=25, selectbackground='#cccccc', cursor='hand2')
        self.nameList.bind('<<ListboxSelect>>', self.selectList)
        self.nameList.grid(row=0, column=0, rowspan=15, sticky=W)
                # add & delete
        self.addDelFrame = Frame(self.mainLeftFrame)
        self.addDelFrame.grid(row=16, column=0, sticky=W+N)
                    # add
        self.addButton = Button(self.addDelFrame, width=4, height=2, text="Add", state=DISABLED, command=self.addUser)
        self.addButton.grid(row=0, column=0)
                    # delete
        self.deleteButton = Button(self.addDelFrame, width=4, height=2, text="Del", state=DISABLED, command=self.deleteUser)
        self.deleteButton.grid(row=0, column=1)

            # MAIN > RIGHT
        self.mainRightFrame = Frame(self.mainFrame, width=80)
        self.mainRightFrame.grid(row=0, column=1, sticky=W+N)
                # student information ###############################
                # Name
        self.nameTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Name:")
        self.nameTitle.grid(row=0, column=0, sticky=W)
        self.nameEntry = Entry(self.mainRightFrame, width=20, state=DISABLED, exportselection=0, textvariable=self.curName)
        self.nameEntry.grid(row=0, column=1, sticky=N+W)
                # Phone
        self.phoneTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Cellphone Number:")
        self.phoneTitle.grid(row=1, column=0, sticky=N+W)
        self.phoneEntry = Entry(self.mainRightFrame, width=20, state=DISABLED, exportselection=0, textvariable=self.curPhone)
        self.phoneEntry.grid(row=1, column=1, sticky=N+W)
                # UID
        self.uidTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="UID:")
        self.uidTitle.grid(row=2, column=0, sticky=N+W)
        self.uidFrame = Frame(self.mainRightFrame, width=40)
        self.uidFrame.grid(row=2, column=1, sticky=N+W)
        self.uidEntry1 = Entry(self.uidFrame, width=2, state=DISABLED, exportselection=0, textvariable=self.curUid1)
        self.uidEntry1.grid(row=0, column=0, sticky=N+W)
        self.uidEntry2 = Entry(self.uidFrame, width=2, state=DISABLED, exportselection=0, textvariable=self.curUid2)
        self.uidEntry2.grid(row=0, column=1, sticky=N+W)
        self.uidEntry3 = Entry(self.uidFrame, width=2, state=DISABLED, exportselection=0, textvariable=self.curUid3)
        self.uidEntry3.grid(row=0, column=2, sticky=N+W)
        self.uidEntry4 = Entry(self.uidFrame, width=2, state=DISABLED, exportselection=0, textvariable=self.curUid4)
        self.uidEntry4.grid(row=0, column=3, sticky=N+W)
                # Arrive Msg
        self.arriveMsgTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Message for Arriving: ")
        self.arriveMsgTitle.grid(row=3, column=0, columnspan=1, sticky=N+W)
        self.arriveMsgEntry = Entry(self.mainRightFrame, width=50, state=DISABLED, exportselection=0, textvariable=self.curArriveMsg)
        self.arriveMsgEntry.grid(row=3, column=1, columnspan=1, sticky=N+W)
                # Leave Msg
        self.leaveMsgTitle = Label(self.mainRightFrame, width=20, height=2, anchor=NE, text="Message for Leaving: ")
        self.leaveMsgTitle.grid(row=4, column=0, columnspan=1, sticky=N+W)
        self.leaveMsgEntry = Entry(self.mainRightFrame, width=50, state=DISABLED, exportselection=0, textvariable=self.curLeaveMsg)
        self.leaveMsgEntry.grid(row=4, column=1, columnspan=1, sticky=N+W)
                # Save to file
        self.saveButton = Button(self.mainRightFrame, text="Save", padx=20, pady=8, state=DISABLED, command=self.saveToDB)
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
        fname = filedialog.askopenfilename(filetypes=(("sqlite Database", "*.db"), ("All files", "*.*")))
        # file opened
        if fname:
            try:
                self.fileName.set(fname); # display filename
                # connect to Database
                conn = sqlite3.connect(fname)
                conn.row_factory = dict_factory
                cur = conn.cursor()
                cur.execute('SELECT * FROM users')
                for item in cur.fetchall():
                    self.listOfName.append(item['name'])
                    self.listOfPhone.append(item['phone'])
                    uid = []
                    for i in range(4):
                        uid.append(item['uid'][i*2:i*2+2])
                    self.listOfUid.append(uid)
                    self.listOfArriveMsg.append(item['arrivemsg'])
                    self.listOfLeaveMsg.append(item['leavemsg'])
                    self.listOfId.append(item['id'])

                conn.close()

                # 放入左边名单
                for item in self.listOfName:
                    print(item)
                    self.nameList.insert(END, item)

                # 让按键可以使用
                self.addButton.configure(state=NORMAL)
                # self.deleteButton.configure(state=NORMAL)
                self.saveButton.configure(state=NORMAL)

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
        if(self.curUserIndex >= 0 and self.curUserIndex < len(self.listOfName)):
            print("test")
            self.listOfName[self.curUserIndex] = self.nameEntry.get()
            self.listOfPhone[self.curUserIndex] = self.phoneEntry.get()
            self.listOfUid[self.curUserIndex] = [self.uidEntry1.get(), self.uidEntry2.get(), self.uidEntry3.get(), self.uidEntry4.get()]
            self.listOfArriveMsg[self.curUserIndex] = self.arriveMsgEntry.get()
            self.listOfLeaveMsg[self.curUserIndex] = self.leaveMsgEntry.get()
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
        # 输入框设为可输入
        self.nameEntry.configure(state=NORMAL)
        self.phoneEntry.configure(state=NORMAL)
        self.uidEntry1.configure(state=NORMAL)
        self.uidEntry2.configure(state=NORMAL)
        self.uidEntry3.configure(state=NORMAL)
        self.uidEntry4.configure(state=NORMAL)
        self.arriveMsgEntry.configure(state=NORMAL)
        self.leaveMsgEntry.configure(state=NORMAL)
        # 删除按键设为可用
        self.deleteButton.configure(state=NORMAL)

    # save to Database
    def saveToDB(self):
        # update the current data to all data listOfLeaveMsg
        if(self.curUserIndex >= 0):
            self.listOfName[self.curUserIndex] = self.nameEntry.get()
            self.listOfPhone[self.curUserIndex] = self.phoneEntry.get()
            self.listOfUid[self.curUserIndex] = [self.uidEntry1.get(), self.uidEntry2.get(), self.uidEntry3.get(), self.uidEntry4.get()]
            self.listOfArriveMsg[self.curUserIndex] = self.arriveMsgEntry.get()
            self.listOfLeaveMsg[self.curUserIndex] = self.leaveMsgEntry.get()
        # connect to DB
        conn = sqlite3.connect(self.fileName.get())
        conn.row_factory = dict_factory
        cur = conn.cursor()
        # update
        for idx in range(len(self.listOfId)):
            uidString = ""
            for i in range(4):
                uidString += self.listOfUid[idx][i]
            cur.execute("UPDATE users SET name=:name, phone=:phone, uid=:uid, arrivemsg=:arrivemsg, leavemsg=:leavemsg WHERE id=:id", {"name": self.listOfName[idx], "phone": self.listOfPhone[idx], "uid": uidString, "arrivemsg": self.listOfArriveMsg[idx], "leavemsg": self.listOfLeaveMsg[idx], "id": self.listOfId[idx]})
        conn.commit()
        conn.close()
        # 显示状态栏
        self.status.set("Saved.")
        self.isModified = False
        # make the file for the machine
        dataToWrite = "";
        for i in range(0, len(self.listOfName), 1):
            dataToWrite += self.listOfName[i] + "\n"
            dataToWrite += self.listOfPhone[i] + "\n"
            for ii in range(4):
                dataToWrite += self.listOfUid[i][ii]
            dataToWrite += "\n"
            dataToWrite += self.listOfArriveMsg[i] + "\n"
            dataToWrite += self.listOfLeaveMsg[i] + "\n"
            # add the isPresent info
            dataToWrite += "0\n"
        # 取路径并形成文件名
        filename = pathlib.PurePath(self.fileName.get()).parents[0].joinpath("USERDATA.RF")
        with pathlib.Path(filename).open(mode='w') as myFile:
            myFile.write(dataToWrite)


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
        self.curArriveMsg.set(self.listOfArriveMsg[self.curUserIndex])
        self.curLeaveMsg.set(self.listOfLeaveMsg[self.curUserIndex])
        self.curUid1.set(self.listOfUid[self.curUserIndex][0])
        self.curUid2.set(self.listOfUid[self.curUserIndex][1])
        self.curUid3.set(self.listOfUid[self.curUserIndex][2])
        self.curUid4.set(self.listOfUid[self.curUserIndex][3])
        # put in database
        conn = sqlite3.connect(self.fileName.get())
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, phone, uid, arrivemsg, leavemsg) VALUES ('', '', '', '', '')")
        self.listOfId.append(str(cur.lastrowid))
        print("last id: " + str(cur.lastrowid))
        conn.commit()
        conn.close()


    # delete user
    def deleteUser(self):
        if messagebox.askokcancel("Delete", "Are you sure you want to delete this user?"):
            # 先取要删除的 ID， 下面会把这个ID从列表中删除
            idToDelete = self.listOfId[self.curUserIndex]
            # 从 全部数据 列表中删除
            self.listOfName.pop(self.curUserIndex)
            self.listOfPhone.pop(self.curUserIndex)
            self.listOfUid.pop(self.curUserIndex)
            self.listOfArriveMsg.pop(self.curUserIndex)
            self.listOfLeaveMsg.pop(self.curUserIndex)
            self.listOfId.pop(self.curUserIndex)
            # update name list
            self.nameList.selection_clear(self.curUserIndex)
            self.nameList.delete(self.curUserIndex)
            self.justDeleted = True

            print(self.nameList.curselection())
            print(self.nameList.size())

            # 重设 当前所选用户为 -1
            self.curUserIndex = -1
            # 输入框设为不能输入
            self.nameEntry.configure(state=DISABLED)
            self.phoneEntry.configure(state=DISABLED)
            self.uidEntry1.configure(state=DISABLED)
            self.uidEntry2.configure(state=DISABLED)
            self.uidEntry3.configure(state=DISABLED)
            self.uidEntry4.configure(state=DISABLED)
            self.arriveMsgEntry.configure(state=DISABLED)
            self.leaveMsgEntry.configure(state=DISABLED)
            # reset current data
            self.curName.set("")
            self.curPhone.set("")
            self.curUid1.set("")
            self.curUid2.set("")
            self.curUid3.set("")
            self.curUid4.set("")
            self.curArriveMsg.set("")
            self.curLeaveMsg.set("")
            # delete from db
            conn = sqlite3.connect(self.fileName.get())
            conn.row_factory = dict_factory
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=:id", {"id": idToDelete})
            conn.commit()
            conn.close()






root = Tk()
app = App(root)
root.mainloop()
