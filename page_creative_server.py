import base64
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import subprocess


with open('pu_k.txt','rb') as a:
    public_key = a.read()


def rsa_encrypt(content):
     pubkey = RSA.importKey(public_key)
     cipher = PKCS1_v1_5.new(pubkey)
     # 加密明文
     return base64.b64encode(cipher.encrypt(content.encode('utf-8'))).decode('utf-8')


user_name = 'Because'
key = 'zsj8320491'
n = str(int(time.time()))

m_ = [user_name,key,n]
m1 = ','.join(m_)

encrypt_text = rsa_encrypt(m1)
