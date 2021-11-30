import numpy as np
from scipy.spatial import Delaunay
import imageio
import math
from PIL import Image, ImageDraw
import scipy.misc as smp
from scipy.interpolate import RectBivariateSpline
from scipy import interpolate
import scipy
from matplotlib.path import Path


# DataPath=os.path.expanduser(~ee364/DataFolder/Lab12/TestData/)

class Triangle:
    def __init__(self, Vertices):

        self.vertices = Vertices
        for i in self.vertices:
            for j in i:
                # if np.issubdtype(j, np.float64)== False:
                if type(j) is not np.float64:
                    raise ValueError("Not Float64")
        if self.vertices.shape != (3,2):
            raise ValueError("Not 3 * 2")

    # def getPoints(self,): # getpoints in trangle # return an np.array(shape(n,2),np.float64) ASk code quality
    #     mask_im = Image.fromarray(np.zeros((1080, 1440)))
    #     modified = ImageDraw.Draw(mask_im)
    #     data = np.zeros((1080, 1440, 3), dtype=np.uint8)
    #     # print(self.vertices[0],"vertices")
    #     # print(self.vertices[1])
    #     # print(self.vertices[2])
    #     modified.polygon(tuple(map(tuple, self.vertices)), fill="white")
    #     # print(tuple(map(tuple, self.vertices)))
    #     # mask_im.show()
    #     a=np.stack(np.asarray(mask_im).nonzero(), axis=1)
    #     # for i in a:
    #     #     data[i[0],i[1]] = [254,0,0]
    #     # modified2.polygon(tuple(map(tuple, np.asarray(mask_im).nonzero())), fill="white")
    #     # mask_im2.show()
    #     # img = smp.toimage(data)  # Create a PIL image
    #     # img.show()
    #     # print(np.asarray(mask_im)[900][50])
    #     del modified
    #
    #     return np.stack(np.asarray(mask_im).nonzero(), axis=1)

    def getPoints(self):
        allpoints = []
        A, B, C = self.vertices
        thrx=np.array((A[0],B[0],C[0]),dtype=np.float64)
        thry = np.array((A[1], B[1], C[1]), dtype=np.float64)
        allx,ally=np.meshgrid(np.arange(np.uint(np.min(thrx)),np.uint(np.max(thrx))+1),np.arange(np.uint(np.min(thry)),np.uint(max(thry))+1))
        pts=list(zip(allx.flatten(),ally.flatten()))
        boolArray=Path([A, B, C]).contains_points(pts)
        for i in range(boolArray.shape[0]):
            if boolArray[i]==True:
                allpoints.append(pts[i])
        return np.array(allpoints,dtype=np.float64)
    # def getPoints(self):
    #     A, B, C = self.vertices
    #     thrx = np.array((A[0],B[0],C[0]),dtype=float)
    #     thry = np.array((A[1], B[1], C[1]), dtype=float)
    #     allx,allys=np.meshgrid(np.arange(np.uint(np.min(thrx)),np.uint(np.max(thrx))+1),np.arange(np.uint(np.min(thry)),np.uint(max(thry))+1))
    #     # points=list(zip(xs.flatten(),ys.flatten()))
    #     # print(points)
    #     pointList=[]
    #     # p = Path([A, B, C])
    #     boolArray=Path([A, B, C]).contains_points(list(zip(allx.flatten(),ally.flatten())))
    #     for i in range(boolArray.shape[0]):
    #         if boolArray[i]==True:
    #             pointList.append(points[i])
    #     return np.array(pointList,dtype=float)
def loadTriangles(leftPointFilePath, rightPointFilePath):
    leftans=[]
    righans=[]
    pointsleft = np.loadtxt(leftPointFilePath,dtype=np.float64)
    # print(pointsleft)
    tril = Delaunay(pointsleft)
    for element in pointsleft[tril.simplices]:
        # print(element)
        leftans.append(Triangle(element))
    # leftreturn = Triangle(tril)

    pointsright = np.loadtxt(rightPointFilePath,dtype=np.float64)
    # trir = Delaunay(pointsright)
    for element in pointsright[tril.simplices]:
        righans.append(Triangle(element))
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
        # print(alpha, "alpha")
        # im = Image.new('L', size)
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
        # print(self.rightImage[0][0],"reight")
        for i in range(0, len(self.leftTriangles)):
            # print(self.leftTriangles[i],"left")
            newpoint = self.rightTriangles[i].vertices * alpha + self.leftTriangles[i].vertices * (1-alpha)
            # print(newpoint, "newpoint")
            HL = self._getTransformH(self.leftTriangles[i], newpoint)
            HR = self._getTransformH(self.rightTriangles[i], newpoint)
            # print(self.leftTriangles[i].vertices, "triangle I")
            # invH = inv(H)
            # print(invH, "inH")
            # print("here")
            target = Triangle(newpoint)
            # print(target.vertices,"tri")
            a = target.getPoints()
            # print(len(a))
            # print(a)
            # print("herheagin")
            # print(a,"getpoints")
            hl = np.array([[HL[0][0], HL[1][0], HL[2][0]], [HL[3][0], HL[4][0], HL[5][0]], [0, 0, 1]], np.float64)
            # print(hl, "small h")
            hr = np.array([[HR[0][0], HR[1][0], HR[2][0]], [HR[3][0], HR[4][0], HR[5][0]], [0, 0, 1]], np.float64)
            # print(hr, "small h")
            invHL = np.linalg.inv(hl)
            invHR = np.linalg.inv(hr)
            # print(invHL, "inHl")
            # print(invHR, "inHr")
            # # hprm
            k=1
            for j in a:
                k=k+1
                # print(k)
                # print(a)
                # print("Makkesure")
                timeh = np.array([[j[0]], [j[1]], [1.0]], np.float64)
                # print("Makkesure")
                hprml = np.dot(invHL, timeh)
                hprmr = np.dot(invHR, timeh)

            #     # print(hprml, "round letf")
            #     print(hprml[0][0], hprml[1][0], "round letf")
            #     print(hprmr[0][0], hprmr[1][0], "round right")
            #     # print("check")

                source_pixelL = fn_imgL(hprml[1][0],hprml[0][0])
            # print("check1")

                source_pixelR = fn_imgR(hprmr[1][0],hprmr[0][0])
            #     # print("check2")
            #     # print(source_pixelL,"sourceLeft")
            #     # print(source_pixelR, "sourceRight")
                data[int(j[1]), int(j[0])] = source_pixelL + source_pixelR
            #     # if int(x) >-1080 and int(y) >0:
            # #     ans1 = self.rightImage[int(xl)][int(yl)]
            # #     ans2 = self.leftImage[int(xr)][int(yr)]
            # #     data[int(x), int(y)] = ans1 * alpha + ans2 * (1 - alpha)
            # img = smp.toimage(data)  # Create a PIL image
            # img.show()
            # ans2 = self.rightImage[int(x)][int(y)]
            # print(ans,"pixel")

        # print(h,"h")
        # for j in self.leftTriangles[i].getPoints():
        # H = np.linalg.solve()

    # for i in
    # for i in self.leftTriangles:
    #     print(i.vertices,"left t")
        return np.array(data,dtype=np.uint8)
    def _getTransformH(self,triangle,target):
        # print("1")
        a = []
        b = []
        tri = triangle.vertices
        tar = target
        # print(tar[0-3],"where1")
        for i in range(0,3):
            a.append(np.array([[tri[i][0], tri[i][1],1,0,0,0], [ 0,0,0,tri[i][0], tri[i][1], 1]], np.float64))
            b.append(np.array([[tar[i][0]], [tar[i][1]]], np.float64))
        H = np.linalg.solve(np.vstack(a),np.vstack(b))
        # print(np.vstack(A),np.vstack(B),"H")
        # invH = np.linalg.inv(H)
        # print(np.vstack(A))
        # print(np.vstack(B))
        # print(H,"HH")
        # print(invH,"inH")
        #print(H)
        return H