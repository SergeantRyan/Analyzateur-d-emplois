from icalendar import Calendar
from subprocess import *
from pkg_resources import *
import collections

SallesCM={"JJ035","EB020","EB021","JJ030"}
SallesTD={"EB209","JJ012","EB116","JJ123"}
SallesSPA={"EL106A","EL106B","EL107","EL108","EL109"}
SallesTP={"EB110","EB109","MM105","MM001","MM002","MM003","MM004","MM005","MM101","MM102","MM103","MM104","MM105","JJ201","JJ202"}
SallesPhysique={"EB001","EB001 BIS","EB005","EB018"}
SallesChimie={"EB013","EB015"}
SallesBio={"EB011","EB016","EB102","EB107"}

JoursFeries={"1111","0105","0805","2905"}
NombreSemaines=29
VolumeTotale=NombreSemaines*5*8*60
JoursFeries=5

def lire(nom_fichier):
    g = open(nom_fichier, 'rb')
    Calendrier = Calendar.from_ical(g.read())
    L = Calendrier.walk()[1:]
    return parcours2(L)

def heure(sceance):
    debut=str(sceance.get("DTSTART"))[21:26]
    fin=str(sceance.get("DTEND"))[21:26]
    return debut,fin

def mins(sceance):
    debut,fin=heure(sceance)
    minutes=int(fin[3:5])-int(debut[3:5])
    heures=int(fin[0:2])-int(debut[0:2])
    if minutes<0:
        minutes+=60
        heures-=1
    return minutes+60*heures

def conversion(minutes):
    return minutes//60,minutes%60

def tauxOccupation(nH,totale):
    return nH*100/totale

def TauxOcc(nME,nJours):
    print(nME,nJours*8*60)
    print(conversion(nME))
    return str((nME*100)/(8*nJours*60))

def deconversion(heures,minutes):
    return minutes+heures*60

def read_desc(sceance):
    prop=sceance.get("DESCRIPTION")
    t=prop.split("\n")
    return t

def getSalle(sceance):
    salle=sceance.get("LOCATION")
    if salle[0:9]=="EB001 BIS":
        return "EB001 BIS"
    elif salle[0:5]=="EL106":
        return salle[0:6]
    return salle[0:5]

def pourcentages(D):
    totale=sum(D[i] for i in D)
    return {i:round(D[i]*100/totale) for i in D}

def proportionsSalles(minutes):
    proportions=dict()
    somme=sum(minutes[i] for i in minutes)
    for temps in minutes:
        proportions[temps]=round(minutes[temps]*100/somme)
    return proportions

def get_prof(infos):
    for info in infos:
        if not (("TP" in info) or ("TD" in info) or ("CM" in info) or ("Exporté" in info) or (info=="")):
            return info

def groupe1(sceance):
    info=sceance.get("SUMMARY")
    if "Groupe-01" in info or "Groupe-A" in info:
        return 1
    return 0

def getCode(sceance):
    s=sceance.get("SUMMARY")
    ch=""
    for i in s:
        if i in {" ",""}:
            return ch
        ch+=i
    return ch

def parcours1(calendrier):
    repartition={"TP":0,"SPA":0,"TD":0,"CM":0}
    for sceance in calendrier:
        prop=read_desc(sceance)
        minutes=mins(sceance)
        salle=getSalle(sceance)
        grp=groupe1(sceance)
        if salle in SallesSPA:
            repartition["SPA"]+=minutes
        elif salle in SallesTP:
            if grp:
                repartition["TP"]+=minutes
        elif salle in SallesCM:
            repartition["CM"]+=minutes
        elif salle=="":
            print(prop)
        else:
            if grp:
                repartition["TD"]+=minutes
    repartition["TD/CM"]=repartition["TD"]+repartition["CM"]
    return repartition

def parcours2(calendrier):
    repartition={"INFO":0,"SPA":0,"TD":0,"CM":0,"PHY":0,"BIO":0,"CH":0}
    for sceance in calendrier:
        salle=getSalle(sceance)
        if salle in SallesSPA:
            grp=groupe1(sceance)
            if grp:
                minutes=mins(sceance)
                repartition["SPA"]+=minutes
        elif salle in SallesTP:
            grp=groupe1(sceance)
            if grp:
                minutes=mins(sceance)
                repartition["INFO"]+=minutes
        elif salle in SallesCM:
            minutes=mins(sceance)
            repartition["CM"]+=minutes
        elif salle in SallesPhysique:
            grp=groupe1(sceance)
            if grp:
                minutes=mins(sceance)
                repartition["PHY"]+=minutes
        elif salle in SallesBio:
            grp=groupe1(sceance)
            if grp:
                minutes=mins(sceance)
                repartition["BIO"]+=minutes
        elif salle in SallesChimie:
            grp=groupe1(sceance)
            if grp:
                minutes=mins(sceance)
                repartition["CH"]+=minutes
        elif salle=="":
            #prop=read_desc(sceance)
            #print(prop)
            pass
        else:
            grp=groupe1(sceance)
            if grp:
                #print(salle)
                minutes=mins(sceance)
                repartition["TD"]+=minutes
    repartition["TD/CM"]=repartition["TD"]+repartition["CM"]
    repartition.pop("TD",None)
    repartition.pop("CM",None)
    return repartition

def parcoursSalles(calendrier):
    matieres=dict()
    minutes=dict()
    profs=dict()
    for sceance in calendrier:
        infos=read_desc(sceance)
        matiere=infos[1]
        code=getCode(sceance)
        m=mins(sceance)
        if code in matieres:
            minutes[matiere]+=m
        else:
            minutes[matiere]=m
            profs[matiere]=infos[-3]
            matieres[code]=matiere
    matieres=collections.OrderedDict(sorted(matieres.items()))
    return matieres,proportionsSalles(minutes),profs,minutes

def lire_salle(nom_fichier):
    g = open(nom_fichier, 'rb')
    Calendrier = Calendar.from_ical(g.read())
    L = Calendrier.walk()[1:]
    return parcoursSalles(L)
