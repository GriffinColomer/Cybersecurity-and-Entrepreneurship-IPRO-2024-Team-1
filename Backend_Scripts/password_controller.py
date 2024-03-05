from sys import argv
from random import randrange

def pass_gen(length):
    password = ''
    for i in range(length):
        match randrange(1, 4):
            case 1:
                password += chr(randrange(48, 58))
            case 2:
                password += chr(randrange(63, 91))
            case 3:
                password += chr(randrange(94, 123))
    return password

def change_old_password(old_password, new_password):
    pass

def check_default_password(new_password):
    pass

def write_password(macaddress, password):
    with open("passwords", "a") as file:
        file.write(f"{macaddress}, {password}\n")

def main():
    macaddress = argv[1]
    password = pass_gen(16)

    try:
        if argv[2] != '':
            change_old_password(argv[2], password)
    except:
        check_default_password(password)
    write_password(macaddress, password)  # Write the password to the "Password Manager"


if __name__ == '__main__':
    main()