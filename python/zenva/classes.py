# Python language basics 7
# Classes and Objects 
# Class fields, methods, and constructors
# Object Instantiation

# A class is just a blueprint that defines an object's attributes and behaviours
class GameCharacter:

    # A field or global variable(assigned to this value when the class is instantiated
    speed = 5

    # Constructor creates a new class instance and sets up the defined fields    
    def __init__(self, name, width, height, x_pos, y_pos):
        self.name = name
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        
    # Method is just a function that typically modifies the class's fields
    def move(self, by_x_amt, by_y_amt):
        self.x_pos += by_x_amt        
        self.y_pos += by_y_amt        

# character_0 is a new instance of the GameCharacter class with defined attributes    
character_0 = GameCharacter('char_0', 50, 100, 100, 100)
print(character_0.name)
character_0.name = 'char_1'
print(character_0.name)

character_0.move(50, 100)
print(character_0.x_pos)
print(character_0.y_pos)



##############################################################################3
# Python language basics 8
# subclasses, superclasses, and inheritance


# PlayerCharacter is a subclass of GameCharacter
# PlayerCharacter has access to everything defined in GameCharacter
class PlayerCharacter(GameCharacter):

    speed = 10
    
    # Should still provide a constructor/initializer
    def __init__(self, name, x_pos, y_pos):
        super().__init__(name, 100, 100, x_pos, y_pos)

    # Method override, PlayerCharacter can only modify y_pos
    def move(self, by_y_amount):
        super().move(0, by_y_amount)

class NonPlayerCharacter(GameCharacter):
    
    speed = 20

    # Should still provide a constructor/initializer
    def __init__(self, name, x_pos, y_pos):
        super().__init__(name, 200, 200, x_pos, y_pos)
    
    # Method override, NonPlayerCharacter can only modify x_pos
    def move(self, by_x_amount):
        super().move(by_x_amount, 0)



player_character = PlayerCharacter('P_character', 500, 500)
print(player_character.name)        # 'P_character'

player_character.move(100)
print(player_character.x_pos)       # 500
print(player_character.y_pos)       # 600

non_player_character = NonPlayerCharacter('NPC', 600, 600)
print(non_player_character.name)    # 'NPC'

non_player_character.move(100)
print(non_player_character.x_pos)       # 700
print(non_player_character.y_pos)       # 600






