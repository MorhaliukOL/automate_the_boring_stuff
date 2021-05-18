# mapit.py - Launches a map in the browser using an address from the
# command line or clipboard.


import sys
import webbrowser
import pyperclip

# Check if adress in command line arguments
if len(sys.argv) > 1:

    adress = ' '.join(sys.argv[1:])

# Check if adress in the clipboard
elif pyperclip.paste():
    adress = pyperclip.paste()

else:
    print('Please provide arguments, or copy location to search to the clipboard')
    sys.exit()

webbrowser.open(f'https://www.google.com/maps/place/{adress}')

