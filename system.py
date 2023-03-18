import karakter, atexit, pickle, random
import pandas as pd
import numpy as np
from collections import defaultdict

makanan = {"Rendang":[20,62], "Sate":[15,57], "Nasi Goreng":[10,52], 
           "Steak":[22,64], "Bakwan":[5,47], "Ayam Goreng":[7,49]}

""" Daily Needs """

def daily(karakter_list):
    for char in karakter_list:
        temp_stamina = char.stamina
        karakter_atk = [char2.atk for char2 in karakter_list]
        rerata_atk = int(sum(karakter_atk)/len(karakter_atk))
        # Di ulang terus sampai stamina habis
        while(temp_stamina > 0):

            if char.batas_hungry < 0:
                char.batas_hungry = 0
            elif char.batas_hungry < 30:
                char.batas_hungry = makan(char)
            elif char.batas_hungry > 100:
                char.batas_hungry = 100
            else:
                if char.stamina < 25:
                    stamina = char.stamina
                    hungry = 1
                else:
                    stamina = random.randint(25, char.stamina)
                    hungry = random.randint(10, 30)
                temp_stamina -= stamina
                char.batas_hungry -= hungry

                if char.atk > rerata_atk:
                    kegiatan = random.randint(0, 100)
                else:
                    kegiatan = random.randint(11, 100)
                
                # Jika umur di bawah 10 hanya latihan jika tidak random latihan atau hunt
                if char.age < 10:
                    if kegiatan <= 50:
                        latihan(char)
                    else:
                        pass
                else:
                    if kegiatan <= 10:
                        boss(char)
                    if kegiatan <= 40:
                        latihan(char)
                    elif kegiatan <= 70:
                        hunt(char)
                    else:
                        pass

    return karakter_list

def ExpUp(karakter, exp_new):
    karakter.exp += exp_new
    if karakter.exp >= karakter.batas_exp:
        levelUp(karakter)

def levelUp(karakter):

    # get new Stats
    if karakter.age < 10:
        health_new = random.randint(20, 60)
        spd_new = random.randint(1, 6)
        defend_new = random.randint(1, 10)
        atk_new = random.randint(1, 10)
        stamina_new = random.randint(0, 2)
    else:
        health_new = random.randint(50, 100)
        spd_new = random.randint(2, 14)
        defend_new = random.randint(10, 25)
        atk_new = random.randint(10, 25)
        stamina_new = random.randint(2, 14)

    # plus new Stats
    karakter.health += health_new
    karakter.spd += spd_new
    karakter.defend += defend_new
    karakter.atk += atk_new
    karakter.stamina += stamina_new

    karakter.level += 1
    karakter.batas_exp += 100
    karakter.exp = 0

def latihan(char):
    if char.age < 10:
          exp_latihan = random.randint(2, 10)
    else:
          exp_latihan = random.randint(10, 30)
    ExpUp(char, exp_latihan)

def hunt(char):
    char.coin += random.randint(50, 100)
    exp_hunt = random.randint(5, 40)
    ExpUp(char, exp_hunt)

def boss(char):
    char.coin += random.randint(500, 700)
    exp_boss = random.randint(50, 70)
    ExpUp(char, exp_boss)

def foyaFoya(char):
    char.coin -= random.randint(500, 2000)

def serang(char, musuh):
    dmg = char.atk*(100/(100+musuh.defend)) * random.uniform(0.75, 1.25)
    critical = random.randint(0, 100)
    miss = random.randint(0, 100)
    if critical <= 20:
          dmg *= 2
    if miss <= 20:
          dmg *= 0
    return dmg

def makan(char):
    keys = list(makanan.keys())
    makan_pilihan = random.randint(0, len(keys)-1)
    if char.age > 10:
        char.batas_hungry += (makanan.get(keys[makan_pilihan])[1] - 30)
        char.coin -= (makanan.get(keys[makan_pilihan])[0] + 20)
    else:
        char.batas_hungry += makanan.get(keys[makan_pilihan])[1]
        char.coin -= makanan.get(keys[makan_pilihan])[0]
    return char.batas_hungry

""" People Needs """

def createPeople(karakter_list, keluarga_list):
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
    saveList(["Name"], list_girl, "list_girl_temp.csv")
    saveList(["Name"], list_boy, "list_boy_temp.csv")
    # save_data(keluarga_list, "keluarga_list.dat")

def duel(karakterA, karakterB):
    healthA = karakterA.health
    healthB = karakterB.health

    if(karakterA.spd >= karakterB.spd):
        while(healthA > 0 and healthB > 0):
            dmg = karakterA.serang(karakterB)
            healthB -= dmg
            dmg = karakterB.serang(karakterA)
            healthA -= dmg
    else:
        while(healthA > 0 and healthB > 0):
            dmg = karakterB.serang(karakterA)
            healthA -= dmg
            dmg = karakterA.serang(karakterB)
            healthB -= dmg
      
    if(healthA <= 0):
        # print(karakterB.name+" Winner")
        # exp_duel = random.randint(30, 50)
        # ExpUp(karakterB, exp_duel)
        # exp_duel = random.randint(10, 30)
        # ExpUp(karakterA, exp_duel)
        return karakterB.name
    else:
        # print(karakterA.name+" Winner")
        # exp_duel = random.randint(30, 50)
        # ExpUp(karakterA, exp_duel)
        # exp_duel = random.randint(10, 30)
        # ExpUp(karakterB, exp_duel)
        return karakterA.name

def GetBestPerson(df_duel_temp, karakter_list=[]):

    df_duel = df_duel_temp.loc[df_duel_temp["age"] >= 10]
    df_duel.reset_index()
    lis_temp = list(df_duel["name"])
    karakter_list_duel = [char for char in karakter_list if char.name in lis_temp]

    for j in range(100):
        random.shuffle(karakter_list_duel)
        for i in range(0,len(karakter_list_duel),2):
            if(i+1 != len(karakter_list_duel)):
                win_name = duel(karakter_list_duel[i],karakter_list_duel[i+1])
                if karakter_list_duel[i].name == win_name:
                    lose_name = karakter_list_duel[i+1].name
                else:
                    lose_name = karakter_list_duel[i].name

                idx = df_duel[df_duel['name']==win_name].index.values
                df_duel.at[idx[0],'win'] += 1

                idx = df_duel[df_duel['name']==lose_name].index.values
                df_duel.at[idx[0],'Lose'] += 1

    return df_duel

def setking(karakter_list_df_temp, karakter_list_df, karakter_list):
    while karakter_list_df.shape[0] > 1:
        if karakter_list_df.shape[0] < 10:
            karakter_list = SetRoles(karakter_list_df, karakter_list_df_temp, karakter_list, "Panglima")
        elif karakter_list_df.shape[0] < 30:
            karakter_list = SetRoles(karakter_list_df, karakter_list_df_temp, karakter_list, "Prajurit")
        karakter_list_df['win'] = 0
        karakter_list_df['Lose'] = 0
        df_hasil = GetBestPerson(karakter_list_df.copy(), karakter_list)
        if df_hasil.shape[0] == 1:
            break
        df_hasil = df_hasil.sort_values(by=['win'], ascending=False)
        karakter_list_df = df_hasil.head(len(df_hasil)//2)
        karakter_list_df = karakter_list_df.reset_index()
        karakter_list_df = karakter_list_df.drop("index", axis=1)
        if karakter_list_df.shape[0] == 1:
            break
        print("-------------------")
        print(len(karakter_list_df))
        print("-------------------")
    if karakter_list_df['sex'][0] == "Laki-laki":
        karakter_list = SetRoles(karakter_list_df, karakter_list_df_temp, karakter_list, "king")
        print("Set King Success")
    else:
        karakter_list = SetRoles(karakter_list_df, karakter_list_df_temp, karakter_list, "Queen")
        print("Set Queen Success")

    return karakter_list

def SetRoles(karakter_list_df, karakter_list_df_temp, karakter_list, new_role):
    names = karakter_list_df["name"].tolist()
    idxs = []
    for name in names:
        idx = karakter_list_df_temp.name[karakter_list_df_temp.name == name].index
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

def setKarakterList(karakter_list_df):
    karakter_list = []
    for i in range(karakter_list_df.shape[0]):
        karakter_list.append(karakter.Karakter("",0,"", data=karakter_list_df, row=i))
    return karakter_list

def saveList(columns, datas, nama_file):
    df_temp = pd.DataFrame(np.array(datas), columns=columns)
    df_temp.to_csv(nama_file)