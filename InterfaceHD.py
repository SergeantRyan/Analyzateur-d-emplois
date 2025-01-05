import tkinter
from tkinter import *

from IPython.core.pylabtools import figsize

from Calendrier import *
from customtkinter import *
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
appSize=(1280,720)

clock=Image.open("Images/clock.png")
clss=Image.open("Images/class.png")

app = CTk()
app.geometry(f"{appSize[0]}x{appSize[1]}")
app.title("Mon EDT (sauf qu'il marche)")
app.iconbitmap("Images/icon.ico")
set_appearance_mode("dark")
set_default_color_theme("blue")

resultat=StringVar()
resultatSalle=StringVar()
calc=None

current_canvas = None

def nomFichier(str):
    n=len(str)
    for i in range(1,n):
        if str[-i]=="/":
            return str[-i+1:]

def histogrammeE(proportions,fic):
    global current_canvas
    fig = Figure(figsize=(14, 7), dpi=100)
    plt = fig.add_subplot(111)
    if current_canvas:
        current_canvas.get_tk_widget().destroy()
    categories = list(proportions.keys())
    minutes = list(proportions.values())
    p=pourcentages(proportions)
    percentages=list(p.values())
    plt.bar(categories, percentages, edgecolor="black",color="purple")
    plt.set_title(f"Répartition {fic}")
    plt.set_xlabel("Salles")
    plt.set_ylabel("Pourcentage")
    for i, percentage in enumerate(percentages):
        h,m=conversion(minutes[i])
        if m!=0:
            plt.text(i, percentage + 0.4, f'{h}h{m}m ({percentage}%)', ha='center')
        else:
            plt.text(i, percentage + 0.4, f'{h}h ({percentage}%)', ha='center')
    canvas = FigureCanvasTkAgg(fig, master=tabView.tab("Emplois"))
    canvas.draw()
    canvas.get_tk_widget().pack(pady=50)
    current_canvas = canvas

def histogrammeS(matieres,proportions,fic):
    data={code:proportions[matieres[code]] for code in matieres}
    codes = list(i for i in data)
    p = list(data.values())
    print(data)
    print(codes)
    print(p)
    plt.figure(figsize=(12,7))
    plt.bar(codes,p, color="purple", edgecolor="black")
    plt.xlabel("Codes")
    plt.ylabel("Percentage")
    plt.title(f"Repartition des Salles de {fic}")

    for i, percentage in enumerate(p):
        plt.text(i,percentage + 0.4, f'{percentage}%', ha='center')

    plt.show()

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

def openSalle():
    filepath=filedialog.askopenfilename()
    if ".ics" in filepath:
        matieres,proportions,profs,minutes=lire_salle(filepath)
        global nME
        nME=sum(minutes[i] for i in minutes)
        resultatSalle.set(texteSalle(matieres,proportions,profs,minutes))
        labelSalle.configure(text=texteSalle(matieres,proportions,profs,minutes))
        histogrammeS(matieres,proportions,nomFichier(filepath))

def openEDT():
    filepath=filedialog.askopenfilename()
    if ".ics" in filepath:
        if "L2" in filepath or "L3" in filepath or "L1" in filepath:
            tableau=lire(filepath)
            resultat.set(texteEmploi(tableau))
            #labelEmploi.configure(text=texteEmploi(tableau))
            histogrammeE(tableau,nomFichier(filepath))
    else:
        labelEmploi = CTkLabel(master=tabView.tab("Emplois"), text="Fichier Invalide!")
        labelEmploi.place(relx=0.5, rely=0.3, anchor="center")

tabView=CTkTabview(master=app,width=round(appSize[0]*0.99),height=round(appSize[1]*0.99))
tabView.pack(padx=50,pady=50)

tabView.add("Emplois")
tabView.add("Salles")

boutonFichier = CTkButton(master=tabView.tab("Emplois"), text="Analyser un Emploi", fg_color="#4158D0", hover_color="#C850C0", corner_radius=10,border_color="#C850C0",border_width=2,image=CTkImage(dark_image=clock, light_image=clock),font=("Arial",15),command=openEDT)
boutonFichier.place(relx=0.5,rely=0.01,anchor="n")
labelEmploi = CTkLabel(master=tabView.tab("Emplois"), text="")
labelEmploi.place(relx=0.5,rely=0.3,anchor="center")
labelRes=CTkLabel(master=tabView.tab("Salles"),text="")
labelRes.place(relx=0.5,rely=0.9,anchor="center")

def entreeValide(v):
    if v.isdigit():
        return True
    return False

def textTaux():
    try:
        value=int(entre.get())
        labelRes.configure(text=TauxOcc(nME, value)+"%")
    except ValueError:
        labelRes.configure(text="Veuillez saisir un entier!")

commandeValide=app.register(entreeValide)

entre=CTkEntry(master=tabView.tab("Salles"), border_width=2,placeholder_text="Saisir le nombre de semaines...",width=300,validatecommand=(commandeValide, "%P"))
entre.place(relx=0.5,rely=0.8,anchor="center")
calcul=CTkButton(master=tabView.tab("Salles"),text="Calculer le taux d'occupation",command=textTaux)
calcul.place(relx=0.2,rely=0.776)

boutonSalle = CTkButton(master=tabView.tab("Salles"), text="Analyser une Salle", fg_color="#4158D0", hover_color="#C850C0", corner_radius=10,border_color="#C850C0",border_width=2,image=CTkImage(dark_image=clss, light_image=clss),font=("Arial",15),command=openSalle)
boutonSalle.place(relx=0.5,rely=0.01,anchor="n")
labelSalle = CTkLabel(master=tabView.tab("Salles"), text="")
labelSalle.place(relx=0.5,rely=0.4,anchor="center")

app.mainloop()