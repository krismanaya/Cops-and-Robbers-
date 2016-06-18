class graph(object): 
    def __init__(self):
        self.m = dict()

    def getvertices(self): 
        return set(self.m.keys())

    def getedges(self):
        e = set()
        for a in self.m.keys():
            for b in self.m[a]:
                e.add((a, b))
        return e

class gamestate(object): 
    def __init__(self,m,n):
        self.m = m
        self.n = n 
        self.cop0 = [0,0]
        self.cop1 = [0,1] 
        self.robber = [m-1,n-1] 

    def movecop(self, cop):
        def moveaxis(axis):
            if cop[axis] < self.robber[axis]: 
                cop[axis] += 1 
            else: 
                cop[axis] -= 1 

        if cop[0] == self.robber[0]: 
            moveaxis(1)
        else: 
            moveaxis(0)

    def movecops(self): 
        self.movecop(self.cop0)
        self.movecop(self.cop1)

    def moverobber(self, dx, dy):
        x = self.robber[0]
        y = self.robber[1]

        if 0 <= x + dx < self.m: 
            x += dx
        else: 
            return False  
        if 0 <= y + dy < self.n: 
            y += dy 
        else: 
            return False 
        print(x,y)
        self.robber[0] = x 
        self.robber[1] = y 

        return True

    def gameover(self):
        if self.cop0 == self.robber or self.cop1 == self.robber: 
            return True
        else: 
            return False 

def makedisconnected(n):
    g = graph()
    g.m = {i: {} for i in range(n)}
    return g

def makepath(n): 
    g = graph()
    g.m = {i: set() for i in range(n)}
    for i in range(n-1): 
        g.m[i].add(i+1)
    for i in range (1,n): 
        g.m[i].add(i-1)
    return g 

def makecycle(n): 
    g = graph()
    g.m = {i: set() for i in range(n)}
    for i in range(n-1): 
        g.m[i].add(i+1)
    for i in range(1,n): 
        g.m[i].add(i-1)
    g.m[0].add(n-1)
    g.m[n-1].add(0)
    return g

def product(g,h): 
    u = []  
    for i in g.getvertices(): 
        for j in h.getedges(): 
            u.append(((i,j[0]),(i,j[1])))
    for i in h.getvertices(): 
        for j in g.getedges(): 
            u.append(((j[0],i),(j[1],i))) 
    g = fromedges(u)
    return g 

def fromedges(e): 
    new_g = graph()
    for e in e: 
        u = e[0]
        v = e[1]
        if u not in new_g.m: 
            new_g.m[u] = {v}
        else: 
            new_g.m[u].add(v)
        if v not in new_g.m: 
            new_g.m[v] = {u}
        else: 
            new_g.m[v].add(u)
    return new_g 

def list2sets(a): 
    return {x for x in a}
