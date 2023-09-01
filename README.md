# blackjack-py
blackjack written on python

### Preparing

1. Install virtualenv

        pip install virtualenv

2. Create virtual environment

        virtualenv venv
    
3. Activate virtual environment

        source venv/bin/activate

### Run game:
    python main.py

### Run tests
    python -m unittest run_test.py 


```python
blackjack-py/
├── game                            # main folder with project
│   ├── constants.py                # contains constants which using in other modules
│   ├── game_class                  # package contains main logic
│   │   ├── cards.py                # contains Card class and function for this class
│   │   ├── common.py               # contains functions which using in other modules
│   │   ├── exceptions.py           # contains custom Exceptions
│   │   ├── game_class.py           # contains Game class
│   │   └── test_game_class.py      # contains test for Game class and class methods
│   ├── game_scene.py               # scene where user play in blackjack
│   ├── main_menu_scene.py          # scene with main menu
│   ├── sheet_scene.py              # scene with table of last ten results
│   └── surfaces.py                 # contains custom surfaces
├── img                             # contains images of cards and icon
│   └── ...
├── main.py                         # script for launching game
├── requirements.txt                # file contains the names of the required packages
├── run_test.py                     # script for launching tests
├── README.md
└── saves                           # folder contains save files
    └──...


```