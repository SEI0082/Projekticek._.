import csv
import networkx as nx
import numpy as np
import PIL.Image as Image


class Maze:   
    """Class Maze má v sobě funkce a proměnné k generování, vyřešení a následné zobrazení bludišť daných šablon"""
    
    def __init__(self):
        """Konstruktor pro Maze"""
        self.maze = []
        self.n = 0
        self.incidence_matrix = 0
        self.nodes = []
        self.final = []


    def get_Maze(self) -> list:
        """Getter pro array s bludištěm"""
        return self.maze
    def set_Maze(self, maze: list):
        """Setter pro array s bludištěm"""
        self.maze = np.copy(maze)

    def get_N(self) -> int:
        """Getter pro počet řádků v bludišti (i sloupců)"""
        return self.n
    def set_N(self, n: int):
        """Setter pro počet řádků v bludišti (i sloupců)"""
        self.n = n

    def get_IM(self):
        """Getter pro sparse matrix incidenční matice bludiště (Matice vztahů)"""
        return self.incidence_matrix
    def set_IM(self, incidence_matrix):
        """Setter pro sparse matrix incidenční matice bludiště (Matice vztahů)"""
        self.incidence_matrix = incidence_matrix

    def get_Nodes(self) -> list:
        """Getter pro array jednotlivých prvků"""
        return self.nodes
    def set_Nodes(self, nodes: list):
        """Setter pro array jednotlivých prvků"""
        self.nodes = np.copy(nodes)

    def get_Final(self) -> list:
        """Getter pro array nejkratší cesty bludištěm"""
        return self.final
    def set_Final(self, final: list):
        """Setter pro array nejkratší cesty bludištěm"""
        self.final = np.copy(final)


    def load(self, path: str):
        """Metoda load(path) načte bludiště z .csv souboru a uloží ho do 'Maze' proměnné"""

        with open(path) as csv_file:

            #   vrátí iterátor řádků v .csv souboru
            csv_reader = csv.reader(csv_file, delimiter=',')

            n = 0
            maze = []

            #   pro jednotlivé řádky .csv souboru, vložím n prvků do proměnné 'maze'
            for row in csv_reader:
                if (n == 0):
                    n = len(row)
                    for i in range(n):
                        maze.append(row[i])

                else:
                    for i in range(n):
                        maze.append(row[i])
            
            #   Před koncem převedu prvky ze znaků na čísla
            for i in range(len(maze)):
                maze[i] = (int)(maze[i])

        #   Nakonec uložím bludiště a jeho velikost do třídy
        self.set_Maze(maze)
        self.set_N((int)(len(maze)**0.5))

    def printMaze(self):
        """Metoda printMaze vypíše uživateli bludiště na obrazovku, ALE také se stará o vkládání finální cesty do bludiště"""
        
        final = self.get_Final()
        n = self.get_N()
        maze = self.get_Maze()

        #   'obyc' je bool proměnná, která určuje, jestli už mám nalezenou finální cestu nebo ne (False = Ano, True = Ne)
        obyc = False
        if(len(final) == 0): obyc = True

        print("-------------------------------------------")

        #   Proces vykreslování bludiště na obrazovku
        for i in range(n):
            for j in range(n):

                #   Pokud je prvek hrana, vykreslí se '■'
                if (maze[i*n + j] == 1):
                    print("■",end=" ")

                #   Avšak pokud je prvek součástí finální cesty, vykreslí se '▪' a nastaví se prvek v poli na číslo 2
                elif (obyc == False and (i*n + j) in final):
                    print("▪",end=" ")
                    maze[i*n + j] = 2

                #   Nakonec prvek bude cesta, průchozí buňka, vypíše se '□'
                else: 
                    print("□",end=" ")
            print()

        print("-------------------------------------------")        
        
    def incidenceMatrix(self):
        """Metoda incidenceMatrix() vytvoří pro dané bludiště tabulku vztahů jednotlivých průchozích buněk pomocí knihovny 'networkx'"""
        
        nodes = []
        edges = []
        n = self.get_N()
        maze = self.get_Maze()

        #   Proběhne pro všechny prvky matice, pokud prvek je průchozí, vloží se do listu 'nodes' a pokud má kolem sebe další průchozí prvek, oba se vloží do listu 'edges'
        for i in range(n):
            for j in range(n):
                now = i*n + j
                if (maze[now] == 0):
                    nodes.append(now)
                    if(j < n - 1 and maze[now + 1] == 0):
                        edges.append([now, now + 1])
                    if(i < n - 1 and maze[now + n] == 0):
                        edges.append([now, now + n])
                    if(i > 0 and maze[now - n] == 0):
                        edges.append([now - n, now])

        #   Vytvořím pomocí networkx incidenční matici podle nodes a edges
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        #   Vložím vytvořené proměnné do třídy
        self.set_IM(nx.incidence_matrix(G))
        self.set_Nodes(nodes)

    def shortestPath(self) -> bool:
        """Metoda shortestPath() vytvoří na základě incidenční matice nejkratší cestu v bludišti a vrací proměnnou typu bool o úspěšnosti nalezení výsledku"""

        A = (self.get_IM()).todense()
        n = self.get_N()
        nodes = self.get_Nodes()
    
        #   list connections má v sobě vzájemně propojené prvky a nodeCosts je list dvou proměnných, kde první proměnná je pozice prvku v bludišti a druhá je její vzdálenost od počátku (defaultně nastavuji na 9999999)
        connections = []
        nodeCosts = []
        nodeCosts.append([0, 0])
        for i in range(1, len(nodes)):
            nodeCosts.append([nodes[i],9999999])

        #   Tyto cykly naplňují listy nodeCosts a connections, tudíž i hledají cestu v bludišti
        for pocet in range(n**2//2):
            for col in range(len(A.T)):
                i = 0
                j = 0

                #   Najde 1. a 2. prvek v A[col]
                while(A[i][col] != 1 and i < len(A)):
                    i += 1
                j = i + 1
                while(A[j][col] != 1 and j < len(A)):
                    j += 1

                #   Předělá jen prvky s vyšší vzdáleností, upraví nodeCosts a přidá prvky do connections
                if(nodeCosts[j][1] > nodeCosts[i][1]):
                    nodeCosts[j][1] = nodeCosts[i][1] + 1
                    connections.append([nodeCosts[j][0],nodeCosts[i][0]])  
                elif(nodeCosts[j][1] < nodeCosts[i][1]):
                    nodeCosts[i][1] = nodeCosts[j][1] + 1
                    connections.append([nodeCosts[i][0],nodeCosts[j][0]]) 

            #   Pokud koncový prvek má cestu, tak se cyklus ukončí 
            if(nodeCosts[-1][1] < 9999999): break           

        #   Pokud ale cesta nebyla nalezena, metoda se ukončí s hodnotou 'False'
        if(nodeCosts[-1][1] == 9999999):
            return False
    
        #   Deklarace finální cesty + její první proměnné
        final = []
        final.append(nodeCosts[-1][0]) 

        #   Cyklus pro nalezení cesty spočívá v tom, že jedu od posledního prvku a hledám všechny se vzdáleností od počátku o 1 menší a zarověň prvky musí být propojené
        for i in range(nodeCosts[-1][1], -1, -1):
            for j in range(len(nodeCosts)-1, -1, -1):

                #   List array slouží k uložení všech prvků s danou vzdáleností
                array = []
                if(nodeCosts[j][1] == i - 1):
                    for k in range(len(nodeCosts)):
                        if(nodeCosts[k][1] == i):
                            array.append(k)
                    for k in range(len(array)):
                        if([nodeCosts[array[k]][0], nodeCosts[j][0]] in connections and final[-1] == nodeCosts[array[k]][0]):
                            final.append(nodeCosts[j][0])
                            break
        
        #   Nakonec zkontroluju, jestli cesta byla nalezena a jestli se její vzdálenost rovná vzdálenosti obou konců
        if(len(final) == nodeCosts[-1][1] + 1):
            self.set_Final(final)   
            return True  
        return False  

    def toImage(self, name: str) -> str:
        """Metoda toImage(name) vytvoří z bludiště 'name'.png obrázek, které se ukládají do složky s 'VVP_SEI0082.py'"""

        n = self.get_N()
        maze = self.get_Maze()

        #   Matice 'data' se vytvoří jako matice RGB hodnot, kde všechny hodnoty jsou 0, neboli černé
        data = np.zeros((n + 2, n + 2, 3), dtype=np.uint8)

        #   Poté následně naplňuji matici správnými hodnotami
        for i in range(n):
            for j in range(n):
                if(maze[i * n + j] == 0):
                    data[i + 1][j + 1] = [255, 255, 255]
                elif(maze[i * n + j] == 2):
                    data[i + 1][j + 1] = [255, 0, 0]

        #   Pomocí knihovny 'PIL' vytvořím obrázek s matice 'data' a vrátím uživateli zprávu o tom, jak se jmenuje
        img = Image.fromarray(data, 'RGB')
        img.save(name + ".png")
        return ("Image of the maze is named: " + name)

    def createMaze(self, preset: str):
        """Metoda createMaze kombinuje všechny dosud vytvořené (až na 'load' metodu) k vytvoření a vyřešení bludiště dané šablony"""
        
        n = self.get_N()

        #   List 'blocked' obsahuje prvky bludiště, které se nemohou přepsat a proměnná 'newMaze' se vytvoří jako bludiště jen s počátkem a koncem 
        blocked = []
        newMaze = np.ones(n**2)
        for i in range(-1,1):
            newMaze[i] = 0
        
        #   Šablona 'S' nebo 'slalom' vloží a zablokuje řádky v třetinách bludiště, aby cesta dotkla 2x levé a pravé hrany bludiště
        if(preset == 'S' or preset == 's' or preset == "slalom"):
            first = n//3    #   Prvni třetina
            second = (2 * n)//3 #   Druhá třetina

            newMaze[n * (first + 1) - 1] = 0    #   Poslední prvek prvni třetiny
            newMaze[n * second] = 0 #   První prvek druhe třetiny

            #   do listu 'blocked' vložím všechny prvky řádku v první a druhé třetině bludiště
            for j in range(n):
                blocked.append(n * first + j)
                blocked.append(n * second + j)

        #   Šablona 'L' nebo 'ladder' vloží do bludiště tolik překážek, že cesta povede zig-zag celým bludištěm
        elif(preset == 'L' or preset == 'l' or preset == "ladder"):

            #   Vytvořím listy, které rozdělí bludiště na 5 * 3 políček
            row = [n//5, (2 * n)//5, (3 * n)//5, (4 * n)//5]
            col = [n//3, (2 * n)//3]

            #   Vložím průchozí buňky pro průchod mezi řádky
            for i in range(2):
                newMaze[n * (row[2*i] + 1) - 1] = 0
                newMaze[n * row[1 + 2*i]] = 0

            #   Vložím průchozí buňky pro průchod mezi sloupci
            newMaze[n * (n - 1) + col[0]] = 0
            newMaze[col[1]] = 0
            for i in range(4):
                newMaze[n * (row[i] - 1) + col[i%2]] = 0
                newMaze[n * (row[i] + 1) + col[i%2]] = 0
            
            #   Nakonec zablokuju vkládání 6 přímek bludiště
            for i in range(2):
                for j in range(n):
                    blocked.append(n * row[i] + j)
                    blocked.append(n * row[i + 2] + j)
                    blocked.append(n * j + col[i])

        #   Šablona 'E' nebo 'edges' vloží do bludiště 'trubku', která vede mezi levým-dolním a pravým-horním vrcholem, tak, aby bludiště trubkou muselo projít k dosažení výsledku
        elif(preset == 'E' or preset == 'e' or preset == "edges"):

            newMaze[n**2 - n * (n-1) - 1] = 0   #   Pravy horní roh
            blocked.append(n**2 - n * (n-1) - 2)  #   1 vedle pravého horního rohu
            
            #   Vkládání průchozích buňek na vedlejší a pod-vedlejší diagonálu + blokace prvků nad a pod průchozíma
            for i in range(n-2, n):
                newMaze[n**2 - i * (n-1) - 1] = 0
                newMaze[n**2 - i * (n - 1)] = 0
            for i in range(1, n - 2):
                newMaze[n**2 - i * (n-1) - 1] = 0
                newMaze[n**2 - i * (n - 1)] = 0

                blocked.append(n**2 - i * (n-1) - 2*n)
                blocked.append(n**2 - i * (n - 1) + 1)

        #   Uložení startovního bludiště
        self.set_Maze(newMaze)

        #   Cyklus pojede, dokud nebude nalezena cesta v bludišti, každým cyklem přidá náhodně 'n' počet prvků do bludiště 
        success = False
        while(success == False):

            #   Random nemá žádné omezení, tudíž nemusím kontrolovat, jestli prvky nejsou v 'blocked'
            if(preset == 'R' or preset == 'r' or preset == "random"):
                rand = np.random.rand(n)
                for i in range(len(rand)):
                    newMaze[(int)(rand[i] * (n**2))] = 0

            #   Pro ostatní šablony kontroluju, jestli náhodně vytvoený prvek není v 'blocked'
            elif(preset == 'S' or preset == 's' or preset == "slalom" or preset == 'L' or preset == 'l' or preset == "ladder" or preset == 'E' or preset == 'e' or preset == "edges"):
                rand = np.random.rand(n)
                for i in range(len(rand)):
                    if((int)(rand[i] * (n**2)) in blocked):
                        continue
                    newMaze[(int)(rand[i] * (n**2))] = 0

            #   Nakonec uloží bludiště a otestuje, jestli má řešení
            self.set_Maze(newMaze)
            self.incidenceMatrix()
            success = self.shortestPath()

        #   Až najde řešení, bludiště se naposled uloží a vypíše i s cestou uživateli vyřešené bludiště na obrazovku
        self.set_Maze(newMaze)  
        self.printMaze()

##-------------------------------------------------

BludisteR = Maze()
BludisteR.set_N(10)
BludisteR.createMaze('random')
BludisteR.toImage("BludisteR")
 
BludisteS = Maze()
BludisteS.set_N(10)
BludisteS.createMaze('slalom')
BludisteS.toImage("BludisteS")
 
BludisteL = Maze()
BludisteL.set_N(9)
BludisteL.createMaze('ladder')
BludisteL.toImage("BludisteL")

BludisteE = Maze()
BludisteE.set_N(10)
BludisteE.createMaze('edges')
BludisteE.toImage("BludisteE")