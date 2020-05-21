# -*- encoding: utf-8 -*-

# ip E:192.168.1.22
# ip J:192.168.1.161

#Types des messages: 0=messages ; 1=demande à la connection (ports) ; 2=réponse à la connection (historique des messages, listes de ports ) ; 3=déconnections

#structure message: type-mon port/ip-heure-pseudo-message

import asyncio
from tkinter import *
from tkinter import filedialog
import random
from datetime import datetime
import json
import menutkinter
import base64
import os
import sys
import ntpath
import codecs #pour envoie de fichier
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import crypto_SP

class Application:

    def __init__(self):

        #variable
        self.lenght_str_max=1000 #longueur max des string pour l'encryptage
        self.size_max=6 #4:max9999 str
        self.if_address=False
        self.string_var_entry_message = "" #permet de récuperer message tkinter
        self.if_button_clicked=False   #savoir si le bouton à été cliqué
        self.global_list_ports_servers=[] #transformer en ensemble?
        self.global_compteur={} #compte les échecs de connections
        self.global_if_mess_received=False
        self.global_hist_mess=[]
        self.global_hist_files={}
        self.global_files_path={}
        self.global_correction_hist_mess=True  #corrige les problèmes d'ordre de l'historique des messages
        self.variable_global_hist_mess=0
        self.continue1=False #initialisation de la première étape de la déconnection
        self.continue2=True #initialisation de la deuxième étape de la déconnection
        self.path="" #chemin ver fichier à envoyer
        self.path_to_fichiers=sys.path[0]+"/reception_fichiers/"

        self.global_dic_reception_files={}
        self.global_list_reception_files=[]



        self.username=""
        self.ip_client=""
        self.ip_server=""
        self.salon=""
        self.port_client=0
        self.port_server=0


    def configuration(self,config):
        print(config)
        # 0 démo, 1 créer, 2 rejoindre
        #config-> 0 type, choix; 1 type, pseudo, mon_port, salon, password ;2 type pseudo, mon_port, port_serveur, password
        if config["type"]==0:
            choix=config["choix"]
            if choix == 1:
                self.username="JUJU"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=0 #ne se connecte à personne
                self.port_server=8887
                self.salon="ok boomer"
                password="1234"
            elif choix==2:
                self.username="MIMILE"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=8887
                self.port_server=8888
                password="1234"
            elif choix==3:
                self.username="MARTI"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=8888
                self.port_server=8889
                password="1234"
            elif choix==4:
                self.username="Pedro"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=8888
                self.port_server=8886
                password="1234"

            elif choix==5:
                self.username="JCVD"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=8886
                self.port_server=8885
                password="1234"
            else:
                self.username="SIMPLE PYCHAT"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=8888
                self.port_server=8888
                password="1234"
        elif config["type"]==1:
            self.username=config["pseudo"]
            self.ip_client="127.0.0.1" #prédéfini car en local
            self.ip_server="127.0.0.1"
            self.port_client=0
            self.port_server=config["mon_port"]
            self.salon=config["salon"]
            password=config["password"]
        elif config["type"]==2:
            self.username=config["pseudo"]
            self.ip_client="127.0.0.1" #prédéfini car en local
            self.ip_server="127.0.0.1"
            self.port_client=config["port_serveur"]
            self.port_server=config["mon_port"]
            password=config["password"]





        if self.port_client!=0: #dans le cas ou est le premier
            self.global_list_ports_servers.append(self.port_client)
            self.global_compteur[self.port_client]=0
            print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")
        self.key=crypto_SP.create_key(password)

    def add_lenght_byte(self, data):
            #ajoute au debut du str sa taille en byte
            return str(len(data)).zfill(self.size_max)+data.decode()

    async def try_send(self,data, destinataire,sent=False, first=False):
        i=0
        while i<2:
            try:
                reader, writer = await asyncio.open_connection(self.ip_client, destinataire)
                writer.write(data.encode())
                print(f"Envoi: {data}")
                writer.close()
                if sent:
                    return True
                break
            except ConnectionRefusedError:
                print(f"Connection impossible à {destinataire}")
                if first:
                    break
                i+=1
                if i>=2:
                    if self.global_compteur[destinataire]<5:
                        self.global_compteur[destinataire]+=1
                    else:
                        del self.global_compteur[destinataire]
                        self.global_list_ports_servers.remove(destinataire)
                    print(f"[Debug] global_compteur: {self.global_compteur}")
                    if sent:
                        return False


    async def send_data(self, data, destinataires, sent=False, sender=0, first=False):
        print(f"[Debug] taille string : {len(data)}")
        print(f"[Debug] message envoyé : {data}")
        data=crypto_SP.encrypt(self.key, data)
        data=self.add_lenght_byte(data)
        if type(destinataires)==int:
            print("test1")
            if not sent:
                await self.try_send(data,destinataires)
            else:
                if await self.try_send(data,destinataires,sent=True, first=True):
                    return True
            if sent:
                return False

        elif type(destinataires)==list:
            for i in destinataires:
                if i != sender:
                    if not sent:
                        await self.try_send(data,i)
                    else:
                        if await self.try_send(data,i, sent=True):
                            return True
            if sent:
                return False
        else:
            print(f"Erreur fonction send: destinataires n'est ni un int ni une liste (destinatiire {destinataires}, type {type(destinataires)}, contenu {data}")

    async def send(self, data, destinataires, sent=False, sender=0, first=False):
        #pépare si il y a trop a envoyer
        if len(data)>self.lenght_str_max:
            #premiere partie envoyé avec le longueur du message totale
            id_file=str(len(data)).zfill(self.size_max)+datetime.utcnow().strftime('%H%M%S%f')[:-3]
            first_data="0"+id_file+data[:self.lenght_str_max]
            await self.send_data(first_data,destinataires,sender=sender)
            data=data[self.lenght_str_max:]
            print("len data")
            print(len(data))
            for i in range(round(len(data)/self.lenght_str_max)+1):
                data_splited="1"+id_file+data[:self.lenght_str_max]
                await self.send_data(data_splited,destinataires,sender=sender)
                data=data[self.lenght_str_max:]
            #envoie le message final
        else:

            if not sent:
                await self.send_data( data, destinataires, sent=sent, sender=sender, first=first)
            else:
                print(sent)
                if await self.send_data( data, destinataires, sent=True, sender=sender, first=first):
                    return True
                else:
                    return False

    def lenght_data(self,data):
        #return nombre de bytes de l'information reçue
        print(f"[Debug] data de lenght_data : {data}")
        size = int(data.decode())
        print(f"[Debug] Taille information recu: {size}")
        return size

    def check_id(self, data):
        #regarde si le message est déja dans l'historique
        id=(data["heure"]+data["pseudo"])
        for i in range(len(self.global_hist_mess)):
            if (self.global_hist_mess[i]["heure"]+self.global_hist_mess[i]["pseudo"])==id:
                return False
        return True

    async def fct_reception(self,reader,writer):
        data = await reader.read(self.size_max)
        size= self.lenght_data(data)
        data = await reader.read(n=size) #serveur attend messages
        data=crypto_SP.decrypt(self.key, data)
        if isinstance(data, bytes):
            data=data.decode()
            return data
        else:
            return True

    def join_data(self,data):

        if data[0]=="0":
            print("[Debug] premier bout de fichier recu")
            id_new_file=int(data[1:1+self.size_max+9])
            print(f"[Debug] id_new_file {id_new_file}")
            self.global_dic_reception_files[id_new_file]=len(self.global_list_reception_files)
            self.global_list_reception_files.append([data[self.size_max+10:]])
            return True
        elif data[0]=="1":
            print("[Debug] Suite de fichier recu")
            lenght_str=int(data[1:self.size_max+1])#len_str est la longueur du fichier au total
            id_file=int(data[1:(1+self.size_max+9)])
            self.global_list_reception_files[self.global_dic_reception_files[id_file]].append(data[self.size_max+10:])# 1 + size max + 9 de l'identifiant
            if len(self.global_list_reception_files[self.global_dic_reception_files[id_file]])>=(lenght_str/self.lenght_str_max):
                print("Fusion fichier")
                data=""
                for i in self.global_list_reception_files[self.global_dic_reception_files[id_file]]:
                    data=data+i
                del self.global_list_reception_files[self.global_dic_reception_files[id_file]]
                del self.global_dic_reception_files[id_file]
                return data
            else:
                return True
        else:
            return data

    async def reception(self, reader, writer):
        data=await self.fct_reception(reader,writer)
        data =self.join_data(data)

        if not data==True:

            addr = writer.get_extra_info('peername') #inutile
            writer.close() #ferme la connexion
            print(f"Serveur: Received {data!r} from {addr[0]}")
            data = json.loads(data)
            if data["type"]==0: #recois un message, ajoute à la listebox, si c'est un nouveau noeud il faut l'ajouter dans sa liste des noeuds connectés
                del data["type"]
                if not data["port"] in self.global_list_ports_servers:
                    self.global_list_ports_servers.append(data["port"])
                    self.global_compteur[data["port"]]=0
                    print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")

                if self.check_id(data):
                    self.global_hist_mess.append(data)

            elif data["type"]==1: #nouvelle connection -->  envoyer jusqu'a 2 noeuds, il faut encore controler que l'on envoie pas sont propre port

            #transfert des noeuds
                if len(self.global_list_ports_servers)==0:#si aucun noeud(port/ip) a proposé
                    str_global_list_ports_servers=""
                elif len(self.global_list_ports_servers)==1:#si 1 noeud(port/ip) a proposé
                    str_global_list_ports_servers=str(self.global_list_ports_servers[0])
                else :  #si plus de 1 noeud(port/ip) a proposé
                    node1,node2 =random.sample(self.global_list_ports_servers,k=2)
                    str_global_list_ports_servers=(str(node1)+","+str(node2)) #pour ip pas besoin de str
                if not data["port"] in self.global_list_ports_servers:
                    self.global_list_ports_servers.append(data["port"])
                    self.global_compteur[data["port"]]=0
                    print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")



                data_to_send=json.dumps({"type":2, "new_nodes":str_global_list_ports_servers, "salon":self.salon, "hist_mess":self.global_hist_mess}) #à trouver une meilleure appelation
                await self.send(data_to_send,data["port"])

            elif data["type"]==2: #reception des information pour les nouvelles connections
                self.salon=data["salon"]
                self.label_username["text"]=self.salon
                self.global_hist_mess=data["hist_mess"]
                self.variable_global_hist_mess=len(data["hist_mess"])
                for i in data["hist_mess"]:
                    self.interface_message.insert(END,("["+i["heure"][:2]+":"+i["heure"][2:4]+"] "+i["pseudo"]+i["message"]))
                print(self.global_hist_mess)

                if data["new_nodes"] !="":
                    self.global_list_ports_servers.extend([int(i) for i in data["new_nodes"].split(",")]) #le int i ne sers à rien si l'on utilise des ip
                    print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")


            elif data["type"]==3: #déconexions
                data["list_port"].remove(self.port_server)
                for i in self.global_list_ports_servers:
                    if i in data["list_port"]:
                        data["list_port"].remove(i)
                if len(data["list_port"])>0:
                    self.global_list_ports_servers.append(random.randint(0,len(data["list_port"])-1))
                    self.global_compteur[random.randint(0,len(data["list_port"])-1)]=0
                    self.global_list_ports_servers.remove(data["port"])
                print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")
            elif data["type"]==4:#requete d'envoie fichier

                if not self.global_hist_files.get(data["id_file"],False):
                    self.global_hist_files[data["id_file"]]=True
                    #envoier que l'on a pas le fichir en question
                    data2={"type":5, "id_file":data["id_file"], "port":self.port_server, "name_file":data["name_file"]}
                    await self.send(json.dumps(data2),data["port"])
            elif data["type"]==5:#envoie du fichier
                with open(self.global_files_path[data["id_file"]],mode="rb") as file:
                    file=file.read()
                file = codecs.encode(file, "base64").decode()
                await self.send(json.dumps({"type":6,"id_file":data["id_file"],"port":self.port_server, "name_file":data["name_file"],"file":file}),data["port"])
            elif data["type"]==6:#reception et renvoie du fichier
                name_file=data["name_file"]
                i=1
                while True:
                    if name_file in os.listdir(self.path_to_fichiers):
                        name_file=name_file.split(".")
                        if i>1:
                            name_file[-2]=name_file[-2][:(name_file[-2].find(f"_copie({i-1})"))]
                        name_file[-2]= name_file[-2]+f"_copie({i})"
                        name_file=".".join(name_file)
                        i+=1
                    else:
                        break
                file_path=self.path_to_fichiers+name_file
                with open(file_path ,mode="wb") as f:
                    f.write(codecs.decode(data["file"].encode(), "base64"))

                self.global_files_path[data["id_file"]]=file_path
                data2={"type":4,"name_file":data["name_file"], "id_file":data["id_file"], "port":self.port_server}
                await self.send(json.dumps(data2), self.global_list_ports_servers,sender=data["port"])






    async def run_server(self):

        print(self.global_list_ports_servers)
        self.server = await asyncio.start_server(self.reception, self.ip_server, self.port_server) #sers à cette adresse
        addr = self.server.sockets[0].getsockname()

        print(f'Serveur: Serving on {addr}')

        async with self.server:
            await self.server.serve_forever()


    async def exit_prog(self):
        data={"type":0,"port":self.port_server,"heure": datetime.utcnow().strftime('%H%M%S%f')[:-3] , "pseudo": self.username, "message":">>> s'est déconnecté <<<"}
        data=json.dumps(data)
        await self.send(data, self.global_list_ports_servers)
        data={"type":3,"port":self.port_server,"list_port":self.global_list_ports_servers}
        data=json.dumps(data)
        await self.send(data, self.global_list_ports_servers)
        self.continue2=False
        await asyncio.sleep(0.5)
        self.server.close()

    def path_leaf(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    async def client(self):

        print(self.global_list_ports_servers)

        if self.port_client !=0:
            sent=False
            data_ini=json.dumps({"type":1, "port":self.port_server})
            while not sent and self.continue2:
                sent=await self.send(data_ini, self.port_client,sent=True,first=True)
                if self.continue1:
                    await self.exit_prog()
                await asyncio.sleep(1)
        i=0
        while self.continue2:
            await asyncio.sleep(0.1)
            if self.if_button_clicked: #si le boutton est cliqué
                self.if_button_clicked = False
                data={"port":self.port_server,"heure": datetime.utcnow().strftime('%H%M%S%f')[:-3] , "pseudo": self.username, "message":("> "+ self.string_var_entry_message)}
                self.global_hist_mess.append(data)

            if self.variable_global_hist_mess<len(self.global_hist_mess):
                data=self.global_hist_mess[self.variable_global_hist_mess]
                data["type"]=0
                await self.send(json.dumps(data),self.global_list_ports_servers,sent=False, sender=data["port"])

                self.interface_message.insert(END, (datetime.now().strftime('[%H:%M] '))+self.global_hist_mess[self.variable_global_hist_mess]["pseudo"]+self.global_hist_mess[self.variable_global_hist_mess]["message"])
                print(self.global_hist_mess[self.variable_global_hist_mess]["message"])
                if self.variable_global_hist_mess<85:
                    print(self.variable_global_hist_mess)
                    self.variable_global_hist_mess+=1
                else :
                    del self.global_hist_mess[0]
            if self.path!="":
                name_file=self.path_leaf(self.path)
                id_file=datetime.utcnow().strftime('%H%M%S%f')[:-3]+self.username+name_file
                print(f"[Debug] name_file{name_file}")
                self.global_hist_files[id_file]=True
                self.global_files_path[id_file]=self.path
                data={"type":4,"name_file":name_file, "id_file":id_file, "port":self.port_server}
                await self.send(json.dumps(data), self.global_list_ports_servers)
                self.path=""


            if self.continue1:
                await self.exit_prog()










    async def interface(self): #création de l'interface
        print(self.global_list_ports_servers)
        def fct_button_send(event=""):
            self.string_var_entry_message=var_entry_message.get()
            self.if_button_clicked=True
            var_entry_message.set("")
        def exit_fenetre():
            print("Fin du programme")
            fenetre.destroy()
            self.continue1=True
        def button_file_pessed():
            fenetre.filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("zip files","*.zip"),("jpeg files","*.jpeg"),("txt files","*.txt"),("gif files","*.gif"),("all files","*.*")))
            self.path = fenetre.filename


        width_fenetre=50
        height_fenetre=25
        width_button=2

        fenetre = Tk()

        menubar = Menu(fenetre)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Connections")
        menu1.add_command(label="Info")
        menu1.add_command(label="Log")
        menubar.add_cascade(label="Info", menu=menu1)
        fenetre.config(menu=menubar)



        var_entry_message=StringVar()
        self.label_username = Label(fenetre, text=f"{self.salon}")
        self.label_username.grid(row=0)

        self.interface_message = Listbox(fenetre,width=width_fenetre, height=height_fenetre)
        self.interface_message.grid(row=1)

        entry_message = Entry(fenetre, textvariable=var_entry_message, width=int(width_fenetre-(width_button*2)-8))
        entry_message.bind("<Return>", fct_button_send)
        entry_message.grid(row=2)

        button_send= Button(fenetre, text="↵",width=width_button, command=fct_button_send)
        button_send.grid(row=2,sticky=E)
        button_file=Button(fenetre, text="┌↑┐",width=width_button,command= button_file_pessed)
        button_file.grid(row=2,sticky=W)

        fenetre.protocol('WM_DELETE_WINDOW', exit_fenetre)

        fenetre.update()

        while self.continue2:

            await asyncio.sleep(0.05)
            if not self.continue1:
                fenetre.update()



    async def main(self):
        print(self.global_list_ports_servers)
        await asyncio.gather(self.run_server(),
                             self.interface(),
                             self.client())

    def run(self):
        self.configuration(menutkinter.start())
        asyncio.run(self.main())


if __name__=="__main__":
    Application().run()
