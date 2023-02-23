
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""

# A dictionary that maps the number to Thai text.
map_thaitext = {"0":"ศูนย์","1":"หนึ่ง", "2":"สอง", "3":"สาม", "4":"สี่", "5":"ห้า","6":"หก","7":"เจ็ด","8":"แปด","9":"เก้า"}
# ตัวแปรนี้เป็นตัวแปรที่เก็บค่าหน่วยของตัวเลขเป็นภาษาไทย สิบ ร้อย พัน หมื่น แสน ล้าน
unit_text = ["","สิบ","ร้อย","พัน","หมื่น","แสน","ล้าน"]

def intiger_process(num,position,edtag):
    # หากหลักสิบเป็นเลข 2 ให้เป็นยี่สิบ
    if num == "2" and position == 1:
        return "ยี่สิบ"
    # หากหลักหลักสิบเปฌน 1 ให้เป็นสิบ (ไม่ใช่หนึ่งสอบ)
    if num == "1" and position == 1:
        return "สิบ"
    # หากหลักหน่วยเป็น 1
    if num == "1" and position == 0  :
        # ถ้า edtag เป็น True return "เอ็ด" ถ้าเป็น false return หนึ่ง 
        if edtag: return "เอ็ด"
        else : return "หนึ่ง"
    # หากเป็น 0 ไม่ต้องเติมอะไร
    if num == "0":
        return ""
    # นอกนั้นเป็นเลขต่อด้วยหลัก
    return map_thaitext[str(num)]+unit_text[int(position)]

def fract_to_text(fract):
    return map_thaitext[str(fract)]

def number_process(number):
    result = ''
    # แยกระกว่า จำนวนเต็มและเศษส่วน
    stedata_s = str(number).split(".")
    intiger = stedata_s[0]
    fract = stedata_s[1]

    # หากจำนวนเต็มเป็นเลข 2 หลังขึ้นไป
    if len(intiger) != 1:
        position = len(intiger)
        # เช็คว่าเลขหลักสิบเป็นเลข 0 หรือไม่
        edtag = False if intiger[1] == "0" else  True
        for i in intiger:
            # call function 
            result += intiger_process(i ,position-1,edtag)
            position-=1
    else :
        # หากเ็นเลขหลักเดียว
        result += map_thaitext[intiger]

    # เช็คว่ามีเศษส่วนมั้ย
    if fract != "0" :
        # เติมจุด
        result += "จุด"
        for i in fract:
            # call function 
            result += fract_to_text(i)
    return result

def number_to_thaitext(datainput):
    #  try to convert to float 
    try:
        data = float(datainput)
        if data >= 0.0 and data < 10000000.0 :
            # call the function to convert
            thaitext = number_process(data)
            return thaitext
        else:
            return "Input data must be between 0 and 9,999,999"
    except:
        return "Invalid input data format (int/float): " + str(datainput)


if __name__ == '__main__':
    while True:
        # Asking the user to input a number to convert to Thai Text.
        datainput = ''
        datainput = input("Enter number to convert to Thai Text (type 'end' to stop):")

        # Checking if the user input is 'end' or 'END' and if it is, it will break the loop.
        if datainput == 'end' or datainput == "END":
            break

        result =  number_to_thaitext(datainput)
        print("Result: ",result)
        