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

        if opt in ("-a"):
            print(f' artista {arg}')
            artista = arg

        elif opt in ("-n"):
            print(f' quantidade {arg}')
            quant = int(arg)

        elif opt in ("-m"):
            print(f' musica {arg}')
            musica = arg.upper()

        elif opt in ("-t"):
            print(f' todas {arg}')
            todas = True

        elif opt in ("-h"):
            print("Help")
            sys.exit()

if __name__ == "__main__":
    main()
