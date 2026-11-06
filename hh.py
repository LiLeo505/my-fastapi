a = 1
print(id(a))
b = 1
print(id(b))
print(a is b)  # True, because small integers are cached in Python
print(a == b)  # True, because the values are equal
print(id(b))
print("这是新的变化吗?")
