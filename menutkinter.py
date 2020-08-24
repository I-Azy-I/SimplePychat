from tkinter import *
from PIL import ImageTk



class Menu_tk:
    def start(self):

        self.config={}
        self.type_menu=0
        self.stop_menu= False

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

        def b_creer_pressed():

            erreur = check_config()
            if erreur == False:
                self.config={"type":1,"pseudo":tkvar_pseudo.get(), "mon_port":int(tkvar_mon_port.get()), "mon_ip":tkvar_mon_ip.get(), "salon": tkvar_salon.get(),"password": tkvar_mdp.get()}
                self.stop_menu=True
                menu_tk.destroy()
            else:
                label_erreur["text"]= erreur

        def b_rejoindre_pressed():
            erreur = check_config()
            if erreur == False:
                self.config={"type":2,"pseudo":tkvar_pseudo.get(), "mon_port":int(tkvar_mon_port.get()),"port_serveur": int(tkvar_port_serveur.get()),"mon_ip":tkvar_mon_ip.get(), "ip_serveur": tkvar_ip_serveur.get(),"password": tkvar_mdp.get()}
                self.stop_menu=True
                menu_tk.destroy()
            else:
                label_erreur["text"]= erreur

        def b_demo_pressed():

            self.config={"type":0,"choix":int_demo.get()}
            self.stop_menu=True
            menu_tk.destroy()




        def menu_creer():
            global type_menu
            if self.type_menu == 0:
                supr_menu_base()
            elif self.type_menu == 2:
                return
            elif self.type_menu == 1:
                supr_menu_rejoindre()
            elif self.type_menu==3:
                supr_menu_demo()

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

            label_erreur.grid(row=6, column=1)

            b_creer.grid(row=7, column=1)

            self.type_menu=2

        def menu_rejoindre():
            global type_menu
            if self.type_menu == 0:
                supr_menu_base()
            elif self.type_menu == 1:
                return
            elif self.type_menu == 2:
                supr_menu_creer()
            elif self.type_menu==3:
                supr_menu_demo()



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

            label_erreur.grid(row=7, column=1 )

            b_rejoindre.grid(row=8, column=1)

            self.type_menu=1


        def menu_demo():
            if self.type_menu == 0:
                supr_menu_base()
            elif self.type_menu ==3:
                return
            elif self.type_menu == 2:
                supr_menu_creer()
            elif self.type_menu == 1:
                supr_menu_rejoindre()
            lab_intro_menu["text"]= "Démonstration"
            choix_1.grid(row=1,column=0,sticky=W)
            choix_2.grid(row=2,column=0,sticky=W)
            choix_3.grid(row=3,column=0,sticky=W)
            choix_4.grid(row=4,column=0,sticky=W)
            choix_5.grid(row=5,column=0,sticky=W)
            choix_6.grid(row=6,column=0,sticky=W)
            choix_7.grid(row=7,column=0,sticky=W)
            choix_8.grid(row=8,column=0,sticky=W)
            b_demo.grid(row=9,column=0,sticky=W)


            self.type_menu=3




    #type menu: 0->base, 1-> rejoindre, 2-> creer, 3-> démo

        menu_tk=Tk()

        menubar = Menu(menu_tk)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Créer",command=menu_creer)
        menu1.add_command(label="Rejoindre",command=menu_rejoindre)
        menu1.add_command(label="Démo",command=menu_demo)

        menubar.add_cascade(label="Option", menu=menu1)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Utilisation")
        menu1.add_command(label="A propos")
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


        label_erreur=Label(menu_tk, foreground="red")

        lab_pseudo=Label(menu_tk, text="Pseudo:")
        tkvar_pseudo=StringVar()
        input_pseudo = Entry(menu_tk, textvariable=tkvar_pseudo, width=30)

        lab_mon_port= Label(menu_tk, text="Mon port:")
        tkvar_mon_port=StringVar()
        input_mon_port = Entry(menu_tk, textvariable=tkvar_mon_port, width=30)

        lab_port_serveur= Label(menu_tk, text="Port serveur:")
        tkvar_port_serveur=StringVar()
        input_port_serveur = Entry(menu_tk, textvariable=tkvar_port_serveur, width=30)

        lab_mon_ip= Label(menu_tk, text="Mon IP:")
        tkvar_mon_ip=StringVar()
        input_mon_ip = Entry(menu_tk, textvariable=tkvar_mon_ip, width=30)

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
