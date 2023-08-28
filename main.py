from gl import Renderer, V2, color
import shaders
import random



width = 1920
height = 1080

rend = Renderer(width,height)

rend.fragmentShader = shaders.flatShader
rend.vertexShader = shaders.alteredVertexShader
rend.glLoadModel(filename="ovni.obj", textname="Ufo.bmp", 
                translate=(7,3,-15), rotate=(0,45,0), scale=(0.8,0.8,0.8), light=(0,0,1))
rend.glRender()

rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.normalMapShader
rend.glLoadModel(filename="barn.obj", textname="barn.bmp", normal = "normalbarn.bmp",
                translate=(-2,-3,-20), rotate=(0,0,0), scale=(0.0061,0.0061,0.0061), light=(0,0,1))
rend.glRender()
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.dirtyShader
rend.glLoadModel(filename="casita.obj", textname="house2.bmp", 
                translate=(-6,-3,-10), rotate=(0,50,0), scale=(0.27,0.27,0.27))
rend.glRender()



rend.fragmentShader = shaders.NegativeShader

rend.glLoadModel(filename="scarecrow.obj", textname="scarecrow.bmp", 
                translate=(-1,-5,-11), rotate=(0,0,0), scale=(0.7,0.7,0.7), light=(0,0,1))
rend.glRender()

rend.fragmentShader = shaders.AlphaClipping_NoAlpha
rend.glLoadModel(filename="vaca.obj", textname="vaca.bmp", 
                translate=(7,-3,-15), rotate=(0,135,0), scale=(0.40,0.40,0.40))
rend.glRender()



rend.glFinish("conshaders.bmp")

def shotMedium():
    rend.glLoadModel(filename="kitty_001.obj", textname="text.bmp", 
                translate=(0,-2,-10), rotate=(0,180,0), scale=(1,1,1))
    rend.glLookat(
            camPos=(0,0,-5),
            dest=(0,0,-10)
            )
    rend.glRender()
    rend.glFinish("mediumShot.bmp")


def shotLowAngle():
    rend.glLoadModel(filename="kitty_001.obj", textname="text.bmp", 
                translate=(0,-2,-10), rotate=(0,180,0), scale=(25,25,25))
    rend.glLookat(camPos=(0,-2,-5),
                dest=(0,0,-10)
    )
    rend.glRender()
    rend.glFinish("lowShot.bmp")
    
def shotHighAngle():
    rend.glLoadModel(filename="kitty_001.obj", textname="text.bmp", 
                translate=(0,-2,-10), rotate=(0,180,0), scale=(15,15,15))
    rend.glLookat(camPos=(0,2,-5),
                dest=(0,0,-10)
    )
    rend.glRender()
    rend.glFinish("highShot.bmp")
    
def shotDutchAngle():
    rend.glLoadModel(filename="kitty_001.obj", textname="text.bmp", 
                translate=(0,-2,-10), rotate=(0,180,-10), scale=(25,25,25))
    rend.glLookat(camPos=(8,0,-1),
                dest=(0,0,-10)
    )
    rend.glRender()
    rend.glFinish("dutchShot.bmp")

#shotMedium()
#shotLowAngle()
#shotHighAngle()
#shotDutchAngle()


# for x in range(100, 501, 1):
#     if x % 2:
#         rend.glColor(0,0,0)
#     else:
#         rend.glColor(1,1,1)

#     rend.glLine(V2(x,x), V2(x+1, x))

# star = [
#     V2(165, 380),V2 (185, 360),V2 (180, 330),V2 (207, 345),V2 (233, 330),V2 (230, 360),V2 (250, 380),
#      V2 (220, 385),V2 (205, 410),V2 (193, 383)
# ]
# rend.glPoly(star, clr =color(1,1,0))

# sq = [V2(321, 335),V2 (288, 286),V2 (339, 251),V2 (374, 302)]
# rend.glPoly(sq, clr=color(1,0,1))

# tria = [
#     V2(377, 249),V2 (411, 197),V2 (436, 249)
# ]
# rend.glPoly(tria, clr=color(0,1,0))


# verts = [
#     V2(413, 177),V2 (448, 159),V2 (502, 88),V2 (553, 53),V2 (535, 36),V2 (676, 37),V2 (660, 52),V2
# (750, 145),V2 (761, 179),V2 (672, 192),V2 (659, 214),V2 (615, 214),V2 (632, 230),V2 (580, 230),V2
# (597, 215) ,V2(552, 214),V2 (517, 144),V2 (466, 180)
#  ]
# rend.glPoly(verts, flag=False, clr=color(0,0,1))


# hoyo = [
# V2(682, 175),V2 (708, 120),V2 (735, 148),V2 (739, 170)

# ]
# rend.glColor(0,0,0)
# rend.glPoly(hoyo, clr = color(0,0,0))

# rend.glTriangle(V2(100, 100), V2(200, 500), V2(300, 100))

# rend.glTriangle(V2(600, 600), V2(900, 600), V2(800, 100) )

# tria = [V2(100,100,1),V2(250,500,1),V2(450,180,1)]

# rend.glBC_Triangle(tria[0], tria[1],tria[2])

