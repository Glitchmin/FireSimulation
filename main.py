from time import sleep
import sys

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpHprInterval, Func, Sequence
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, DirectionalLight, AmbientLight


modelCube = None

def createCube(parent, index, walls, r, g, b, a, x, y, z):
    modelCube.setColor(r, g, b, a)
    cube = modelCube.copyTo(parent)
    cube.setScale(.5)
    cube.setPos(x, y, z)
    # membership = set()  # the walls this cube belongs to

    return cube


class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        walls = {}
        pivots = {}
        rotations = {}

        global modelCube
        modelCube = loader.loadModel("cube.egg")


        for i in range(100):
            createCube(self.render, i, walls, 0.59, 0.27, 0, 1,
                       i % 10 - 2.5, i // 10 - 2.5, 0)

        for i in range(10):
            for j in range(1, 4):
                createCube(self.render, i, walls, 1, 1, 1, 1,
                           -2.5, -2.5 + i, j)
                createCube(self.render, i, walls, 1, 1, 1, 1,
                           6.5, -2.5 + i, j)

        for i in range(10):
            for j in range(1, 4):
                createCube(self.render, i, walls, 1, 1, 1, 1,
                           -2.5 + i, -2.5, j)
                createCube(self.render, i, walls, 1, 1, 1, 1,
                           -2.5 + i, 6.5, j)

        self.directionalLight = DirectionalLight('directionalLight')
        self.directionalLightNP = self.cam.attachNewNode(self.directionalLight)
        self.directionalLightNP.setHpr(-20., -20., 0.)
        self.render.setLight(self.directionalLightNP)
        # self.cam.setPos(-7., -10., 4.)
        # self.cam.lookAt(0., 0., 0.)

        self.seq = Sequence()
    #
    # def testCamera(self):
    #     for i in range(1, 100):
    #         sleep(0.1)
    #         self.cam.setPos(i * 10, i, i)
    #         self.cam.lookAt(0., 0., 0.)


app = MyApp()
app.run()
