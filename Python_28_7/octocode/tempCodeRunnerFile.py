# Step 1: Initial basket
basket = [
    ['apple', 'bananas'],   # الفواكه
    ['milk', 'water']       # المشروبات
]

print("Original Basket:")
print(basket)

input("Press Enter to update the basket...")

# Step 2: تحديث الفواكه
fruits = basket[0]
fruits = ['Oranges'] + fruits[:-1] + ['Kiwis', fruits[-1]]  # تحديث دفعة واحدة
basket[0] = fruits

# Step 3: تحديث المشروبات
drinks = basket[1]
drinks = ['Coffee'] + [item for item in drinks if item != 'water'] + ['Tea']
basket[1] = drinks

# Step 4: إضافة عناصر جديدة
basket.append([1, 2, 3])

# Step 5: طباعة النتيجة النهائية
print("Updated Basket:")
for i, section in enumerate(basket, start=1):
    print(f"Section {i}: {section}")