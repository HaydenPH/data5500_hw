class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    def calculate_area(self):
        return self.length * self.width


rectangle = Rectangle(length = 5, width = 3)

rectangle_area = rectangle.calculate_area()
rectangle_area

