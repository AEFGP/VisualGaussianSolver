import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy
from io import BytesIO
from PIL import Image
import random

# This algorithms is from Rosetta Code.
# I didn't had time to implement my own.
# It's trivial.

SNAP = []
def gauss(A):
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp
            SNAP.append(deepcopy(A))
            
        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]
            SNAP.append(deepcopy(A))

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
            SNAP.append(deepcopy(A))
    return x



if __name__ == "__main__":
    A = [[1.,-1.,1.,-1., 14],
         [1.,0.,0.,0., 4],
         [1.,1.,1.,1., 2],
         [1.,2.,4.,8., 2]]

    A = np.random.randint(-100,100, size=(30,31))
    A = A.tolist()
    print( gauss(A) )
    
    
    buffer = BytesIO()
    imgs  = []
    for i in range(len(SNAP)):
        plt.matshow(SNAP[i])
        plt.savefig(buffer)
        buffer.seek(0)
        imgs.append(deepcopy(buffer))
        plt.close()

    imgs = [Image.open(i) for i in imgs]
    imgs[0].save(str(random.randint(1,100000))+".gif", save_all=True, append_images=imgs, duration=100, loop=0)
        
        
