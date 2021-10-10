import random
import string

def random_string(letter_count, digit_count):
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1) # it converts the string to list.
    random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.
    final_string = ''.join(sam_list)
    return final_string
