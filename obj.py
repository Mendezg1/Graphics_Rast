from texture import Texture

class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
            except:
                continue

            if prefix.strip() == "v": #Vertex
                self.vertices.append(list(map(float, value.lstrip().split(" "))))
            elif prefix.strip() == "vt": #textura
                self.texcoords.append(list(map(float, value.lstrip().split(" "))))
            elif prefix.strip() == "vn": #normales
                self.normals.append(list(map(float, value.lstrip().split(" "))))
            elif prefix.strip() == "f": #Caras
                self.faces.append([list(map(int, vert.split("/"))) for vert in value.rstrip(" ").split(" ")])

