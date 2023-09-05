from direct.gui.DirectGui import *
from panda3d.core import *

class Menu:
    def __init__(self, *btns):
        self.font = loader.loadFont("Minecrafter.Alt.ttf")
        self.bg_image = loader.loadTexture("menu_bg.jpg")
        self.btn_image = loader.loadTexture("btn.png")

        self.menuScreen = DirectFrame(frameColor = (0, 0, 0, 1),
                                     frameSize=(-1, 1, -1, 1),
                                     image= self.bg_image,
                                     parent=render2d                                     
                                     )
        self.titleMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "PyCraft",
                            scale = 0.2,
                            pos = (0, 0, 0.6),
                            parent = self.titleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1))
        height = 0.25
        for btn in btns:
            button = DirectButton(text = btn[0],
                            command = btn[1],
                            pos = (0, 0, height),
                            parent = self.titleMenu,
                            scale = 0.1,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1),
                            frameTexture = self.btn_image,
                            frameSize = (-5, 5, -1, 1),
                            text_scale = 0.75,
                            relief = DGG.FLAT,
                            pressEffect = 1,                        
                            text_pos = (0, -0.2))
            button.setTransparency(True)
            height -= 0.225

    def show(self):
        self.menuScreen.show()
        self.titleMenu.show()

    def hide(self):
        self.menuScreen.hide()
        self.titleMenu.hide()