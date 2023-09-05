import pickle

class MapManager:
    def __init__(self):
        self.model = "block/block.egg"
        self.texture = loader.loadTexture("block/block.png")
        self.color = (0.0, 0.6, 0.0, 1)
        self.colors = [
            (0.5, 0.3, 0.0, 1),
            (0.2, 0.2, 0.3, 1),
            (0.5, 0.5, 0.2, 1),
            (0.0, 0.6, 0.0, 1),
            (0.4, 0.2, 0, 1),
            (0.38431, 0.38431, 0.35686, 1)
        ]
        self.newLand()
        
        
    def newLand(self):
        """Створення нового вузла-локації"""
        self.land = render.attachNewNode("Land")
    
    def getColor(self, num):
        if num < len(self.colors):
            return self.colors[num]
        else:
            return self.colors[-1]

    def addBlock(self, pos, num_color):
        """Додавання нового блоку в точці pos"""
        self.block = loader.loadModel(self.model)
        self.block.setTexture(self.texture)
        self.block.setPos(pos)
        self.block.setColor(self.getColor(num_color))
        self.block.reparentTo(self.land)

        self.block.setTag("pos", str(pos))
        self.block.setTag("color", str(num_color))

    
    def loadLand(self, filename):
        with open(filename, "r") as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for col in line:
                    for z in range(int(col)+1):
                        self.addBlock((x,y,z), z)
                    x += 1
                y+=1

    def findBlock(self, pos):
        """Пошук блоку в координатах pos по тегу"""
        return self.land.findAllMatches("=pos=" + str(pos))
    
    def isEmpty(self, pos):
        x, y, z = pos
        blocks = self.findBlock((round(x), round(y), round(z))) 
        if blocks:
            return False
        else:
            return True

    def save(self):
        blocks = self.land.getChildren()
        with open("save.dat", "wb") as file:
            x,y,z = base.camera.getPos()
            pickle.dump((x,y,z), file)
            pickle.dump(len(blocks), file)
            for block in blocks:
                x,y,z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file)
                color = block.getTag("color")
                pickle.dump(color, file)
    
    def load(self):
        self.land.removeNode()
        self.newLand()
        with open("save.dat", "rb") as file:
            x,y,z = pickle.load(file)
            k = pickle.load(file)
            for i in range(k):
                pos = pickle.load(file)
                color = pickle.load(file)
                self.addBlock(pos, int(color))
        return x,y,z

