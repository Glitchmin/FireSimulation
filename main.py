from time import sleep

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpHprInterval, Func, Sequence


def createCube(parent, index, cubeMembership, walls):
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
            rgb = [0., 0., 0.]

            r, g, b = rgb
            color = (r, g, b, 1.)

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
    x = index % 9 // 3 - 1
    y = index // 9 - 1
    z = index % 9 % 3 - 1
    cube.setScale(.5)
    cube.setPos(x, y, z)
    membership = set()  # the walls this cube belongs to
    cubeMembership[cube] = membership

    if x == -1:
        walls["left"].append(cube)
        membership.add("left")
    elif x == 1:
        walls["right"].append(cube)
        membership.add("right")
    if y == -1:
        walls["front"].append(cube)
        membership.add("front")
    elif y == 1:
        walls["back"].append(cube)
        membership.add("back")
    if z == -1:
        walls["bottom"].append(cube)
        membership.add("bottom")
    elif z == 1:
        walls["top"].append(cube)
        membership.add("top")

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

        for i in range(27):
            createCube(self.render, i, cubeMembership, walls)

        self.directionalLight = DirectionalLight('directionalLight')
        self.directionalLightNP = self.cam.attachNewNode(self.directionalLight)
        self.directionalLightNP.setHpr(-20., -20., 0.)
        self.render.setLight(self.directionalLightNP)
        self.cam.setPos(-7., -10., 4.)
        self.cam.lookAt(0., 0., 0.)


        def reparentCubes(wallID):
            pivot = pivots[wallID]
            children = pivot.getChildren()
            children.wrtReparentTo(self.render)
            pivot.clearTransform()
            children.wrtReparentTo(pivot)
            for cube in walls[wallID]:
                cube.wrtReparentTo(pivot)

        def updateCubeMembership(wallID, negRotation=False):
            wallOrder = rotations[wallID]["order"]
            if not negRotation:
                wallOrder = wallOrder[::-1]
            for cube in walls[wallID]:
                oldMembership = cubeMembership[cube]
                newMembership = set()
                cubeMembership[cube] = newMembership
                for oldWallID in oldMembership:
                    if oldWallID in wallOrder:
                        index = wallOrder.index(oldWallID)
                        newWallID = wallOrder[index - 1]
                        newMembership.add(newWallID)
                    else:
                        newMembership.add(oldWallID)
                for oldWallID in oldMembership - newMembership:
                    walls[oldWallID].remove(cube)
                for newWallID in newMembership - oldMembership:
                    walls[newWallID].append(cube)

        self.seq = Sequence()

        def addInterval(wallID, negRotation=False):
            self.seq.append(Func(reparentCubes, wallID))
            rot = rotations[wallID]["hpr"]
            if negRotation:
                rot = rot * -1.
            self.seq.append(LerpHprInterval(pivots[wallID], 2.5, rot))
            self.seq.append(Func(updateCubeMembership, wallID, negRotation))
            "Added " + ("negative " if negRotation else "") + wallID + " rotation."

        def acceptInput():
            # <F> adds a positive Front rotation
            self.accept("f", lambda: addInterval("front"))
            # <Shift+F> adds a negative Front rotation
            self.accept("shift-f", lambda: addInterval("front", True))
            # <B> adds a positive Back rotation
            self.accept("b", lambda: addInterval("back"))
            # <Shift+B> adds a negative Back rotation
            self.accept("shift-b", lambda: addInterval("back", True))
            # <L> adds a positive Left rotation
            self.accept("l", lambda: addInterval("left"))
            # <Shift+L> adds a negative Left rotation
            self.accept("shift-l", lambda: addInterval("left", True))
            # <R> adds a positive Right rotation
            self.accept("r", lambda: addInterval("right"))
            # <Shift+R> adds a negative Right rotation
            self.accept("shift-r", lambda: addInterval("right", True))
            # <O> adds a positive bOttom rotation
            self.accept("o", lambda: addInterval("bottom"))
            # <Shift+O> adds a negative bOttom rotation
            self.accept("shift-o", lambda: addInterval("bottom", True))
            # <T> adds a positive Top rotation
            self.accept("t", lambda: addInterval("top"))
            # <Shift+T> adds a negative Top rotation
            self.accept("shift-t", lambda: addInterval("top", True))
            # <Enter> starts the sequence
            self.accept("enter", startSequence)

        def ignoreInput():
            self.ignore("f")
            self.ignore("shift-f")
            self.ignore("b")
            self.ignore("shift-b")
            self.ignore("l")
            self.ignore("shift-l")
            self.ignore("r")
            self.ignore("shift-r")
            self.ignore("o")
            self.ignore("shift-o")
            self.ignore("t")
            self.ignore("shift-t")
            self.ignore("enter")

        def startSequence():
            # do not allow input while the sequence is playing...
            ignoreInput()
            # ...but accept input again once the sequence is finished
            self.seq.append(Func(acceptInput))
            self.seq.start()
            "Sequence started."
            # create a new sequence, so no new intervals will be appended to the started one
            self.seq = Sequence()


        acceptInput()

    def testCamera(self):
        print("test")
        for i in range(1, 100):
            sleep(0.1)
            print("hej")
            self.cam.setPos(i*10, i, i)
            self.cam.lookAt(0., 0., 0.)


app = MyApp()
app.run()


