import os
import sys
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

from main import main

if __name__ == '__main__':
    main.run_main()