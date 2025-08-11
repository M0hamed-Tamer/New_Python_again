# def color_text(text, color_code):
#     return f"\033[{color_code}m{text}\033[0m"

# print(color_text("Mohamed Tamer", 31 ))
# print ("\033[4mMohamed Tamer\033[0m")
# ===================================================

# def colored(text, color=None, bg_color=None, bold=False, underline=False):
#     codes = []
    
#     if color:
#         colors = {
#             'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
#             'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37
#         }
#         codes.append(str(colors.get(color.lower(), 37)))
    
#     if bg_color:
#         bg_colors = {
#             'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
#             'blue': 44, 'magenta': 45, 'cyan': 46, 'white': 47
#         }
#         codes.append(str(bg_colors.get(bg_color.lower(), 40)))
    
#     if bold:
#         codes.append('1')
    
#     if underline:
#         codes.append('4')
    
#     if codes:
#         return f"\033[{';'.join(codes)}m{text}\033[0m"
#     return text


# print(colored("Name", color='red', bold=True))
# print(colored("grate", color='green', bg_color='black'))
# print(colored("link", color='blue', underline=True))
# ========================================================

from time import sleep

class TerminalColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def show_menu():
    print(f"{TerminalColors.HEADER}=== قائمة الاختيارات ===")
    print(f"{TerminalColors.GREEN}1. عرض الملفات")
    print(f"{TerminalColors.BLUE}2. إنشاء مجلد جديد")
    print(f"{TerminalColors.WARNING}3. حذف ملف")
    print(f"{TerminalColors.FAIL}4. خروج{TerminalColors.RESET}")

while True:
    show_menu()
    choice = input("اختر رقمًا من القائمة: ")
    
    if choice == "1":
        print(f"{TerminalColors.CYAN}عرض الملفات...{TerminalColors.RESET}")
    elif choice == "2":
        print(f"{TerminalColors.GREEN}جارٍ إنشاء المجلد...{TerminalColors.RESET}")
    elif choice == "3":
        print(f"{TerminalColors.FAIL}تحذير! هذا سيحذف الملف!{TerminalColors.RESET}")
    elif choice == "4":
        print(f"{TerminalColors.HEADER}مع السلامة!{TerminalColors.RESET}")
        break
    else:
        print(f"{TerminalColors.WARNING}اختيار غير صحيح!{TerminalColors.RESET}")
    
    sleep(1)

