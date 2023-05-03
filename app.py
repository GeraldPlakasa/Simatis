from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for
import karakter, atexit, pickle, random
import pandas as pd
import numpy as np
from collections import defaultdict
import system as systm
import pickle

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
    karakter_df = systm.load_karakter()
    return render_template("index.html", enumerate=enumerate, df=karakter_df, systm=systm)

@app.route("/karakter")
def home_v():

    karakter_df = systm.load_karakter()
    karakter_list = systm.set_karakter_list(karakter_df.copy())
    karakter_list_new = systm.daily_system(karakter_df, karakter_list)

    return render_template("index_v.html", day=day, karakter_list=karakter_list_new, enumerate=enumerate)

@app.route("/addpeople")
def addPeople():
    karakter_df = systm.load_karakter()
    karakter_list = systm.set_karakter_list(karakter_df.copy())
    keluarga_list = []
    systm.create_people(karakter_list, keluarga_list)
    print("Add People Success")

    return redirect('/karakter')

@app.route("/setpeople")
def setPeople():
    karakter_list = []
    keluarga_list = []
    systm.create_people(karakter_list, keluarga_list)
    print("Set People Success")
    systm.reset_time()
    setKing()
    
    return redirect('/karakter')

@app.route("/setKing")
def setKing():
    karakter_df = systm.load_karakter()
    karakter_list = systm.set_karakter_list(karakter_df)
    karakter_df_fighter = karakter_df.loc[karakter_df["role"] == "Fighter"]
    karakter_list = systm.set_king(karakter_df, karakter_df_fighter, karakter_list)

    systm.save_karakter(karakter_list)
    print("Set King Success")

    return redirect('/karakter')

@app.route("/game")
def game():
    return render_template("game.html")