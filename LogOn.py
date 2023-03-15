# This is the py to run first
#

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from MainWin3 import Ui_MainWindow
from About import Ui_Form
from AddSubs import Ui_AddNewWindow
from EditSubs import Ui_EditSubsWindow
from IssueMag import Ui_IssueMagWindow
from getMonth import find_month, find_Month_Num
from StarDate import getStarDate, getNextIssueDate
from getIssueInfo import get_Metadata, extract_pg1_text
import csv
import datetime
import re
import About_rc  # DO NOT DELETE THESE ARE USED
import Images_rc  # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^


def Set_Stardate():
    starDate = getStarDate()  # returns date YYMMDDhhmmss
    SD = starDate
    return SD


def exitClick():
    sys.exit(0)


def getListIssues():
    line = "Issue Numbers and Dates\n\nIssue\tMonth\tYear\t  Date\n"
    theList = issuesList[0]
    for row in issuesList:
        line = line + f"  {row[0]} \t {row[1]} \t{row[2]}\t{row[3]}"

        line = line + "\n"
    return line


def getListNASubscribers():
    e = "Email"
    n = "Name"
    y = "Years"
    fir = "First"
    las = "Last"
    a = "Act"
    d = "DETAILS"
    s = "SUBSCRIPTION"
    tot = len(subsNotActive)
    line = f"List of PREVEOUS Magazine Subscribers Who No Longer Receive OLM: TOTAL {tot}\n\n" \
           f"\t\t{d.ljust(80)}{s.rjust(20)}\n\t" \
           f"{e.ljust(50)}\t\t{n.ljust(21)}{y.ljust(13)}{fir.ljust(15)}{las.ljust(13)}{a}\n"
    # theList = issuesList[0]
    for row in subsNotActive:
        line = line + f"  {row[0].ljust(50)}\t{row[1].ljust(28)}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}"
        line = line + "\n"
    return line


def getListLISubscribers():
    e = "Email"
    n = "Name"
    y = "Years"
    fir = "First"
    las = "Last"
    a = "Act"
    d = "DETAILS"
    s = "SUBSCRIPTION"
    tot = len(subsLastIssue)
    line = f"List of Magazine Subscribers Who will Receive Their Last Issue Next: TOTAL {tot}\n\n" \
           f"\t\t{d.ljust(80)}{s.rjust(20)}\n\t" \
           f"{e.ljust(50)}\t\t{n.ljust(21)}{y.ljust(13)}{fir.ljust(15)}{las.ljust(13)}{a}\n"
    # theList = issuesList[0]
    for row in subsLastIssue:
        line = line + f"  {row[0].ljust(50)}\t{row[1].ljust(28)}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}"
        line = line + "\n"
    return line


def getListSubscribers():
    e = "Email"
    n = "Name"
    y = "Years"
    fir = "First"
    las = "Last"
    a = "Act"
    d = "DETAILS"
    s = "SUBSCRIPTION"
    tot = len(Subscribers)
    line = f"Magazine Subscribers List: FULL LIST {tot}\n\n" \
           f"\t\t{d.ljust(80)}{s.rjust(20)}\n\t" \
           f"{e.ljust(50)}\t\t{n.ljust(21)}{y.ljust(13)}{fir.ljust(15)}{las.ljust(13)}{a}\n"
    # theList = issuesList[0]
    for row in Subscribers:
        line = line + f"  {row[0].ljust(50)}\t{row[1].ljust(28)}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}"
        line = line + "\n"
    return line


def getListActiveSubscribers():
    e = "Email"
    n = "Name"
    y = "Years"
    fir = "First"
    las = "Last"
    a = "Act"
    d = "DETAILS"
    s = "SUBSCRIPTION"
    tot = len(subsActive)
    line = f"List of All Magazine Subscribers That Are Active: TOTAL {str(tot)}\n\n" \
           f"\t\t{d.ljust(80)}{s.rjust(20)}\n\t" \
           f"{e.ljust(50)}\t\t{n.ljust(21)}{y.ljust(13)}{fir.ljust(15)}{las.ljust(13)}{a}\n"
    # theList = issuesList[0]
    for row in subsActive:
        line = line + f"  {row[0].ljust(50)}\t{row[1].ljust(28)}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}"
        line = line + "\n"
    return line


def validEmail(input_email):
    EMOK = False
    em = str(input_email)
    pattern = "[a-zA-Z0-9._]+[a-zA-Z0-9]+@+[a-zA-Z]+\.+[a-zA-Z]"  # add a $ to end?
    if re.search(pattern, em):  # Email IS valid format
        EMOK = True
    else:  # Not valid Email
        EMOK = False
    return EMOK


class Ui_LogOnUI(object):

    def __init__(self):
        self.timer = None
        self.rbtimer = None
        self.IssueMagWindow = None
        self.AllOK = None
        self.okToDelete = None
        self.editing = None
        self.EditSubs = None
        self.nextPubDate = None
        self.nextPublish = None
        self.nextIssueNumber = None
        self.AddNewSubs = None
        self.About_UI = None
        self.ui = None
        self.Main_UI = None
        self.totActiveSubs = 0
        self.dblen = 0

    def closeaddSubs(self):
        self.openMW()
        self.AddNewSubs.close()
        self.start()

    def addSubs(self):  # Add new subscriber window
        self.Main_UI.close()

        self.stop()
        self.AddNewSubs = QtWidgets.QMainWindow()
        self.ui = Ui_AddNewWindow()
        self.ui.setupUi(self.AddNewSubs)
        self.active_Subscribers()
        self.ui.pushButtonExit.clicked.connect(self.closeaddSubs)
        self.ui.labelActiveNumber.setText(str(self.totActiveSubs))
        self.ui.spinBoxFirstIssue.setValue(self.nextIssueNumber)
        self.ui.pushButtonAddNew.clicked.connect(self.checkInputs)
        self.ui.pushButtonClear.clicked.connect(self.clearClick)
        self.ui.labelSIDNumber.setText(str(self.dblen))
        self.AddNewSubs.show()

    def clearClick(self):
        self.ui.lineEditEmail.setText("")
        self.ui.lineEditName.setText("")

    def checkInputs(self):
        self.AllOK = False
        emailField = self.ui.lineEditEmail.text()
        nameField = self.ui.lineEditName.text()
        nameField = nameField.strip()
        subsYears = str(self.ui.spinBoxYears.value())
        firstIssue = str(self.ui.spinBoxFirstIssue.value())

        # print(emailField + " " + nameField + " " + subsYears + " " + firstIssue)
        EMOK = validEmail(emailField)
        if EMOK == False:
            self.badEmail()
            self.AllOK = False
        else:
            AllOK = True
            if len(nameField) < 3:
                self.AllOK = False
                self.badName()
            else:
                self.AllOK = True
        if self.AllOK:
            self.add_This_Subscriber()

    def add_This_Subscriber(self):  # Add New subscriber to list
        em = self.ui.lineEditEmail.text()
        na = self.ui.lineEditName.text()
        su = self.ui.spinBoxYears.value()
        fi = self.ui.spinBoxFirstIssue.value()

        issues = su * 6  # 6 issues a yesr times 6
        issues = issues + fi  # add on first issue number
        issues -= 1  # minus 1 to make 6 issues inc fi
        if su == 0:  # add 1 if 0 years (fi = last issue, li)
            issues += 1

        li = str(issues)  # last issue
        su = str(su)  # subscription len, Years
        fi = str(fi)
        Subscribers.append([em, na, su, fi, li, ""])  # add to end of list
        self.active_Subscribers()  # update to get [5]
        self.ui.lineEditName.setText("")
        self.ui.lineEditEmail.setText("")
        # self.AllOK = False
        self.dblen = len(Subscribers)
        # self.ui.labelSIDNumber.setText(str(self.dblen))
        # self.ui.labelActiveNumber.setText(str(self.totActiveSubs))
        self.ui.labelNewSubs.setText(na)
        self.saveSubscribers()

    def saveSubscribers(self):
        with open('Subscribers.csv', 'w', newline='') as sS:
            writer = csv.writer(sS)
            writer.writerows(Subscribers)

    def noSelection(self):
        msg = QMessageBox()
        msg.setWindowTitle("SUBSCRIBER NAME ERROR")
        msg.setText("I Did Not Find Anyone to Edit:\n\n"
                    "Please Select a Name from The\n"
                    "Dropdown List To Edit.\n"
                    "No One To Edit...")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def badName(self):
        msg = QMessageBox()
        msg.setWindowTitle("SUBSCRIBER NAME ERROR")
        msg.setText("Please check the Name Entered:\n\n"
                    "The Name is either too Short or'\n"
                    "you have entered spaces only\n"
                    "Minimum Name length is 3 char's")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def badEmail(self):
        msg = QMessageBox()
        msg.setWindowTitle("EMAIL ADDRESS ERROR")
        msg.setText("Please check the Email Address:\n\n"
                    "It needs to be 'Name@dom.???.???'\n"
                    "E.G. bvsoftware@bvsoft.com")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def doit(self):  # Time loop called every second on Main window
        sd = Set_Stardate()
        starDate = sd
        pbNum = self.getPBNum()
        self.ui.progressBar.setProperty("value", pbNum)
        self.ui.lcdNumber.setProperty("value", starDate)

    def getPBNum(self):
        pbNum = find_Month_Num(self.nextPubDate)
        return pbNum

    def start(self):
        self.timer.start()  # #

    def stop(self):
        self.timer.stop()

    def openMW(self):
        self.nextIssueNumber = 1
        self.dblen = len(Subscribers)
        self.Main_UI = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.Main_UI)

        self.ui.pushButton_Lock.clicked.connect(self.lockClicked)
        self.ui.pushButton_CloseApp.clicked.connect(exitClick)
        self.ui.pushButton_AddSubs.clicked.connect(self.addSubs)
        # self.ui.pushButton_MagDates.clicked.connect(self.issueMagazine)
        self.ui.pushButton_IssueMag.clicked.connect(self.issueMagazine)
        self.nextIssueNumber = (issue.next_Issue(self.nextIssueNumber))  # get from def issue
        self.ui.label_NextIssueNum.setText(str(self.nextIssueNumber))
        now = datetime.datetime.now()
        starDate = getStarDate()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.start()
        self.timer.timeout.connect(self.doit)
        allIssues = getListIssues()
        self.ui.pushButton_NotActive.clicked.connect(self.listNotActiveSubs)
        self.ui.pushButton_LastIssue.clicked.connect(self.listLastIssueSubs)
        self.ui.pushButton_Active.clicked.connect(self.listActiveSubs)
        self.ui.pushButton_ListSubs.clicked.connect(self.listSubs)
        self.ui.pushButtonEdit.clicked.connect(self.editButtonClick)
        self.ui.pushButton_MagDates.clicked.connect(self.magDatesClick)
        self.ui.textEdit.setText(allIssues)
        monthNow = now.month
        month = find_month(monthNow)  # import getMonth.py to return month as string, pass in month a number
        self.ui.label_monthNow.setText(str(month) + " >")
        # need to get next issue month
        self.nextPublish = monthNow
        self.nextPubDate = (issue.get_Next_Issue_Month(self.nextPublish))
        self.ui.label_Publish.setText("< " + str(self.nextPubDate))
        self.ui.label_NumSubs.setText("< SUBSCRIBERS in Database of " + str(self.dblen))
        self.active_Subscribers()
        self.ui.label_SubsCount.setText(str(self.totActiveSubs))
        self.ui.pushButton_Active.setEnabled(False)
        self.ui.pushButton_LastIssue.setEnabled(False)
        self.ui.pushButton_NotActive.setEnabled(False)
        self.ui.pushButtonEdit.setEnabled(False)
        self.ui.comboBox.currentIndexChanged.connect(self.subscriberSelected)
        self.Main_UI.show()

        LogOnUI.close()

    def issueMagazine(self):  # open issue window
        # print("issue Magazine")
        self.stop()
        self.Main_UI.close()
        self.issue_Magazine_window()

    def magDatesClick(self):
        allIssues = getListIssues()
        self.ui.textEdit.setText(allIssues)

    def editButtonClick(self):
        selectedSubs = self.ui.comboBox.currentText()
        if len(selectedSubs) < 3:
            self.noSelection()
        else:
            selectedSubs = self.ui.comboBox.currentText()
            for rownum in Subscribers:
                if selectedSubs == rownum[1]:
                    thisSubsEmail = rownum[0]
                    self.editSubscriber(rownum)

    #
    #####################################################################################################
    #               Issue Magazine

    def issue_Magazine_window(self):
        nid = getNextIssueDate()  # get nid
        self.rbtimer = QTimer()  # timer checks if radiobutton checked
        self.rbtimer.setInterval(1000)
        self.rbtimer.start()
        self.rbtimer.timeout.connect(self.checkrbtimer)

        self.IssueMagWindow = QtWidgets.QMainWindow()  # setup ui
        self.ui = Ui_IssueMagWindow()
        self.ui.setupUi(self.IssueMagWindow)
        self.ui.lcdNumber.setProperty("value", nid)  # next issue date
        self.ui.pushButton_Lock.clicked.connect(self.lockClicked)  # Buttons
        self.ui.pushButton_CloseApp.clicked.connect(exitClick)
        self.ui.pushButton_AddSubs.clicked.connect(self.backtoAddSubs)
        self.ui.pushButton_MagDates.clicked.connect(self.magDates)  # need to stop rdtimer
        self.ui.pushButton_ListSubs.clicked.connect(self.backtoMW)
        self.ui.pushButtonFindIssue.clicked.connect(self.find_Issue)
        self.ui.pushButtonSendNow.clicked.connect(self.send_Now)
        # set label with next publish date
        self.ui.label_IssueMonthTitle.setText(str(self.nextPubDate))

        # populate combo with issue numbers
        self.populateComboIssues()


        self.IssueMagWindow.show()

    def find_Issue(self):
        pass

    def send_Now(self):
        pass

    def magDates(self):
        # self.rbtimer.stop()
        self.ui.radioButtonNone.setChecked(True)
        self.magDatesClick()

    def checkrbtimer(self):  # see if or which radio button selected
        line = "Sending This Issue To\n\n"
        if self.ui.radioButtonAll.isChecked():
            linesubs = getListActiveSubscribers()
            line = line + linesubs
            self.ui.textEdit.setText(line)
        if self.ui.radioButtonLast.isChecked():
            linesubs = getListLISubscribers()
            line = line + linesubs
            self.ui.textEdit.setText(line)
        if self.ui.radioButtonNot.isChecked():
            linesubs = getListNASubscribers()
            line = line + linesubs
            self.ui.textEdit.setText(line)
        if self.ui.radioButtonEveryone.isChecked():
            linesubs = getListSubscribers()
            line = line + linesubs
            self.ui.textEdit.setText(line)

    def populateComboIssues(self):  # combobox = Issue Numbers
        self.ui.comboBox.clear()
        for row in issuesList:
            self.ui.comboBox.addItem(row[0])
        comboIndex = self.nextIssueNumber
        lastIssue = comboIndex - 1
        self.ui.comboBox.setCurrentIndex(lastIssue-1)

        data = get_Metadata(lastIssue)
        p1text = extract_pg1_text(lastIssue)
        info = f"Last Issue was {str(lastIssue)} Created on {str(data.creation_date)}\n" \
                f"By {str(data.author)}\n" \
                f"Using {str(data.creator)}\n" \
                f"\n SNIPPET FROM FRONT COVER \n\n{p1text}"

        self.ui.textEdit.setText(info)

    def backtoMW(self):
        self.rbtimer.stop()
        self.IssueMagWindow.close()
        self.openMW()
        self.listSubs()

    def backtoAddSubs(self):
        self.IssueMagWindow.close()
        self.addSubs()

    # ##########################################################################################################
    #         EDIT SUBS UI

    def editSubscriber(self, rownum):
        self.editing = rownum  # self.editing holds list of values for selected name
        self.Main_UI.close()
        self.stop()
        self.EditSubs = QtWidgets.QMainWindow()
        self.ui = Ui_EditSubsWindow()
        self.ui.setupUi(self.EditSubs)
        self.ui.pushButtonExit.clicked.connect(self.closeEditSubsWin)
        self.ui.pushButtonDel.clicked.connect(self.deleteSubscriber)
        self.ui.pushButtonAddNew.clicked.connect(self.applyClick)
        self.ui.lineEditName.setText(rownum[1])
        self.ui.lineEditEmail.setText(rownum[0])
        self.ui.labelNextPubDate.setText(str(self.nextPubDate))

        self.EditSubs.show()

    def applyClick(self):
        subsYears = str(self.ui.spinBoxYears.value())
        firstIssue = str(self.ui.spinBoxFirstIssue.value())
        thisSubsName = self.editing[1]  # self.editing is from DB
        sureYN = QMessageBox()
        sureYN.setWindowTitle("CONFIRM EDIT")
        sureYN.setText(f"Are you sure you want to do this?\n\n"
                       f"{self.editing[1]} Will Be Saved as\n"
                       f"{self.editing[0]}\n"
                       f"Subscription Length {subsYears} Year(s)\n"
                       f"from Issue {firstIssue}")
        sureYN.setIcon(QMessageBox.Question)
        sureYN.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        sureYN.setDefaultButton(QMessageBox.No)
        sureYN.buttonClicked.connect(self.apply_popup_button)
        x = sureYN.exec_()

    def apply_popup_button(self, i):
        yn = str(i.text())
        if yn == "&Yes":
            Subscribers.remove(self.editing)  # remove current value
            self.checkInputs()  # add subs if All ok
            self.closeEditSubsWin()

    def deleteSubscriber(self):
        self.okToDelete = False

        self.ui.pushButtonDel.setEnabled(False)
        sureYN = QMessageBox()
        sureYN.setWindowTitle("ARE YOU SURE?")
        sureYN.setText(f"Are you sure you want to do this?\n\n"
                       f"{self.editing[1]} Will Be DELETED\n"
                       f"THIS CAN NOT BE UNDONE")
        sureYN.setIcon(QMessageBox.Question)
        sureYN.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        sureYN.setDefaultButton(QMessageBox.No)
        sureYN.buttonClicked.connect(self.popup_button)
        x = sureYN.exec_()

        # self.Main_UI.show()
        if self.okToDelete:
            self.closeEditSubsWin()
        else:
            self.ui.pushButtonDel.setEnabled(True)

    def popup_button(self, i):
        yn = str(i.text())
        if yn == "&Yes":
            msg = QMessageBox()
            msg.setWindowTitle("SUBSCRIBER DELETED")
            msg.setText(f"Subscriber {self.editing[1]} DELETED:\n\n"
                        "This Means They Will No Longer'\n"
                        "Receive O. L. M.\n"
                        "Removed From Database")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            Subscribers.remove(self.editing)
            self.saveSubscribers()
            self.okToDelete = True

    def closeEditSubsWin(self):
        self.openMW()
        self.EditSubs.close()
        self.start()

    #                                      END EDIT UI
    ############################################################################################
    #                                     MAIN WINDOW
    def subscriberSelected(self):
        selected = self.ui.comboBox.currentText()
        selected = str(selected)
        if selected == "List Subs":
            line = getListSubscribers()
            self.ui.textEdit.setText(line)
        line = f"Details for Selected Subscriber {selected}\n\n"
        n = "Name"
        e = "Email"
        s = "Subscription"
        fi = "First Issue"
        li = "Last Issue"
        for row in Subscribers:
            if row[5] == "Y":
                status = "\tActive Subscriber"
            elif row[5] == "L":
                status = f"\tNext Issue is LAST ISSUE {selected} will receive"
            else:
                status = f"\t{selected} is NOT an Active Subscriber\n" \
                         f"\tThe last Issue they received was Issue {row[4]}\n"
            if selected == row[1]:
                lastIssue = row[4]
                firstIssue = row[3]
                for i in issuesList:
                    if i[0] == lastIssue:
                        lastDate = i[3]
                    if i[0] == firstIssue:
                        firstDate = i[3]
                line = line + f"\t{n.ljust(30, '.')} {selected}\n" \
                              f"\t{e.ljust(31, '.')} {row[0]}\n" \
                              f"\t{s.ljust(28, '.')} {row[2]} Year(s)\n" \
                              f"\t{fi.ljust(30, '.')} {row[3]} on {firstDate}\n" \
                              f"\t{li.ljust(30, '.')} {row[4]} on {lastDate}\n\n" \
                              f"{status}\n"
                self.ui.textEdit.setText(line)

    def active_Subscribers(self):  # Find Active (Y): Last Issue (L): Not Active (N)
        self.totActiveSubs = 0
        subsActive.clear()  # Clear the lists before adding
        subsLastIssue.clear()
        subsNotActive.clear()
        for row in Subscribers:  # update to set [5] to Y N or L
            if row[4] > str(self.nextIssueNumber):
                row[5] = "Y"
                self.totActiveSubs += 1  # len(subsActive) ?
                subsActive.append(row)

            elif row[4] == str(self.nextIssueNumber):
                row[5] = "L"
                self.totActiveSubs += 1
                subsLastIssue.append(row)
                subsActive.append(row)
            else:
                row[5] = "N"
                subsNotActive.append(row)

    def listNotActiveSubs(self):
        line = getListNASubscribers()
        self.populateComboNotActive()
        self.ui.textEdit.setText(line)
        self.ui.pushButton_Active.setEnabled(True)
        self.ui.pushButton_LastIssue.setEnabled(True)
        self.ui.pushButton_NotActive.setEnabled(True)

    def listLastIssueSubs(self):
        line = getListLISubscribers()
        self.populateComboLast()
        self.ui.textEdit.setText(line)
        self.ui.pushButton_Active.setEnabled(True)
        self.ui.pushButton_LastIssue.setEnabled(True)
        self.ui.pushButton_NotActive.setEnabled(True)

    def listSubs(self):
        line = getListSubscribers()
        self.populateCombo()
        self.ui.textEdit.setText(line)
        self.ui.pushButton_Active.setEnabled(True)
        self.ui.pushButton_LastIssue.setEnabled(True)
        self.ui.pushButton_NotActive.setEnabled(True)
        self.ui.pushButtonEdit.setEnabled(True)

    def listActiveSubs(self):
        line = getListActiveSubscribers()
        self.populateComboActive()
        self.ui.textEdit.setText(line)
        self.ui.pushButton_Active.setEnabled(True)
        self.ui.pushButton_LastIssue.setEnabled(True)
        self.ui.pushButton_NotActive.setEnabled(True)

    def populateComboNotActive(self):  # combobox = Not Active Subscribers
        self.ui.comboBox.clear()
        for row in subsNotActive:
            self.ui.comboBox.addItem(row[1])

    def populateComboLast(self):  # combobox = last issue Subscribers
        self.ui.comboBox.clear()
        for row in subsLastIssue:
            self.ui.comboBox.addItem(row[1])

    def populateCombo(self):  # combo = All
        self.ui.comboBox.clear()
        for row in Subscribers:
            self.ui.comboBox.addItem(row[1])

    def populateComboActive(self):  # combo = Active Subscribers
        self.ui.comboBox.clear()
        for row in subsActive:
            self.ui.comboBox.addItem(row[1])

    def lockClicked(self):
        self.Main_UI.close()
        LogOnUI.show()

    #               End Main UI Window
    #########################################################################################
    #               About Window
    def openAbout(self):
        self.About_UI = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.About_UI)
        LogOnUI.close()
        self.About_UI.show()
        self.aboutInfo()
        self.ui.pushButtonAboutExit.clicked.connect(self.aboutExit)

    def aboutInfo(self):  # text shown in the About window
        self.ui.textEditAbout.setText(
            "OLM - LCARS System Software designed for"
            "(Outer Limits Magazine by BVSoftware - OPE"
            "\n\n"
            "Data File OLMIssueDates.csv:\n"
            " data is Issue numbers and dates.\n"
            "\nThere is data in the file to last until Feb 2028\n"
            "Edit this csv to extend this time\n"
            "Subscribers.csv is data. keep same format"
        )

    def aboutExit(self):
        self.About_UI.close()
        LogOnUI.show()

    #                               End About
    ###############################################################################################
    #                               UI setup - LOG ON Window
    #                               pushbutton.connects set below
    def setupUi(self, LogOnUI):
        LogOnUI.setObjectName("LogOnUI")
        LogOnUI.resize(1000, 629)
        LogOnUI.setMinimumSize(QtCore.QSize(1000, 500))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        LogOnUI.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/OLM Alien.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LogOnUI.setWindowIcon(icon)
        LogOnUI.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(LogOnUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setStyleSheet("background-image: url(:/windows/MainLogOntop.png);\n"
                                   "background-repeat: no-repeat;\n"
                                   "background-position: center;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 439, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.pushButton_LogIn = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_LogIn.setMinimumSize(QtCore.QSize(152, 70))
        self.pushButton_LogIn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_LogIn.setStyleSheet("background-image: url(:/Buttons/LogInBTN.png);\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "background-repeat: no-repeat;\n"
                                            "background-position: center;")
        self.pushButton_LogIn.setText("")
        self.pushButton_LogIn.setObjectName("pushButton_LogIn")
        self.pushButton_LogIn.clicked.connect(self.openMW)

        self.horizontalLayout.addWidget(self.pushButton_LogIn)
        self.pushButton_Exit = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_Exit.setMinimumSize(QtCore.QSize(152, 70))
        self.pushButton_Exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_Exit.setStyleSheet("background-image: url(:/Buttons/ExitBTN.png);\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "background-repeat: no-repeat;\n"
                                           "background-position: center;")
        self.pushButton_Exit.setText("")
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.pushButton_Exit.clicked.connect(exitClick)

        self.horizontalLayout.addWidget(self.pushButton_Exit)
        self.pushButton_About = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_About.setMinimumSize(QtCore.QSize(152, 70))
        self.pushButton_About.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_About.setStyleSheet("background-image: url(:/Buttons/AboutBTN.png);\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "background-repeat: no-repeat;\n"
                                            "background-position: center;")
        self.pushButton_About.setText("")
        self.pushButton_About.setObjectName("pushButton_About")
        self.pushButton_About.clicked.connect(self.openAbout)

        self.horizontalLayout.addWidget(self.pushButton_About)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 41))
        self.frame.setStyleSheet("background-image: url(:/windows/bottombar.png);\n"
                                 "background-color: rgb(0, 0, 0);\n"
                                 "background-repeat: no-repeat;\n"
                                 "background-position: center;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        LogOnUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LogOnUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        LogOnUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LogOnUI)
        self.statusbar.setObjectName("statusbar")
        LogOnUI.setStatusBar(self.statusbar)

        self.retranslateUi(LogOnUI)
        QtCore.QMetaObject.connectSlotsByName(LogOnUI)

    def retranslateUi(self, LogOnUI):
        _translate = QtCore.QCoreApplication.translate
        LogOnUI.setWindowTitle(_translate("LogOnUI", "OLM - Library Computer Access/Retrieval System"))
        self.pushButton_LogIn.setToolTip(_translate("LogOnUI", "Log In"))
        self.pushButton_Exit.setToolTip(_translate("LogOnUI", "Exit - Quit"))
        self.pushButton_About.setToolTip(_translate("LogOnUI", "About OLM-LCARS"))


#                           End Logon UI
#########################################################################################
#                           Magazine ISSUE - Get details
class Issues(object):

    def __init__(self):
        self.nextmonth = 2
        self.next_Issue_Month = 0
        self.next_Issue_Number = 1
        self.yearnow = None
        self.monthnow = 1
        self.mcount = 0
        self.ycount = 0

        self.evenBool = True

    def next_Issue(self, nextIssueNumber):

        self.ycount = 0
        now = datetime.datetime.today()
        self.yearnow = now.year
        self.monthnow = now.month
        # self.monthnow = 10           # set this to test
        if (self.monthnow % 2) == 0:
            self.evenBool = True
        else:
            # odd number month
            self.evenBool = False
        if self.evenBool:  # Even number month
            for row in issueYear:
                if str(issueYear[self.ycount]) == str(self.yearnow):
                    if issueMonth[self.ycount] == str(self.monthnow):
                        self.next_Issue_Number = self.ycount
                self.ycount = self.ycount + 1
            nextIssueNumber = self.next_Issue_Number
            nextIssueNumber = nextIssueNumber + 2
            return nextIssueNumber
        else:
            self.monthnow = self.monthnow + 1
            for row in issueYear:
                if str(issueYear[self.ycount]) == str(self.yearnow):
                    if issueMonth[self.ycount] == str(self.monthnow):
                        self.next_Issue_Number = self.ycount
                self.ycount = self.ycount + 1
            nextIssueNumber = self.next_Issue_Number
            nextIssueNumber = nextIssueNumber + 1
            # print(nextIssueNumber)
            return nextIssueNumber

    def get_Next_Issue_Month(self, nextPublish):
        thismonth = nextPublish
        # thismonth = 8         # set this to test
        self.nextmonth = nextPublish
        if (thismonth % 2) == 0:
            if thismonth == 12:
                thismonth = 0
            self.nextmonth = thismonth + 2
        else:
            self.nextmonth = thismonth + 1
        month = find_month(int(self.nextmonth))
        return month


#
############################################################################################
#                           Lists
issueMonth = []  # needed
issueYear = []  # needed
issueDate = []  # holds YEARS only
issuesList = []  # All info: issueNumb, Month, Year, Date
Subscribers = []  # All info: Email, Name, Years, FirstIssue, LastIssue, Active(Y,L,N)
subsActive = []  # List All Active subs from Subscribers (Active = Y)
subsLastIssue = []  # List All who are on Last issue
subsNotActive = []  # List All who are NO LONGER Active
f = open('OLMIssueDates.csv', 'r')  # Issues
readList = csv.reader(f)
header = next(readList)
for row in readList:
    issuesList.append(row)
    # issueNumber.append(row[0])
    issueMonth.append(row[1])  # issueMonth and issueYear used to
    issueYear.append(row[2])  # get next issue number via date now
    # issueDate.append(row[3])
S = open('Subscribers.csv', 'r')
readList = csv.reader(S)
# header = next(readList)
num = 0
for row in readList:
    Subscribers.append(row)
    num = num + 1
db = num  # num replaced by len() insure is num still used?

#######################################################################################

if __name__ == "__main__":
    import sys

    issue = Issues()
    app = QtWidgets.QApplication(sys.argv)
    LogOnUI = QtWidgets.QMainWindow()
    ui = Ui_LogOnUI()
    ui.setupUi(LogOnUI)
    LogOnUI.show()
    sys.exit(app.exec_())
