val_list = [16754, 27936, 12544,0,0,0,0,0,0,0,0,0,0,0,0,0]
word_list = list()

for i, item in enumerate(val_list):
    word_list.append(val_list[i] >> 8)
    word_list.append(val_list[i] & 0xff)

hex_list  = [hex(c)[2:] for c in word_list]
ascii_list = [chr(c) for c in word_list]

print(val_list)
print(hex_list)
print(ascii_list)
print(''.join(ascii_list))
s = ''.join(map(str,ascii_list))
print(s)


#
#
#def long_list_to_word(val_list, big_endian=True):
#
#   # allocate list for long int
#    word_list = list()
#    # fill registers list with register items
#    for i, item in enumerate(val_list):
#        if big_endian:
#            word_list.append(val_list[i] >> 16)
#            word_list.append(val_list[i] & 0xffff)
#        else:
#            word_list.append(val_list[i] & 0xffff)
#            word_list.append(val_list[i] >> 16)
#    # return long list
#    return word_list
#
#
