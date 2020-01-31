import time
import psutil
import copy
# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for stare in l:
            scrie.write(str(stare))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        return self.sirAfisare()
    def __str__(self):
        return self.sirAfisare()

    def sirAfisare(self):
        stive=self.info
        sir="\n"

        x=0
        for st in stive:
            sir+=str(x)+": "
            x+=1
            for i in range(len(st)):
                sir+= st[i]+ " "
            sir+="\n"
        return(sir)





class Graph:  # graful problemei
    def __init__(self, start, scop , culori):
        self.nrStive = len(start)
        self.start = start
        self.scop = scop
        self.culori=culori
    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []  # pornesc cu lista vida de succesori
        # pentru fiecare stiva i vreau sa incerc sa iau un bloc
        for i in range(self.nrStive):
            # test sa vad daca pot extrage bloc
            if int(nodCurent.info[i][1])>0:
                # mai jos copiez informatia nodului curent in nodul intermediar
                # pentru fiecare stiva j diferita de stiva i (ca sa nu ajung la starea de dinainte)
                for j in range(self.nrStive):
                    if i != j and int(nodCurent.info[j][1])<int(nodCurent.info[j][0]) and int(nodCurent.info[j][1])>0 :
                        x=0
                        for culoare in culori:
                            if (culoare[0]==nodCurent.info[i][2] and culoare[1]==nodCurent.info[j][2]) or (culoare[1]==nodCurent.info[i][2] and culoare[0]==nodCurent.info[j][2]) :
                                x=1
                                infoNou = copy.deepcopy(nodCurent.info)
                                nodSuccesor = NodParcurgere(infoNou,
                                                            nodCurent)  # sau pot pune nodCurent ca parinte daca nu vreau sa afisez si pasii intermediari
                                nodSuccesor.info[j][2] = culoare[2]
                                if (int(nodCurent.info[j][0])>=int(nodCurent.info[i][1])+int(nodCurent.info[j][1])):
                                     # actualizez nodul, punand blocul lipsa pe stiva j
                                     nodSuccesor.info[i][1]='0'
                                     del nodSuccesor.info[i][2]
                                     nodSuccesor.info[j][1]=str(int(nodCurent.info[i][1])+int(nodCurent.info[j][1]))
                             # adaug nodul succesor in lista de succesori
                                else:
                                     nodSuccesor.info[i][1] =str(int(nodSuccesor.info[i][1])-(int(nodSuccesor.info[j][0])-int(nodSuccesor.info[j][1])))
                                     nodSuccesor.info[j][1] =str(int(nodCurent.info[j][0]))
                                listaSuccesori.append(nodSuccesor)

                        if x==0:
                            infoNou = copy.deepcopy(nodCurent.info)
                            nodSuccesor = NodParcurgere(infoNou, nodCurent)
                            nodSuccesor.info[j][2] = 'apa vida'
                            if (int(nodCurent.info[j][0]) >= int(nodCurent.info[i][1]) + int(nodCurent.info[j][1])):
                                nodSuccesor.info[i][1]='0'
                                del nodSuccesor.info[i][2]
                                nodSuccesor.info[j][1] = str(int(nodCurent.info[i][1]) + int(nodCurent.info[j][1]))
                            else:
                                nodSuccesor.info[i][1] =str( int(nodSuccesor.info[i][1]) - (
                                            int(nodSuccesor.info[j][0]) - int(nodSuccesor.info[j][1])))
                                nodSuccesor.info[j][1] = str(int(nodCurent.info[j][0]))
                            listaSuccesori.append(nodSuccesor)

        return listaSuccesori

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


f = open("C:\\Users\\user\\Desktop\\inputtema1.txt", "r")
verif=0
y=0
ver=0
start=[]
scop=[]
culori=[]
for line in f:
        x=0
        for word in line.split():
            if word =='stare_initiala':
                verif=1
                y=-1
                ver=1
            if word =='stare_finala':
                verif=2
                y=-1
                ver=1
            if verif==0 and x==0 and ver==0:
                culori.insert(y, [])
            if verif==1 and x==0 and ver==0:
                start.insert(y, [])
            if verif==2 and x==0 and ver==0:
                scop.insert(y, [])
            if verif==0:
                culori[y].insert(x,word)
                x+=1
            if verif==1 and ver==0:
                start[y].insert(x,word)
                x+=1
            if verif==2 and ver==0:
                scop[y].insert(x,word)
                x+=1

        y+=1
        ver=0
f.close()


gr = Graph( start, scop , culori)

#### algoritm BF
# presupunem ca vrem mai multe solutii (un numar fix)
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritmul la afisarea primei solutii
nrSolutiiCautate = 4
continua = True
def breadth_first(gr):
    global nrSolutiiCautate,lungimeasemanare,lungimesolutie,continua
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(start, None)]
      # variabila pe care o setez la false cand consider ca s-au afisat suficiente solutii
    lungimesolutie=0
    for i in (scop):
        lungimesolutie+=1
    while (len(c) > 0 and continua):
#        print( str(c))
 #       input()
        lungimeasemanare = 0
        nodCurent = c.pop(0)
        for i in  (nodCurent.info): # cautam in toate elementele introduse j scopuri
            for j in  (scop):
                if i[1] !=0:
                    if i[1] == j[0] and i[2]==j[1]:
                        lungimeasemanare+=1
        if lungimeasemanare == lungimesolutie:
            scrie.write("Solutia numarul "+str(4-nrSolutiiCautate+1))
            nodCurent.afisDrum()
            nrSolutiiCautate -= 1
            scrie.write(" \n################# \n\n\n")
        if nrSolutiiCautate == 0:
            continua = False
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)


#def depth_first(gr):
#    df(NodParcurgere(start, None))
#
#def df(nodCurent):
#    global nrSolutiiCautate, continua,lungimesolutie,lungimeasemanare
#    if not continua:
#        return
#    lungimesolutie = 0
#    for i in (scop):
#        lungimesolutie += 1
#    lungimeasemanare=0
#    for i in (nodCurent.info):  # cautam in toate elementele introduse j scopuri
#        for j in (scop):
#           if i[1] != 0:
#                if i[1] == j[0] and i[2] == j[1]:
#                    lungimeasemanare += 1
#    if lungimeasemanare == lungimesolutie:
#        print("Solutia numarul", 4 - nrSolutiiCautate + 1)
#        nodCurent.afisDrum()
#        nrSolutiiCautate-=1
#        if nrSolutiiCautate==0:
#            continua=False
#    lSuccesori=gr.genereazaSuccesori(nodCurent)
#    for sc in lSuccesori:
#        df(sc)

#depth_first(gr)

scrie = open("C:\\Users\\user\\Desktop\\outputtema1.txt", "w")
time1=time.time()
breadth_first(gr)
time2=time.time()
ms=round(1000*(time2-time1))
scrie.write("Programul a rulat "+str(ms)+" ms\n")
scrie.write(str(psutil.virtual_memory()))

scrie.close()
