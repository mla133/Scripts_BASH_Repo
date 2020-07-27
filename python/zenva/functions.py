# Python language basics 6
# functions
# implementing, calling, parameters, return values

x_pos = 0
e_x_pos = 4

# Function to increase x_pos by 1
def move():
    global x_pos  # must retrieve the global value
    x_pos += 1    # changes the value of the global x_pos variable


# Function to move x_pos by 'amount'
def move_by(amount):
    global x_pos
    x_pos += amount


# Function to check for collision, True if collide, False if not
def check_for_collision():
    global x_pos, e_x_pos
    if x_pos == e_x_pos:
        return True
    else:
        return False   

move_by(3)
print(check_for_collision())
move()
print(check_for_collision())
move()
print(check_for_collision())
