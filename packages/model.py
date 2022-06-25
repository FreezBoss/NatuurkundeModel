import math
import packages.BiNaS as BiNaS

dt = 1e-4 # dt is gelijk aan een duizendste seconde


class Draad:

    def __init__(self, lengte, straal, soortelijke_weerstand, voltage, dichtheid, emissie, warmtegeleidingscoofitient, soortelijke_warmte):

        self.lengte = lengte
        self.straal = straal
        self.soortelijke_weerstand = soortelijke_weerstand
        self.voltage = voltage
        self.dichtheid = dichtheid
        self.emissie = emissie
        self.warmtegeleidingscoofitient = warmtegeleidingscoofitient
        self.soortelijke_warmte = soortelijke_warmte

        self.doorsnede = math.pi * straal ** 2 # Doorsnede oppervlak in m^2
        self.oppervlakte = 2 * math.pi * self.straal * lengte # Buiten oppervlakte in m^2
        self.weerstand = (soortelijke_weerstand * lengte) / self.doorsnede # Weerstand in ohm
        self.stroomsterkte = 1 / self.weerstand * voltage # Stroomsterkte in ampère
        self.beg_vermogen = self.stroomsterkte * voltage * dt # Vermogen in (J/dt)
        self.massa = self.dichtheid * (math.pi * self.straal ** 2 * self.lengte) # Totale massa van de draad

    def vermogen(self, vorige_temperatuur, vloeistof, bakje, hoogte, buitenlucht_temp):

        weerstand = self.weerstand * (1 + self.warmtegeleidingscoofitient * vorige_temperatuur) # Weerstand afhankelijk van de tempratuur van de draad
        stroomsterkte = 1 / weerstand * self.voltage # Stroomsterkte in ampère
        self.beg_vermogen = stroomsterkte * self.voltage * dt # Vermogen

        bovenkant = math.pi * vloeistof.straal ** 2 # Pi*r^2
        bak_oppervlakte = bakje.oppervlak # Buitenoppervlak bakje

        straling_verlies_verdamping = (bakje.hoogte - hoogte) * 2 * math.pi * bakje.straal * BiNaS.sigma * (vorige_temperatuur ** 4) * bakje.emissie * dt
        straling_verlies_verdamping = straling_verlies_verdamping * (math.pi * vloeistof.straal ** 2) / (2 * ((math.pi * vloeistof.straal ** 2) + bakje.hoogte-hoogte * math.pi * 2 * bakje.straal))
                straling_verlies_verdamping = straling_verlies_verdamping - (bakje.hoogte - hoogte) * 2 * math.pi * bakje.straal * BiNaS.sigma * (buitenlucht_temp ** 4) * bakje.emissie * dt
       

        straling_verlies_bak = BiNaS.sigma * bak_oppervlakte * (vorige_temperatuur ** 4 - buitenlucht_temp ** 4) * bakje.emissie * dt

        straling_verlies_water = BiNaS.sigma * bovenkant * (vorige_temperatuur ** 4 - buitenlucht_temp ** 4) * vloeistof.emissie * dt


        tot_straling_verlies = straling_verlies_water + straling_verlies_bak + straling_verlies_verdamping
        return self.beg_vermogen - tot_straling_verlies


class Vloeistof:

    def __init__(self, straal, hoogte, dichtheid, soortelijke_warmte, kookpunt, emissie, verdampingswarmte):

        self.straal = straal
        self.hoogte = hoogte
        self.dichtheid = dichtheid
        self.soortelijke_warmte = soortelijke_warmte
        self.kookpunt = kookpunt
        self.emissie = emissie
        self.verdampingswarmte = verdampingswarmte

        self.vollume = math.pi * straal ** 2 * hoogte
        self.massa = self.vollume * dichtheid # Totale startmassa van de vloeistof
        
    def verdamping(self, vermogen):

        gewicht_min = vermogen / self.verdampingswarmte
        vollume_min = gewicht_min / self.dichtheid

        return vollume_min


    def temperatuur(self, vermogen, bakje, draad):


        toegevoegde_temperatuur = vermogen / (self.soortelijke_warmte * self.massa + bakje.soortelijke_warmte * bakje.massa + draad.soortelijke_warmte * draad.massa) # Delta T in kelvin / celcius van vloeistof + bakje

        return toegevoegde_temperatuur


class Bakje:

    def __init__(self, straal, hoogte, dichtheid, soortelijke_warmte, dikte, emissie):

        self.straal = straal
        self.hoogte = hoogte
        self.dichtheid = dichtheid
        self.soortelijke_warmte = soortelijke_warmte
        self.dikte = dikte
        self.emissie = emissie

        self.vollume = math.pi * (straal + dikte) ** 2 * (hoogte + dikte) - math.pi * (straal + dikte) ** 2 * (hoogte + dikte)
        self.oppervlak = 2 * math.pi * (straal + dikte) * (hoogte + dikte) + math.pi * (straal + dikte) ** 2 + (math.pi * (straal + dikte) ** 2 - math.pi * straal ** 2)
        self.massa = dichtheid * self.vollume
