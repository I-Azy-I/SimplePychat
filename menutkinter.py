from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import os
import socket

class Menu_tk:
    def start(self):

        self.config={}
        self.type_menu=0
        self.stop_menu= False
        self.path=""

        def check_config():

            erreur=""
            if len(tkvar_pseudo.get())<2:
                erreur=erreur+"/Pseudo trop court"
            try:
                int(tkvar_mon_port.get())
            except:
                erreur=erreur+"/mon port invalide"
            if self.type_menu!=2:
                try:
                    int(tkvar_port_serveur.get())
                except:
                    erreur=erreur+"/port serveur invalide"
                if tkvar_ip_serveur.get().count(".")!=3:
                    erreur=erreur+"/IP serveur pas valable"
            if self.type_menu!=1:
                if len(tkvar_salon.get())<2:
                    erreur=erreur+"/nom salon trop court"
            if len(tkvar_mdp.get())<5:
                erreur=erreur+"/Mdp trop court"
            if tkvar_mon_ip.get().count(".")!=3:
                erreur=erreur+"/Mon IP pas valable"
            if not os.path.isdir(tkvar_chemin.get()):
                erreur=erreur+"/Chemin non valide"




            if erreur=="":
                return False
            else:
                return erreur


        def supr_menu_base():
            image1.grid_forget()
            image2.grid_forget()

        def supr_menu_rejoindre():
            lab_pseudo.grid_forget()
            input_pseudo.grid_forget()

            lab_port_serveur.grid_forget()
            input_port_serveur.grid_forget()

            lab_mon_ip.grid_forget()
            input_mon_ip.grid_forget()

            lab_ip_serveur.grid_forget()
            input_ip_serveur.grid_forget()

            lab_mon_port.grid_forget()
            input_mon_port.grid_forget()

            lab_mdp.grid_forget()
            input_mdp.grid_forget()

            label_erreur.grid_forget()
            label_erreur["text"]=""

            b_chemin_fichier.grid_forget()
            input_chemin.grid_forget()

            b_rejoindre.grid_forget()

        def supr_menu_creer():
            lab_pseudo.grid_forget()
            input_pseudo.grid_forget()

            lab_mon_port.grid_forget()
            input_mon_port.grid_forget()

            lab_mon_ip.grid_forget()
            input_mon_ip.grid_forget()

            lab_salon.grid_forget()
            input_salon.grid_forget()

            lab_mdp.grid_forget()
            input_mdp.grid_forget()

            label_erreur.grid_forget()
            label_erreur["text"]=""

            b_chemin_fichier.grid_forget()
            input_chemin.grid_forget()

            b_creer.grid_forget()

        def supr_menu_demo():
            choix_1.grid_forget()
            choix_2.grid_forget()
            choix_3.grid_forget()
            choix_4.grid_forget()
            choix_5.grid_forget()
            choix_6.grid_forget()
            choix_7.grid_forget()
            choix_8.grid_forget()
            b_demo.grid_forget()

        def supr_menu_propos():
            label_a_propos1.grid_forget()
            label_a_propos2.grid_forget()
        def supr_menu_utilisation():
            label_utilisation1.grid_forget()
            label_utilisation2.grid_forget()
            label_utilisation3.grid_forget()
            label_utilisation4.grid_forget()

        def supr_menu():
            if self.type_menu == 0:
                supr_menu_base()
            elif self.type_menu == 1:
                supr_menu_rejoindre()
            elif self.type_menu == 2:
                supr_menu_creer()
            elif self.type_menu==3:
                supr_menu_demo()
            elif self.type_menu==4:
                supr_menu_propos()
            elif self.type_menu==5:
                supr_menu_utilisation()

        def b_creer_pressed():

            erreur = check_config()
            if erreur == False:
                self.config={"type":1,"pseudo":tkvar_pseudo.get(), "mon_port":int(tkvar_mon_port.get()), "mon_ip":tkvar_mon_ip.get(), "salon": tkvar_salon.get(),"password": tkvar_mdp.get(), "path": tkvar_chemin.get()}
                self.stop_menu=True
                menu_tk.destroy()
            else:
                label_erreur["text"]= erreur

        def b_rejoindre_pressed():
            erreur = check_config()
            if erreur == False:
                self.config={"type":2,"pseudo":tkvar_pseudo.get(), "mon_port":int(tkvar_mon_port.get()),"port_serveur": int(tkvar_port_serveur.get()),"mon_ip":tkvar_mon_ip.get(), "ip_serveur": tkvar_ip_serveur.get(),"password": tkvar_mdp.get(),"path": tkvar_chemin.get()}
                self.stop_menu=True
                menu_tk.destroy()
            else:
                label_erreur["text"]= erreur

        def b_demo_pressed():

            self.config={"type":0,"choix":int_demo.get()}
            self.stop_menu=True
            menu_tk.destroy()




        def menu_creer():
            supr_menu()

            lab_intro_menu["text"]= "Création d'un salon"

            lab_pseudo.grid(row=1, column=0, stick=W)
            input_pseudo.grid(row=1, column=1)

            lab_mon_port.grid(row=2, column=0,stick=W)
            input_mon_port.grid(row=2, column=1)

            lab_mon_ip.grid(row=3, column=0,stick=W)
            input_mon_ip.grid(row=3, column=1)

            lab_salon.grid(row=4, column=0, stick=W)
            input_salon.grid(row=4, column=1)

            lab_mdp.grid(row=5, column=0,stick=W)
            input_mdp.grid(row=5, column=1)

            b_chemin_fichier.grid(row=6, column=0, stick=W)
            input_chemin.grid(row=6, column=1)

            label_erreur.grid(row=7, column=1)



            b_creer.grid(row=8, column=1)
            self.type_menu=2

        def menu_rejoindre():
            supr_menu()



            lab_intro_menu["text"]= "Rejoindre un salon"

            lab_pseudo.grid(row=1, column=0, stick=W)
            input_pseudo.grid(row=1, column=1)

            lab_mon_port.grid(row=2, column=0, stick=W)
            input_mon_port.grid(row=2, column=1)

            lab_port_serveur.grid(row=3, column=0,stick=W)
            input_port_serveur.grid(row=3, column=1)

            lab_mon_ip.grid(row=4, column=0,stick=W)
            input_mon_ip.grid(row=4, column=1)

            lab_ip_serveur.grid(row=5, column=0,stick=W)
            input_ip_serveur.grid(row=5, column=1)



            lab_mdp.grid(row=6, column=0,stick=W)
            input_mdp.grid(row=6, column=1)

            b_chemin_fichier.grid(row=7, column=0, stick=W)
            input_chemin.grid(row=7, column=1)

            label_erreur.grid(row=8, column=1 )

            b_rejoindre.grid(row=9, column=1)



            self.type_menu=1


        def menu_demo():
            supr_menu()
            lab_intro_menu["text"]= "Démonstration"
            choix_1.grid(row=1,column=0,sticky=W)
            choix_2.grid(row=2,column=0,sticky=W)
            choix_3.grid(row=3,column=0,sticky=W)
            choix_4.grid(row=4,column=0,sticky=W)
            choix_5.grid(row=5,column=0,sticky=W)
            choix_6.grid(row=6,column=0,sticky=W)
            choix_7.grid(row=7,column=0,sticky=W)
            choix_8.grid(row=8,column=0,sticky=W)

            b_demo.grid(row=10,column=0,sticky=W)




            self.type_menu=3


        def menu_propos():
            supr_menu()

            lab_intro_menu["text"]= "A propos"
            label_a_propos1.grid()
            label_a_propos2.grid()
            self.type_menu=4
        def menu_utilisations():
            supr_menu()

            lab_intro_menu["text"]= "Utilisation"
            label_utilisation1.grid()
            label_utilisation2.grid()
            label_utilisation3.grid()
            label_utilisation4.grid()

            self.type_menu=5
        def b_chemin_pressed():
            print("test")
            menu_tk.directory = filedialog.askdirectory()
            if isinstance(menu_tk.directory, str) and menu_tk.directory!="":
                 tkvar_chemin.set(menu_tk.directory)



    #type menu: 0->base, 1-> rejoindre, 2-> creer, 3-> démo

        menu_tk=Tk()

        menubar = Menu(menu_tk)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Créer",command=menu_creer)
        menu1.add_command(label="Rejoindre",command=menu_rejoindre)
        menu1.add_command(label="Démo",command=menu_demo)

        menubar.add_cascade(label="Option", menu=menu1)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Utilisation",command=menu_utilisations)
        menu1.add_command(label="A propos", command=menu_propos)
        menubar.add_cascade(label="Aide", menu=menu1)

        menu_tk.config(menu=menubar)
        lab_intro_menu= Label(menu_tk)
        lab_intro_menu.grid(row=0)

        img1=ImageTk.PhotoImage(file=sys.path[0]+"/Sp_pp.png")
        image1 = Label(menu_tk, image=img1)
        image1.grid(row=0,column=0)

        img2=ImageTk.PhotoImage(file=sys.path[0]+"/Sp_GG.png")
        image2 = Label(menu_tk, image=img2)
        image2.grid()

        #à propos
        label_a_propos1=Label(menu_tk, text="Simple Pychat et une application de chat sous forme de salon en pair-à-pair avec cryptage des messages et bien d'autres fonctionnalités.",wrap=300)
        label_a_propos2=Label(menu_tk, text="Ce programme a été fait par Julien Berthod et Emile Schupbach.",wrap=300)
        #utilisation
        label_utilisation1=Label(menu_tk,text="Dans le menu option se situe 3 choix: Créer, Rejoindre ou Démo",wrap=300)
        label_utilisation2=Label(menu_tk,text="Créer permet d'initaliser un salon",wrap=300)
        label_utilisation3=Label(menu_tk,text="Rejoindre permet de rejoidre un salon existant",wrap=300)
        label_utilisation4=Label(menu_tk,text="Démo de lancer des pairs préconfigurés sur un réseau local à la machine",wrap=300)



        label_erreur=Label(menu_tk, foreground="red")

        lab_pseudo=Label(menu_tk, text="Pseudo:")
        tkvar_pseudo=StringVar()
        input_pseudo = Entry(menu_tk, textvariable=tkvar_pseudo, width=30)

        lab_mon_port= Label(menu_tk, text="Mon port:")
        tkvar_mon_port=StringVar()
        input_mon_port = Entry(menu_tk, textvariable=tkvar_mon_port, width=30)
        tkvar_mon_port.set("8888")

        lab_port_serveur= Label(menu_tk, text="Port serveur:")
        tkvar_port_serveur=StringVar()
        input_port_serveur = Entry(menu_tk, textvariable=tkvar_port_serveur, width=30)


        lab_mon_ip= Label(menu_tk, text="Mon IP:")
        tkvar_mon_ip=StringVar()
        input_mon_ip = Entry(menu_tk, textvariable=tkvar_mon_ip, width=30)
        tkvar_mon_ip.set(socket.gethostbyname(socket.gethostname()))

        lab_ip_serveur= Label(menu_tk, text="IP serveur:")
        tkvar_ip_serveur=StringVar()
        input_ip_serveur = Entry(menu_tk, textvariable=tkvar_ip_serveur, width=30)


        lab_mdp= Label( menu_tk, text="Mot de passe (5 caractères min):")
        tkvar_mdp=StringVar()
        input_mdp = Entry(menu_tk,show="*" ,textvariable=tkvar_mdp, width=30)

        lab_salon= Label(menu_tk, text="Salon:")
        tkvar_salon=StringVar()
        input_salon = Entry(menu_tk, textvariable=tkvar_salon, width=30)

        b_rejoindre=Button(menu_tk, text="REJOINDRE", command=b_rejoindre_pressed)
        b_creer=Button(menu_tk, text="CREER", command=b_creer_pressed)
        b_demo=Button(menu_tk, text="LANCER", command=b_demo_pressed)

        b_chemin_fichier=Button(menu_tk, text="Fichier de téléchargement ┌↓┐", command=b_chemin_pressed)
        tkvar_chemin=StringVar()
        input_chemin = Entry(menu_tk ,textvariable=tkvar_chemin, width=30)



        int_demo=IntVar()
        choix_1=Radiobutton(menu_tk, text="Pair 1", variable=int_demo, value=1)
        choix_2=Radiobutton(menu_tk, text="Pair 2", variable=int_demo, value=2)
        choix_3=Radiobutton(menu_tk, text="Pair 3", variable=int_demo, value=3)
        choix_4=Radiobutton(menu_tk, text="Pair 4", variable=int_demo, value=4)
        choix_5=Radiobutton(menu_tk, text="Pair 5", variable=int_demo, value=5)
        choix_6=Radiobutton(menu_tk, text="Pair 6", variable=int_demo, value=6)
        choix_7=Radiobutton(menu_tk, text="Pair 7", variable=int_demo, value=7)
        choix_8=Radiobutton(menu_tk, text="Pair 8", variable=int_demo, value=8)



        menu_tk.mainloop()
        if not self.stop_menu:
            quit()

        return self.config
