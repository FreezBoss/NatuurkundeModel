import packages.model as model
import packages.BiNaS as binas

import json, math, pygame

pygame.init()

# Open de config

with open("config.json", "r") as f:
    data = json.load(f)

# Animation setup

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Natuurkunde model")

WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREY = (220, 220, 220)

def water(Y, height, beg_height):
    X=190; width=120;
    pygame.draw.rect(WIN, BLUE, (X, Y, width, height))

def rectangle(X, Y, width, height):
    pygame.draw.rect(WIN, GREY, (X, Y, width, height))

def show_time(tijd):
    font = pygame.font.Font("freesansbold.ttf", 24)
    tijd = font.render(f"Tijd: {tijd} s", True, (0, 0, 0))
    WIN.blit(tijd, (10, 10))

def show_vermogen(vermogen):
    font = pygame.font.Font("freesansbold.ttf", 24)
    tijd = font.render(f"Energie in: {vermogen} W", True, (0, 0, 0))
    WIN.blit(tijd, (10, 40))

def show_hoogte(hoogte):
    font = pygame.font.Font("freesansbold.ttf", 24)
    tijd = font.render(f"Hoogte water: {hoogte} cm", True, (0, 0, 0))
    WIN.blit(tijd, (10, 70))

def show_tempratur(temprature):
    font = pygame.font.Font("freesansbold.ttf", 18)
    tijd = font.render(f"{temprature - 273} C", True, (0, 0, 0))
    WIN.blit(tijd, (225, 250))

def helft_verdampt(tijd):
    font = pygame.font.Font("freesansbold.ttf", 24)
    tijd = font.render(f"De helft is verdampt na {tijd} s", True, (0, 0, 0))
    WIN.blit(tijd, (10, 100))

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
time_past = None

def main(starttempratuur, startvollume, hoogte, time_past):
    clock = pygame.time.Clock()
    run = True
    time = 0
    while run:
        clock.tick(30)

        time += model.dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        

        WIN.fill(WHITE)


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

            helft_verdampt(round(time_past, 1))




        water_height = hoogte * 10
        water_y = 190 + (120 - water_height)

        rectangle(180, 190, 10, 120)
        rectangle(310, 190, 10, 120)
        rectangle(180, 308, 140, 10)
        show_time(round(time,2))
        show_vermogen(round(vermogen / model.dt, 2))
        water(water_y, water_height, beg_hoogte)
        show_tempratur(round(starttempratuur))
        show_hoogte(round(hoogte, 1))
        pygame.display.update()

    
    pygame.quit()

if __name__ == "__main__":
    main(starttempratuur, startvollume, hoogte, time_past)