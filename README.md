# sudoku-slayer
COMP.4200 Sudoku Slayer

## Prerequisites

Code examples are provided for Windows 10 only

Python 3.8 or higher is required to run and install Sudoku Slayer:

'''
py --version
Python 3.8.1
''''
### Installation

Download or clone the Sudoku Slayer github repository from https://github.com/Flannelz/sudoku-slayer

'''
git clone https://github.com/Flannelz/sudoku-slayer
'''

You can run the included batch file to install Sudoku Slayer automatically or install components manually:

#### Automatic Install

Move to the repository directory for the Sudoku Slayer.

Run install.bat

'''
install.bat
'''

Note: executing install.bat will automatically reinstall any existing Sudoku Slayer installation. This may be useful when making local changes to your Sudoku Slayer repository.

#### Manual Install

Move to the repository directory for the Sudoku Slayer.

Install requirements for Sudoku Slayer:

'''
py -m pip install requirements.txt
'''

Install Sudoku Slayer:
'''
py -m pip install .
'''

You are now ready to use Sudoku Slayer!