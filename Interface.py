from tkinter import *
from Calendrier import *
from tkinter import filedialog
from distutils.core import setup

required={"icalendar", "pyinstaller"}
'''
myLabel1 = Label(root, text="Licence 1")
myLabel2 = Label(root, text="Licence 2")
myLabel1.grid(row=0,column=0)
myLabel2.grid(row=0,column=1)
'''

global tableau


def texteEmploi(tableau):
    return "\nTotale: "+str(tableau[1][0])+" Heures, "+str(tableau[1][1])+" Minutes\n\nTP: "+str(tableau[1][2])+" Heures, "+str(tableau[1][3])+" Minutes : "+str(tableau[0][0])+"%\n\nTD : "+str(tableau[1][4])+" Heures, "+str(tableau[1][5])+" Minutes : "+str(tableau[0][1])+"%\n\nCM : "+str(tableau[1][6])+" Heures, "+str(tableau[1][7])+" Minutes : "+str(tableau[0][2])+"%\n\n"

def texteSalle(tableau):
    ch="\n"
    n=len(tableau[1])
    for i in range(n):
        if tableau[0][i]=="":
            add="INCONNU : "+str(tableau[1][i])+"% , "+str(tableau[2][i])+", "+str(tableau[3][i][0])+" Heures\n\n"
        else:
            add=str(tableau[0][i])+" : "+str(tableau[1][i])+"% , "+str(tableau[2][i])+", "+str(tableau[3][i][0])+" Heures\n\n"
        ch+=add
    return ch

def openEDT():
    filepath=filedialog.askopenfilename()
    if ".ics" in filepath:
        if "L2" in filepath or "L3" in filepath or "L1" in filepath:
            tableau=lire(filepath)
            resultat.set(texteEmploi(tableau))
        else:
            resultat.set("EMPLOI INVALIDE")

def openSalle():
    filepath=filedialog.askopenfilename()
    if ".ics" in filepath:
        tableau=lire_salle(filepath)
        resultatSalle.set(texteSalle(tableau))
        print(tableau)

'''
def afficherL1():
    texte=lire("c:/Users/TideP/Downloads/ADECal_L1INFO.ics")
    resultat.set(str(texte))

def afficherL2():
    texte=lire("c:/Users/TideP/Downloads/ADECal_L2INFO.ics")
    resultat.set(str(texte))

def afficherL3():
    texte=lire("c:/Users/TideP/Downloads/ADECal_L3INFO.ics")
    resultat.set(str(texte))
'''

#installer(required)
root = Tk()
root.title("Logiciel Licence Informatique Champollion")

resultat=StringVar()
resultatSalle=StringVar()
boutonsFrame=Frame(root)
boutonsFrame.pack()

boutonsLabelFrame=LabelFrame(boutonsFrame, text="Emplois")
boutonsLabelFrame.grid(row=0,column=0)

boutonFichier=Button(boutonsLabelFrame,text="Importer un Fichier", padx=30,pady=5, command=openEDT)
boutonFichier.grid(row=0,column=0)

'''
boutonL1=Button(boutonsLabelFrame, text="L1 Info", padx=75,pady=25, command=afficherL1)
boutonL1.grid(row=0,column=1)
boutonL2=Button(boutonsLabelFrame, text="L2 Info",padx=75,pady=25, command=afficherL2)
boutonL2.grid(row=0,column=2)
boutonL3=Button(boutonsLabelFrame, text="L3 Info",padx=75,pady=25, command=afficherL3)
boutonL3.grid(row=0,column=3)
'''

graphicFrame=LabelFrame(boutonsFrame, text="Affichage")
graphicFrame.grid(row=1,column=0)

resultLabel=Label(graphicFrame, textvariable=resultat)
resultLabel.grid(row=0,column=0)

salleFrame=LabelFrame(boutonsFrame, text="Salles")
salleFrame.grid(row=2,column=0)

salleBouton=Button(salleFrame, text="Importer une Salle", padx=30,pady=5, command=openSalle)
salleBouton.grid(row=1,column=0)

salleResultat=Label(salleFrame, textvariable=resultatSalle)
salleResultat.grid(row=2,column=0)

root.resizable(width=False, height=True)
root.geometry("1280x720")

#setup(console=['Interface.py'])
root.mainloop()