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


def zephyrus_prompt(prompt_msg, choices=None):
    choice = input(f"{prompt_msg}\nzephyrus> ").lower()

    if isinstance(choices, str):
        if choice != choices:
            logger.info(f"zephyrus_prompt: Expected {choices} got '{choice}'")
            return
        return choice
    elif isinstance(choices, list):
        if choice not in choices:
            logger.info(f"zephyrus_prompt: Expected one of these: {choices} got '{choice}'")
            return
        return choice
