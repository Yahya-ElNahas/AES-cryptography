import random as rand

key = []
round_keys = []
rcon = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']
s_box = {}

def initialize():
    initialize_key()
    initialize_s_box()
    initialize_round_keys()

def randByte():
    res = hex(rand.randint(0, 255))[2:]
    if len(res) == 1:
        res = '0' + res
    return res

def initialize_key():
    for i in range(0, 16):
        key.append(randByte())

def initialize_s_box():
    bytes = []
    for i in range(0, 256):
        h = hex(i)[2:]
        if len(h) == 1:
            h = '0' + h
        bytes.append(h)
    for i in range(0, 16):
        s_box[int_to_hex(i)[1]] = {}
        for j in range(0, 16):
            byte = bytes.pop(rand.randint(0, len(bytes)-1))
            s_box[int_to_hex(i)[1]][int_to_hex(j)[1]] = byte
    # print(s_box)

def initialize_round_keys():
    round_keys.append(key)
    for i in range(0, 10):
        round_keys.append([])
        lastCol = []
        for j in range(0, 4):
            col = []
            if j == 0:
                col = getLastCol()
            else:
                col = lastCol
            col = rotWord(col)
            col = xor(col, getCol(j, i))
            if j == 0:
                col = xor(col, [rcon[i], '00', '00', '00'])
            for c in col:
                round_keys[i+1].append(c)
            lastCol = col

def getCol(col_index, round):
    return round_keys[round][col_index*4:col_index*4+4]

def getLastCol():
    last = round_keys[len(round_keys)-2]
    return last[len(last)-4:len(last)]

def rotWord(word):
    t = word.pop(0)
    word.append(t)
    return word

def xor(col1, col2):
    res = []
    for i in range(0, len(col1)):
        res.append(xor_hex(col1[i], col2[i]))
    return res

def xor_hex(h1, h2):
    a = int(h1, 16)
    b = int(h2, 16)
    return int_to_hex(a^b)

def int_to_hex(num):
    num = hex(num)
    num = num[2:len(num)]
    if(len(num) == 1):
        num = '0' + num
    return num

def add_round_key(data, round):
    res = []
    return xor(data, round_keys[round])

def sub_bytes(data):
    res = []
    for i in data:
        res.append(s_box[i[0]][i[1]])
    return res

def shift_rows(data):
    d = [[],[],[],[]]
    for i in range(0, 4):
        d[i] = data[i::4]
    res = []
    for i in range(1, 4):
        d[i] = d[i][i:] + d[i][:i]
    for i in range(0, 4):
        for j in range(0, 4):
            res.append(d[j][i])
    return res

def mix_columns(data):
    matrix = [['02', '03', '01', '01'], 
              ['01', '02', '03', '01'],
              ['01', '01', '02', '03'],
              ['03', '01', '01', '02']]
    res = []
    for i in range(0, 4):
        r = []
        for j in range(0, 4):
            row = matrix[i]
            col = data[j*4:j*4+4]
            r.append(mult_mtrx(row, col))
        res.append(r)
    r = []
    for i in range(0, 4):
        for j in range(0, 4):
            r.append(res[j][i])
    return r

def mult_mtrx(row, col):
    res = '00'
    for i in range(0, 4):
        a = '00'
        if row[i] == '01':
            a = col[i]
        elif row[i] == '02': 
            a = xor_by_2(col[i])
        else:
            a = xor_hex(xor_by_2(col[i]), col[i])
        res = xor_hex(res, a)
    return res

def xor_by_2(h):
    n = int(h, 16)
    r = int(leftShift_1(n), 2)
    n = int_to_bin(n)
    if n[0] == '1':
        return int_to_hex(r^int('00011011', 2))
    return int_to_hex(r)

def int_to_bin(h):
    h = bin(h)[2:]
    while len(h) < 8:
        h = '0' + h
    return h

def leftShift_1(n):
    n = int_to_bin(n)
    res = ''
    for i in range(1, len(n)):
        res += n[i]
    res += '0'
    return res

def EncryptBlock(message):
    cypher = []
    i = 0
    while i < len(message):
        cypher.append(message[i:i+2])
        i += 2
    cypher = add_round_key(cypher, 0)
    for i in range(0, 9):
        cypher = sub_bytes(cypher)
        cypher = shift_rows(cypher)
        cypher = mix_columns(cypher)
        cypher = add_round_key(cypher, i+1)
    cypher = sub_bytes(cypher)
    cypher = shift_rows(cypher)
    cypher = add_round_key(cypher, 10)
    res = ''
    for i in cypher:
        res += i
    return res

def fix_block(txt):
    while len(txt) % 32 != 0:
        txt += '0'
    return txt

def text_to_hex(txt):
    res = ''
    for i in txt:
        res += int_to_hex(ord(i))
    return res

def Encrypt(message):
    initialize()
    msgs = []
    message = fix_block(text_to_hex(message))
    i = 0
    while i < len(message):
        msgs.append(message[i:i+32])
        i += 32
    res = ''
    for i in msgs:
        res += EncryptBlock(i)
    return res

def Decrypt(message, key, s_box):
    msg = []
    i = 0
    while i < len(message):
        cypher.append(message[i:i+2])
        i += 2
    pass

message = "Hello"
cypher = Encrypt(message)
print('Plain Text:', [message])
print('Cypher Text:', [cypher])