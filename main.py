from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'win-size 1600 1000')
# loadPrcFileData('', 'fullscreen True')
loadPrcFileData('', 'show   -frame-rate-meter True')
loadPrcFileData('', 'window-title PyCraft')

from mapmanager import MapManager
from hero import Hero
from menu import Menu

class PyCraft(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Load the environment model.
        self.scene = self.loader.loadModel("ocean_sky_sphere/scene.bam")
        # self.scene.setTexture(
            # loader.loadTexture("ocean_sky_sphere/textures/Material.001_baseColor.jpeg"))
        self.scene.setPos(-200, 200, 0)
        self.scene.setScale(2)
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(100)
        self.land = MapManager()
        self.start = False
        self.menu = Menu(["New game", self.newGame],
                        ["Load game", self.loadGame],
                        ["Save game", self.saveGame],
                        ["exit", base.userExit])
        base.accept('escape', self.showMenu)

    def showMenu(self):
        """"Показати або сховати меню"""
        if self.menu.menuScreen.isHidden():
            self.menu.show()
        elif self.start:
            self.menu.hide()
       

    def newGame(self):
        self.land.loadLand("map/land.txt")
        self.hero = Hero((10,15,3), self.land)
        self.start = True
        self.menu.hide()
    
    def loadGame(self):
        try:
            x,y,z = self.land.load()
            self.hero = Hero((x,y,z), self.land)
            self.start = True
            self.menu.hide()
        except:
            self.newGame()

    def saveGame(self):
        if self.start:
            self.land.save()
            self.menu.hide()
        
app = PyCraft()
app.run()

# gltf2bam scene.gltf scene.bam