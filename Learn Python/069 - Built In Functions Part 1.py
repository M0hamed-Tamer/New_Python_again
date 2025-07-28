# ------------------------
# -- Built In Functions --
# ------------------------
# all()
# any()
# bin()
# id()
# ------------------------

# x = [1, 2, 3, 4,"محمد تامر" ]

# if all(x):#كل العناصر متشابهه

#   print("All Elements Is True")

# else:#لا

#   print("Theres At Least One Element Is False")

x = [0, 0, []]

if any(x):

  print("There's At Least One Element is True")

else:

  print("Theres No Any True Elements")

print(bin(100))

a = 1 ; b = "mohamed tamer"
print(id(a))
print(id(b))