def remove_duplicates(input_string): 
    return ''.join(set(input_string)) 

def alter(text : str, s: int) -> str:
    result = ""
    if s < 0:
        text = remove_duplicates(text)
    for char in enumerate(text):
        if (char.isupper()) is False:
            base = 65
            result += chr((ord(char) + s - 65) % 26 + 65)
        else:
            base = 97
            result += chr((ord(char) + s - 97) % 26 + 97)
        result += chr((ord(char) + s - base)% 26 + base)
    return result

if __name__ == '__main__':
    # que = input('Do you whant to encrypt or decript: ')
    # text = input(f'enter a fraze you whant to {que}: ')
    que = 'encrypt'
    text = 'tva'
    if que == 'encrypt':
        s = 4
        print ("Text  : " + text)
        print ("Shift : " + str(s))
        print ("Cipher: " + alter(text,s))
    else:
        s = -4
        print ("Cipher  : " + text)
        print ("Shift : " + str(s))
        print ("Text : " + remove_duplicates(alter(text,s)))