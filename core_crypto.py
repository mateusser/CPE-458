#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

from Crypto.Cipher import AES

def otp_encrypt(pt,key):
    ct = ""
    if(len(pt) > len(key)):
        raise Exception("KeyLengthError")
        return ct

    for i in range(len(pt)):
        ct += chr(ord(pt[i:i+1]) ^ ord(key[i:i+1]))
    return ct


def pkcs7_pad(plain,blocksize):
    padbyte = blocksize - len(plain)%blocksize
    for i in range(padbyte):
        plain += chr(padbyte)
    return plain


def pkcs7_strip(plain,blocksize):
    numblocks = len(plain)/(blocksize) + (1 if len(plain)%blocksize else 0)

    newplain = plain[0:(numblocks-1)*blocksize]
    padblock = plain[(numblocks-1)*blocksize:]
    padbytes = int(padblock[-1:].encode("hex"),16)
    #Validate padding - we should never see a pad end in zero
    if padbytes == 0:
        raise Exception("PaddingError")
    #make sure all the pad bytes make sense
    for i in range(padbytes-1):
        if padblock[-padbytes+i:-padbytes+i+1] != chr(padbytes):
            raise Exception("PaddingError")
    newplain += padblock[:-padbytes]

    return newplain


#C_i = E_k(M_i xor C_(i-1)), C_0 = IV
#plain, iv, and key all expected to be of size BLOCKSIZE
def cbc_encrypt(plain, iv, key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    plain = pkcs7_pad(plain,BLOCKSIZE)

    numcipherblocks = len(plain)/(BLOCKSIZE) + (1 if len(plain)%BLOCKSIZE else 0)

    cipher = ""
    c_imin1 = iv
    for i in range(numcipherblocks):
        m_xor_c = ""
        m_i = plain[i*BLOCKSIZE: i*BLOCKSIZE + BLOCKSIZE]
        #M_i xor C_(i-1))
        for j in range(BLOCKSIZE):
            m_xor_c += chr(ord(m_i[j:j+1]) ^ ord(c_imin1[j:j+1]))
        #E_k(M_i xor C_(i-1)),
        c_imin1 = aes_obj.encrypt(m_xor_c)
        cipher += c_imin1
    cipher = iv + cipher
    return cipher


#M_i = D_k(C_i) xor C_(i-1)
def cbc_decrypt(cipher, key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    iv = cipher[:BLOCKSIZE]

    cipher = cipher[BLOCKSIZE:]

    numplainblocks = len(cipher)/BLOCKSIZE

    plain = ""
    c_imin1 = iv #grab the IV
    for i in range(numplainblocks):
        c_i = cipher[i*BLOCKSIZE:i*BLOCKSIZE + BLOCKSIZE]
        #D_k(C_i)
        m_xor_c = aes_obj.decrypt(c_i)
        #D_k(C_i) xor C_(i-1)
        for j in range(BLOCKSIZE):
            plain += chr(ord(m_xor_c[j:j+1]) ^ ord(c_imin1[j:j+1]))
        c_imin1 = cipher[i*BLOCKSIZE:i*BLOCKSIZE + BLOCKSIZE]

    plain = pkcs7_strip(plain, BLOCKSIZE)

    return plain


def ecb_encrypt(plain,key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    plain = pkcs7_pad(plain,BLOCKSIZE)

    numcipherblocks = len(plain)/(BLOCKSIZE) + (1 if len(plain)%BLOCKSIZE else 0)

    cipher = ""
    for i in range(numcipherblocks):
        m_i = plain[i*BLOCKSIZE: i*BLOCKSIZE + BLOCKSIZE]
        #E_k(M_i),
        cipher += aes_obj.encrypt(m_i)
    return cipher


def ecb_decrypt(cipher,key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    numcipherblocks = len(cipher)/(BLOCKSIZE) + (1 if len(cipher)%BLOCKSIZE else 0)

    plain = ""
    for i in range(numcipherblocks):
        m_i = cipher[i*BLOCKSIZE: i*BLOCKSIZE + BLOCKSIZE]
        #E_k(M_i),
        plain += aes_obj.decrypt(m_i)

    plain = pkcs7_strip(plain,BLOCKSIZE)

    return plain


def print_message_in_blocks(message, block_size):
    blocks = get_message_in_blocks(message, block_size)
    for block in blocks:
        print '[{}]'.format(block)


def get_message_in_blocks(message, block_size):
    blocks = []
    n_blocks = len(message)/block_size
    if len(message) % block_size:
        n_blocks += 1
    for i in range(n_blocks):
        blocks.append(message[block_size*i : block_size*(i + 1)])
    return blocks

def xor_strings(plaintext, key):
    pt_len = len(plaintext)
    k_len = len(key)
    if k_len < pt_len:
        key = key*(pt_len / k_len) + key[:(pt_len % k_len)]
    elif k_len > pt_len:
        key = key[:pt_len]

    xor = ''
    for k, c in zip(key, plaintext):
        xor += '{}'.format(chr(ord(k) ^ ord(c)))

    return xor
