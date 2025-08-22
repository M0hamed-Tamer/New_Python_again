#!/bin/bash

# لون أخضر للنجاح
green="\e[32m"
# لون أحمر للخطأ
red="\e[31m"
# لون أصفر للتنبيه
yellow="\e[33m"
# رجوع للون العادي
reset="\e[0m"

# دالة لطباعة عنوان واضح
print_title() {
  echo -e "${yellow}==============================="
  echo -e "🔧 أدوات Bash - Toolkit"
  echo -e "===============================${reset}"
}

# القائمة التفاعلية
show_menu() {
  echo
  echo -e "${green}اختر عملية:${reset}"
  echo "1. عرض الملفات في مجلد"
  echo "2. حذف ملف"
  echo "3. تغيير ملكية مجلد"
  echo "4. إنشاء مجلد جديد"
  echo "5. البحث عن ملف باسم أو امتداد"
  echo "6. التبديل إلى قسم (mount)"
  echo "0. خروج"
}

# العمليات

show_files() {
  read -p "اكتب مسار المجلد: " dir
  if [ -d "$dir" ]; then
    ls -lh "$dir"
  else
    echo -e "${red}❌ المجلد غير موجود${reset}"
  fi
}

delete_file() {
  read -p "اكتب اسم الملف أو المسار: " file
  if [ -f "$file" ]; then
    rm "$file"
    echo -e "${green}🗑️ تم حذف الملف${reset}"
  else
    echo -e "${red}❌ الملف غير موجود${reset}"
  fi
}

change_owner() {
  read -p "اكتب مسار المجلد: " dir
  if [ -d "$dir" ]; then
    sudo chown -R "$USER:$USER" "$dir"
    echo -e "${green}✅ تم تغيير الملكية${reset}"
  else
    echo -e "${red}❌ المجلد غير موجود${reset}"
  fi
}

make_directory() {
  read -p "اكتب اسم المجلد الجديد: " newdir
  mkdir -p "$newdir"
  echo -e "${green}📁 تم إنشاء المجلد: $newdir${reset}"
}

search_file() {
  read -p "🔍 اكتب الاسم أو الامتداد (مثلاً: *.mp4): " name
  read -p "من أي مجلد تبدأ البحث؟ (مثلاً /home أو .): " start
  find "$start" -name "$name" 2>/dev/null
}

mount_partition() {
  read -p "اكتب اسم القسم (مثلاً: /dev/sda5): " part
  read -p "اكتب المجلد اللي عايز توصله فيه (مثلاً: /mnt/mydisk): " mountpoint
  sudo mkdir -p "$mountpoint"
  sudo mount "$part" "$mountpoint" && echo -e "${green}✅ تم التوصيل بنجاح${reset}" || echo -e "${red}❌ فشل التوصيل${reset}"
}

# التشغيل الرئيسي

clear
print_title

while true; do
  show_menu
  echo
  read -p ">> " choice
  echo
  case $choice in
    1) show_files ;;
    2) delete_file ;;
    3) change_owner ;;
    4) make_directory ;;
    5) search_file ;;
    6) mount_partition ;;
    0) echo -e "${yellow}👋 خروج...${reset}"; break ;;
    *) echo -e "${red}⚠️ اختيار غير صحيح${reset}" ;;
  esac
done
