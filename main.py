from time import sleep

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpHprInterval, Func, Sequence


def createCube(parent, index, cubeMembership, walls, r, g, b, a, x, y, z):
    vertexFormat = GeomVertexFormat.getV3n3cp()
    vertexData = GeomVertexData("cube_data", vertexFormat, Geom.UHStatic)
    tris = GeomTriangles(Geom.UHStatic)

    posWriter = GeomVertexWriter(vertexData, "vertex")
    colWriter = GeomVertexWriter(vertexData, "color")
    normalWriter = GeomVertexWriter(vertexData, "normal")

    vertexCount = 0

    for direction in (-1, 1):

        for i in range(3):

            normal = VBase3()
            normal[i] = direction

            color = (r, g, b, a)

            for a, b in ((-1., -1.), (-1., 1.), (1., 1.), (1., -1.)):
                pos = VBase3()
                pos[i] = direction
                pos[(i + direction) % 3] = a
                pos[(i + direction * 2) % 3] = b

                posWriter.addData3f(pos)
                colWriter.addData4f(color)
                normalWriter.addData3f(normal)

            vertexCount += 4

            tris.addVertices(vertexCount - 2, vertexCount - 3, vertexCount - 4)
            tris.addVertices(vertexCount - 4, vertexCount - 1, vertexCount - 2)

    geom = Geom(vertexData)
    geom.addPrimitive(tris)
    node = GeomNode("cube_node")
    node.addGeom(geom)
    cube = parent.attachNewNode(node)
    cube.setScale(.5)
    cube.setPos(x, y, z)
    membership = set()  # the walls this cube belongs to
    cubeMembership[cube] = membership

    return cube


class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        walls = {}
        pivots = {}
        rotations = {}
        cubeMembership = {}
        wallIDs = ("front", "back", "left", "right", "bottom", "top")
        hprs = {}
        hprs["front"] = hprs["back"] = VBase3(0., 0., 90.)
        hprs["left"] = hprs["right"] = VBase3(0., 90., 0.)
        hprs["bottom"] = hprs["top"] = VBase3(90., 0., 0.)
        wallOrders = {}
        wallOrders["front"] = wallOrders["back"] = ["left", "top", "right", "bottom"]
        wallOrders["left"] = wallOrders["right"] = ["back", "top", "front", "bottom"]
        wallOrders["bottom"] = wallOrders["top"] = ["left", "front", "right", "back"]

        for wallID in wallIDs:
            walls[wallID] = []
            pivots[wallID] = self.render.attachNewNode('pivot_%s' % wallID)
            rotations[wallID] = {"hpr": hprs[wallID], "order": wallOrders[wallID]}

        for i in range(100):
            createCube(self.render, i, cubeMembership, walls, 0.59, 0.27, 0, 1,
                       i % 10 - 2.5, i // 10 - 2.5, 0)

        for i in range(10):
            for j in range(1, 4):
                createCube(self.render, i, cubeMembership, walls, 1, 1, 1, 1,
                           -2.5, -2.5 + i, j)
                createCube(self.render, i, cubeMembership, walls, 1, 1, 1, 1,
                           6.5, -2.5 + i, j)

        for i in range(10):
            for j in range(1, 4):
                createCube(self.render, i, cubeMembership, walls, 1, 1, 1, 1,
                           -2.5 + i, -2.5, j)
                createCube(self.render, i, cubeMembership, walls, 1, 1, 1, 1,
                           -2.5 + i, 6.5, j)

        self.directionalLight = DirectionalLight('directionalLight')
        self.directionalLightNP = self.cam.attachNewNode(self.directionalLight)
        self.directionalLightNP.setHpr(-20., -20., 0.)
        self.render.setLight(self.directionalLightNP)
        self.cam.setPos(-7., -10., 4.)
        self.cam.lookAt(0., 0., 0.)

        self.seq = Sequence()

    def testCamera(self):
        for i in range(1, 100):
            sleep(0.1)
            self.cam.setPos(i * 10, i, i)
            self.cam.lookAt(0., 0., 0.)


app = MyApp()
app.run()
