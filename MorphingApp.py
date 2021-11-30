import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog,QGraphicsScene
from PyQt5.QtGui import  QPixmap, QImage,QPen,QBrush
from PyQt5.QtCore import QRectF, Qt,QPointF
from MorphingGUI import *
from scipy.interpolate import RectBivariateSpline
from imageio import imread as libread
import numpy as np
from scipy.spatial import Delaunay
import imageio
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import scipy
from matplotlib.path import Path
import sys
np.set_printoptions(threshold=sys.maxsize)


def imread(filePath):
    startImage = libread(filePath)
    return np.array(startImage)


class MorphingApp(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MorphingApp, self).__init__(parent)
        self.scenelorig = QGraphicsScene()
        self.scenel = QGraphicsScene()
        self.scenerorig = QGraphicsScene()
        self.scener = QGraphicsScene()
        self.scenedrawL = QGraphicsScene()
        self.scenedrawR = QGraphicsScene()
        self.scenefinal = QGraphicsScene()
        self.leftPointFilePath = ""
        self.rightPointFilePath = ""
        self.leftImagePath = ""
        self.rightImagePath = ""
        self.leftTriangles = []
        self.rightTriangles = []
        self.allpointsleft = []
        self.allpointsright = []
        self.existsL=""
        self.existsR=""
        self.existphotoL = ""
        self.existphotoR = ""
        self.back = 0
        self.setupUi(self)
        self.pushButton_2.setDisabled(True)
        self.sceneldraw = QGraphicsScene()
        self.scenerdraw = QGraphicsScene()
        self.horizontalSlider.setDisabled(True)

        # self.textEdit.setDisabled(True)
        self.textEdit.setReadOnly(True)
        self.checkBox.setDisabled(True)
        self.LoadStarting.setEnabled(True)
        self.LoadEnding.setEnabled(True)
        self.StartImage.setMouseTracking(True)
        self.EndImage.setMouseTracking(True)
        self.pushButton_2.clicked.connect(self.startblending)
        self.LoadStarting.clicked.connect(self.LloadData)
        self.LoadEnding.clicked.connect(self.RloadData)
        self.checkBox.stateChanged.connect(self.Alltriangle)
        self.horizontalSlider.valueChanged.connect(self.changetext)
        self.scener2 = QGraphicsSceneRdraw(self)
        self.scenel2 = QGraphicsSceneLdraw(self)

        self.pixmapL = QPixmap()
        self.pixmapR = QPixmap()
        self.checkLclick = 0
        self.checkRclick = 0
        self.flag = 0
        self.flagL = 0
        self.flagR = 0
        self.flagB = 0
        self.leftx = 0
        self.lefty = 0
        self.rightx = 0
        self.righty = 0
        self.dflag=0
        self.flagline = 0
        self.filetxt = 0
        self.fileopen = 0

    def changetext(self):
        a=self.horizontalSlider.value()
        self.textEdit.setText(str(round(a*0.01,2)))
    def startblending(self):
        leftImage = imread(self.leftImagePath)
        rightImage = imread(self.rightImagePath)
        leftTriangles, rightTriangles = loadTriangles(self.leftPointFilePath, self.rightPointFilePath)
        morpher = Morpher(leftImage, leftTriangles, rightImage, rightTriangles)
        nparry = morpher.getImageAtAlpha(round(self.horizontalSlider.value()*0.01,2))
        img = Image.fromarray(nparry,'L')
        q_img = ImageQt(img)
        pixmap = QPixmap.fromImage(q_img)
        self.scenefinal.addPixmap(pixmap)
        self.scenefinal.setSceneRect(self.scenefinal.sceneRect())
        self.BlendImage.setScene(self.scenefinal)
        self.BlendImage.fitInView(0,0,self.scenefinal.width(),self.scenefinal.height())
        self.BlendImage.show()

    def Alltriangle(self):
        # print("2")

        check = self.checkBox.isChecked()
        self.scenel2.clear()
        self.scener2.clear()
        self.scenel2.setSceneRect(self.scenel2.sceneRect())
        self.scenel2.addPixmap(self.pixmapL)
        self.scenel2.setSceneRect(self.scenel2.sceneRect())
        # print("3")
        self.scener2.addPixmap(self.pixmapR)
        self.allpointsleft = []
        self.allpointsright = []

        if self.existsL and self.existsR:
            for i in self.leftTriangles:
                for j in i.vertices:
                    self.allpointsleft.append(j)
            for i in self.rightTriangles:
                for j in i.vertices:
                    self.allpointsright.append(j)
            for i in self.allpointsleft:
                x = i[0]
                y = i[1]
                self.scenel2.setSceneRect(self.scenel2.sceneRect())
                self.scenel2.addEllipse(x - 14, y - 14, 28, 28, Qt.red, Qt.red)
                self.scenel2.setSceneRect(self.scenel2.sceneRect())
            for i in self.allpointsright:
                x = i[0]
                y = i[1]
                self.scener2.addEllipse(x - 14, y - 14, 28, 28, Qt.red, Qt.red)
        # print("4")
        if self.filetxt ==1:
            for i in self.leftTriangles:
                for j in i.vertices:
                    self.allpointsleft.append(j)
            for i in self.rightTriangles:
                for j in i.vertices:
                    self.allpointsright.append(j)
            if check is True:
                for i in self.leftTriangles:
                    if self.dflag == 0:
                        self.scenel2.addLine(i[0][0],i[0][1],i[1][0],i[1][1],QPen(Qt.red, 4))
                        self.scenel2.addLine(i[1][0], i[1][1], i[2][0], i[2][1], QPen(Qt.red, 4))
                        self.scenel2.addLine(i[2][0], i[2][1], i[0][0], i[0][1], QPen(Qt.red, 4))
                    else:
                        self.scenel2.addLine(i[0][0], i[0][1], i[1][0], i[1][1], QPen(Qt.yellow, 4))
                        self.scenel2.addLine(i[1][0], i[1][1], i[2][0], i[2][1], QPen(Qt.yellow, 4))
                        self.scenel2.addLine(i[2][0], i[2][1], i[0][0], i[0][1], QPen(Qt.yellow, 4))
                    self.scenel2.setSceneRect(self.scenel2.sceneRect())
                for i in self.rightTriangles:
                    if self.dflag == 0:
                        self.scener2.addLine(i[0][0], i[0][1], i[1][0], i[1][1], QPen(Qt.red, 4))
                        self.scener2.addLine(i[1][0], i[1][1], i[2][0], i[2][1], QPen(Qt.red, 4))
                        self.scener2.addLine(i[2][0], i[2][1], i[0][0], i[0][1], QPen(Qt.red, 4))
                    else:
                        self.scener2.addLine(i[0][0], i[0][1], i[1][0], i[1][1], QPen(Qt.yellow, 4))
                        self.scener2.addLine(i[1][0], i[1][1], i[2][0], i[2][1], QPen(Qt.yellow, 4))
                        self.scener2.addLine(i[2][0], i[2][1], i[0][0], i[0][1], QPen(Qt.yellow, 4))
                    self.scener2.setSceneRect(self.scener2.sceneRect())
        # print("5")
        #
        if self.scenel2.xold and self.scenel2.yold:
            self.scenel2.addEllipse(self.scenel2.xold - 14, self.scenel2.yold - 14, 28, 28, Qt.green, Qt.green)
        if self.back == 1:
            self.scenel2.addEllipse(self.scenel2.xold - 14, self.scenel2.yold - 14, 28, 28, Qt.green, Qt.green)
            self.back = 0
        if self.scenel2.leftpoints:
            if self.scenel2.xold and self.scenel2.yold:
                self.scenel2.addEllipse(self.scenel2.xold - 14, self.scenel2.yold - 14, 28, 28, Qt.green, Qt.green)
            # print(self.scenel2.leftpoints,"left")
            for i in self.scenel2.leftpoints:
                x = i[0]
                y = i[1]
                self.scenel2.addEllipse(x - 14, y - 14, 28, 28, Qt.blue, Qt.blue)
        if self.scener2.xold and self.scener2.yold:
            self.scener2.addEllipse(self.scener2.xold - 14, self.scener2.yold - 14, 28, 28, Qt.green, Qt.green)
        if self.scener2.rightpoints:

            for i in self.scener2.rightpoints:
                if i[0] and i[1]:
                    # print("pass??")
                    x = i[0]
                    y = i[1]
                    self.scener2.addEllipse(x - 14, y - 14, 28, 28, Qt.blue, Qt.blue)

        self.scenel2.setSceneRect(self.scenel2.sceneRect())
        self.StartImage.setScene(self.scenel2)
        self.scenel2.setSceneRect(self.scenel2.sceneRect())
        self.scener2.setSceneRect(self.scener2.sceneRect())
        self.EndImage.setScene(self.scener2)

        pass

    def LloadData(self):

        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open PNG or JPG file ...', filter="XML files (*.png *.jpg)")

        if not filePath:
            return

        self.LloadDataFromFile(filePath)

    def LloadDataFromFile(self, filePath):
        self.pixmapL = QPixmap(filePath)
        self.scenel2 = QGraphicsSceneLdraw(self)
        self.scenel2.addPixmap(self.pixmapL)
        self.StartImage.setScene(self.scenel2)
        self.StartImage.fitInView(0, 0, self.scenel2.width(), self.scenel2.height())
        self.StartImage.show()
        self.leftImagePath = filePath
        self.leftPointFilePath = filePath + ".txt"
        self.existsL = os.path.isfile(self.leftPointFilePath)
        self.existphotoL = os.path.isfile(filePath)
        if self.existsL and self.existsR:
            self.filetxt = 1
            self.leftTriangles,self.rightTriangles = loadTriangles(self.leftPointFilePath,self.rightPointFilePath)
            self.allpointsleft=[]
            self.allpointsright=[]
            for i in self.leftTriangles:
                for j in i.vertices:
                    self.allpointsleft.append(j)
            for i in self.allpointsleft:
                x = i[0]
                y = i[1]
                self.scenel.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
                self.scenel2.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
                self.scenel2.setSceneRect(self.scenel2.sceneRect())
            for i in self.rightTriangles:
                for j in i.vertices:
                    self.allpointsright.append(j)
            for i in self.allpointsright:
                x = i[0]
                y = i[1]
                self.scener.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
                self.scener2.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
        else:
            if self.existphotoL and self.existphotoR:
                a = open(self.leftPointFilePath, "w")
                a.close()
                b = open(self.rightPointFilePath,  "w")
                b.close()
                self.fileopen = 1


        print("AAAAAAAAAAAAAAAAAAAAAAAA")
        if self.existphotoL and self.existphotoR:
            self.pushButton_2.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.Alltriangle()

        pass

    def RloadData(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open PNG or JPG file ...', filter="XML files (*.png *.jpg)")

        if not filePath:
            return

        self.RloadDataFromFile(filePath)

    def RloadDataFromFile(self, filePath):
        self.pixmapR = QPixmap(filePath)
        self.scener2 = QGraphicsSceneRdraw(self)
        self.scener2.addPixmap(self.pixmapR)
        self.EndImage.setScene(self.scener2)
        self.EndImage.fitInView(0, 0, self.scener2.width(), self.scener2.height())
        self.EndImage.show()
        self.rightImagePath = filePath
        self.rightPointFilePath = filePath + ".txt"
        self.existsR = os.path.isfile(self.rightPointFilePath)
        self.existphotoR = os.path.isfile(filePath)
        if self.existsL and self.existsR:
            self.filetxt = 1
            self.leftTriangles, self.rightTriangles = loadTriangles(self.leftPointFilePath, self.rightPointFilePath)
            self.allpointsleft = []
            self.allpointsright = []
            for i in self.leftTriangles:
                for j in i.vertices:
                    self.allpointsleft.append(j)
            for i in self.allpointsleft:
                x = i[0]
                y = i[1]
                self.scenel.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
                self.scenel2.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
            for i in self.rightTriangles:
                for j in i.vertices:
                    self.allpointsright.append(j)
            for i in self.allpointsright:
                x = i[0]
                y = i[1]
                self.scener.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
                self.scener2.addEllipse(x - 10, y - 10, 20, 20, Qt.red, Qt.red)
        else:
            if self.existphotoL and self.existphotoR:
                a = open(self.leftPointFilePath, "w")
                a.close()
                b = open(self.rightPointFilePath,  "w")
                b.close()
                self.fileopen = 1
        if self.existphotoL and self.existphotoR:
            self.pushButton_2.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.Alltriangle()
        pass

    def mousePressEvent(self, event):
        print(self.flagB, "B")
        print(self.flagL, "L")
        print(self.flagR, "R")
        print("checkhere")

        if self.flagL == 1 and self.flagR == 1 and self.flagB == 1:
            if self.leftx and self.lefty and self.rightx and self.righty:
                if (self.leftx, self.lefty) not in self.scenel2.leftpoints:
                    print("save??")
                    self.scenel2.save_points(self.leftx, self.lefty)
                    self.scener2.save_points(self.rightx, self.righty)
                    self.dflag = 1
                    if self.filetxt == 1:
                        print("should be hereh  if 3")
                        self.leftTriangles, self.rightTriangles = loadTriangles(self.leftPointFilePath,
                                                                                self.rightPointFilePath)
            self.scenel2.leftpoints.append((self.leftx, self.lefty))
            self.scener2.rightpoints.append((self.rightx, self.righty))
            self.Alltriangle()
            self.flagB = 0
            self.flagL = 0
            self.flagR = 0

            if self.scenel2.xold != self.leftx and self.scenel2.yold != self.lefty:
                if self.scenel2.xold and self.scenel2.yold:
                    self.flagL = 1
        if self.flagL == 1:
            self.leftx = self.scenel2.xold
            self.lefty = self.scenel2.yold
        if self.flagR == 1:
            self.rightx = self.scener2.xold
            self.righty = self.scener2.yold
            self.flagB = self.flagB+1

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key_Backspace:
            if self.flagL == 1 and self.flagR == 0 and self.flagB == 0:
                self.flag = 0
                self.flagL = 0
                self.leftx = None
                self.lefty = None
                self.scenel2.xold = None
                self.scenel2.yold = None
                self.Alltriangle()
            if self.flagL == 1 and self.flagR == 1 and self.flagB == 1:
                self.flag = 1
                self.flagR = 0
                self.flagB = 0
                self.rightx = None
                self.righty = None
                self.scener2.xold = None
                self.scener2.yold = None
                self.scener2.flag == 1
                self.back=1
                self.Alltriangle()
        pass


class QGraphicsSceneLdraw(QGraphicsScene):
    def __init__(self,ui,parent=None):
        QGraphicsScene.__init__(self, parent)
        self.ui = ui
        self.original = self
        self.click = 0  # left first 0 right first 1
        self.leftpoints = []
        self.savetxtname = "save_L.txt"
        self.xold=None
        self.yold=None
        self.x=None
        self.y=None
        self.ifitthree=0

    def save_points(self,x,y):
        if self.ui.existsL and self.ui.existsR:
            with open(self.ui.leftPointFilePath, "a") as file:
                file.write("\n")
                x=str(round(x, 1))
                lenx=8-len(x)
                for i in range(0,lenx):
                    file.write(" ")
                file.write(x)
                y = str(round(y, 1))
                leny = 8 - len(y)
                for i in range(0, leny):
                    file.write(" ")
                file.write(y)
                file.close()
        if self.ui.fileopen == 1:
            self.ifitthree = self.ifitthree +1
            with open(self.ui.leftPointFilePath, "a") as file:
                x=str(round(x, 1))
                lenx=8-len(x)
                for i in range(0,lenx):
                    file.write(" ")
                file.write(x)
                y = str(round(y, 1))
                leny = 8 - len(y)
                for i in range(0, leny):
                    file.write(" ")
                file.write(y)
                file.write("\n")
                file.close()
            if self.ifitthree >=3:
                self.ui.filetxt = 1

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.ui.Alltriangle()
        if self.ui.flag == 0:
            self.ui.flagL = 1
            Green_pen = QPen(Qt.green)
            Green_brush = QBrush(Qt.green)
            self.x = event.scenePos().x()
            self.y = event.scenePos().y()
            self.ui.flag = 1
            self.addEllipse(self.x - 14, self.y - 14, 28, 28, Green_pen, Green_brush)
            self.xold = self.x
            self.yold = self.y



class QGraphicsSceneRdraw(QGraphicsScene):
    def __init__(self,ui,parent=None):
        QGraphicsScene.__init__(self, parent)
        self.ui = ui
        self.original = self
        self.click = 0  # left first 0 right first 1
        self.rightpoints = []
        self.savetxtname = "save_R.txt"
        self.flag = 1
        self.xold=None
        self.yold=None
        self.x=None
        self.y=None
        self.flag =1

    def save_points(self,x,y):
        if self.ui.existsL and self.ui.existsR:
            with open(self.ui.rightPointFilePath, "a") as file:
                file.write("\n")
                x = str(round(x, 1))
                lenx = 8 - len(x)
                for i in range(0, lenx):
                    file.write(" ")
                file.write(x)
                y = str(round(y, 1))
                leny = 8 - len(y)
                for i in range(0, leny):
                    file.write(" ")
                file.write(y)
                file.close()
        if self.ui.fileopen == 1:
            with open(self.ui.rightPointFilePath, "a") as file:
                x = str(round(x, 1))
                lenx = 8 - len(x)
                for i in range(0, lenx):
                    file.write(" ")
                file.write(x)
                y = str(round(y, 1))
                leny = 8 - len(y)
                for i in range(0, leny):
                    file.write(" ")
                file.write(y)
                file.write("\n")
                file.close()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.ui.Alltriangle()
        if self.flag == 1:
            if self.ui.scenel2.xold:
                print("dontcome?")
                self.ui.scenel2.addEllipse(self.ui.scenel2.xold - 14, self.ui.scenel2.yold - 14, 28, 28, Qt.green, Qt.green)
                self.flag=0
        if self.ui.flag == 1:
            self.ui.flagR = 1
            Green_pen = QPen(Qt.green)
            Green_brush = QBrush(Qt.green)
            self.x = event.scenePos().x()
            self.y = event.scenePos().y()
            self.addEllipse(self.x - 14, self.y - 14, 28, 28, Green_pen, Green_brush)
            self.ui.flag = 0
            self.xold = self.x
            self.yold = self.y



class Triangle:
    def __init__(self, Vertices):

        self.vertices = Vertices
        for i in self.vertices:
            for j in i:
                if type(j) is not np.float64:
                    raise ValueError("Not Float64")
        if self.vertices.shape != (3,2):
            raise ValueError("Not 3 * 2")
    def __getitem__(self, item):
        return self.vertices[item]

    def getPoints(self) -> np.ndarray:
        xmax = int(max(self.vertices[:, 0]) + 1)
        xmin = int(min(self.vertices[:, 0]))
        ymax = int(max(self.vertices[:, 1]) + 1)
        ymin = int(min(self.vertices[:, 1]))

        allx, ally = np.meshgrid(range(xmin, xmax), range(ymin, ymax))
        xandy = np.dstack((allx, ally))
        findxy_flat = xandy.reshape((-1, 2))
        mpath = Path(self.vertices)
        maskflat = mpath.contains_points(findxy_flat)

        return findxy_flat[maskflat]

def loadTriangles(leftPointFilePath, rightPointFilePath):
    leftans=[]
    righans=[]
    pointsleft = np.loadtxt(leftPointFilePath,dtype=np.float64)
    tril = Delaunay(pointsleft)
    for element in pointsleft[tril.simplices]:
        leftans.append(Triangle(element))

    pointsright = np.loadtxt(rightPointFilePath,dtype=np.float64)
    # trir = Delaunay(pointsright)
    for element in pointsright[tril.simplices]:
        righans.append(Triangle(element))
        # print(element,"find")
    # rightreturn = Triangle(trir)
    return (leftans,righans)

class Morpher:
    def __init__(self, LeftImage, LeftTriangles, RightImage, RightTriangles):
        if type(LeftImage) != np.ndarray or type(RightImage) != np.ndarray:
            raise TypeError("It is not numpy arrays.")
        for i in LeftImage:
            for j in i:
                if np.issubdtype(j, np.uint8)== False:
                    raise ValueError("Not unit8")

        if type(LeftTriangles)!= list:
            raise TypeError("Not List!")
        for i in LeftTriangles:
            if type(i) is not Triangle:
                raise ValueError("Not Triangle")

        for i in RightImage:
            for j in i:
                if np.issubdtype(j, np.uint8)== False:
                    raise ValueError("Not unit8")

        if type(RightTriangles)!= list:
            raise TypeError("Not List!")
        for i in LeftTriangles:
            if type(i) is not Triangle:
                raise ValueError("Not Triangle")
        self.leftImage = LeftImage
        self.leftTriangles = LeftTriangles
        self.rightImage = RightImage
        self.rightTriangles = RightTriangles

    def getImageAtAlpha(self, alpha):
        rightsource = self.rightImage*alpha
        leftsource = self.leftImage*(1-alpha)
        maxxl = self.leftImage.shape[0]
        maxyl = self.leftImage.shape[1]
        maxxr = self.rightImage.shape[0]
        maxyr = self.rightImage.shape[1]
        # print(self.leftImage.shape[0],self.leftImage.shape[1])
        fn_imgL = scipy.interpolate.RectBivariateSpline(np.arange(0, maxxl), np.arange(0, maxyl), leftsource,kx=1,ky=1)
        fn_imgR = scipy.interpolate.RectBivariateSpline(np.arange(0, maxxr), np.arange(0, maxyr), rightsource,kx=1,ky=1)
        data = np.zeros((maxxr, maxyr), dtype=np.uint8)
        for i in range(0, len(self.leftTriangles)):
            newpoint = self.rightTriangles[i].vertices * alpha + self.leftTriangles[i].vertices * (1 - alpha)
            HL = self._getTransformH(self.leftTriangles[i], newpoint)
            HR = self._getTransformH(self.rightTriangles[i], newpoint)
            target = Triangle(newpoint)
            a = target.getPoints()

            hl = np.array([[HL[0][0], HL[1][0], HL[2][0]], [HL[3][0], HL[4][0], HL[5][0]], [0, 0, 1]], np.float64)
            hr = np.array([[HR[0][0], HR[1][0], HR[2][0]], [HR[3][0], HR[4][0], HR[5][0]], [0, 0, 1]], np.float64)
            invHL = np.linalg.inv(hl)
            invHR = np.linalg.inv(hr)
            for j in a:
                timeh = np.array([[j[0]], [j[1]], [1.0]], np.float64)

                hprml = np.dot(invHL, timeh)
                hprmr = np.dot(invHR, timeh)
                source_pixelL = fn_imgL(hprml[1][0],hprml[0][0])
                source_pixelR = fn_imgR(hprmr[1][0],hprmr[0][0])

                data[int(j[1]), int(j[0])] = source_pixelL + source_pixelR

        return np.array(data,dtype=np.uint8)

    def _getTransformH(self,triangle,target):
        tri = triangle.vertices
        tar = target
        A = []
        B = []
        for i in range(0,3):
            A.append(np.array([[tri[i][0], tri[i][1],1,0,0,0], [ 0,0,0,tri[i][0], tri[i][1], 1]], np.float64))
            B.append(np.array([[tar[i][0]], [tar[i][1]]], np.float64))
        H = np.linalg.solve(np.vstack(A),np.vstack(B))
        return H

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()

    currentForm.show()
    currentApp.exec_()