# // الرقم الصحيح للقسمه
# %  باقي القسمه
# print (10 / 3)
# print (10 // 3)
# print (10 % 3)
# ==========================================
second = int (input ("Please Type The Number Of Second :  "))
hours = second //3600
minutes = (second % 3600) // 60
remaining_second = second % 60 
print (f'The Duration Is " {hours} hours, {minutes} minutes,and {remaining_second}seconds.')