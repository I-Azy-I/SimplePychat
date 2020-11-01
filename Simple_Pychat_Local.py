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
from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import crypto_SP

class Application:

    def __init__(self):

        #variable
        self.size_max_hist_mess=50
        self.lenght_str_max=1000 #longueur max des string pour l'encryptage
        self.size_max=4 #4:max9999 str
        self.if_address=False
        self.string_var_entry_message = "" #permet de récuperer message tkinter
        self.if_button_clicked=False   #savoir si le bouton à été cliqué
        self.global_list_servers=[] #transformer en ensemble?
        self.global_compteur={} #compte les échecs de connections
        self.global_if_mess_received=False
        self.global_hist_mess=[]
        self.global_hist_files={}
        self.global_files_path={}
        self.global_correction_hist_mess=True  #corrige les problèmes d'ordre de l'historique des messages
        self.variable_global_hist_mess=0
        self.is_running=True #initialisation  la déconnexion
        self.path="" #chemin ver fichier à envoyer
        self.path_to_fichiers=sys.path[0]+"/reception_fichiers/"
        self.bridge_queue=asyncio.Queue()

        self.global_dic_reception_files={}
        self.global_list_reception_files=[]
        self.global_path_file_listbox={}



        self.username=""
        self.ip_server=""
        self.my_ip=""
        self.salon=""
        self.port_server=0
        self.my_port=0


    def configuration(self,config):


        # 0 démo, 1 créer, 2 rejoindre
        #config-> 0 type, choix; 1 type, pseudo, mon_port, salon, password ;2 type pseudo, mon_port, port_serveur, password
        if config["type"]==0:

            self.path_to_fichiers=sys.path[0]+"/reception_fichiers/"
            choix=config["choix"]
            if choix == 1:
                self.username="Pair 1"
                self.ip_server=0
                self.my_ip="127.0.0.1"
                self.port_server=0 #ne se connecte à personne
                self.my_port=8887
                self.salon="Salon"
                password="123456789"
            elif choix==2:
                self.username="Pair 2"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8887
                self.my_port=8888
                password="123456789"
            elif choix==3:
                self.username="Pair 3"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8888
                self.my_port=8889
                password="123456789"
            elif choix==4:
                self.username="Pair 4"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8888
                self.my_port=8886
                password="123456789"

            elif choix==5:
                self.username="Pair 5"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8886
                self.my_port=8885
                password="123456789"
            elif choix==6:
                self.username="Pair 6"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8886
                self.my_port=8884
                password="123456789"
            elif choix==7:
                self.username="Pair 7"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8885
                self.my_port=8882
                password="123456789"
            elif choix==8:
                self.username="Pair 8"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8889
                self.my_port=8883
                password="123456789"
            else:
                self.username="SIMPLE PYCHAT"
                self.ip_server="127.0.0.1"
                self.my_ip="127.0.0.1"
                self.port_server=8888
                self.my_port=8888
                password="123456789"

        #création
        elif config["type"]==1:
            self.username=config["pseudo"]
            self.ip_server=0
            self.my_ip=config["mon_ip"]
            self.port_server=0
            self.my_port=config["mon_port"]
            self.salon=config["salon"]
            self.path_to_fichiers=config["path"]+"/"
            password=config["password"]
        #rejoindre
        elif config["type"]==2:
            self.username=config["pseudo"]
            self.ip_server=config["ip_serveur"]
            self.my_ip=config["mon_ip"]
            self.port_server=config["port_serveur"]
            self.my_port=config["mon_port"]
            self.path_to_fichiers=config["path"]+"/"
            password=config["password"]

        self.my_addr=(self.my_ip,self.my_port)
        if self.ip_server!=0: #dans le cas ou n'est le premier

            self.global_list_servers.append((self.ip_server, self.port_server))
            self.global_compteur[(self.ip_server, self.port_server)]=0
            #print(f"[Debug] global_list_ports_servers: {self.global_list_servers}")
        self.key=crypto_SP.create_key(password)

    def add_lenght_byte(self, data):
            #ajoute au debut du str sa taille en byte
            return str(len(data)).zfill(self.size_max)+data.decode()

    async def try_send(self,data, destinataire ,sent=False, first=False):
        i=0
        while i<2:
            try:
                reader, writer = await asyncio.open_connection(destinataire[0], destinataire[1])
                writer.write(data.encode())

                writer.close()
                if sent:
                    return True
                break
            except ConnectionRefusedError:
                #print(f"Connection impossible à {destinataire}")
                if first:
                    break
                i+=1
                if i>=2:
                    if destinataire in self.global_compteur:
                        if self.global_compteur[destinataire]<5:
                            self.global_compteur[destinataire]+=1
                        else:
                            del self.global_compteur[destinataire]
                            self.global_list_servers.remove(destinataire)
                        #print(f"[Debug] global_compteur: {self.global_compteur}")
            if sent:
                return False


    async def send_data(self, data, destinataires, sent=False, sender=0, first=False):
        #print(f"[Debug] taille string : {len(data)}")
        data=crypto_SP.encrypt(self.key, data)
        data=self.add_lenght_byte(data)
        if isinstance(destinataires,tuple):
            if not sent:
                await self.try_send(data,destinataires)
            else:
                if await self.try_send(data,destinataires,sent=True, first=True):
                    return True
            if sent:
                return False

        elif isinstance(destinataires,list):
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
            print("Envoi message en plusieurs parties")
            #premiere partie envoyé avec le longueur du message totale
            #num_pos=round(len(data)/self.lenght_str_max)+2
            id_file=str(len(data[:self.size_max])).zfill(self.size_max)+datetime.utcnow().strftime('%H%M%S%f')[:-3] #id:
            first_data= {"part":"0","id": id_file, "file": data[:self.lenght_str_max],"position":0 }
            await self.send_data(json.dumps(first_data),destinataires,sender=sender)
            #print("envoie premier bout de fichier")
            data=data[self.lenght_str_max:]
            total_pos=round(len(data)/self.lenght_str_max)
            for i in range(total_pos):
                #print(f"Envoie bout de fichier {i+1}")
                data_splited={"part":"1","position":(i+1), "id":id_file,"file":data[:self.lenght_str_max]}
                #print(data_splited["file"][-20:])
                await self.send_data(json.dumps(data_splited),destinataires,sender=sender)
                data=data[self.lenght_str_max:]

            #print(f"Envoie dernier bout de fichier {i+2}")
            data_splited={"part":"2","id":id_file,"file":data, "position":(total_pos+1)}
            await self.send_data(json.dumps(data_splited),destinataires,sender=sender)


            #envoie le message final
        else:
            print(f"Envoi message")
            if not sent:
                await self.send_data( data, destinataires, sent=sent, sender=sender, first=first)
            else:
                #print(sent)
                if await self.send_data( data, destinataires, sent=True, sender=sender, first=first):
                    return True
                else:
                    return False

    def lenght_data(self,data):
        #return nombre de bytes de l'information reçue
        #print(f"[Debug] data de lenght_data : {data}")
        size = int(data.decode())
        #print(f"[Debug] Taille information recu: {size}")

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
            #print("test 1")
            data=data.decode()
            return data
        else:
            #print("test 2")
            return True

    def join_data(self,data):
        if "part" in data:
            #les bouts de fichiers recu sont ajoutés à une liste sous le format (postion,data) {id:[liste[(pos,data)],taille]}

            id = data["id"]
            position=data["position"]
            print(f" Reception: partie {position}")
            if id not in self.global_dic_reception_files:
                self.global_dic_reception_files[id]=[[],""] #deucième partie du tuple

            self.global_dic_reception_files[id][0].append((position,data["file"]))
            #print(f"Bout fichier {position} de {id} recu")
            if data["part"]=="2":
                print(f" Nombre totale de parties: {position}")
                self.global_dic_reception_files[id][1]=position
            if self.global_dic_reception_files[id][1] !="":
                #print(f"1: {len(self.global_dic_reception_files[id][0])}")
                #print(f"2: {self.global_dic_reception_files[id][1]+1}")
                if len(self.global_dic_reception_files[id][0])==self.global_dic_reception_files[id][1]+1:
                    #print("fusion des fichiers")
                    reception_file_ordered=[""]*(self.global_dic_reception_files[id][1]+1)
                    print(" vérification ordre parties de fichiers")
                    for i in range(len(self.global_dic_reception_files[id][0])-1,-1,-1):
                        print(f"Ajout en {self.global_dic_reception_files[id][0][i][0]}")
                        reception_file_ordered[self.global_dic_reception_files[id][0][i][0]]=self.global_dic_reception_files[id][0][i][1]
                        self.global_dic_reception_files[id][0].pop(i)
                    del self.global_dic_reception_files[id]
                    print(" création fichier")
                    data=""
                    reception_file_ordered.reverse()
                    for i in range(len(reception_file_ordered)-1,-1,-1):
                        data=data+reception_file_ordered[i]
                        reception_file_ordered.pop(i)
                    del reception_file_ordered
                    print(" fusion terminée")
                    #print(data)
                    data=json.loads(data)
                    return data
            return True


            """
            if data[part]=="0":
                print("[Debug] premier bout de fichier recu")
                id_new_file=data[id]
                print(f"[Debug] id_new_file {id_new_file}")
                self.global_dic_reception_files[id_new_file]=data[data]
                self.global_list_reception_files.append([data[self.size_max+10:]])
                return True
            elif data[0]=="1":
                print("[Debug] Suite de fichier recu")
                lenght_str=int(data[1:self.size_max+1])#len_str est la longueur du fichier au total
                id_file=int(data[1:(1+self.size_max+9)])
                self.global_list_reception_files[self.global_dic_reception_files[id_file]].append(data[self.size_max+10:])# 1 + size max + 9 de l'identifiant
                return True
            elif data[0]=="2":
                lenght_str=int(data[1:self.size_max+1])#len_str est la longueur du fichier au total
                id_file=int(data[1:(1+self.size_max+9)])
                self.global_list_reception_files[self.global_dic_reception_files[id_file]].append(data[self.size_max+10:])# 1 + size max + 9 de l'identifiant
                print("Fusion fichier")
                data=""
                for i in self.global_list_reception_files[self.global_dic_reception_files[id_file]]:
                    data=data+i
                del self.global_list_reception_files[self.global_dic_reception_files[id_file]]
                del self.global_dic_reception_files[id_file]
                return data
            """
        else:
            return data

    async def reception(self, reader, writer):
        data = await self.fct_reception(reader,writer)
        data = json.loads(data)
        data =self.join_data(data)

        if not data==True:
            writer.close() #ferme la connexion
            if "addr_server" in data:

                data["addr_server"]=tuple(data["addr_server"])
            if data["type"]==0: #recois un message, ajoute à la listebox, si c'est un nouveau noeud il faut l'ajouter dans sa liste des noeuds connectés
                print("Reception: type 0")
                if not data["addr_server"] in self.global_list_servers:
                    self.global_list_servers.append(data["addr_server"])
                    self.global_compteur[data["addr_server"]]=0
                    #print(f"[Debug] global_list_servers: {self.global_list_servers}")


                if self.check_id(data):
                    if len(self.global_hist_mess)>=self.size_max_hist_mess:
                        del self.global_hist_mess[0]
                    self.global_hist_mess.append(data)
                    self.interface_message.insert(END, (datetime.now().strftime('[%H:%M] '))+data["pseudo"]+data["message"])
                    if data["color"]!="":
                        self.interface_message.itemconfig(END, foreground=data["color"])
                    sender=data["addr_server"]
                    data["addr_server"]=self.my_addr
                    await self.send(json.dumps(data),self.global_list_servers,sent=False, sender=sender)


            elif data["type"]==1: #nouvelle connection -->  envoyer jusqu'a 2 noeuds, il faut encore controler que l'on envoie pas sa propre addr
                print("Reception: type 1")
            #transfert des noeuds
                global_list_servers_reduced=[]
                if len(self.global_list_servers)==0:#si aucun noeud(port/ip) a proposé
                    global_list_servers_reduced=[]
                elif len(self.global_list_servers)==1:#si 1 noeud(port/ip) a proposé
                    global_list_servers_reduced.append(self.global_list_servers[0])
                else :  #si plus de 1 noeud(port/ip) a proposé
                    node1,node2 =random.sample(self.global_list_servers,k=2)
                    global_list_servers_reduced.append(node1)
                    global_list_servers_reduced.append(node2)

                if not data["addr_server"] in self.global_list_servers:
                    #print(data["addr_server"])
                    self.global_list_servers.append(data["addr_server"])
                    self.global_compteur[data["addr_server"]]=0
                    #print(f"[Debug] global_list_servers: {self.global_list_servers}")



                data_to_send=json.dumps({"type":2, "new_nodes":global_list_servers_reduced, "salon":self.salon, "hist_mess":self.global_hist_mess}) #à trouver une meilleure appelation
                await self.send(data_to_send,data["addr_server"])

            elif data["type"]==2: #reception des information pour les nouvelles connections
                print("Reception: type 2")
                self.salon=data["salon"]
                self.label_username["text"]=(self.salon+" / "+self.username)
                self.global_hist_mess=data["hist_mess"]
                self.variable_global_hist_mess=len(data["hist_mess"])
                for i in data["hist_mess"]:
                    self.interface_message.insert(END,("["+str(int(i["heure"][:2])+2)+":"+i["heure"][2:4]+"] "+i["pseudo"]+i["message"]))
                    if i["color"]!="":
                        self.interface_message.itemconfig(END, foreground=i["color"])
                if len(data["new_nodes"])>0:
                    data["new_nodes"][0]=tuple(data["new_nodes"][0])
                    self.global_list_servers.append(data["new_nodes"][0])
                    self.global_compteur[data["new_nodes"][0]]=0
                    if len(data["new_nodes"])>1:
                        data["new_nodes"][1]=tuple(data["new_nodes"][1])
                        self.global_list_servers.append(data["new_nodes"][1])
                        self.global_compteur[data["new_nodes"][1]]=0
                    #print(f"[Debug] global_servers: {self.global_list_servers}")
                data={"type":0,"addr_server":self.my_addr,"heure": datetime.utcnow().strftime('%H%M%S%f')[:-3] , "pseudo": self.username, "message":">>> s'est connecté <<<","color":"green"}
                if len(self.global_hist_mess)>=self.size_max_hist_mess:
                    del self.global_hist_mess[0]
                self.global_hist_mess.append(data)
                self.interface_message.insert(END, (datetime.now().strftime('[%H:%M] '))+data["pseudo"]+data["message"])
                if data["color"]!="":
                    self.interface_message.itemconfig(END, foreground=data["color"])
                data=json.dumps(data)

                await self.send(data, self.global_list_servers)

            elif data["type"]==3: #déconexions
                print("Reception: type 3")
                #permet de changer en tuple les adresse vu que json les met sous forme de liste
                for i in range(len(data["list_addr"])):
                    data["list_addr"][i]=tuple(data["list_addr"][i])
                data["list_addr"].remove(self.my_addr)
                for i in self.global_list_servers:
                    if i in data["list_addr"]:
                        data["list_addr"].remove(i)
                if len(data["list_addr"])>0:
                    new_addr=data["list_addr"][random.randint(0,len(data["list_addr"])-1)]
                    self.global_list_servers.append(new_addr)
                    self.global_compteur[new_addr]=0
                self.global_list_servers.remove(data["addr_server"])
                del self.global_compteur[data["addr_server"]]

                #print(f"{self.username}[Debug] global_list_servers: {self.global_list_servers}")


            elif data["type"]==4:#requete d'envoie fichier
                print("Reception: type 4")
                if not data["id_file"] in self.global_hist_files:
                    self.global_hist_files[data["id_file"]]=True
                    #envoier que l'on a pas le fichir en question
                    data2={"type":5, "id_file":data["id_file"], "addr_server":self.my_addr, "name_file":data["name_file"]}
                    await self.send(json.dumps(data2),data["addr_server"])
            elif data["type"]==5:#envoi du fichier
                print("Reception: type 5")
                with open(self.global_files_path[data["id_file"]],mode="rb") as file:
                    file=file.read()
                file = codecs.encode(file, "base64").decode()
                await self.send(json.dumps({"type":6,"username":self.username,"id_file":data["id_file"],"addr_server":self.my_addr, "name_file":data["name_file"],"file":file}),data["addr_server"])
            elif data["type"]==6:#reception et renvoie du fichier
                print("Reception: type 6")
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
                self.interface_message.insert(END,(datetime.now().strftime('[%H:%M] ')+"'"+data["name_file"]+"' reçu de " +data["username"]))
                self.interface_message.itemconfig(END, foreground="orange")
                list_accepted_picture_format=["png","jpeg","jpg","gif","PNG","JPEG","JPG","GIF"]
                if data["name_file"].split(".")[-1] in list_accepted_picture_format:
                    self.interface_message.insert(END,(datetime.now().strftime(">>> Cliquez pour avoir un aperçu <<<")))
                    self.interface_message.itemconfig(END, foreground="orange")
                    self.global_path_file_listbox[(self.interface_message.size()-1)]=name_file
                self.global_files_path[data["id_file"]]=file_path
                data2={"type":4,"name_file":data["name_file"], "id_file":data["id_file"], "addr_server":self.my_addr}
                await self.send(json.dumps(data2), self.global_list_servers,sender=data["addr_server"])






    async def run_server(self):

        #print(self.global_list_servers)
        self.server = await asyncio.start_server(self.reception, self.my_ip, self.my_port) #sers à cette adresse
        addr = self.server.sockets[0].getsockname()

        #print(f'Serveur: Serving on {addr}')

        async with self.server:
            await self.server.serve_forever()


    async def exit_prog(self):
        print("Fermeture du programme en cours...")
        #envoie du message de deconnexion
        self.is_running=False
        self.fenetre.destroy()
        data={"type":0,"addr_server":self.my_addr,"heure": datetime.utcnow().strftime('%H%M%S%f')[:-3] , "pseudo": self.username, "message":">>> s'est déconnecté <<<","color":"red"}
        data=json.dumps(data)
        try:
            await self.send(data, self.global_list_servers)
        except OSError:
            print("[WinError 121] Le délai de temporisation de sémaphore a expiré")
        await asyncio.sleep(1)
        #envois d'information pour que le système reste robuste malgré le noeud en moins
        data={"type":3,"addr_server":self.my_addr,"list_addr":self.global_list_servers}
        data=json.dumps(data)
        try:
            await self.send(data, self.global_list_servers)
        except OSError:
            print("[WinError 121] Le délai de temporisation de sémaphore a expiré")
        await asyncio.sleep(0.5)
        sys.exit()



    def path_leaf(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)


    async def send_message(self):
        data={"type":0,"addr_server":self.my_addr,"heure": datetime.utcnow().strftime('%H%M%S%f')[:-3] , "pseudo": self.username, "message":("> "+ self.string_var_entry_message),"color":""}
        if len(self.global_hist_mess)>=self.size_max_hist_mess:
            del self.global_hist_mess[0]
        self.global_hist_mess.append(data)
        self.interface_message.insert(END, (datetime.now().strftime('[%H:%M] '))+data["pseudo"]+data["message"])
        if data["color"]!="":
            self.interface_message.itemconfig(END, foreground=data["color"])
        await self.send(json.dumps(data),self.global_list_servers)

    async def initialize_send_file(self):
        name_file=self.path_leaf(self.path)
        id_file=datetime.utcnow().strftime('%H%M%S%f')[:-3]+self.username+name_file
        #print(f"[Debug] name_file{name_file}")
        self.global_hist_files[id_file]=True
        self.global_files_path[id_file]=self.path
        data={"type":4,"name_file":name_file, "id_file": id_file, "addr_server":self.my_addr}
        self.interface_message.insert(END,(datetime.now().strftime('[%H:%M] ')+"'"+data["name_file"]+"' envoyé"))
        self.interface_message.itemconfig(END, foreground="orange")
        self.path=""
        await self.send(json.dumps(data), self.global_list_servers)

#initialise la première connexion
    async def initialize(self):
        #print(self.global_list_servers)

        if self.ip_server!=0:
            sent=False
            data_ini=json.dumps({"type":1, "addr_server":self.my_addr})
            while not sent and self.is_running:
                try:
                    sent=await self.send(data_ini, (self.ip_server, self.port_server) ,sent=True,first=True)
                except OSError:
                    print("[WinError 121] Le délai de temporisation de sémaphore a expiré")
                print("Tentative de connexion échouée ")
                await asyncio.sleep(1)

    async def interface(self): #création de l'interface
        def display_picture(event=""):
            line_selected=self.interface_message.curselection()
            #print(f"{self.username} [Debug] global_list_ports_servers: {self.global_list_servers}")
            #print(line_selected)
            if len(line_selected)==1:
                line_selected=line_selected[0]
                if line_selected in self.global_path_file_listbox:
                    #print("[debug] Affichage image")
                    img = Image.open((self.path_to_fichiers+self.global_path_file_listbox[line_selected]))
                    img.show()
        #print(self.global_list_servers)
        def fct_button_send(event=""):
            self.string_var_entry_message=var_entry_message.get()
            asyncio.create_task(self.send_message())
            var_entry_message.set("")
        def exit_fenetre():
            #print("Fin du programme")
            asyncio.create_task(self.exit_prog())

        def button_file_pessed():
            self.fenetre.filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("zip files","*.zip"),("gif files","*.gif"),("jpeg files","*.jpeg"),("jpg files","*.jpg"),("png files","*.png"),("txt files","*.txt"),("gif files","*.gif"),("all files","*.*")))
            if isinstance(self.fenetre.filename, str) and self.fenetre.filename!="":
                self.path = self.fenetre.filename
                asyncio.create_task(self.initialize_send_file())



        width_fenetre=50
        height_fenetre=25
        width_button=2

        self.fenetre = Tk()




        var_entry_message=StringVar()
        self.label_username = Label(self.fenetre, text=self.salon+" / "+self.username)
        self.label_username.grid(row=0)

        self.interface_message = Listbox(self.fenetre,width=width_fenetre, height=height_fenetre,selectmode='single')
        self.interface_message.bind("<Button-1>", display_picture)
        self.interface_message.bind('<FocusOut>', lambda e: self.interface_message.selection_clear(0, END))
        self.interface_message.grid(row=1)


        entry_message = Entry(self.fenetre, textvariable=var_entry_message, width=int(width_fenetre-(width_button*2)-8))
        entry_message.bind("<Return>", fct_button_send)
        entry_message.grid(row=2)

        button_send= Button(self.fenetre, text="↵",width=width_button, command=fct_button_send)
        button_send.grid(row=2,sticky=E)
        button_file=Button(self.fenetre, text="┌↑┐",width=width_button,command= button_file_pessed)
        button_file.grid(row=2,sticky=W)

        self.fenetre.protocol('WM_DELETE_WINDOW', exit_fenetre)

        self.fenetre.update()

        while self.is_running:
            self.fenetre.update()
            await asyncio.sleep(0.05)



    async def main(self):
        #print(self.global_list_servers)
        await asyncio.gather(self.run_server(),
                             self.interface(),
                             self.initialize())

    def run(self):

        self.configuration(menutkinter.Menu_tk.start(self))
        asyncio.run(self.main())


if __name__=="__main__":
    Application().run()
