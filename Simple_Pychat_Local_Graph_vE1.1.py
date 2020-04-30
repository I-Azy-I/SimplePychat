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


class Application:

    def __init__(self):
        self.if_address=False
        self.string_var_entry_message = "" #permet de récuperer message tkinter
        self.if_button_clicked=False   #savoir si le bouton à été cliqué
        self.global_list_ports_servers=[] #transformer en ensemble?
        self.global_if_mess_received=False
        self.global_hist_mess=[]
        choix=int(input("1 ou 2 ou +: "))
        if choix == 1:
            self.username="JUJU"
            self.ip_client="127.0.0.1"
            self.ip_server="127.0.0.1"
            self.port_client=0#ne se connecte à personne
            self.port_server=8887
        elif choix==2:
            self.username="MIMILE"
            self.ip_client="127.0.0.1"
            self.ip_server="127.0.0.1"
            self.port_client=8887
            self.port_server=8888
        elif choix==3:
            self.username="Pedro"
            self.ip_client="127.0.0.1"
            self.ip_server="127.0.0.1"
            self.port_client=8888
            self.port_server=8889
        elif choix==4:
            self.username="Polo"
            self.ip_client="127.0.0.1"
            self.ip_server="127.0.0.1"
            self.port_client=8888
            self.port_server=8886

        elif choix==5:
            self.username="JCVD"
            self.ip_client="127.0.0.1"
            self.ip_server="127.0.0.1"
            self.port_client=8886
            self.port_server=8885
        else:
            self.username="SIMPLE PYCHAT"
            self.ip_client="127.0.0.1"
            self.ip_server="127.0.0.1"
            self.port_client=8888
            self.port_server=8888
        if self. port_client!=0: #dans le cas ou est le premier
            self.global_list_ports_servers.append(self.port_client)
            print(f"[Debug] global_list_ports_servers: {self.global_list_ports_servers}")



    async def send(self, message, destinataires, sent=False, sender=0):
        if type(destinataires)==int:
            print("test1")
            try:
                reader, writer = await asyncio.open_connection(self.ip_client, destinataires)
                writer.write(message.encode())
                writer.close()
                if sent:
                    return True

            except ConnectionRefusedError:
                print(f"Connection impossible à {destinataires}")
                if sent:
                    return False

        elif type(destinataires)==list:
            for i in range(len(destinataires)):
                if destinataires[i] != sender:
                    try:
                        reader, writer = await asyncio.open_connection(self.ip_client, destinataires[i])
                        writer.write(message.encode())
                        writer.close()
                        if sent:
                            return True
                    except ConnectionRefusedError:
                        print(f"Connection impossible à {destinataires[i]}")
                        if sent:
                            return False
        else:
            print("Erreur fonction send: destinataires n'est ni un int ni une liste")

    async def reception(self, reader, writer):


        def check_id(self, data):
            #regarde si le message est déja dans l'historique
            id=(data["heure"]+data["pseudo"])
            for i in range(len(self.global_hist_mess)):
                if (self.global_hist_mess[i]["heure"]+self.global_hist_mess[i]["pseudo"])==id:
                    return False
            return True

        #def update_global_hist_mess (self):
        #    while len(self.global_hist_mess)>50:
        #        del self.global_hist_mess[0]


        data = await reader.read(100) #serveur attend messages
        data = data.decode()         # décode message
        addr = writer.get_extra_info('peername') #innutil
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

            #historique des message doit etre ajouté ici
            data_to_send=json.dumps({"type":2, "new_nodes":str_global_list_ports_servers}) #à trouver une meilleure appelation
            await self.send(data_to_send,data["port"])

        elif data["type"]==2:
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
                data={"port":self.port_server,"heure": datetime.utcnow().strftime('%H%M%S%f')[:-3] , "pseudo": self.username, "message":("> "+ self.string_var_entry_message)} #le message est ce qui est écrit dans l'interface
                self.global_hist_mess.append(data)


            if i<len(self.global_hist_mess):
                data=self.global_hist_mess[i]
                data["type"]=0
                await self.send(json.dumps(data),self.global_list_ports_servers,sent=False, sender=data["port"])
                i=i+1







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

        listbox_message = Listbox(fenetre)
        listbox_message.pack()

        entry_message = Entry(fenetre, textvariable=var_entry_message, width=30)
        entry_message.pack()

        button_send= Button(fenetre, command=fct_button_send)
        button_send.pack()

        fenetre.update()
        i=0
        while True:

            await asyncio.sleep(0.05)
            if i<len(self.global_hist_mess):
                listbox_message.insert(i, (datetime.now().strftime('[%H:%M] '))+self.global_hist_mess[i]["pseudo"]+self.global_hist_mess[i]["message"])
                i+=1


            fenetre.update()



    async def main(self):
        print(self.global_list_ports_servers)
        await asyncio.gather(self.server(),
                             self.interface(),
                             self.client())

    def run(self):
        asyncio.run(self.main())


if __name__=="__main__":
    Application().run()
