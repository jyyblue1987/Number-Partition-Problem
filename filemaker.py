import random

MAX_INT = pow(10, 12)

# Generate files
def fileMake(f_name):
    path = f_name
    file = open(path, 'w')
    for j in range(50):
        if j > 0:
            file.write("\n")
        for i in range(0, 100):
            #x = uuid.uuid4().int & (1<<64)-1
            x = random.randint(0, MAX_INT)
            if i > 0:
                file.write(" ")

            file.write(str(x))
        
    file.close()

for i in range(1, 5):
    name = 'test' + str(i) + '.txt'
    fileMake(name)