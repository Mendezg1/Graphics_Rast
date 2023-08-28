import math

def matrixmult(m1, m2):
    row2 = len(m1)
    col2 = len(m1[0])
    row1 = len(m2)
    col1 = len(m2[0])

    # Verificar si las matrices se pueden multiplicar
    if col1 != row2:
        raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación.")

    # Crear una matriz resultante llena de ceros que tenga las dimensiones requeridas
    mr = result = [[sum([m1[i][k] * m2[k][j] for k in range(len(m2))]) for j in
                   range(len(m2[0]))] for i in range(len(m1))]

    return mr

def vectbymat(vector, matriz):
    row = len(matriz)
    col = len(matriz[0])
    lvector = len(vector)

    # Verificar si las dimensiones son compatibles para la multiplicación
    if lvector != row:
        raise ValueError("Las dimensiones del vector y la matriz no son compatibles para la multiplicación.")

    # Crear un vector resultante lleno de ceros que tenga el tamaño del vector inicial
    vres = [0] * lvector

    # Realizar la multiplicación de vector por matriz
    for i in range(row):
        for j in range(col):
            vres[i] += vector[j] * matriz[i][j]

    return vres

def barycentricCoords(A,B,C,P):
    areaPBC = (B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])
    
    areaAPC = (C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])
    
    areaABC = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
    try:
        u = areaPBC / areaABC
        v = areaAPC / areaABC
        w = 1 - u - v
        return u, v, w
    except:
        return -1,-1,-1
"""""
    Conversación con ChatGPT:
    ¿como puedo hacer una función que consiga la inversa de una matriz en Python sin librerías externas?
"""""

def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[0] * rows for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    
    return transposed

def cofactor(matrix, row, col):
    submatrix = [row[:col] + row[col+1:] for row in (matrix[:row] + matrix[row+1:])]
    return submatrix

def determinant(matrix):
    size = len(matrix)
    
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for col in range(size):
        det += ((-1) ** col) * matrix[0][col] * determinant(cofactor(matrix, 0, col))
    
    return det

def inverse(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("La matriz no tiene inversa.")
    
    size = len(matrix)
    adjoint = []
    for i in range(size):
        row = []
        for j in range(size):
            sign = (-1) ** (i + j)
            cof = determinant(cofactor(matrix, i, j))
            row.append(sign * cof)
        adjoint.append(row)
    
    adjoint = transpose(adjoint)
    inverse_matrix = [[element / det for element in row] for row in adjoint]
    
    return inverse_matrix

def producto_cruz(vector1, vector2):
    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Los vectores deben ser de tamaño 3 para calcular el producto cruz.")
    
    return [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    ]

def producto_punto(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener la misma longitud para calcular el producto punto.")
    
    return sum(vector1[i] * vector2[i] for i in range(len(vector1)))
    

    """
    Charla con ChatGPT:
    ¿como puedo hacer una función que reste vectores sin usar librerias externas en python?
    """

def restar_vectores(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener la misma longitud para restarlos.")
    
    return [vector1[i] - vector2[i] for i in range(len(vector1))]


def multi_vector(vector, op):
    return [x * op for x in vector]
        
    

    """
    Charla con ChatGPT:
    ¿Cómo puedo normalizar un vector sin librerías externas?
    
    *Nota:
    Las charlas con ChatGPT fueron seguidas, por eso sin especificar que era una función en Python, fue dada en Python.
    """

def normalizar(vector):
    magnitud = math.sqrt(sum(i**2 for i in vector))
    if magnitud == 0:
        return vector
    
    return [i / magnitud for i in vector]
    










