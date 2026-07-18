import bcrypt


#hashing using bcrypt
def hash_generation(password):
    salt = bcrypt.gensalt()
    byte_psw = password.encode('utf-8')
    hashed_psw = bcrypt.hashpw(byte_psw, salt)

    return hashed_psw.decode('utf-8')

#Hash validation against the password
def is_hash_valid(password, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = password.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid