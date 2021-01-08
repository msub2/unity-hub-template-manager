import uhtm
from sys import argv

if __name__ == "__main__":
    if len(argv) == 1:
        # Launch GUI
        print('The GUI for this program has not yet been implemented.')
    elif len(argv) == 2:
        # User intends to use program via CLI with default Editor path
        if uhtm.verify_paths(argv[1]):
            uhtm.create_template()
        else:
            print('Paths could not be verified.')
    elif len(argv) == 3:
        # User intends to use program via CLI with custom Editor path
        if uhtm.verify_paths(argv[1], argv[2]):
            uhtm.create_template()
        else:
            print('Paths could not be verified.')
    else:
        print('Too many arguments!')
