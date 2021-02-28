import sys
import numpy as np

args = sys.argv
bitmap_file = args[1]
ascii_file = args[2]
if len(args) == 4:
    encoding = args[3]
else:
    encoding = '.,-~:;=!*#$@'
    
# Get bit matrix
lines = open(bitmap_file).readlines()[3:]
A = np.array([[int(i) for i in line[:-3].split(' ')] for line in lines])

# Convert to ascii
image = ""
for i in range(len(A)):
    line = []
    for j in range(len(A[i])):
        line.append(encoding[A[i,j]])
    image += ''.join(line) + '\n'
    
# Create ascii image file
f = open(ascii_file, "w")
f.write(image)
f.close()
