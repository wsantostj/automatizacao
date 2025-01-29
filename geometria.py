import numpy as np
import matplotlib.pyplot as plt


def add_circle(matrix, center, radius):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if (i - center[0]) ** 2 + (j - center[1]) ** 2 <= radius ** 2:
                matrix[i, j] = 1

# Function to concatenate matrix
def concatenate_matrix(matrix, repetitions=(2, 2)):

    return np.tile(matrix, repetitions)

def porosity(matrix):
    void = (matrix == 0).sum()
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


def savetxt(matrix):
    p = []
    for u in range(matrix.shape[0]):
        for v in range(matrix.shape[1]):
            if matrix[u, v] == 1:
                p.append([v, matrix.shape[0] - u])
    
    file = 'file.dat'
    np.savetxt(file, p, fmt='%i')

 
 
def geometry(matrix, topology, r, repetitions = (3,3), number = 15, repetitions_v = 3):

    # Adicionar o círculo central
    if topology == "random":
        concatenated_matrix = concatenate_matrix(matrix, repetitions)
        for cr in center_random:
            add_circle(concatenated_matrix, cr, r)
        


    # Adicionar o círculo central
    elif topology == "centered":
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
    return concatenated_matrix    

#%%

nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)


# Centro da matriz
middle = (0, matrix.shape[1] // 2)

center = (matrix.shape[0] // 2, matrix.shape[1] // 2)


n = 10
center_random = []
for n in range(n):
    center_random.append((np.random.randint(0, nx*3), np.random.randint(0, ny*3)))

    
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
#%%

nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)


order = 0.5
i = min(nx,ny) //2
porose = 0
while porose <= order:
    nx, ny = 200, 200
    matrix = np.zeros((ny, nx), dtype=np.uint8)
    matrix = geometry(matrix, topology = "oblique", r = i, repetitions = (3,3))
    porose = porosity(matrix)
    i -= 0.5
        

# Visualização
plt.imshow(matrix, cmap='gray')
plt.title("Matriz Concatenada 2x2")
plt.axis('off')
plt.show()

#%%
nx, ny = 200, 200
matrix = np.zeros((ny, nx), dtype=np.uint8)


concatenated_matrix = geometry(matrix, 'random', 50, (3,3))


savetxt(concatenated_matrix)


porose = porosity(concatenated_matrix)

# Visualização
plt.imshow(concatenated_matrix, cmap='gray')
plt.title("Matriz Concatenada 2x2")
plt.axis('off')
plt.show()
