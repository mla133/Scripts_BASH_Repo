with open('pi.mm', 'r') as reader:
    line = reader.readline()

    while line != '':
        print(line,end='')
        line = reader.readline()
