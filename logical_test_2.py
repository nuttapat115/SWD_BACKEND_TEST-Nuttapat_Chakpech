
"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
def number_process(data):
    result = ''
    roman_map = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 'C': 100, 'XC': 90, 'L': 50, 'XL': 40, 'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1}
    # วนลูปดึงค่า key,value จาก roman_map
    for sym , value in roman_map.items():
        # หาก value มากกว่าหรือเท่ากับ data input ให้เพิ่ม key ลง result และลบ data ด้วย value วนจนกว่า data input เป็น 0
        while value <= data :
            result += sym
            data -= value
    return result
        

def arabic_to_roman(datainput):
    try:
        data = int(datainput)
        if data >= 0 and data <= 1000 :
            # call number_process function
            thaitext = number_process(data)
            return thaitext
        else:
            return "Input data must be between 0 and 1,000"
    except:
        return "Invalid input data format (int): " + str(datainput)

if __name__ == '__main__':
    while True:
        # Asking the user to input a number to convert to Thai Text.
        datainput = ''
        datainput = input("Enter number to convert to Thai Text (type 'end' to stop):")

        # Checking if the user input is 'end' or 'END' and if it is, it will break the loop.
        if datainput == 'end' or datainput == "END":
            break

        result =  arabic_to_roman(datainput)
        print("Result: ",result)