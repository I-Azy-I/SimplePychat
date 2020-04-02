# -*- encoding: utf-8 -*-

# ip E:192.168.1.22
# ip J:192.168.1.161

#Types des messages: 0=messages ; 1=demande à la connection (ports) ; 2=réponse à la connection (historique des messages, listes de ports )

import asyncio
from tkinter import *
import random

class Application:

    def __init__(self):
        self.if_address=False
        self.string_var_entry_message = "" #permet de récuperer message tkinter
        self.if_button_clicked=False   #savoir si le bouton à été cliqué
        self.global_list_ports_servers=[]
        self.global_new_mess_listbox_message=[]
        self.global_if_mess_received=False
        self.global_mess_received=[]
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
        if self. port_client!=0:
            self.global_list_ports_servers.append(self.port_client)
        print(self.global_list_ports_servers)



    async def send(self, message, destinataires, bool=False, blacklist=0):

        if type(destinataires)==int:
            try:
                reader, writer = await asyncio.open_connection(self.ip_client, destinataires)
                writer.write(message.encode())
                writer.close()
                if bool:
                    return True

            except ConnectionRefusedError:
                print(f"Connection impossible à {destinataires}")
                if bool:
                    return False


        elif type(destinataires)==list:
            for i in range(len(destinataires)):
                if destinataires[i] != blacklist:
                    try:
                        reader, writer = await asyncio.open_connection(self.ip_client, destinataires[i])
                        writer.write(message.encode())
                        writer.close()
                        if bool:
                            return True
                    except ConnectionRefusedError:
                        print(f"Connection impossible à {destinataires[i]}")
                        if bool:
                            return False
        else:
            print("Erreur fonction send: destinataires n'est ni un int ni une liste")


    async def reception(self, reader, writer):
        print(self.global_list_ports_servers)
        data = await reader.read(100) #serveur attend messages
        message = data.decode()         # décode message
        addr = writer.get_extra_info('peername')
        writer.close() #ferme la connexion
        print(f"Serveur: Received {message!r} from {addr[0]}")
        type=message[:1]
        message=message[1:]
        if type=="0": #recois un message, ajoute à la listebox, si c'est un nouveau noeud il faut l'ajouter dans sa liste des noeuds connectés
            self.global_new_mess_listbox_message.append(message[4:])
            port=int(message[:4])
            if not port in self.global_list_ports_servers:
                self.global_list_ports_servers.append(port)
            self.global_mess_received.append((message[4:], port))
        elif type=="1": #nouvelle connection -->  envoyer jusqu'a 2 noeuds, il faut encore controler que l'on envoie pas sont propre port
            port=int(message)
            if len(self.global_list_ports_servers)==0:
                str_global_list_ports_servers=""
            elif len(self.global_list_ports_servers)==1:
                str_global_list_ports_servers=str(self.global_list_ports_servers[0])
            else :
                node1,node2 =random.sample(self.global_list_ports_servers,k=2)
                print(str(node1)+","+str(node2)) #pour ip pas besoin de str
            if not port in self.global_list_ports_servers:
                self.global_list_ports_servers.append(port)

            #historique des message doit etre ajouté ici

                await self.send("2"+str_global_list_ports_servers,port)

        elif type=="2":
            if message !="":
                self.global_list_ports_servers.extend([int(i) for i in message.split(",")])
                print(self.global_list_ports_servers)






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
            bool=False
            while not bool:
                mess_ini="1"+str(self.port_server) #ip deja string
                bool=await self.send(mess_ini, self.port_client,True)
                await asyncio.sleep(1)
        i=0
        while True:
            await asyncio.sleep(0.1)
            if self.if_button_clicked: #si le boutton est cliqué
                self.if_button_clicked = False
                message="0"+f"{self.port_server}" + self.username + "> "+ self.string_var_entry_message #le message est ce qui est écrit dans l'interface
                self.global_new_mess_listbox_message.append(message[5:])
                await self.send(message,self.global_list_ports_servers)




            if i<len(self.global_mess_received):
                (message,port)=self.global_mess_received[i]
                message=f"{self.port_server}" + message
                await self.send(message,self.global_list_ports_servers,bool=False,blacklist=port)
                t=0
                while t<len(self.global_list_ports_servers):
                    await asyncio.sleep(0.05)
                    if self.global_list_ports_servers[t]==port:
                        t=t+1
                    else:
                        try:
                            reader, writer = await asyncio.open_connection(self.ip_client, self.global_list_ports_servers[t])
                            writer.write(message.encode())
                            writer.close()

                        except ConnectionRefusedError:
                            print(f"Connection impossible à {port}")
                        t=t+1
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
            if i<len(self.global_new_mess_listbox_message):
                listbox_message.insert(i, self.global_new_mess_listbox_message[i])
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
