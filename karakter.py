import random

class Karakter:

    def __init__(self, name, age, sex, data=[], row=0):
        if len(data)>0:
            self.name = data["name"][row]
            self.age = data["age"][row]
            self.sex = data["sex"][row]
            self.sex_role = data["sex_role"][row]
            self.atk = data["atk"][row]
            self.defend = data["defend"][row]
            self.health = data["health"][row]
            self.spd = data["spd"][row]
            self.exp = data["exp"][row]
            self.batas_exp = data["batas_exp"][row]
            self.stamina = data["stamina"][row]
            self.level = data["level"][row]
            self.coin = data["coin"][row]
            self.batas_hungry = data["batas_hungry"][row]
            self.role = data["role"][row]
            self.pasangan = data["pasangan"][row]
            self.siap_pasangan = data["siap_pasangan"][row]
        else:
            self.name = name
            if age <= 0:
                age = 1
            elif age > 100:
                age = 100
            self.age = age
            
            self.setSexRole()
            self.setKekuatan()
            self.level = 0
            self.coin = 750
            self.batas_hungry = 100
            self.sex = sex
            ran_role = random.randint(0, 100)
            if ran_role > 10:
                self.role = "Fighter"
            else:
                self.role = "Penduduk"
            self.pasangan = None
            self.siap_pasangan = False
    
    def setSexRole(self):
        if self.age < 7:
            self.sex_role = "Anak-anak"
        elif self.age < 15:
            self.sex_role = "Remaja"
        elif self.age < 30:
            self.sex_role = "Dewasa Muda"
        elif self.age < 60:
            self.sex_role = "Dewasa Tua"
        else:
            self.sex_role = "Lansia"

    def setKekuatan(self):
        self.atk = random.randint(1, 20)
        self.defend = random.randint(0, 20)
        self.health = random.randint(200, 1000)
        self.spd = random.randint(0, 10)
        self.exp = 0
        self.batas_exp = 100
        if self.age < 15:
            self.stamina = int(random.randint(25, 75) * (self.age - 1)/(14 - 1)) + 1
        elif self.age >= 15 and self.age <= 40 :
            self.stamina = random.randint(75, 150)
        else:
            self.stamina = int((random.randint(25, 75) / ((self.age - 40)/(100 - 40))) / 10)

    def save(self):
        data = {"name":self.name, "age":self.age, "sex":self.sex, "sex_role":self.sex_role,
                "atk":self.atk, "defend":self.defend, "health":self.health, "spd":self.spd,
                "exp":self.exp, "batas_exp":self.batas_exp, "stamina":self.stamina, "level":self.level,
                "coin":self.coin, "batas_hungry":self.batas_hungry, "role":self.role,
                "pasangan":self.pasangan, "siap_pasangan":self.siap_pasangan}
        return data

    def serang(self, musuh):
        dmg = self.atk*(100/(100+musuh.defend)) * random.uniform(0.75, 1.25)
        critical = random.randint(0, 100)
        miss = random.randint(0, 100)
        if critical <= 20:
              dmg *= 2
        if miss <= 20:
              dmg *= 0
        return dmg

    def info(self):
        print("Name : "+self.name)
        print("Age : "+str(self.age))
        print("Kelamin : "+self.sex)
        print("sex_Role : "+self.sex_role)
        print("Pasangan : "+str(self.pasangan))
        print("Level : "+str(self.level))
        print("Coin : "+str(self.coin))
        print("ATK : "+str(self.atk))
        print("DEF : "+str(self.defend))
        print("SPD : "+str(self.spd))
        print("Health : "+str(self.health))
        print("Stamina : "+str(self.stamina))
        print("EXP : "+str(self.exp))
        print(" ")