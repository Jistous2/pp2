x = 5
y = "John"
print(x)
print(y)



x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0



myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"


"""incorrect variable names
2myvar = "John"
my-var = "John"
my var = "John"
"""



x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)



fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)



x = "Python"
y = "is"
z = "awesome"
print(x, y, z)


x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()



def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)



x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)