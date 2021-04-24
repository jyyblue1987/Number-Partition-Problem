#import uuid
import random

MAX_INT = pow(10, 12)

# Generate files
def fileMake(f_name):
    path = f_name
    file = open(path, 'w')
    for i in range(0, 100):
        if i > 0:
            file.write('\n')
            
        x = random.randint(0, MAX_INT)
        file.write(str(x))
    file.close()

for i in range(1, 10):
    name = 'test' + str(i) + '.txt'
    fileMake(name)