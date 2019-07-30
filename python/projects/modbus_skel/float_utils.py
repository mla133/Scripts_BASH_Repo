# -*- coding: utf-8 -*-

# Python module: Some functions for modbus data mangling

import struct

#####################################
# long long format (64 bits) function
#####################################
def word_list_to_longlong(val_list, big_endian=True):
    """Word list (16 bits int) to longlong list (64 bits int)

        By default word_list_to_long() use big endian order. For use little endian, set
        big_endian param to False.

        :param val_list: list of 16 bits int value
        :type val_list: list
        :param big_endian: True for big endian/False for little (optional)
        :type big_endian: bool
        :returns: list of 64 bits int value
        :rtype: list
    """
    # allocate list for long int
    long_list = [None] * int(len(val_list) / 4)
    # fill registers list with register items
    for i, item in enumerate(long_list):
        if big_endian:
            long_list[i] = (val_list[i * 2] << 16) + val_list[(i * 2) + 1]
        else:
            long_list[i] = (val_list[(i * 2) + 1] << 16) + val_list[i * 2]
    # return long list
    return long_list

def longlong_list_to_word(val_list, big_endian=True):
    """Long list (32 bits int) to word list (16 bits int)

        By default long_list_to_word() use big endian order. For use little endian, set
        big_endian param to False.

        :param val_list: list of 32 bits int value
        :type val_list: list
        :param big_endian: True for big endian/False for little (optional)
        :type big_endian: bool
        :returns: list of 16 bits int value
        :rtype: list
    """
    # allocate list for long int
    word_list = list()
    # fill registers list with register items
    for i, item in enumerate(val_list):
        if big_endian:
            word_list.append(val_list[i] >> 16)
            word_list.append(val_list[i] & 0xffff)
        else:
            word_list.append(val_list[i] & 0xffff)
            word_list.append(val_list[i] >> 16)
    # return long list
    return word_list
