import sys
def main(a):
    if a[1:][0]=='0':
        print("Skript tugadi")
        sys.exit()
    print("Skript boshlandi")
if __name__ == "__main__":
    main(sys.argv)
