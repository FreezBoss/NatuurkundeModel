import packages.model as model
import packages.BiNaS as binas

import json, math
from matplotlib import pyplot as plt

plt.style.use('seaborn')

# Open de config

with open("config.json", "r") as f:
    data = json.load(f)


# Draad object maken

draad = model.Draad(
    data["draad"]["lengte"],
    data["draad"]["straal"],
    binas.Constantaan().soortelijke_weerstand,
    data["draad"]["voltage"],
    binas.Constantaan().dichtheid,
    binas.Constantaan().emissie,
    binas.Constantaan().weerstandstempratuurcoefficient,
    binas.Constantaan().soortelijke_warmte
)

# Vloeistof object maken

vloeistof = model.Vloeistof(
    data["vloeistof"]["straal"],
    data["vloeistof"]["hoogte"],
    binas.Water().dichtheid,
    binas.Water().soortelijke_warmte,
    binas.Water().kookpunt,
    binas.Water().emissie,
    binas.Water().verdampingswarmte
)

# Bakje object maken

bakje = model.Bakje(
    data["bakje"]["straal"],
    data["bakje"]["hoogte"],
    binas.Alluminium().dichtheid,
    binas.Alluminium().soortelijke_warmte,
    data["bakje"]["dikte"],
    binas.Alluminium().emissie
)

starttempratuur = data["algemeen"]["starttempratuur"]
startvollume = vloeistof.vollume
hoogte = startvollume / (math.pi * vloeistof.straal ** 2) * 100
beg_hoogte = hoogte
tot_e = 0
time = 0
time_past = None

time_list = []
y_val = []

# Berekeningen doen:

def main(starttempratuur, startvollume, hoogte, time_past):
    time = 0
    tot_e = 0
    for i in range(5000000):
        time = time+model.dt
        if time_past == None:
            tot_e += draad.beg_vermogen


            # Berekeningen doen:

        if time_past == None:
            vermogen = draad.vermogen(starttempratuur, vloeistof, bakje, hoogte / 100, 15 + 273.15)
        else:
            vermogen = draad.vermogen(starttempratuur, vloeistof, bakje, hoogte / 100, 15 + 273.15) - draad.beg_vermogen
            starttempratuur += vloeistof.temperatuur(vermogen, bakje, draad)

        if starttempratuur < binas.Water().kookpunt and time_past == None:

            starttempratuur += vloeistof.temperatuur(vermogen, bakje, draad)

        elif hoogte >= (beg_hoogte) / 2:
            startvollume -= vloeistof.verdamping(vermogen)
            hoogte = startvollume / (math.pi * vloeistof.straal ** 2) * 100

        else: 
            if time_past == None:
                time_past = time
                print(time_past)
                print(round(tot_e,4))


            water_height = hoogte * 10
            water_y = 190 + (120 - water_height)
        if 1 == 1:
            y_val.append(starttempratuur -273.15)
            time_list.append(i * model.dt)


main(starttempratuur, startvollume, hoogte, time_past)

plt.axis([0, 500, 0, 110])
plt.plot(time_list, y_val)

plt.locator_params(axis='y', nbins=20)
plt.locator_params(axis='x', nbins=20)

plt.xlabel('Tijd in seconden')
plt.ylabel("Temperatuur in °C")
plt.title('Temperatuur water')
plt.grid(True)

plt.show()