from panda3d.core import NodePath

class Hero:
    """Управління героєм та камерою"""
    def __init__(self, pos, land):
        self.start_pos = pos
        self.land = land
        self.height = 2
        self.current_color = 0
        base.disableMouse() # вимкнення стандартного керування камерою
        base.camera.setPos(self.start_pos) # стартова позиція камери
        base.camLens.setFov(90) # кут огляду камери
        base.camLens.setNear(0.2) 
        base.camera.reparentTo(render)

        self.mouse_step = 0.2
        self.key_step = 0.15

        self.heading = 0 # напрям камери
        self.pitch = 0 # нахил камери
        # координати центру вікна
        self.x_center = base.win.getXSize() // 2
        self.y_center = base.win.getYSize() // 2

        self.ground = True # на землі чи ні
        self.can_move = True # чи можна рухатися вперед
        self.jump_power = 0.4 # сила стрибка
        self.fall_speed = 0 # швидкість падіння
        self.acceleration = 0.025 # прискорення падіння

        self.point = NodePath("point") #точка для перевірки зіткнень
        self.point.reparentTo(render)

        #кожні 20 мілісекунд виклик функції руху movement()
        taskMgr.doMethodLater(0.02, self.movement, 'movement-task')

        self.keys = {} #словник зі станом кнопок
        for key in ['mouse3', 'w', 'a', 's', 'd', 'space']:
            self.keys[key] = 0 # початковий стан - 0
            base.accept(key, self.setKey, [key, 1]) # при натисканні змінюємо стан на 1
            base.accept(key+'-up', self.setKey, [key, 0]) # при відпусканні - на 0

        base.accept("mouse1", self.build)
        base.accept("x", self.destroy)
        base.accept("wheel_up", self.changeColor, ["wheel_up"] )
        base.accept("wheel_down", self.changeColor, ["wheel_down"])
        base.accept("z", self.land.save)
        base.accept("n", self.land.load)

        self.buildSound = base.loader.loadSfx("block/wood03.ogg")
        self.destroySound = base.loader.loadSfx("block/gravel.ogg")
        

    def setKey(self, key_name, state):
        """Задання стану кнопки: 1 - натиснуто, 0 - не натиснуто"""
        self.keys[key_name] = state

    def check_collision(self):
        """Перевірка зіткнень"""
        # перевіряємо чи пусто в точці перед нами
        pitch = base.camera.getP()
        base.camera.setP(0)
        self.point.setPos(base.camera, (0, 1, -1))
        pos = self.point.getPos()
        self.point.setPos(base.camera, (0, 1, 0))
        pos1 = self.point.getPos()
        if self.land.isEmpty(pos) and self.land.isEmpty(pos1): # якщо пусто 
            self.can_move = True                #- можемо рухатися
        else:
            self.can_move = False
        
        if self.keys['s']:
            self.point.setPos(base.camera, (0, -1, -1))
        
            pos = self.point.getPos()
            if self.land.isEmpty(pos): # якщо пусто 
                self.can_move = True   #- можемо рухатися
            else:
                self.can_move = False

        x,y,z = base.camera.getPos()
        if self.land.isEmpty((x, y, z-self.height)):
            self.ground = False
        else: 
            self.ground = True
            self.fall_speed = 0
        
        base.camera.setP(pitch)

    def movement(self, task):
        """Керування з клавіатури"""
        
        self.check_collision() #перевіряємо зіткнення

        if self.ground and self.can_move:
            move_x = (self.keys['d'] - self.keys['a']) * self.key_step
            move_y = (self.keys['w'] - self.keys['s']) * self.key_step
            pitch = base.camera.getP()
            base.camera.setP(0)
            base.camera.setPos(base.camera, move_x, move_y, 0)
            base.camera.setP(pitch)

        if self.keys['space'] and self.ground:
            self.fall_speed = -self.jump_power
            self.ground = False

        if not self.ground:
            move_x = (self.keys['d'] - self.keys['a']) * 0.05
            move_y = (self.keys['w'] - self.keys['s']) * 0.05
            self.fall_speed += self.acceleration

            pitch = base.camera.getP()
            base.camera.setP(0)
            base.camera.setPos(base.camera, move_x, move_y, -self.fall_speed)
            base.camera.setP(pitch)

            if base.camera.getZ() < -30:
                base.camera.setPos(self.start_pos)


        if self.keys['mouse3']:
            mouse_pos = base.win.getPointer(0) #отримуєм об'єкт миші
            new_x =  mouse_pos.getX() #поточні координати миші
            new_y =  mouse_pos.getY() 
            # координати центру вікна
            self.x_center = base.win.getXSize() // 2
            self.y_center = base.win.getYSize() // 2
            if base.win.movePointer(0, self.x_center, self.y_center):
                self.heading = self.heading - (new_x - self.x_center) * self.mouse_step
                self.pitch =  self.pitch - (new_y - self.y_center) * self.mouse_step

            base.camera.setHpr(self.heading,self.pitch, 0)

        return task.again

    def build(self):
        """Будуємо блок в точці перед нами"""

        self.point.setPos(base.camera, (0, 2, 0))
        x,y,z = self.point.getPos()
        pos = (round(x), round(y), round(z))
        if self.land.isEmpty(pos):
            self.land.addBlock(pos, self.current_color)
            self.buildSound.play()

    def destroy(self):
        """Видаляємо блок в точці перед нами"""

        self.point.setPos(base.camera, (0, 2, 0))
        x,y,z = self.point.getPos()
        pos = (round(x), round(y), round(z))
        blocks = self.land.findBlock(pos)
        for block in blocks:
            block.removeNode()
            self.destroySound.play()

    def changeColor(self, wheel):
        
        if wheel == "wheel_up":
            self.current_color += 1
            if self.current_color >= len(self.land.colors):
                self.current_color = 0
        else:
            self.current_color -= 1
            if self.current_color < 0:
                self.current_color = len(self.land.colors)-1
        






