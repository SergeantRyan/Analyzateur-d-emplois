from tkinter import *
from Calendrier import *
from tkinter import filedialog

global tableau

def texteEmploi(D):
    ch=""
    s=0
    p=pourcentages(D)
    th,tm=conversion(sum(D[j] for j in D))
    for i in D:
        heures,minutes=conversion(D[i])
        if minutes:
            ch+=i+f": {heures}h {minutes}m ({p[i]}%)\n\n"
        else:
            ch+=i+f": {heures}h ({p[i]}%)\n\n"
    if tm:
        ch+=f"Total: {th}h {tm}m"
    else:
        ch+=f"Total: {th}h"
    return ch

def texteSalle(matieres,proportions,profs,minutes):
    ch="\n"
    tm=0
    for code in matieres:
        matiere=matieres[code]
        c=minutes[matiere]
        h,m=conversion(c)
        tm+=c
        if code=="":
            if m!=0:
                ch+=f"INCONNU - {matiere}, {profs[matiere]} - {h}h {m}m ({proportions[matiere]}%)\n\n"
            else:
                ch+=f"INCONNU - {matiere}, {profs[matiere]} - {h}h ({proportions[matiere]}%)\n\n"  
        else:
            if m!=0:
                ch+=f"{code} - {matiere}, {profs[matiere]} - {h}h {m}m ({proportions[matiere]}%)\n\n"
            else:
                ch+=f"{code} - {matiere}, {profs[matiere]} - {h}h ({proportions[matiere]}%)\n\n"
    h,m=conversion(tm)
    if m!=0:
        ch+=f"Total: {h}h {m}m"
    else:
        ch+=f"Total: {h}h"
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
        matieres,proportions,profs,minutes=lire_salle(filepath)
        resultatSalle.set(texteSalle(matieres,proportions,profs,minutes))

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