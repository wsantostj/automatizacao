# [1.1] Imports 

import numpy as np
import matplotlib.pyplot as plt

#%% [1.2] Just the functions used later


def add_circle(matrix, center, radius):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if (i - center[0]) ** 2 + (j - center[1]) ** 2 <= radius ** 2:
                matrix[i, j] = 1

# Function to concatenate matrix
def concatenate_matrix(matrix, repetitions=(2, 2)):

    return np.tile(matrix, repetitions)

def porosity(matrix):
    total = matrix.size
    return float(round((matrix == 0).sum( ) / total, 2))

def concatenate_alternately_with_rotation(matrix, repetitions_v):

    concatenated_matrix = []
    for i in range(repetitions_v):
        if i % 2 == 0:  # Odd index (0, 2...): original matrix
            concatenated_matrix.append(matrix)
        else:           # Even index (1, 3...): rotated matrix
            concatenated_matrix.append(np.rot90(matrix, 2))
    return np.vstack(concatenated_matrix)


def savetxt(file, matrix):
    p = []
    for u in range(matrix.shape[0]):
        for v in range(matrix.shape[1]):
            if matrix[u, v] == 1:
                p.append([v, matrix.shape[0] - u])
    
    np.savetxt(file, p, fmt='%i')

 

def geometry(matrix, topology, r, repetitions = (3,3), number = 15, repetitions_v = 3):
    
    if topology == "centered":
        add_circle(matrix, center, r)
        # Concatenar a matriz 2x2
        # Adicionar círculos nos cantos
        for corner in corners:
            add_circle(matrix, corner, r)
        concatenated_matrix = concatenate_matrix(matrix, repetitions)
    

    elif topology == "square":
        # Adicionar círculos nos cantos
        for corner in corners:
            add_circle(matrix, corner, r)
        concatenated_matrix = concatenate_matrix(matrix, repetitions)
            
    elif topology == "oblique":
        add_circle(matrix, middle, r)
        for corner in corners2:
            add_circle(matrix, corner, r)
        concatenated_matrix = concatenate_matrix(matrix, repetitions = (1, repetitions_v))
        concatenated_matrix = concatenate_alternately_with_rotation(concatenated_matrix, repetitions_v = 3)
    
    """ 
        # Adicionar o círculo central
        if topology == "random":
            concatenated_matrix = concatenate_matrix(matrix, repetitions)
            for cr in center_random:
                add_circle(concatenated_matrix, cr, r = min(nx,ny) // 2)
            
    """

        # Adicionar o círculo central
    return concatenated_matrix    

#%% [1.3] Boundery Conditions or positions where the circles will be placed

nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)


# Centro da matriz
middle = (0, matrix.shape[1] // 2)

center = (matrix.shape[0] // 2, matrix.shape[1] // 2)


# n = 4
# center_random = []
# R_max = min(nx, ny) //2

# # Função para calcular distância entre dois pontos
# def distance(p1, p2):
#     return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# # Geração de centros aleatórios sem sobreposição
# while len(center_random) < n:
#     # Gera um novo centro aleatório
#     new_center = (
#         np.random.randint(0, matrix.shape[0]),
#         np.random.randint(0, matrix.shape[1])
#     )
    
#     # Verifica se ele não se sobrepõe aos já existentes
#     if all(distance(new_center, existing) >= 2 * R_max for existing in center_random):
#         center_random.append(new_center)

# for n in range(n):
#     center_random.append((np.random.randint(0, matrix.shape[0]), np.random.randint(0, matrix.shape[1])))

    
# Coordenadas dos cantos
corners = [
(0, 0),  # Canto superior esquerdo
(0, matrix.shape[1] - 1),  # Canto superior direito
(matrix.shape[0] - 1, 0),  # Canto inferior esquerdo
(matrix.shape[0] - 1, matrix.shape[1] - 1)  # Canto inferior direito
]

corners2 = [
(matrix.shape[1] -1, matrix.shape[1] -1),  # Canto superior direito
(matrix.shape[0] - 1, 0)  # Canto inferior esquerdo
] 
#%% [1.4] Geometry generation for square geometry and save into a diretory


geometry_name = "square"
nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)
n_samples = 20

for order in np.linspace(0.4, 0.8, n_samples):
    i = min(nx,ny) // 2
    porose = 0
    while porose <= order:
        nx, ny = 200, 200
        matrix = np.zeros((ny, nx), dtype=np.uint8)
        matrix = geometry(matrix, topology = geometry_name, r = i, repetitions = (3,3))
        porose = porosity(matrix)
        i -= 0.5
    savetxt(f"{geometry_name}_{porose}.dat", matrix)        


%env geometry_name=$geometry_name
! mkdir -p "$HOME/GEOMETRIES/$geometry_name"
! mv $geometry_name*.dat "$HOME/GEOMETRIES/$geometry_name"


# Visualização
plt.imshow(matrix, cmap='gray')
plt.title(f"{geometry_name} {porose} 2d")
plt.axis('off')
plt.show()

#%% [1.5] Geometry generation for oblique geometry and save into a diretory

geometry_name = "oblique"
nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)
n_samples = 20

for order in np.linspace(0.4, 0.8, n_samples):
    i = min(nx,ny) // 2
    porose = 0
    while porose <= order:
        nx, ny = 200, 200
        matrix = np.zeros((ny, nx), dtype=np.uint8)
        matrix = geometry(matrix, topology = geometry_name, r = i, repetitions = (3,3))
        porose = porosity(matrix)
        i -= 0.5
    savetxt(f"{geometry_name}_{porose}.dat", matrix)        


%env geometry_name=$geometry_name
! mkdir -p "$HOME/GEOMETRIES/$geometry_name"
! mv $geometry_name*.dat "$HOME/GEOMETRIES/$geometry_name"


# Visualização
plt.imshow(matrix, cmap='gray')
plt.title(f"{geometry_name} {porose} 2d")
plt.axis('off')
plt.show()


#%% [1.6] Geometry generation for square geometry and save into a diretory
geometry_name = 'centered'
nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)
n_samples = 20

for order in np.linspace(0.4, 0.8, n_samples):
    i = min(nx,ny) // 2
    porose = 0
    while porose <= order:
        nx, ny = 200, 200
        matrix = np.zeros((ny, nx), dtype=np.uint8)
        matrix = geometry(matrix, topology = geometry_name, r = i, repetitions = (3,3))
        porose = porosity(matrix)
        i -= 0.5
    savetxt(f"{geometry_name}_{porose}.dat", matrix)        

%env geometry_name=$geometry_name
! mkdir -p "$HOME/GEOMETRIES/$geometry_name"
! mv $geometry_name*.dat "$HOME/GEOMETRIES/$geometry_name"


# Visualização
plt.imshow(matrix, cmap='gray')
plt.title(f"{geometry_name} {porose} 2d")
plt.axis('off')
plt.show()


#%%
nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)


concatenated_matrix = geometry(matrix, 'random', 10, (3,3))


savetxt(concatenated_matrix)


porose = porosity(concatenated_matrix)

# Visualização
plt.imshow(concatenated_matrix, cmap='gray')
plt.title("Matriz Concatenada 2x2")
plt.axis('off')
plt.show()
