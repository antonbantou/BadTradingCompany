from tkinter import *
from tkinter import messagebox
import json
from PIL import ImageTk,Image
import requests
import csv
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
import subprocess

#Reminder: gotta install Pillow, otherwise images won't work / the program won't. Maybe set up an installation bs?
#dont forget to download libs: requests, pandas, matplotlib


#recieving bitcoin prices from the coincap api
    


root = Tk()
loginframe = Frame(root)
loginframe.pack()
style.use("ggplot")

#Default setup for window size and name
root.title("Bad Trading Incorporated - Trader App")
root.iconbitmap("logo.ico")

#Reminder: it really dislikes .packing on the same line. Just do it in two steps.

#Banner settings
fulllogoimg = ImageTk.PhotoImage(Image.open("logo.png"))
logoimg = ImageTk.PhotoImage(Image.open("logopicture.png"))
talllogoimg = ImageTk.PhotoImage(Image.open('talllogo.png'))
bannerLabel = Label(loginframe, image = fulllogoimg)
bannerLabel.pack()

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


#main screen - trading, prices, wallet, etc
def animate(i):
    graph_data = open('bitcoin-usd.csv', 'r').read()
    dataList = graph_data.split('\n')
    xList = []
    yList = []
    flag = 0
    for line in dataList:
        if flag == 0:
            flag = 1
            pass
        elif len(line) > 1:
            x, y = line.split(',')
            xList.append(int(x))
            yList.append(float(y))
    a.clear()
    a.plot(xList, yList)

def prices():
    url = "http://api.coincap.io/v2/assets/bitcoin/history?interval=m1"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers = headers, data = payload)

    json_data = json.loads(response.text.encode("utf8"))
    bitcoin_data = json_data["data"]

    #Turning the raw json data into a dataframe so matlab doesnt piss its pants
    bitcoindf = pd.DataFrame(bitcoin_data)


    #Get rid of time column, obsolete when we have date
    bitcoindf = pd.DataFrame(bitcoin_data, columns=['time', 'priceUsd'])

    #saving data to the csv
    bitcoindf.to_csv("bitcoin-usd.csv", index=False)

#Drawing the main graph after login
def mainscreen():
    prices()
    
    canvas = FigureCanvasTkAgg(f, root)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 1, column = 2)

    bannLabel = Label(root, image = talllogoimg)
    bannLabel.grid(row = 1, column = 1)
    
    graph_data = pd.read_csv('bitcoin-usd.csv')
    finaldata = float(graph_data['priceUsd'].iloc[-1:])

    priceLabel = Label(root, text = "Current Price of BTC: " + str(finaldata))
    priceLabel.config(font = ('Helvetica bold', 15))
    priceLabel.grid(row = 2, column = 2)


#Login function
def login():
    flag = 0
    user = entryFieldUsername.get()
    password = entryFieldPassword.get()
    accountdata = open("accounts.txt", "r")
    for line in accountdata:
        info = line.split(",")
        veriuser = info[0]
        veripass = info[1]
        #Fuck if I know why, but for some god forsaken reason appending also adds spaces to the end of the password.
        #For this reason, we simply calculate with less of the string. I am not fixing the original issue.
        if (veriuser == user) and (veripass[:-1] == password):
            flag = 1
    if flag == 0:
        messagebox.showerror("Error", "Login details were incorrect")
    else:
        loginframe.destroy()
        mainscreen()
    accountdata.close()


#Signup function
def signup():
    signupWindow = Toplevel()
    signupWindow.grab_set()
    signupBanner = Label(signupWindow, image = logoimg)
    signupBanner.pack()

    signupUsername = Entry(signupWindow)
    signupUsername.pack()
    signupUsername.insert(0, "Username")

    signupPassword = Entry(signupWindow)
    signupPassword.pack()
    signupPassword.insert(0, "Password")

    signupVerificationPassword = Entry(signupWindow)
    signupVerificationPassword.pack()
    signupVerificationPassword.insert(0, "Re-Type Password")


    completeSignupButton = Button(signupWindow, text = "Create Account", command = lambda: completesignup(signupUsername.get(), signupPassword.get(), signupVerificationPassword.get(), signupWindow))
    completeSignupButton.pack()

#Verifying and Saving signup details
def completesignup(username, password, verificationPassword, signupWindow):
    if verificationPassword != password:
        messagebox.showerror("Error", "Passwords were not the same")
    else:
        signupWindow.destroy()
        accountdata = open("accounts.txt", "a")
        accountdata.write(username + "," + password + "\n")
        accountdata.close()

#Log in / signup fields
entryFieldUsername = Entry(loginframe)
entryFieldUsername.pack()
entryFieldUsername.insert(0, "Username")


entryFieldPassword = Entry(loginframe, show = "*")
entryFieldPassword.pack()
entryFieldPassword.insert(0, "Password")


 
#Log in / signup buttons
loginButton = Button(loginframe, text = "Log in", command = login)
loginButton.pack()

signupButton = Button(loginframe, text = "Make New Account", command = signup)
signupButton.pack()

ani = animation.FuncAnimation(f, animate, interval = 60000)
root.mainloop()