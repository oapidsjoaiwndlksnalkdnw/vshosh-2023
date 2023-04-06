import secrets, hmac, base64, struct, hashlib, time
from flask import Flask, redirect

api = Flask('api')


users = {1:'5WB73N5JLTA6QOY26NT7CPAPOZ66UGBJ'}     #secret storage db


def provisioning_uri(secret):
    return f"otpauth://totp/Demo:example%40hotmail.ru?secret={secret}&issuer=Demo"

def hotp(secret, intv):
    key = base64.b32decode(secret, True)
    message = struct.pack(">Q", intv)
    hash = hmac.new(key, message, hashlib.sha1).digest()
    tmp = tmp = hash[19] & 15
    hash = (struct.unpack(">I", hash[tmp:tmp+4])[0] & 2147483647) % 10**6
    return hash

def genprivkey(uid):
    return "".join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567') for _ in range(32))

@api.route('/totp/<secret>')
def totp(secret):
    time_ = int(time.time())//30
    x = str(hotp(secret,intv=time_))
    return {'code':x.zfill(6),'time':time_}

@api.route('/secret/<uid>')
def key(uid):
    if uid in users:
        return {'ic':users[uid], 'link':provisioning_uri(users[uid])}
    else:
        users[uid] = genprivkey(uid)
        return {'ic':users[uid], 'link':provisioning_uri(users[uid])}

@api.route('/users')
def users_():
    return {'users':list(users.keys())}
@api.route('/get/id/<int:id>')
def totp_id(id):
    k = key(id)['ic']
    lnk = key(id)['link']
    code = totp(k)['code']
    time_ = totp(k)['time']
    return {'code':code, 'link':lnk, 'time':time_}
api.run(port=5000)