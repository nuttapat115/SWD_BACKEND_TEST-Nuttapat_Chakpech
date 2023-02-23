def index_of_most(arr):
    # เช่น [1,2,1,3,5,6,4] ลำดับที่มีค่ามากที่สุด คือ index = 5 
    # กำหนดค่าเริ่มต้น
    max_temp = arr[0]
    index_of_max = 0
    index_now = 0
    for i in arr:
        # ถ้า i มากกว่า max ปัจจุบัน
        if i > max_temp:
            # เปลี่ยน max
            max_temp = i
            # update index
            index_of_max = index_now
        index_now += 1
    
    return index_of_max

if __name__ == '__main__':
    data = [1,2,1,3,5,6,4]
    print(index_of_most(data))
    