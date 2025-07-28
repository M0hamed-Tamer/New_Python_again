# map
def numbers(x):
    return x * 4
result = [1, 3, 5, 7, 9]
num = map(numbers, result)
print(list(num))
print('#'*30)
###############################
# filter
# للتحقق من الاعداد الموجبه
def is_even(x):
    return x % 2 == 0
num = [5 ,6 ,7 ,8]
result= filter(is_even , num )
print(list(result))
print('#'*30)
def remove_special_and_convert(s):
    return int(''.join(filter(str.isdigit, s)))
strings = ["abc123", "def456!", "ghi789@#"]
result = map(remove_special_and_convert, strings)
print(list(result))
print('#'*30)

####################################
# reduce
from functools import reduce
def add (x , y):
    return x + y
num = [1,2,3,4,5,6,7,8,9,10]
result = reduce(add ,num)
print(result)
print('#'*30)
# print(dir(map))


###########################################################
from functools import reduce

# قائمة المنتجات
products = [
    {"name": "Product 1", "price": 40},
    {"name": "Product 2", "price": 60},
    {"name": "Product 3", "price": 80},
]

# إضافة ضريبة 10%
add_tax = lambda product: {**product, "price_with_tax": product["price"] * 1.10}

# تصفية المنتجات التي يزيد سعرها عن 50
is_expensive = lambda product: product["price"] > 50

# حساب إجمالي التكلفة
sum_prices = lambda total, product: total + product["price_with_tax"]

# تطبيق الدوال الثلاث
products_with_tax = map(add_tax, products)
expensive_products = filter(is_expensive, products_with_tax)
total_cost = reduce(sum_prices, expensive_products, 0)

print(total_cost)  # Output: 154.0

###############################################
# شكل الدالة lambda
# lambda arguments: expression

numbers = [1, 2, 3, 4, 5]
# مضاعفة كل رقم في القائمة
result = map(lambda x: x * 2, numbers)
print(list(result))  # Output: [2, 4, 6, 8, 10]
