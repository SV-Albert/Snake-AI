import random

class Segment:

    def __init__ (self, X, Y):
        self.X = int(X)
        self.Y = int(Y)
    
    def setNext (self, next):
        self.next = next

class Snake:

    def __init__ (self, head, tail):
        self.head = head
        self.tail = tail
        self.length = 3
        self.direction = "down"
    
    def move(self):
        nextX = self.head.X
        nextY = self.head.Y
        nextSeg = self.head.next
        if self.direction == "up": 
            self.head.Y -= 1
        elif self.direction == "down":
            self.head.Y += 1
        elif self.direction == "right":
            self.head.X += 1
        elif self.direction == "left":
            self.head.X -= 1

        for i in range(self.length-1):
            xBuff = nextSeg.X
            yBuff = nextSeg.Y
            nextSeg.X = nextX
            nextSeg.Y = nextY
            if (i < self.length-2):
                nextSeg = nextSeg.next
            nextX = xBuff
            nextY = yBuff

    def isDead(self, height, width):
        if self.length > 4:
            currentSeg = self.head.next.next.next
            for i in range (self.length):
                if currentSeg.X == self.head.X and currentSeg.Y == self.head.Y:
                    return True
                if i < self.length-4:
                    currentSeg = currentSeg.next
        if self.head.Y < 0 or self.head.Y >= height or self.head.X >= width or self.head.X < 0:
            return True

    def grow(self):
        self.length += 1
        newSeg = Segment(self.head.X, self.head.Y)
        newSeg.next = self.head
        self.head = newSeg
        
class Apple: 

    def __init__ (self, width, height):
        self.xMax = width - 1
        self.yMax = height - 1
        self.generate()

    def generate(self):
        self.X = random.randint(0, self.xMax)
        self.Y = random.randint(0, self.yMax)   
    