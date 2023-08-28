from mate import vectbymat, producto_punto, normalizar, producto_cruz
import random


def vertexShader(vertex, **kwargs):

    modelm = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    pmatrix = kwargs["proyMatrix"]
    vpmatrix = kwargs["viewpMatrix"]
    

    if modelm:
        vt = [
        vertex[0],
        vertex[1],
        vertex[2],
        1
        ]
        vt = vectbymat(vectbymat(vectbymat(vectbymat(vt, modelm), viewMatrix), pmatrix),vpmatrix) 
        # vt = vectbymat(vt, modelm)
        # vt = vectbymat(vt, viewMatrix)
        # vt = vectbymat(vt, pmatrix)
        # vt = vectbymat(vt, vpmatrix)
        

        vt = [vt[0]/vt[3], 
            vt[1]/vt[3], 
            vt[2]/vt[3]]
    else:
        vt = vertex
    return vt


def alteredVertexShader(vertex, **kwargs):

    modelm = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    pmatrix = kwargs["proyMatrix"]
    vpmatrix = kwargs["viewpMatrix"]
    normals = kwargs["normal"]
    
    if modelm:
        
        blowamount = 0.3
    
        vt = [vertex[0] ,
        vertex[1] + (normals[1] * blowamount),
        vertex[2] ,
        1]
        
        
        
        vt = vectbymat(vectbymat(vectbymat(vectbymat(vt, modelm), viewMatrix), pmatrix),vpmatrix) 
        # vt = vectbymat(vt, modelm)
        # vt = vectbymat(vt, viewMatrix)
        # vt = vectbymat(vt, pmatrix)
        # vt = vectbymat(vt, vpmatrix)

        vt = [vt[0]/vt[3], 
            vt[1]/vt[3], 
            vt[2]/vt[3]]
    else:
        vt = vertex
    return vt

def fragmentShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    
    if texture:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (0.83,0.83,0.83)
    return color

    """
    Este Shader (en caso mantenga un modelo punteado) es un intento de utilizar la técnica de Alpha Clipping o Rendering Cutout
    sin el valor alpha.
    El motivo de no tener valor alpha es que me fue imposible convertir el bit depth a 32 bits sin echar a perder el archivo.
    
    Para explicar la lógica, pues no fue pensado para solo utilizar un random y listo:
    Se tomó en cuenta que la esquina inferior izquierda es (0,0) y la superior derecha es (1,1).
    Por cada triángulo que entrara a la función, se tomaron unos valores de xy promediadios según los min y max calculados.
    A estos se les sacó un ratio en base al width y height del FrameBuffer respectivamente.
    Luego, para calcular la probabilidad de que este se dibuje es mayor según más a la derecha y arriba está.
    """
    
def clipped(a):
    isClipped = 0.0
    
    if a < 0.2:
        isClipped += 0.1 / 2
    elif a < 0.3:
        isClipped += 0.2 / 2
    elif a < 0.4:
        isClipped += 0.3 / 2
    elif a < 0.5:
        isClipped += 0.4 / 2
    elif a < 0.6:
        isClipped += 0.5 / 2
    elif a < 0.7:
        isClipped += 0.6 / 2
    elif a < 0.8:
        isClipped += 0.7 / 2
    elif a < 0.9:
        isClipped += 0.8 / 2
    elif a == 1:
        isClipped += 1
    return isClipped

def AlphaClipping_NoAlpha(**kwargs):
    dLight = kwargs["dLight"]
    normal = kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    y = kwargs["y"]
    x = kwargs["x"]
    
    ratiox = x / (1920 *0.65) 
    ratioy = y / 950
    
    if texture:
        tcolor = texture.getColor(texCoords[0], texCoords[1])
    
    intensidad = producto_punto(normal, dLight)
    
    color = (intensidad * tcolor[0], intensidad * tcolor[1], intensidad * tcolor[2])
    
    if (ratioy + ratiox) >= 1.85:
        if intensidad > 0:
            return color
        else:
            return(0.196,0.804,0.196)
    elif ((ratioy + ratiox) <= 1.11):
        return (0.196,0.804,0.196)
        
    
    if (random.random() * 2.1) < (ratioy + ratiox):
        if intensidad > 0:
            return color
        else:
            return(0,0,0)
    else:
        return(0.196,0.804,0.196)
    
def Rainbow(**kwargs):
    dLight = kwargs["dLight"]
    normal = kwargs["triangleNormal"]
    y = kwargs["y"]
    x = kwargs["x"]
    
    ratiox = x / (1920 *0.65) 
    ratioy = y / 950
    
    intensidad = producto_punto(normal, dLight)
    
    if (ratiox + ratioy) <= 1.2:
        if intensidad > 0:
            return (intensidad * 0.34,intensidad * 0.14,intensidad * 0.39)
        else:
            return (0.73,0.73,0.73)
    elif (ratiox + ratioy) <= 1.32:
        if intensidad > 0:
            return (intensidad * 0,intensidad * 0, intensidad * 1)
        else:
            return (0.73,0.73,0.73)
    elif (ratiox + ratioy) <= 1.44:
        if intensidad > 0:
            return (intensidad * 0.32,intensidad * 0.82,intensidad * 0.96)
        else:
            return (0.73,0.73,0.73)
    elif (ratiox + ratioy) <= 1.56:
        if intensidad > 0:
            return (intensidad * 0,intensidad * 1,intensidad * 0)
        else:
            return (0.73,0.73,0.73)
    elif (ratiox + ratioy) <= 1.68:
        if intensidad > 0:
            return (intensidad * 1,intensidad * 1,intensidad * 0)
        else:
            return (0.73,0.73,0.73)
    elif (ratiox + ratioy) <= 1.8:
        if intensidad > 0:
            return (intensidad * 1,intensidad * 0.4,intensidad * 0)
        else:
            return (0.73,0.73,0.73)
    elif (ratiox + ratioy) <= 2.1:
        if intensidad > 0:
            return (intensidad * 1,intensidad * 0,intensidad * 0)
        else:
            return (0.73,0.73,0.73)
    
def NegativeShader(**kwargs):
    dLight = kwargs["dLight"]
    normal = kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    
    if texture:
        tcolor = texture.getColor(texCoords[0], texCoords[1])
    
    intensidad = producto_punto(normal, dLight)
    
    color = (1 - (intensidad * tcolor[0]),1 - (intensidad * tcolor[1]), 1 - (intensidad * tcolor[2]))
    
    if intensidad > 0:
            return color
    else:
        return(0.83,0.83,0.83)
    
    """
    Este shader busca 'ensuciar' la textura alterando la intensidad del centro del modelo aleatoriamente.
    """
def dirtyShader(**kwargs):
    dLight = kwargs["dLight"]
    normal = kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    y = kwargs["y"]
    x = kwargs["x"]
    
    ratiox = x / (1920 *0.65) 
    ratioy = y / 950
    
    if texture:
        tcolor = texture.getColor(texCoords[0], texCoords[1])
    
        intensidad = producto_punto(normal, dLight)
        
        if (ratiox + ratioy) >= 0.4 or (ratiox + ratioy) <= 1.8:
            if random.random() > 0.25:
                intensidad = max(intensidad * 0.3, 0.0)
                
        if tcolor:
            color = (intensidad * tcolor[0], intensidad * tcolor[1], intensidad * tcolor[2])
        
            if intensidad > 0:
                return color
            else: 
                return (0,0,0)
        else:
            return (1,1,1)
            
    else:
        return (1,1,1)
    
def flatShader(**kwargs):
    dLight = kwargs["dLight"]
    normal = kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    
    if texture:
        tcolor = texture.getColor(texCoords[0], texCoords[1])
    
        intensidad = producto_punto(normal, dLight)
        
        if tcolor:
            color = (intensidad * tcolor[0], intensidad * tcolor[1], intensidad * tcolor[2])
        
            if intensidad > 0:
                return color
            else: 
                return (0,0,0)
        else:
            return (1,1,1)
    else:
        return (1,1,1)
    
def normalMapShader(**kwargs):
    dLight = kwargs["dLight"]
    normal = kwargs["triangleNormal"]
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]
    normalMap = kwargs["normalMap"]
    tangent = kwargs["tangent"]
    if texture:
        tcolor = texture.getColor(texCoords[0], texCoords[1])
        
        if normalMap:
            texNormal = normalMap.getColor(texCoords[0],texCoords[1])
            
            texNormal = [
                texNormal[0] * 2 -1,
                texNormal[1] * 2 -1,
                texNormal[2] * 2 -1
            ]
            
            texNormal = normalizar(texNormal)
            
            bitangent = producto_cruz(normal, tangent)
            bitangent = normalizar(bitangent)
            
            matriz_tang = [
                [0,0,normal[0]],
                [0,0,normal[1]],
                [0,0,normal[2]]
            ]
            
            texNormal = vectbymat(texNormal, matriz_tang)
            texNormal = normalizar(texNormal)
            intensidad = producto_punto(texNormal, dLight)
        else:
            intensidad = producto_punto(normal, dLight)
        
        if tcolor:
            color = (intensidad * tcolor[0], intensidad * tcolor[1], intensidad * tcolor[2])
        
            if intensidad > 0:
                return color
            else: 
                return (0,0,0)
        else:
            return (1,1,1)
    else:
        return (1,1,1)