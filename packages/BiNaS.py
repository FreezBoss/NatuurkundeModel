
# Constanten

sigma = 5.67037e-8 # constante van Stefan-Boltzmann


class Constantaan:
    def __init__(self):


        self.emissie = (55 * 0.05 + 45 * 0.072) / 100 # 55% koper emissie 45% nikkel
        self.soortelijke_weerstand = 45e-8 # soortelijke weerstand in ohm meter
        self.dichtheid = 89e2 # Kg per kubike meter
        self.smeltpunt = 1540 # Kelvin
        self.weerstandstempratuurcoefficient = 0.05e-3 # K^-1
        self.soortelijke_warmte = 0.41e3

class Water:
    def __init__(self):

        self.emissie = 0.95 # Emissiecoofitient water
        self.dichtheid = 0.9982e3 # Kg per kubike meter
        self.soortelijke_warmte = 4.18e3 # J/kg/K
        self.kookpunt = 373.15 # Kelvin
        self.verdampingswarmte = 2.26e6 # J/kg

class Alluminium:
    def __init__(self):

        self.emissie = 0.77 # Emissiecoofitient Aluminium
        self.dichtheid = 2.7e3 # Kg per kubike meter
        self.soortelijke_warmte = 0.88e3 # J/kg/K
        self.smeltpunt = 933 # Kelvin