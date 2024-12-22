from icalendar import Calendar
from subprocess import *
import subprocess
import sys
import requests
from pkg_resources import *
import pkg_resources

FichierL1 = "C:/Users/TideP/Downloads/ADECal_L1INFO.ics"
FichierL2 = "ADECal_L2INFO.ics"
FichierL3 = "ADECal_L3INFO.ics"
Fichier_EL108 = "ADECal_EL108.ics"

fichier=FichierL1

def lire(nom_fichier):
    g = open(nom_fichier, 'rb')
    Calendrier = Calendar.from_ical(g.read())
    L = Calendrier.walk()[1:]
    return parcours(L)

def heure(sceance):
    debut=str(sceance.get("DTSTART"))[21:26]
    fin=str(sceance.get("DTEND"))[21:26]
    return debut,fin

def duree(sceance):
    debut,fin=heure(sceance)
    minutes=int(fin[3:5])-int(debut[3:5])
    heures=int(fin[0:2])-int(debut[0:2])
    if minutes<0:
        minutes+=60
        heures-=1
    return heures, minutes

def conversion(heures,minutes):
    while minutes>=60:
        minutes-=60
        heures+=1
    return heures,minutes

def deconversion(heures,minutes):
    while heures>0:
        minutes+=60
        heures-=1
    return minutes

def read_desc(sceance):
    prop=sceance.get("DESCRIPTION")
    t=prop.split("\n")
    return t

def proportions(htotale,htp,htd,hcm,totale,tp,td,cm):
    tp=deconversion(htp,tp)
    td=deconversion(htd,td)
    cm=deconversion(hcm,cm)
    totale=deconversion(htotale,totale)
    return (round(tp*100/totale),round(td*100/totale),round(cm*100/totale))

def totale_minutes(heures):
    somme_minutes=0
    for temps in heures:
        heure=temps[0]
        minute=temps[1]
        minutes=deconversion(heure,minute)
        somme_minutes+=minutes
    return somme_minutes

def proportions_salles(heures): 
    somme_minutes=totale_minutes(heures)
    proportions=[]
    for temps in heures:
        heure=temps[0]
        minute=temps[1]
        minutes=deconversion(heure,minute)
        proportion=round(minutes*100/somme_minutes)
        proportions.append(proportion)
    return proportions

def get_prof(sceance):
    infos=read_desc(sceance)[2:]
    for info in infos:
        if not (("TP" in info) or ("TD" in info) or ("CM" in info) or ("Exporté" in info) or (info=="")):
            return info

def parcours(calendrier):
    heures_TP=0
    heures_TD=0
    heures_CM=0
    minutes_CM=0
    minutes_TP=0
    minutes_TD=0
    somme_heures=0
    somme_minutes=0
    for sceance in calendrier:
        prop=read_desc(sceance)
        print(prop)
        duration=duree(sceance)
        if prop[3][0:2]=="CM":
            heures_CM+=duration[0]
            minutes_CM+=duration[1]
            somme_heures+=duration[0]
            somme_minutes+=duration[1]
            '''if minutes_CM>=60:
                minutes_CM-=60
                heures_CM+1'''
        elif prop[3][0:2]=="TD":
            if "Groupe-01" in prop[3]:
                heures_TD+=duration[0]
                minutes_TD+=duration[1]
                somme_heures+=duration[0]
                somme_minutes+=duration[1]
                '''if minutes_TD>=60:
                    minutes_TD-=60
                    heures_TD+=1
                '''
                
        elif prop[3][0:2]=="TP":
            if "Groupe-A" in prop[3]:
                heures_TP+=duration[0]
                minutes_TP+=duration[1]
                somme_heures+=duration[0]
                somme_minutes+=duration[1]
                '''if minutes_TP>=60:
                    minutes_TP-=60
                    heures_TP+=1
                    somme_minutes-=60
                    somme_heures+=1
                '''
        else:
            print(read_desc(sceance),duree(sceance))
            #print("SKIP LINE")
        '''
        if "TD" in prop[3] or "TP" in prop[3] or "CM" in prop[3]:
            somme_heures+=duration[0]
            somme_minutes+=duration[1]
            if somme_minutes>=60:
                somme_minutes-=60
                somme_heures+=1
        '''
    
    heures_TD,minutes_TD=conversion(heures_TD,minutes_TD)
    heures_CM,minutes_CM=conversion(heures_CM,minutes_CM)
    heures_TP,minutes_TP=conversion(heures_TP,minutes_TP)
    somme_heures,somme_minutes=conversion(somme_heures,somme_minutes)
    return [proportions(somme_heures,heures_TP,heures_TD,heures_CM,somme_minutes,minutes_TP,minutes_TD,minutes_CM),[somme_heures,somme_minutes,heures_TP,minutes_TP,heures_TD,minutes_TD,heures_CM,minutes_CM]]
    #return ((somme_heures,somme_minutes),(heures_TP,minutes_TP),(heures_TD,minutes_TD),(heures_CM,minutes_CM))
    #return conversion(heures_TP+heures_TD+heures_CM,minutes_CM+minutes_TD+minutes_TP)

def parcours_salle(calendrier):
    matières=[]
    heures=[]
    profs=[]
    for sceance in calendrier:
        infos=read_desc(sceance)
        matière=infos[1]
        prof=get_prof(sceance)
        hduration,mduration=duree(sceance)
        if not matière in matières:
            matières.append(matière)
            heures.append([hduration,mduration])
            profs.append(prof)
        else:
            indice=matières.index(matière)
            heures[indice][0]+=hduration
            heures[indice][1]+=mduration
            heures[indice][0],heures[indice][1]=conversion(heures[indice][0],heures[indice][1])
    print(heures)
    return [matières,proportions_salles(heures),profs,heures]

def lire_salle(nom_fichier):
    g = open(nom_fichier, 'rb')
    Calendrier = Calendar.from_ical(g.read())
    L = Calendrier.walk()[1:]
    return parcours_salle(L)

    '''
        salle=prop[3]
        if salle[0:2]=="CM":
            heures_CM+=duree(prop)[0]
            minutes_CM+=duree(prop)[1]
            if minutes_CM>60:
                minutes_CM-=60
                heures_CM+=1
        elif salle[0:2]=="TD":
            if salle[-1]=="2":
                somme_heures+=duree(sceance)[0]
                somme_minutes+=duree(sceance)[1]
                while somme_minutes>60:
                    somme_minutes-=60
                    somme_heures+=1
    return somme_heures,somme_minutes
    '''

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

'''
def installer(required):
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing   = required - installed

    if missing:
    # implement pip as a subprocess:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
        
def run_cmd(cmd):
    ps = run(cmd, stdout=PIPE, stderr=STDOUT, shell=True, text=True)
    print(ps.stdout)
'''

'''
def read(nom_fichier):
    L=lire(FichierL1)
    return parcours(L)
'''

liste=lire(FichierL1)

'''print(liste)
for sceance in liste:
    print(read_desc(sceance))
    print("")'''


'''
liste=lire_salle(Fichier_EL108)
print(liste)
'''