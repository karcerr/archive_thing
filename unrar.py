from PIL import Image


saved_data = open('/home/class11a2/PycharmProjects/untitled/venv/saved_data.txt', 'r')
temp = saved_data.readline().split()
end_len = int(temp[0])
file_extension = temp[1]
codes = {}
for line in saved_data.readlines():
    temp = line.split()
    codes[temp[0]] = int(temp[1])
saved_data.close()
archived_file = open('/home/class11a2/PycharmProjects/untitled/venv/archived_file', 'rb')
encrypted_file = open('/home/class11a2/PycharmProjects/untitled/venv/encrypted_file.' + file_extension, 'wb')
temp_str = ''
num_sym = 0
for i in archived_file.readlines():
    for j in i:
        num_sym += 1

archived_file.seek(0)
for i in range(num_sym - (end_len != 0)):
    byte = int.from_bytes(archived_file.read(1), byteorder='big')
    clear_byte = '0' * (10 - len(bin(byte))) + bin(byte)[2:]
    for sym in clear_byte:
        temp_str += sym
        if temp_str in codes:
            encrypted_file.write(codes[temp_str].to_bytes(1, byteorder='big'))
            temp_str = ''
for byte in archived_file.read(1):
    clear_byte = '0' * (10 - len(bin(byte))) + bin(byte)[2:]
    for sym in range(8 - end_len):
        temp_str += clear_byte[sym]
        if temp_str in codes:
            encrypted_file.write(codes[temp_str].to_bytes(1, byteorder='big'))
            temp_str = ''
archived_file.close()
encrypted_file.close()
print("Encryption completed")
