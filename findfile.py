#  Copyright (c) 2023. Bro Video Software.
from PyQt5.QtWidgets import QFileDialog
import os


def findIssue(self):
    fname = QFileDialog.getOpenFileName(self, "Locate Issue to Add", "", "All Files (*.*);;pdf (*.pdf)")

    #print(fname)
    return fname


fname = findIssue(self=None)
print(fname)
# print(os.getcwd())
p = os.getcwd()
os.chdir(p + "/Mags")
n = os.getcwd()
print("n")
print(n)
issuesInDir = os.listdir()
print(issuesInDir)
print("m")
# c = os.curdir
# print(c)
