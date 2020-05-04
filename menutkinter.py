from tkinter import *



def start():

    global quit_menu
    global config
    global type_menu
    quit_menu=False
    config={}
    type_menu=0
    def supr_menu_rejoindre():
        lab_pseudo.grid_forget()
        input_pseudo.grid_forget()

        lab_port.grid_forget()
        input_port.grid_forget()

        lab_ip.grid_forget()
        input_ip.grid_forget()

        lab_mdp.grid_forget()
        input_mdp.grid_forget()

        b_rejoindre.grid_forget()

    def menu_rejoindre():
        global type_menu

        if type_menu == 1:
            return
        elif type_menu == 2:
            supr_menu_creer()
        elif type_menu==3:
            supr_menu_demo()



        lab_intro_menu["text"]= "Rejoindre un salon"

        lab_pseudo.grid(row=1, column=0, stick=W)
        input_pseudo.grid(row=1, column=1)

        lab_port.grid(row=2, column=0,stick=W)
        input_port.grid(row=2, column=1)

        lab_ip.grid(row=3, column=0, stick=W)
        input_ip.grid(row=3, column=1)

        lab_mdp.grid(row=4, column=0,stick=W)
        input_mdp.grid(row=4, column=1)

        b_rejoindre.grid(row=5, column=1)

        type_menu=1




    def supr_menu_creer():
        lab_pseudo.grid_forget()
        input_pseudo.grid_forget()

        lab_port.grid_forget()
        input_port.grid_forget()

        lab_salon.grid_forget()
        input_salon.grid_forget()

        lab_mdp.grid_forget()
        input_mdp.grid_forget()

        b_creer.grid_forget()
    def menu_creer():
        global type_menu

        if type_menu == 2:
            return
        elif type_menu == 1:
            supr_menu_rejoindre()
        elif type_menu==3:
            supr_menu_demo()

        lab_intro_menu["text"]= "Création d'un salon"

        lab_pseudo.grid(row=1, column=0, stick=W)
        input_pseudo.grid(row=1, column=1)

        lab_port.grid(row=2, column=0,stick=W)
        input_port.grid(row=2, column=1)

        lab_salon.grid(row=3, column=0, stick=W)
        input_salon.grid(row=3, column=1)

        lab_mdp.grid(row=4, column=0,stick=W)
        input_mdp.grid(row=4, column=1)

        b_creer.grid(row=5, column=1)

        type_menu=2
    def supr_menu_demo():
        choix_1.grid_forget()
        choix_2.grid_forget()
        choix_3.grid_forget()
        choix_4.grid_forget()
        choix_5.grid_forget()
        b_demo.grid_forget()

    def menu_demo():
        global type_menu
        if type_menu ==3:
            return
        elif type_menu == 2:
            supr_menu_creer()
        elif type_menu == 1:
            supr_menu_rejoindre()
        lab_intro_menu["text"]= "Démonstration"
        choix_1.grid(row=1,column=0,sticky=W)
        choix_2.grid(row=2,column=0,sticky=W)
        choix_3.grid(row=3,column=0,sticky=W)
        choix_4.grid(row=4,column=0,sticky=W)
        choix_5.grid(row=5,column=0,sticky=W)
        b_demo.grid(row=6,column=0,sticky=W)


        type_menu=3

    def b_demo_pressed():
        global config
        global quit_menu
        config={"type":0,"choix":int_demo.get()}
        quit_menu=True




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


    lab_intro_menu=Label(menu_tk, text="SimplePychat")
    lab_intro_menu.grid(row=0)

    lab_pseudo=Label(menu_tk, text="Pseudo:")
    tkvar_pseudo=StringVar()
    input_pseudo = Entry(menu_tk, textvariable=tkvar_pseudo, width=30)

    lab_ip= Label(menu_tk, text="Ip:")
    tkvar_ip=StringVar()
    input_ip = Entry(menu_tk, textvariable=tkvar_ip, width=30)

    lab_port= Label(menu_tk, text="Port:")
    tkvar_port=StringVar()
    input_port = Entry(menu_tk, textvariable=tkvar_port, width=30)

    lab_mdp= Label( menu_tk, text="Mot de passe:")
    tkvar_mdp=StringVar()
    input_mdp = Entry(menu_tk,show="*" ,textvariable=tkvar_mdp, width=30)

    lab_salon= Label(menu_tk, text="Salon:")
    tkvar_salon=StringVar()
    input_salon = Entry(menu_tk, textvariable=tkvar_salon, width=30)

    b_rejoindre=Button(menu_tk, text="REJOINDRE")
    b_creer=Button(menu_tk, text="CREER")
    b_demo=Button(menu_tk, text="*____*", command=b_demo_pressed)


    int_demo=IntVar()
    choix_1=Radiobutton(menu_tk, text="JUJU", variable=int_demo, value=1)
    choix_2=Radiobutton(menu_tk, text="MIMILE", variable=int_demo, value=2)
    choix_3=Radiobutton(menu_tk, text="Pedro", variable=int_demo, value=3)
    choix_4=Radiobutton(menu_tk, text="Polo", variable=int_demo, value=4)
    choix_5=Radiobutton(menu_tk, text="JCVD", variable=int_demo, value=5)


    while True:
        if quit_menu:
            menu_tk.destroy()
            return config
        menu_tk.update()
