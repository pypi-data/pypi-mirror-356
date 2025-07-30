import re

common=['123456789','0123456789']
special=['@','#','$','%','&']


def mail_verif(mail):
    cond = re.compile('^[0-9a-zA-Z.]+@+[a-z]+.+[a-z]')
    return bool(cond.match(mail))

def passwd_verif(passwd):

    if len(passwd)<=8:
     return False
    elif passwd in common:
        return False
    elif (for i in special  if i in passwd):
        return False
    else:
        return True


def phone_verif(tel):
    tel=str(tel)
    cond =re.compile('^6+{2,5,7,8,9}+[0-9]{7}')
    return bool(cond.match(tel))




