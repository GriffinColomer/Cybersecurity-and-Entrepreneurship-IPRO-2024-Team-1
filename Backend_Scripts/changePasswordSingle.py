import sys

param1 = sys.argv[1]
param2 = sys.argv[2]

def main(me1, me2):
    print("-------------- changePasswordSingle has run --------------")
    print(f"Received parameters: {me1}, {me2}")

main(param1, param2)