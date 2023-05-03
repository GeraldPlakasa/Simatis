"""
Script by : Gerald Plakasa
"""

import karakter, atexit, pickle, random
import pandas as pd
import numpy as np
from collections import defaultdict
import re, os
from datetime import datetime

food = {"Rendang":[20,62], "Sate":[15,57], "Nasi Goreng":[10,52], 
           "Steak":[22,64], "Bakwan":[5,47], "Ayam Goreng":[7,49]}

""" Daily Needs """

def daily_system(karakter_df, karakter_list):

    TIME_FILE = 'Time.pkl'

    # Load the time variable from the file
    day, month, year, DAY_TEMP = get_time(TIME_FILE)

    # Update the day counter
    day += 1

    # Check if it's time for the daily action
    if day >= DAY_TEMP:
        karakter_list = daily(karakter_list)
        save_karakter(karakter_list)
        DAY_TEMP += 1

    # Check if the month has changed
    if day > 30:
        karakter_list = salary(karakter_list)
        save_karakter(karakter_list)
        day = 1
        month += 1

        # Check if the year has changed
        if month > 12:
            karakter_list = age_up_list(karakter_list)
            dead(karakter_list)
            save_karakter(karakter_list)
            month = 1
            year += 1

        DAY_TEMP = 1

    print(str(day)+"/"+str(month)+"/"+str(year))

    # Update the time variable
    set_time(TIME_FILE, day, month, year)

    return karakter_list

def daily(karakter_list):
    # Calculate average attack of all characters
    average_attack = int(sum(char.atk for char in karakter_list) / len(karakter_list))
    
    # Loop through all characters in the list
    for char in karakter_list:

        char.setSexRole()

        # Set remaining stamina to current stamina of the character
        remaining_stamina = char.stamina
        
        # Continue until the character runs out of stamina
        while(remaining_stamina > 0):
            
            # Make sure the character's hunger is between 0 and 100
            char.batas_hungry = max(0, char.batas_hungry)
            char.batas_hungry = min(100, char.batas_hungry)
            
            # If the character's hunger is low, make them eat
            if char.batas_hungry < 30:
                char.batas_hungry = makan(char)
            else:
                # Calculate the amount of stamina and hunger lost during the activity
                if char.stamina < 25:
                    stamina = char.stamina
                    hungry = 1
                else:
                    stamina = random.randint(25, char.stamina)
                    hungry = random.randint(10, 30)
                
                # Deduct stamina and hunger from the character
                remaining_stamina -= stamina
                char.batas_hungry -= hungry

                # Determine the activity of the character based on their attack and the average attack of all characters
                if char.atk > average_attack:
                    activity = random.randint(0, 100)
                else:
                    activity = random.randint(11, 100)
                
                # Determine the character's activity based on their age and the randomly determined activity
                if char.age < 10:
                    if activity <= 50:
                        do_training(char)
                    else:
                        pass
                else:
                    if activity <= 1:
                        do_foya_foya(char)
                    elif activity <= 6:
                        do_boss_battle(char)
                    elif activity <= 36:
                        do_training(char)
                    elif activity <= 66:
                        do_hunting(char)

    # Return the updated list of characters
    return karakter_list

def gain_exp(karakter, exp_new):
    karakter.exp += exp_new
    if karakter.exp >= karakter.batas_exp:
        level_up(karakter)

def level_up(karakter):
    # Define new stat ranges based on the character's age
    if karakter.age < 10:
        health_range = (20, 60)
        spd_range = (1, 6)
        defend_range = (1, 10)
        atk_range = (1, 10)
        stamina_range = (0, 2)
    else:
        health_range = (50, 100)
        spd_range = (2, 14)
        defend_range = (10, 25)
        atk_range = (10, 25)
        stamina_range = (2, 14)

    # Generate new stats
    health_new = random.randint(*health_range)
    spd_new = random.randint(*spd_range)
    defend_new = random.randint(*defend_range)
    atk_new = random.randint(*atk_range)
    stamina_new = random.randint(*stamina_range)

    # Update the character's stats and level
    karakter.health += health_new
    karakter.spd += spd_new
    karakter.defend += defend_new
    karakter.atk += atk_new
    karakter.stamina += stamina_new

    karakter.level += 1
    karakter.batas_exp += 100
    karakter.exp = 0

def do_training(char):
    if char.age < 10:
        exp_gain = random.randint(2, 10)
    else:
        exp_gain = random.randint(10, 30)
    gain_exp(char, exp_gain)

def do_hunting(char):
    coin_gain = random.randint(50, 100)
    exp_gain = random.randint(5, 40)
    char.coin += coin_gain
    gain_exp(char, exp_gain)

def do_boss_battle(char):
    coin_gain = random.randint(500, 700)
    exp_gain = random.randint(50, 70)
    char.coin += coin_gain
    gain_exp(char, exp_gain)

def do_foya_foya(char):
    coin_loss = random.randint(500, 2000)
    char.coin -= coin_loss

def attack(attacker, defender):
    # Generate random number between 1-100 to determine hit chance
    hit_chance = random.randint(1, 100)
    # If hit chance is below or equal to 20%, attack misses and damage is 0
    if hit_chance <= 20:
        return 0
    else:
        # Calculate damage by multiplying attacker's attack power, defender's defense power,
        # and a random number between 0.75 and 1.25
        damage = attacker.atk * (100 / (100 + defender.defend)) * random.uniform(0.75, 1.25)
        # Generate random number between 1-100 to determine critical hit chance
        critical_chance = random.randint(1, 100)
        # If critical chance is below or equal to 20%, double the damage
        if critical_chance <= 20:
            damage *= 2
        # Return the final damage
        return damage

def makan(char):
    # Get list of available food
    food_list = list(food.keys())

    # Randomly choose a food from the list
    food_choice = random.randint(0, len(food_list)-1)

    # Get the price and energy value of the chosen food
    food_price = food.get(food_list[food_choice])[0]
    food_energy = food.get(food_list[food_choice])[1]

    # Adjust batas_hungry based on the character's age and deduct the cost of the food
    if char.age > 10:
        char.batas_hungry += (food_energy - 30)
        char.coin -= (food_price + 20)
    else:
        char.batas_hungry += food_energy
        char.coin -= food_price

    # Ensure that batas_hungry is between 0 and 100
    char.batas_hungry = max(0, char.batas_hungry)
    char.batas_hungry = min(100, char.batas_hungry)

    return char.batas_hungry

def get_time(TIME_FILE):

    try:
        with open(TIME_FILE, 'rb') as f:
            time = pickle.load(f)
    except FileNotFoundError:
        time = [1, 1, 1]

    day, month, year = time
    DAY_TEMP = day

    return day, month, year, DAY_TEMP

def set_time(TIME_FILE, day, month, year):
    time = [day, month, year]
    with open(TIME_FILE, 'wb') as f:
        pickle.dump(time, f)

def reset_time():
    time = [1, 1, 1]
    with open('Time.pkl', 'wb') as f:
        pickle.dump(time, f)

def age_up_list(karakter_list):
    for char in karakter_list:
        char.age += 1
    return karakter_list

def salary(karakter_list):
    # Define a dictionary with the corresponding coins for each role
    coin_dict = {
        "King": 2500,
        "Queen": 2500,
        "Panglima": 1000,
        "Prajurit": 500,
    }

    # Loop over each character in the list
    for char in karakter_list:
        # Get the corresponding coin value for the character's role, defaulting to 100
        coin_value = coin_dict.get(char.role, 100)
        # Add the coin value to the character's coin attribute
        char.coin += coin_value

    return karakter_list

def dead(karakter_list):
    # Calculate the probability of random death
    p_random_death = 0.01

    # Calculate the probability of death from old age
    p_old_age_death = 0.05

    # Random death
    if random.random() < p_random_death:
        n_dead = random.randint(1, 5)
        for i in range(n_dead):
            dead_char = random.choice(karakter_list)
            # karakter_list.remove(dead_char)
            print(f"{dead_char.name} Mati Random")

    # Death from old age
    dead_chars = [char for char in karakter_list if char.age >= 100 and random.random() < p_old_age_death]
    for dead_char in dead_chars:
        # karakter_list.remove(dead_char)
        print(f"{dead_char.name} Mati!!!")

""" People Needs """

def create_people(karakter_list, keluarga_list):
    try:
        df_girl = pd.read_csv("nama_girl_temp.csv")
    except:
        df_girl = pd.read_csv("nama_girl.csv")

    try:
        df_boy = pd.read_csv("nama_boy_temp.csv")
    except:
        df_boy = pd.read_csv("nama_boy.csv")

    list_girl = list(df_girl["Name"])
    list_boy = list(df_boy["Name"])

    n = 1000
    
    for i in range(n):
        if i < int(n/2):
            umur = random.randint(15, 40)
        else:
            umur = random.randint(1, 99)
        
        kelamin = random.randint(0, 10)
        if kelamin < 5:
            sex = "Laki-laki"
            nama = random.choices(list_boy)[0]
            list_boy.remove(nama)
        else:
            sex = "Perempuan"
            nama = random.choices(list_girl)[0]
            list_girl.remove(nama)
        karakter_list.append(karakter.Karakter(nama, umur, sex))

    save_karakter(karakter_list)
    save_list(["Name"], list_girl, "list_girl_temp.csv")
    save_list(["Name"], list_boy, "list_boy_temp.csv")
    # save_data(keluarga_list, "keluarga_list.dat")

def duel(karakter_a, karakter_b):

    health_a = karakter_a.health
    health_b = karakter_b.health
    
    # Loop until one character's health reaches zero
    while health_a > 0 and health_b > 0:
        # Determine which character goes first based on their speed
        if karakter_a.spd >= karakter_b.spd:
            # Character A attacks first
            # Subtract damage from Character B's health
            health_b -= karakter_a.attack(karakter_b)
            # If Character B is still alive, Character B attacks
            if health_b > 0:
                # Subtract damage from Character A's health
                health_a -= karakter_b.attack(karakter_a)
        else:
            # Character B attacks first
            # Subtract damage from Character A's health
            health_a -= karakter_b.attack(karakter_a)
            # If Character A is still alive, Character A attacks
            if health_a > 0:
                # Subtract damage from Character B's health
                health_b -= karakter_a.attack(karakter_b)

    # Determine the winner based on which character's health reached zero first
    return karakter_b.name if health_a <= 0 else karakter_a.name

def get_best_person(df_duel_temp, karakter_list=[]):
    # Filter out characters under 10 years old
    df_duel = df_duel_temp[df_duel_temp["age"] >= 10]

    # Create a list of characters eligible for duels
    lis_temp = list(df_duel["name"])
    karakter_list_duel = [char for char in karakter_list if char.name in lis_temp]

    # Run 100 rounds of duels
    for j in range(100):
        random.shuffle(karakter_list_duel)
        for i in range(0,len(karakter_list_duel),2):
            # Duel between two characters
            if(i+1 != len(karakter_list_duel)):
                win_name = duel(karakter_list_duel[i],karakter_list_duel[i+1])

                # Update win and lose count in the dataframe
                if karakter_list_duel[i].name == win_name:
                    win_char = karakter_list_duel[i]
                    lose_char = karakter_list_duel[i+1]
                else:
                    win_char = karakter_list_duel[i+1]
                    lose_char = karakter_list_duel[i]

                df_duel.loc[df_duel['name']==win_name, 'win'] += 1
                df_duel.loc[df_duel['name']==lose_char.name, 'Lose'] += 1

    return df_duel

def set_king(karakter_df, karakter_df_fighter, karakter_list):

    file_name = "Panglima.csv"
    os.remove(file_name)

    while karakter_df_fighter.shape[0] > 1:
        if karakter_df_fighter.shape[0] < 10:
            karakter_list = set_roles(karakter_df_fighter, karakter_df, karakter_list, "Panglima")
        elif karakter_df_fighter.shape[0] < 30:
            karakter_list = set_roles(karakter_df_fighter, karakter_df, karakter_list, "Prajurit")
        karakter_df_fighter['win'] = 0
        karakter_df_fighter['Lose'] = 0
        df_hasil = get_best_person(karakter_df_fighter.copy(), karakter_list)
        if df_hasil.shape[0] == 1:
            break
        df_hasil = df_hasil.sort_values(by=['win'], ascending=False)
        karakter_df_fighter = df_hasil.head(len(df_hasil)//2)
        karakter_df_fighter = karakter_df_fighter.reset_index()
        karakter_df_fighter = karakter_df_fighter.drop("index", axis=1)
        if karakter_df_fighter.shape[0] == 1:
            break
        print("-------------------")
        print(len(karakter_df_fighter))
        print("-------------------")
    if karakter_df_fighter['sex'][0] == "Laki-laki":
        karakter_list = set_roles(karakter_df_fighter, karakter_df, karakter_list, "King")
        print("Set King Success")
    else:
        karakter_list = set_roles(karakter_df_fighter, karakter_df, karakter_list, "Queen")
        print("Set Queen Success")

    return karakter_list

def set_roles(karakter_df_fighter, karakter_df, karakter_list, new_role):
    names = karakter_df_fighter["name"].tolist()
    idxs = []
    for name in names:
        idx = karakter_df.name[karakter_df.name == name].index
        idxs.append(idx)
    for idx in idxs:
        karakter_list[idx[0]].role = new_role
    return karakter_list

""" Data Needs """

def load_karakter():
    try:
        data = pd.read_csv("karakter_list.csv")
    except Exception as e:
        print(e)
        data = []
    return data

def save_karakter(karakter_list):

    dd = defaultdict(list)
    karakter_list_temp = [karakter.save() for karakter in karakter_list]
    for d in karakter_list_temp: # you can list as many input dicts as you want here
        for key, value in d.items():
            dd[key].append(value)
    df = pd.DataFrame(dd)
    df.to_csv("karakter_list.csv")

def set_karakter_list(karakter_list_df):
    karakter_list = []
    for i in range(karakter_list_df.shape[0]):
        karakter_list.append(karakter.Karakter("",0,"", data=karakter_list_df, row=i))
    return karakter_list

def save_list(columns, datas, nama_file):
    df_temp = pd.DataFrame(np.array(datas), columns=columns)
    df_temp.to_csv(nama_file)

""" Dashboard Needs """

def get_jumlah_penduduk(df):
    return re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(df.shape[0]))

def get_jumlah_roles_leader(df):
    hasil = df['name'].loc[df['role']=="Queen"]
    hasil_2 = df['name'].loc[df['role']=="King"]
    return hasil.shape[0] + hasil_2.shape[0]
def get_jumlah_roles_penduduk(df):
    hasil = df['name'].loc[df['role']=="Penduduk"]
    return hasil.shape[0]
def get_jumlah_roles_fighter(df):
    hasil = df['name'].loc[df['role']=="Fighter"]
    return hasil.shape[0]
def get_jumlah_roles_panglima(df):
    hasil = df['name'].loc[df['role']=="Panglima"]
    return hasil.shape[0]
def get_jumlah_roles_prajurit(df):
    hasil = df['name'].loc[df['role']=="Prajurit"]
    return hasil.shape[0]

def get_leader_name(df):
    hasil = df['name'].loc[df['role']=="Queen"]
    if hasil.shape[0] > 0:
        return hasil.to_list()[0]
    hasil_2 = df['name'].loc[df['role']=="King"]
    if hasil_2.shape[0] > 0:
        return hasil_2.to_list()[0]

def get_leader_roles(df):
    hasil = df['name'].loc[df['role']=="Queen"]
    if hasil.shape[0] > 0:
        return "Queen"
    hasil_2 = df['name'].loc[df['role']=="King"]
    if hasil_2.shape[0] > 0:
        return "King"

def get_leader_atribut(df):
    hasil = df['name'].loc[df['role']=="Queen"]
    if hasil.shape[0] == 1:
        return get_queen_atribut(df)

    hasil_2 = df['name'].loc[df['role']=="King"]
    if hasil_2.shape[0] == 1:
        return get_king_atribut(df)

def get_king_atribut(df):
    df_hasil = df.loc[df['role']=="King"]
    df_hasil = df_hasil.reset_index()

    atks = df_hasil['atk'][0]
    defs = df_hasil['defend'][0]
    healths = df_hasil['health'][0]
    spds = df_hasil['spd'][0]
    staminas = df_hasil['stamina'][0]

    return [atks, defs, healths, spds, staminas]

def get_queen_atribut(df):
    df_hasil = df.loc[df['role']=="Queen"]
    df_hasil = df_hasil.reset_index()

    atks = df_hasil['atk'][0]
    defs = df_hasil['defend'][0]
    healths = df_hasil['health'][0]
    spds = df_hasil['spd'][0]
    staminas = df_hasil['stamina'][0]

    return [atks, defs, healths, spds, staminas]

def get_rich_name(df):
    idx = df['coin'].nlargest(1).index[0]
    return df.loc[idx, 'name']
def get_rich_coin(df):
    idx = df['coin'].nlargest(1).index[0]
    return re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(df.loc[idx, 'coin']))

def get_anak_count(df):
    hasil = df.loc[df['sex_role']=="Anak-anak"]
    return hasil.shape[0]
def get_remaja_count(df):
    hasil = df.loc[df['sex_role']=="Remaja"]
    return hasil.shape[0]
def get_dewasa_muda_count(df):
    hasil = df.loc[df['sex_role']=="Dewasa Muda"]
    return hasil.shape[0]
def get_dewasa_tua_count(df):
    hasil = df.loc[df['sex_role']=="Dewasa Tua"]
    return hasil.shape[0]
def get_lansia_count(df):
    hasil = df.loc[df['sex_role']=="Lansia"]
    return hasil.shape[0]

def get_datetime(df):
    return datetime.now()

def get_best_panglima(df):
    # Filter dataframe to only include Panglima roles and reset the index
    panglima_df = df[df['role']=="Panglima"].reset_index()

    # Get a list of unique karakter from the Panglima dataframe
    karakter_list = set_karakter_list(panglima_df.copy())

    # Add two new columns to the Panglima dataframe to store win and lose counts
    panglima_df['win'] = 0
    panglima_df['Lose'] = 0

    # Get the best Panglima based on their karakter scores
    best_panglima_df = get_best_person(panglima_df.copy(), karakter_list)
    best_panglima_df = best_panglima_df.sort_values(by=['win'])

    # Create a list of Panglima names from the original Panglima dataframe
    panglima_names = panglima_df['name'].to_list()

    # Create two new lists to store the Panglima rankings and timestamps
    panglima_list = [0]*len(panglima_names)
    timestime_list = [datetime.now()]*len(panglima_names)

    # update their rank in the rankings list
    for i, name in enumerate(best_panglima_df['name'].to_list()):
        idx = panglima_names.index(name)
        panglima_list[idx] = i+1

    # Try to load an existing Panglima CSV file
    try:
        df_load = pd.read_csv("Panglima.csv")
        df_load = df_load.drop(["Unnamed: 0"], axis=1)

        # Shift the data in the CSV file down by one row
        for i in range(4):
            df_load["name"+str(i+1)] = df_load["name"+str(i+2)]
            df_load["power"+str(i+1)] = df_load["power"+str(i+2)]
            df_load["timestamp"+str(i+1)] = df_load["timestamp"+str(i+2)]

        # Update the last row in the CSV file with the new Panglima rankings and timestamps
        df_load["name5"] = panglima_names
        df_load["power5"] = panglima_list
        df_load["timestamp5"] = timestime_list

    # If the CSV file does not exist, create a new dataframe with the new Panglima rankings and timestamps
    except:
        df_load = pd.DataFrame({"name1":panglima_names, "power1":[0]*len(panglima_names), "timestamp1":[0]*len(panglima_names),
                                "name2":panglima_names, "power2":[0]*len(panglima_names), "timestamp2":[0]*len(panglima_names),
                                "name3":panglima_names, "power3":[0]*len(panglima_names), "timestamp3":[0]*len(panglima_names),
                                "name4":panglima_names, "power4":[0]*len(panglima_names), "timestamp4":[0]*len(panglima_names),
                                "name5":panglima_names, "power5":panglima_list, "timestamp5":timestime_list})
    df_load.to_csv("Panglima.csv")
    return "Rank"

def get_best_panglima_name(df):
    df_load = pd.read_csv("Panglima.csv")

    list_df = []
    for i in range(df_load.shape[0]):
        list_df.append({"name":df_load["name1"][i], 
                        "power1":df_load["power1"][i],
                        "power2":df_load["power2"][i],
                        "power3":df_load["power3"][i],
                        "power4":df_load["power4"][i],
                        "power5":df_load["power5"][i]})
    return list_df
def get_best_panglima_time(df):
    df_load = pd.read_csv("Panglima.csv")

    list_df = []
    for i in range(df_load.shape[0]):
        list_df.append({"timestamp1":df_load["timestamp1"][i],
                        "timestamp2":df_load["timestamp2"][i],
                        "timestamp3":df_load["timestamp3"][i],
                        "timestamp4":df_load["timestamp4"][i],
                        "timestamp5":df_load["timestamp5"][i]})
    return list_df
