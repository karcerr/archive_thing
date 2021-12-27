def double_min(fr):
    min1 = fr[0][0]
    p1 = 0
    min2 = fr[1][0]
    p2 = 1
    for j in range(2, size):
        if min1 < min2:
            min1, min2 = min2, min1
            p1, p2 = p2, p1
        if min1 > forest[j][0]:
            min1 = forest[j][0]
            p1 = j
        elif min2 > forest[j][0]:
            min2 = forest[j][0]
            p2 = j
    if min1 < min2:
        p1, p2 = p2, p1
    return p1, p2


optimised_bytes = {}


def create_new_bytes(line, branch, t):
    if branch[4] == '':
        create_new_bytes(line + '0', t[branch[1]], t)
        create_new_bytes(line + '1', t[branch[2]], t)
    else:
        optimised_bytes[branch[4]] = line
    return


file_path = input("File path:\n")
file_extension = file_path.split('.')[-1]
symbols = {}
file = open(file_path, 'rb')

file.seek(0)
print("(1/6) Creating symbols array started.")
for b in file:
    for a in b:
        if a in symbols:
            symbols[a] += 1
        else:
            symbols[a] = 1
print("(2/6) Creating symbols array finished.")

forest = []
tree = []

print("(3/6) Creating tree started.")
for i in symbols:
    forest.append([symbols[i], len(forest)])
    tree.append([len(tree), -1, -1, -1, i])
size = len(forest)
while size >= 2:
    pos1, pos2 = double_min(forest)
    tree.append([len(tree), forest[pos2][1], forest[pos1][1], -1, ''])
    tree[forest[pos2][1]][3] = len(tree) - 1
    tree[forest[pos1][1]][3] = len(tree) - 1
    if pos1 < pos2:
        forest[pos1] = [forest[pos1][0] + forest[pos2][0], len(tree) - 1]
        forest[size - 1], forest[pos2] = forest[pos2], forest[size - 1]
    else:
        forest[pos2] = [forest[pos1][0] + forest[pos2][0], len(tree) - 1]
        forest[size - 1], forest[pos1] = forest[pos1], forest[size - 1]
    size -= 1

create_new_bytes('', tree[-1], tree)
print("(4/6) Creating tree finished.")

archived_file = open('/home/class11a2/PycharmProjects/untitled/venv/archived_file', 'wb')

byte = ''
end_len = 0
file.seek(0)
print("(5/6) Creating compressed file started.")
for i in file:
    for sym in i:
        byte += optimised_bytes[sym]
        while len(byte) >= 8:
            archived_file.write(int(byte[:8], 2).to_bytes(1, byteorder='big'))
            byte = byte[8:]
file.close()
if len(byte) > 0:
    end_len = 8 - len(byte)
    archived_file.write(int(byte + '0' * end_len, 2).to_bytes(1, byteorder='big'))
print("(6/6) Creating compressed file finished.")

saved_data = open('/home/class11a2/PycharmProjects/untitled/venv/saved_data.txt', 'w')
saved_data.write("{} {}\n".format(end_len, file_extension))
for i in optimised_bytes:
    saved_data.write("{} {}\n".format(optimised_bytes[i], i))
saved_data.close()
print("File is compressed at {}".format("/home/class11a2/PycharmProjects/untitled/venv"))
archived_file.close()
