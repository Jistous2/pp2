import math

# 1. Convert degree to radian
degree = 15
radian = degree * (math.pi / 180)
print(f"Output radian: {radian:.6f}")

# 2. Area of a trapezoid
height = 5
base1 = 5
base2 = 6
trapezoid_area = ((base1 + base2) * height) / 2
print(f"Expected Output: {trapezoid_area}")

# 3. Area of regular polygon
n = 4
side = 25
polygon_area = (n * side ** 2) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {polygon_area:.0f}")

# 4. Area of a parallelogram
base = 5
height_parallelogram = 6
parallelogram_area = base * height_parallelogram
print(f"Expected Output: {float(parallelogram_area)}")