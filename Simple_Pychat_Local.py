# -*- encoding: utf-8 -*-

# ip E:192.168.1.22
# ip J:192.168.1.161

#Types des messages: 0=messages ; 1=demande à la connection (ports) ; 2=réponse à la connection (historique des messages, listes de ports )

#structure message: type-mon port/ip-heure-pseudo-message

import asyncio
from tkinter import *
import random
from datetime import datetime
import json
import menutkinter
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import crypto_SP

class Application:

    def __init__(self):

        #variable
        self.size_max=4 #4:max9999 str
        self.if_address=False
        self.string_var_entry_message = "" #permet de récuperer message tkinter
        self.if_button_clicked=False   #savoir si le bouton à été cliqué
        self.global_list_ports_servers=[] #transformer en ensemble?
        self.global_if_mess_received=False
        self.global_hist_mess=[]
        self.global_correction_hist_mess=True  #corrige les problèmes d'ordre de l'historique des messages
        self.variable_global_hist_mess=0




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
                password="1234"
            elif choix==2:
                self.username="MIMILE"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=8887
                self.port_server=8888
                password="1234"
            elif choix==3:
                self.username="Pedro"
                self.ip_client="127.0.0.1"
                self.ip_server="127.0.0.1"
                self.port_client=8888
                self.port_server=8889
                password="1234"
            elif choix==4:
                self.username="Polo"
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
            print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")
        self.key=crypto_SP.create_key(password)

    def add_lenght_byte(self, data):
            #ajoute au debut du str sa taille en byte
            return str(len(data)).zfill(self.size_max)+data.decode()

    async def try_send(self,data, destinataire,sent=False):
        try:
            reader, writer = await asyncio.open_connection(self.ip_client, destinataire)
            writer.write(data.encode())
            print(f"Envoi: {data}")
            writer.close()
            if sent:
                return True

        except ConnectionRefusedError:
            print(f"Connection impossible à {destinataire}")
            if sent:
                return False

    async def send(self, data, destinataires, sent=False, sender=0):
        data=crypto_SP.encrypt(self.key, data)
        data=self.add_lenght_byte(data)
        if type(destinataires)==int:
            print("test1")
            if not sent:
                await self.try_send(data,destinataires)
            else:
                if await self.try_send(data,destinataires,sent=True):
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

    def lenght_data(self,data):
        #return nombre de bytes de l'information reçue
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

    async def reception(self, reader, writer):
        data = await reader.read(self.size_max)
        size= self.lenght_data(data)
        print(size)
        data = await reader.read(n=size) #serveur attend messages
        data=crypto_SP.decrypt(self.key, data)
        print(type(data))
        if isinstance(data, bytes):
            data=data.decode()
            addr = writer.get_extra_info('peername') #inutile
            writer.close() #ferme la connexion
            print(f"Serveur: Received {data!r} from {addr[0]}")
            data = json.loads(data)
            if data["type"]==0: #recois un message, ajoute à la listebox, si c'est un nouveau noeud il faut l'ajouter dans sa liste des noeuds connectés
                del data["type"]
                if not data["port"] in self.global_list_ports_servers:
                    self.global_list_ports_servers.append(data["port"])
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
                    print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")



                data_to_send=json.dumps({"type":2, "new_nodes":str_global_list_ports_servers, "salon":self.salon, "hist_mess":self.global_hist_mess}) #à trouver une meilleure appelation
                await self.send(data_to_send,data["port"])

            elif data["type"]==2:
                self.salon=data["salon"]
                self.global_hist_mess=data["hist_mess"]
                self.variable_global_hist_mess=len(data["hist_mess"])
                for i in data["hist_mess"]:
                    self.interface_message.insert(END,("["+i["heure"][:2]+":"+i["heure"][2:4]+"] "+i["pseudo"]+i["message"]))
                print(self.global_hist_mess)

                if data["new_nodes"] !="":
                    self.global_list_ports_servers.extend([int(i) for i in data["new_nodes"].split(",")]) #le int i ne sers à rien si l'on utilise des ip
                    print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")






    async def server(self):

        print(self.global_list_ports_servers)
        server = await asyncio.start_server(self.reception, self.ip_server, self.port_server) #sers à cette adresse

        addr = server.sockets[0].getsockname()
        print(f'Serveur: Serving on {addr}')

        async with server:
            await server.serve_forever()





    async def client(self):

        print(self.global_list_ports_servers)
        if self.port_client !=0:
            sent=False
            data_ini=json.dumps({"type":1, "port":self.port_server})
            while not sent :
                sent=await self.send(data_ini, self.port_client,True)
                await asyncio.sleep(1)
        i=0
        while True:
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
                if self.variable_global_hist_mess<5:
                    self.variable_global_hist_mess+=1
                else :
                    del self.global_hist_mess[0]









    async def interface(self): #création de l'interface
        print(self.global_list_ports_servers)
        def fct_button_send():
            self.string_var_entry_message=var_entry_message.get()
            self.if_button_clicked=True
            var_entry_message.set("")


        fenetre = Tk()
        var_entry_message=StringVar()
        label_username = Label(fenetre, text=f"{self.username}")
        label_username.pack()
        self.interface_message = Listbox(fenetre)
        self.interface_message.pack()
        entry_message = Entry(fenetre, textvariable=var_entry_message, width=30)
        entry_message.pack()
        button_send= Button(fenetre, command=fct_button_send)
        button_send.pack()

        fenetre.update()

        while True:

            await asyncio.sleep(0.05)





            fenetre.update()



    async def main(self):
        print(self.global_list_ports_servers)
        await asyncio.gather(self.server(),
                             self.interface(),
                             self.client())

    def run(self):
        self.configuration(menutkinter.start())
        asyncio.run(self.main())


if __name__=="__main__":
    Application().run()
