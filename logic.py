class World:
    """Class for the whole scene"""

    def __init__(self, rows, columns):
        self.numRows = rows
        self.numColumns = columns
        self.matrix = [[Cell(-1) for x in range(self.numColumns)] for y in range(self.numRows)]
        self.change_list = []

    def print(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                print(self.matrix[i][j], end=' ')
            print()
        print()

    def next_cycle(self):
        self.change_list.clear()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if i > 0:
                    if self.matrix[i - 1][j].age > 0:
                        self.matrix[i][j].numNeighbour += 1
                    if j > 0:
                        if self.matrix[i - 1][j - 1].age > 0:
                            self.matrix[i][j].numNeighbour += 1
                    if j + 1 < self.numColumns:
                        if self.matrix[i - 1][j + 1].age > 0:
                            self.matrix[i][j].numNeighbour += 1
                if j > 0:
                    if self.matrix[i][j - 1].age > 0:
                        self.matrix[i][j].numNeighbour += 1
                if j + 1 < self.numColumns:
                    if self.matrix[i][j + 1].age > 0:
                        self.matrix[i][j].numNeighbour += 1
                if i + 1 < self.numRows:
                    if j > 0:
                        if self.matrix[i + 1][j - 1].age > 0:
                            self.matrix[i][j].numNeighbour += 1
                    if j + 1 < self.numColumns:
                        if self.matrix[i + 1][j + 1].age > 0:
                            self.matrix[i][j].numNeighbour += 1
                    if self.matrix[i + 1][j].age > 0:
                        self.matrix[i][j].numNeighbour += 1
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j].age < 0:
                    if self.matrix[i][j].numNeighbour == 3:
                        self.matrix[i][j].age = 1
                        self.change_list.append((i, j))
                else:
                    if self.matrix[i][j].numNeighbour == 2 or self.matrix[i][j].numNeighbour == 3:
                        self.matrix[i][j].age += 1
                        if self.matrix[i][j].age == Cell.maxAge:
                            self.matrix[i][j].age = -1
                        self.change_list.append((i, j))
                    else:
                        self.matrix[i][j].age = -1
                        self.change_list.append((i, j))
                self.matrix[i][j].numNeighbour = 0


class Cell:
    """Class for each cell of the whole scene"""
    maxAge = 10

    def __init__(self, x):
        self.numNeighbour = 0
        self.age = x

    def __str__(self):
        tmp = str(self.age) + ',' + str(self.numNeighbour)
        return tmp
