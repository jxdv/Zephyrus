import sys

from .log import ZephyrusLogger

logger = ZephyrusLogger(__name__)


def print_logo():
    print(r"""
        

 ______          _                          
|___  /         | |                         
   / / ___ _ __ | |__  _   _ _ __ _   _ ___ 
  / / / _ \ '_ \| '_ \| | | | '__| | | / __|
 / /_|  __/ |_) | | | | |_| | |  | |_| \__ \
/_____\___| .__/|_| |_|\__, |_|   \__,_|___/
          | |           __/ |               
          |_|          |___/                


    """)


def zephyrus_prompt(prompt_msg, choice_type=None, choices=None):
    if choice_type == "int":
        try:
            choice = int(input(f"{prompt_msg}\nzephyrus> "))
        except ValueError:
            logger.error("zephyrus_prompt: Wrong data type!")
            sys.exit(1)
    else:
        choice = input(f"{prompt_msg}\nzephyrus> ")

    if isinstance(choices, str):
        return choice == choices
    elif isinstance(choices, list):
        return choice in choices
    else:
        return choice
