# print ("Welcome to place the rabbit .")
# rabbit = "🐇"
# place = [
#     ["🍀","🍀","🍀"],
#     ["🍀","🍀","🍀"],
#     ["🍀","🍀","🍀"],
#     ]
# for i in place:
#     print(i)
# try:
#     user_input =input("""Where should the  rabbit go? 🐇
# Please choose a row and a column: """)
#     raw = int(user_input [0] )-1
#     col = int(user_input [1])-1
#     place [raw] [col] = rabbit
#     for i in place:
#         print(i)
# except IndexError:
#     print ("No, list assignment index out of range ")

# ============================================================
# نطبع رسالة ترحيب
print("Welcome to place the rabbit.")

# رمز الأرنب
rabbit = "🐇"

# المصفوفة الأساسية (3 صفوف × 3 أعمدة) كلها نبات 🍀
place = [
    ["🍀", "🍀", "🍀"],
    ["🍀", "🍀", "🍀"],
    ["🍀", "🍀", "🍀"],
]

# نعرض المصفوفة الحالية
for row in place:
    print(row)

try:
    # نطلب من المستخدم يدخل الصف والعمود
    # مثال: "1 2" → صف 1 وعمود 2
    user_input = input("""Where should the rabbit go? 🐇
Please choose a row and a column: """)

    # نحول أول رقم من النص إلى int
    # ونطرح 1 علشان نحوله من 1-based إلى 0-based
    raw = int(user_input[0]) - 1

    # نحول ثاني رقم من النص إلى int
    col = int(user_input[1]) - 1

    # نغير المكان المحدد ونضع الأرنب فيه
    place[raw][col] = rabbit

    # نعرض المصفوفة بعد التعديل
    for row in place:
        print(row)

# لو الصف أو العمود خارج النطاق (زي 4 أو 0)
# هيمسك الخطأ ويطبع رسالة مناسبة
except IndexError:
    print("❌ No, list assignment index out of range")

# لو المستخدم دخل حاجة مش رقم (زي 'a b')
# نطبع له رسالة خطأ
except ValueError:
    print("❌ Please enter valid numbers.")
