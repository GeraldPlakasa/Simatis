from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for
import karakter, atexit, pickle, random
import pandas as pd
import numpy as np
from collections import defaultdict
import system as systm

day = 1
month = 1
year = 1
day_temp = 1

# def sensor():
#     global day
#     day += 1
#     print("Scheduler is alive!")
#     # print(day)

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(sensor,'interval',seconds=10)
# sched.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: sched.shutdown())

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/karakter")
def home_v():
    global day
    global day_temp
    global month
    day += 1

    karakter_list_df = systm.load_karakter()
    karakter_list = systm.setKarakterList(karakter_list_df.copy())

    if day >= day_temp:
        karakter_list = systm.daily(karakter_list)
        systm.save_karakter(karakter_list)
        day_temp += 1

    if day > 30:
        month += 1
        day = 1
        day_temp = 1

    print(str(day)+"-"+str(month))
    
    return render_template("index_v.html", day=day, karakter_list=karakter_list, enumerate=enumerate)

@app.route("/addpeople")
def addPeople():
    karakter_list_df = systm.load_karakter()
    karakter_list = systm.setKarakterList(karakter_list_df.copy())
    keluarga_list = []
    systm.createPeople(karakter_list, keluarga_list)
    print("Add People Success")

    return redirect('/karakter')

@app.route("/setpeople")
def setPeople():
    karakter_list = []
    keluarga_list = []
    systm.createPeople(karakter_list, keluarga_list)
    print("Set People Success")
    
    return redirect('/karakter')

@app.route("/setking")
def setKing():
    karakter_list_df_temp = systm.load_karakter()
    karakter_list = systm.setKarakterList(karakter_list_df_temp)
    karakter_list_df = karakter_list_df_temp.loc[karakter_list_df_temp["role"] == "Fighter"]
    karakter_list = systm.setking(karakter_list_df_temp, karakter_list_df, karakter_list)

    systm.save_karakter(karakter_list)

    return redirect('/karakter')

@app.route("/game")
def game():
    
    return render_template("game.html")