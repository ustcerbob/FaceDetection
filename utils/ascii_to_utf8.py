import re


def unicodetostr(s):

    strTobytes = []
    for i in s.split('\\x'):
        if i != '':
            num = int(i, 16)
            strTobytes.append(num)
    a = bytes(strTobytes).decode()
    return a


def ti(m):
    s = str(m.group())
    a = unicodetostr(s)
    return a

def ascii_to_utf8(origin):
    pat = re.compile(r'(\\x[0-9a-fA-F][0-9a-fA-F])+')
    string = re.sub(pat, ti, origin)
    return string



if __name__ == '__main__':
    result = str(b'\xe6\x9d\x8e\xe5\xb8\x85\xe4\xbc\x9f')
    result = 'lishuaiwei'
    after = ascii_to_utf8(result)
    print(after[2:-1])
