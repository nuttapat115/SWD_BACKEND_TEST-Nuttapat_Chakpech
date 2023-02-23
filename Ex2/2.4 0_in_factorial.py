def factorial(num):
    if num == 1 : # base
        return 1
    else:
        return num*factorial(num-1)
    
def count_o_atBack(data):
    data = str(data)
    # invert data
    data = data[::-1]
    count = 0
    for i in data:
        if i == "0":
            count += 1
        else:
            break 
    return count

def fac_count0(num):
    fac = factorial(num)
    count = count_o_atBack(fac)
    return fac, count


if __name__ == '__main__':
    while True:
        num = ''
        num = input("enter number: ")
        if num == 'end':
            break
        try:
            num = int(num)
        except:
            print("Please enter a number")
        fac, count = fac_count0(num)
        print(f'{num}! = {fac} มีเลข 0 ต่อท้าย {count} ตัว')