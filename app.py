import getopt
import sys

def main():
    artista = ''
    musica = ''
    quant = 15
    todas = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:n:m:l:tvh")
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-a", "--artista"):
            print(f' artista {arg}')
            artista = arg

        elif opt in ("-n", "--numero"):
            quant = int(arg)

        elif opt in ("-m", "--musica"):
            musica = arg.upper()

        elif opt in ("-t", "--todas"):
            todas = True

        elif opt in ("-h", "--help"):
            print("Help")
            sys.exit()

if __name__ == "__main__":
    main()
