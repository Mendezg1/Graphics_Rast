import struct
from collections import namedtuple
from obj import Obj
from mate import matrixmult, barycentricCoords, producto_cruz, restar_vectores, normalizar, inverse
from texture import Texture
from math import pi, sin, cos, tan, radians

V2 = namedtuple('Point2', ['x','y'])
V3 = namedtuple('Point2', ['x','y','z'])

POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

pointstack = []

def resetpoints():
    pointstack.clear()

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b*255), 
                  int(g*255),
                  int(r*255)])
    
def rgba(r,g,b,a):
    return bytes([int(a),
                  int(b*255), 
                  int(g*255),
                  int(r*255)])

class Model(object):
    def __init__(self, filename, textname = None, translate=(0,0,0), rotate=(0,0,0), scale=(1,1,1)):
        model = Obj(filename)

        self.faces = model.faces
        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals

        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        
        if textname:
            self.texture = Texture(textname)

class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.glClearColor(0,0,0)
        self.glClear()
        self.objects = []
        self.vertexShader = None
        self.fragmentShader = None
        self.primitiveType = TRIANGLES
        self.vertexBuffer=[ ]
        self.directionalLight = None
        self.glCamMatrix()
        self.VPMatrix = self.glViewPort(0,0,self.width, self.height)
        self.glPMatrix()
        self.glBackground("valle.bmp")
        self.clearBackground()
        
        self.activeTexture = None
    
    def glPMatrix(self, fov = 60, n = 0.1, f = 1000):
        aspectRatio = self.vpWidth / self.vpHeight
        t = tan(( fov * pi / 180) / 2) * n
        r = aspectRatio * t
        
        self.PMatrix = [
            [n/r , 0, 0, 0],
            [0, n/t, 0, 0],
            [0, 0, -(f+n)/(f-n), (-2*f*n) / (f - n)],
            [0, 0, -1, 0]
        ]
        
    def glViewPort(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height
        
        return [
            [self.vpWidth/2 , 0, 0, self.vpX+(self.vpWidth/2)],
            [0, self.vpHeight/2, 0, self.vpY+ (self.vpHeight/2)],
            [0, 0, 0.5, 0.5],
            [0, 0, 0, 1]
        ]
        
    def glCamMatrix(self,translate=(0,0,0), rotate=(0,0,0)):
        self.CMatrix = self.glModelMatrix(translate, rotate)
        
        self.VMatrix = inverse(self.CMatrix) 
        
    def glLookat(self, camPos = (0,0,0), dest = (0,0,0)):
        WUp = (0,1,0)
        forward = normalizar(restar_vectores(camPos, dest)) 
        right = normalizar(producto_cruz(WUp, forward))
        up = normalizar(producto_cruz(forward, right)) 
        
        self.CMatrix = [[right[0],up[0],forward[0],camPos[0]],
                                    [right[1],up[1],forward[1],camPos[1]],
                                    [right[2],up[2],forward[2],camPos[2]],
                                    [0,0,0,1]]
        
        self.VMatrix = inverse(self.CMatrix)
            

    def glRotationMat(self, pitch = 0, yaw = 0, roll = 0):

        pitchMat = [
            [1,0,0,0],
            [0,cos(radians(pitch)),-sin(radians(pitch)),0],
            [0,sin(radians(pitch)),cos(radians(pitch)),0],
            [0,0,0,1]
        ]
        
        yawMat = [
            [cos(radians(yaw)), 0, sin(radians(yaw)), 0],
            [0,1,0,0],
            [-sin(radians(yaw)),0,cos(radians(yaw)),0],
            [0,0,0,1]
        ]
        
        rollMat = [
            [cos(radians(roll)),-sin(radians(roll)),0,0],
            [sin(radians(roll)),cos(radians(roll)),0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]
        
        return matrixmult(matrixmult(pitchMat,yawMat), rollMat)
    

    def glAddVertices(self, vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)

    def glPrimitiveAssembly(self,uVerts,tVerts, tTextC,normals):
        primitives = [ ]
        if self.primitiveType == TRIANGLES:
            for i in range(0,len(tVerts), 3):
                triangle = [ ]
                l = len(tVerts) - 1
                if(i == l):
                    i = len(tVerts)
                    triangle.append(uVerts[i-3])
                    triangle.append(uVerts[i-2])
                    triangle.append(uVerts[i-1])
                    triangle.append(tVerts[i-3])
                    triangle.append(tVerts[i-2])
                    triangle.append(tVerts[i-1])
                    
                elif(i > l):
                    dif = i - tVerts
                    triangle.append(uVerts[i-dif])
                    triangle.append(uVerts[i-dif +1])
                    triangle.append(uVerts[i-dif + 2])
                    triangle.append(tVerts[i-dif])
                    triangle.append(tVerts[i-dif +1])
                    triangle.append(tVerts[i-dif + 2])
                    
                else:
                    triangle.append(uVerts[i])
                    triangle.append(uVerts[i+1])
                    triangle.append(uVerts[i+2])
                    triangle.append(tVerts[i])
                    triangle.append(tVerts[i+1])
                    triangle.append(tVerts[i+2])
                    
                triangle.append(tTextC[i])
                triangle.append(tTextC[i + 1])
                triangle.append(tTextC[i + 2])
                
                triangle.append(normals[int(i/3)])
                
                primitives.append(triangle)
        if self.primitiveType == LINES:
            for i in range(0, len(tVerts), 2):
                line = []
                line.append(tVerts[i])
                line.append(tVerts[i+1])
                primitives.append(line)
        
        return primitives
    def glPoly(self, verts, flag = True, clr = color(1,1,1)):
        lon = len(verts) - 1
        for i in range(lon):
            self.glLine(verts[i], verts[i+1], clr)
        self.glLine(verts[0], verts[lon], clr)
        points = len(pointstack) - 1
        for i in range(points):
            if i < points:
                if(flag):
                    if i < (int(points/2) - 1):
                        for v0 in pointstack[i]:
                            for v1 in pointstack[points-i]:
                                self.glLine(v0, v1, clr)
                    elif i == int(points/2):
                        for v0 in pointstack[0]:
                            for v1 in pointstack[i]:
                                self.glLine(v0, v1, clr)
                        for v0 in pointstack[0]:
                            for v1 in pointstack[i + 2]:
                                self.glLine(v0, v1, clr)
                        for v0 in pointstack[0]:
                            for v1 in pointstack[int(points/2) + 1]:
                                self.glLine(v0, v1, clr)
                else:
                    # En la idea original este segmento del código no existiría, pero el algoritmo al que llegué tenía mal 
                    # desempeño con la tetera, por lo que agregué esto para que mejorara un poco, pero aún así sigue sin
                    # llenarla correctamente
                    mid = int(points/2)
                    if i < (int(points/2) - 1):
                        for v0 in pointstack[i]:
                            for v1 in pointstack[points-i]:
                                self.glLine(v0, v1, clr)
                    elif i == int(points/2):
                        for v0 in pointstack[mid]:
                            for v1 in pointstack[i]:
                                self.glLine(v0, v1, clr)
                        for v0 in pointstack[mid]:
                            for v1 in pointstack[i + 2]:
                                self.glLine(v0, v1, clr)
                        for v0 in pointstack[mid]:
                            for v1 in pointstack[int(points/2) + 1]:
                                self.glLine(v0, v1, clr)
        resetpoints()
                
            

    def glClearColor(self, r, g, b, a = None):
        if a:
            self.clearColor = rgba(r,g,b,a)
        else:
            self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
                        for x in range(self.width)]
        
        self.zbuffer = [[float('inf') for y in range(self.height)]
                        for x in range(self.width)]
        
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y]=clr or self.currColor
            
    def glBC_Triangle(self,uA,uB,uC, A,B,C, vtA, vtB, vtC, normal):
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))
        
        eje1 = restar_vectores(uB, uA)
        eje2 = restar_vectores(uC, uA)
        
        deltauv1 = restar_vectores(vtB, vtA)
        deltauv2 = restar_vectores(vtC, vtA)
        
        f = 1 / (deltauv1[0] * deltauv2[1] - deltauv1[1] * deltauv2[0])
        
        tangent = [f * deltauv2[1] * eje1[0] - deltauv1[1] * eje2[0],
                   f * deltauv2[1] * eje1[1] - deltauv1[1] * eje2[1],
                   f * deltauv2[1] * eje1[2] - deltauv1[1] * eje2[2]]
        
        tangent = normalizar(tangent)
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                P = (x,y)
                u, v, w = barycentricCoords(A ,B,C,P)
                if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1:
                    z = u * A[2] + v * B[2] + w * C[2]
                    
                    if 0 <= x < self.width and 0 <= y < self.height:
                        z = u * A[2] + v * B[2] + w * C[2]
                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z
                            
                            uvs = (u * vtA[0] + v * vtB[0] + w * vtC[0],
                                   u * vtA[1] + v * vtB[1] + w * vtC[1])
                            
                            if self.fragmentShader:
                                colorP = self.fragmentShader(texCoords = uvs,
                                                             normalMap = self.normalMap,
                                                             texture = self.activeTexture,
                                                             triangleNormal = normal,
                                                             dLight = self.directionalLight,
                                                             y = y,
                                                             x = x,
                                                             tangent = tangent)
                                self.glPoint(x, y, color(colorP[0], colorP[1], colorP[2]))
                            else:
                                self.glPoint(x,y, colorP)

    def glTriangle(self, A,B,C, clr= None):
        # self.glLine(v0,v1,clr or self.currColor)
        # self.glLine(v1,v2,clr or self.currColor)
        # self.glLine(v2,v0,clr or self.currColor)
        if A[1] < B[1]:
            A, B = B, A
        if A[1] < C[1]:
            A, C = C, A
        if B[1] < C[1]:
            B, C = C, B

        if B[1] == C[1]:
            #Abajo
            self.flatBottom(A,B,C)
        elif A[1] == B[1]:
            #Arriba
            self.flatTop(A,B,C)
        else:
            #Ambos
            D = (A[0] + ((B[1] - A[1]) / (C[1] - A[1])) * (C[0] - A[0]), B[1])
    def flatBottom (self,A,B,C):
        try:
            mBA = (B[0] - A[0]) / (B[1] - A[1])
            mCA = (C[0] - A[0]) / (C[1] - A[1])
        except: 
            pass
        else:
            x0 = B[0]
            x1 = C[0]

            for y in range(B[1], A[1]):
                self.glLine(V2(x0, y), V2(x1,y))
                x0 += mBA
                x1 += mCA
    
    def flatTop(self, A,B,C):
        try:
            mBC = (B[0] - C[0]) / (B[1] - C[1])
            mAC = (A[0] - C[0]) / (A[1] - C[1])
        except: 
            pass
        else:
            x0 = A[0]
            x1 = B[0]

            for y in range(B[1], C[1], -1):
                self.glLine(V2(x0, y), V2(x1,y))
                x0 -= mAC
                x1 -= mBC
        

    def glModelMatrix(self, translate=(0,0,0),rotate = (0,0,0), scale=(1,1,1)):
        translateMat = [[1,0,0,translate[0]],
                        [0,1,0,translate[1]],
                        [0,0,1,translate[2]],
                        [0,0,0,1]]
        scaleMat = [[scale[0],0,0,0],
                    [0,scale[1],0,0],
                    [0,0,scale[2],0],
                    [0,0,0,1]]
        
        rotateMat = self.glRotationMat(rotate[0], rotate[1], rotate[2])
        
        return matrixmult(matrixmult(translateMat, scaleMat), rotateMat)

    def glLine(self, v0, v1, clr=None):
        #Bresenham line algorithm
        #m=(v1.y-v0.y)/(v1.x-v0.x)
        #y=v0.y
        #for x in range(v0.x, v1.x + 1):
            #self.glPoint(x,int(y))
            #y+=m
        selfpoints = []
        x0=int(v0.x)
        x1=int(v1.x)
        y0=int(v0.y)
        y1=int(v1.y)

        #si el punto 0 es igual al punto 1 solo dibujar un punto
        if x0==x1 and y0==y1:
            self.glPoint(x0,y0)
            return
        
        dy = abs(y1-y0)
        dx = abs(x1-x0)

        steep = dy > dx

        # si la linea tiene pendiente > 1 
        # se intercambian las x por y para poder
        # dibujar la linea de manera vertical en vez de horizontal 
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        # Si el punto inicial en X es mayor que el punto final en X
        # intercambiamos los puntos para siempre dibujar de
        # izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1-y0)
        dx = abs(x1-x0)


        offset=0
        limit=0.5
        m = dy/dx
        y=y0

        for x in range(x0, x1+1):
            if steep:
                #Dibujar de manera vertical
                self.glPoint(y,x, clr or self.currColor)
                selfpoints.append(V2(y,x))
            else:
                #Dibujar de manera horizontal
                self.glPoint(x,y, clr or self.currColor)
                selfpoints.append(V2(x,y))

            offset += m

            if offset >= limit:
                if y0<y1:
                    y+=1
                else:
                    y-=1
                
                limit +=1
        pointstack.append(selfpoints)
    
    def loadNormalMap(self,textname):
        self.normalMap = Texture(textname)
    
    def glBackground(self, filename):
        self.background = Texture(filename)
                                  
    def clearBackground(self):
        
        self.glClear()
        
        if self.background:
            
            for x in range(self.vpX, self.vpX + self.vpWidth + 1):
                for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                    
                    u = (x - self.vpX) / self.vpWidth
                    v = (y - self.vpY) / self.vpHeight
                    
                    texColor = self.background.getColor(u,v)
                    
                    if texColor :
                        self.glPoint(x,y,color(texColor[0],texColor[1],texColor[2]))
        

    def glLoadModel(self, filename, textname = None, normal = None, translate=(0,0,0),rotate=(0,0,0) ,scale=(1,1,1), light = (0,0,-1)):
       
        if normal:
            self.loadNormalMap(normal)
        else:
            self.normalMap = None
        self.directionalLight = light
        self.objects.append(Model(filename, textname, translate,rotate,scale))
        

    def glRender(self):
        transformedVerts = []
        normalverts = []
        texturec = []
        normals = []

        if len(self.objects) > 0:
            for model in self.objects:
                mMatrix = self.glModelMatrix( translate=model.translate, scale=model.scale, rotate=model.rotate)
                
                if model.texture:
                    self.activeTexture = model.texture
                fi = 0
                for face in model.faces:
                    vertCount = len(face)
                    v0=model.vertices[face[0][0] -1]
                    v1=model.vertices[face[1][0] -1]
                    v2=model.vertices[face[2][0] -1]
                    
                    normalverts.append(v0)
                    normalverts.append(v1)
                    normalverts.append(v2)
                    # vn0 = model.normals[face[0][2] - 1]
                    # vn1 = model.normals[face[1][2] - 1]
                    # vn2 = model.normals[face[2][2] - 1]
                    triangleNormal = producto_cruz(restar_vectores(v1,v0),restar_vectores(v2,v0) )
                    triangleNormal = normalizar(triangleNormal)
                    normals.append(triangleNormal)
                    if vertCount == 4:
                        v3=model.vertices[face[3][0] -1]
                        normalverts.append(v0)
                        normalverts.append(v2)
                        normalverts.append(v3)
                        # vn3 = model.normals[face[3][2] - 1]
                        triangleNormal = producto_cruz(restar_vectores(v2,v0),restar_vectores(v3,v0) )
                        triangleNormal = normalizar(triangleNormal)
                        normals.append(triangleNormal)
                                          
                    if self.vertexShader:
                        
                        if model.normals:
                            vn0 = model.normals[face[0][2] - 1]
                            vn1 = model.normals[face[1][2] - 1]
                            vn2 = model.normals[face[2][2] - 1]
                            if vertCount == 4:
                                vn3 = model.normals[face[3][2]-1]
                            v0=self.vertexShader(v0, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix,
                                                normal = vn0)
                            v1=self.vertexShader(v1, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix,
                                                normal = vn1)
                            v2=self.vertexShader(v2, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix,
                                                normal = vn2)
                            if vertCount == 4:
                                v3=self.vertexShader(v3, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix,
                                                normal = vn3)
                        else:
                            v0=self.vertexShader(v0, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix)
                            v1=self.vertexShader(v1, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix)
                            v2=self.vertexShader(v2, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix)
                            if vertCount == 4:
                                v3=self.vertexShader(v3, modelMatrix=mMatrix,
                                                viewMatrix = self.VMatrix,
                                                proyMatrix = self.PMatrix,
                                                viewpMatrix = self.VPMatrix)
                    
                    transformedVerts.append(v0)
                    transformedVerts.append(v1)
                    transformedVerts.append(v2)
                    if vertCount == 4:
                        transformedVerts.append(v0)
                        transformedVerts.append(v2)
                        transformedVerts.append(v3)
                    if model.texture:
                        vt0 = model.texcoords[face[0][1] - 1]
                        vt1 = model.texcoords[face[1][1] - 1]
                        vt2 = model.texcoords[face[2][1] - 1]
                        if vertCount == 4:
                            vt3 = model.texcoords[face[3][1] - 1]
                        texturec.append(vt0)
                        texturec.append(vt1)
                        texturec.append(vt2)
                        if vertCount == 4:
                            texturec.append(vt0)
                            texturec.append(vt2)
                            texturec.append(vt3)
                            
                    fi += 1
        else:
            for vert in self.vertexBuffer:
                if self.vertexShader:
                    transformedVerts.append(self.vertexShader(vert, modelMatrix = False))
                else:
                    transformedVerts.append(vert)

        primitives = self.glPrimitiveAssembly(normalverts, transformedVerts, texturec, normals)

        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                self.glBC_Triangle(prim[0], prim[1], prim[2],
                                   prim[3], prim[4], prim[5],
                                   prim[6], prim[7], prim[8],
                                   prim[9])
            if self.primitiveType == LINES:
                self.glLine(prim[0], prim[1])

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14+40+(self.width*self.height * 4)))
            file.write(dword(0))
            file.write(dword(14+40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword((self.width*self.height * 4)))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #ColorTable
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])