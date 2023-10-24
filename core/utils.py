import random

from .log import ZephyrusLogger

logger = ZephyrusLogger(__name__)


def print_logo():
    """Print ascii art logo"""

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
    """
    Display the `prompt_msg` as a user prompt, wait for input, and validate the input
    against provided `choices`.

    Args:
        prompt_msg (str): The message to be displayed as a user prompt.
        choices (str or list, optional): A single string or a list of strings representing valid choices. If provided,
            the user's input will be compared to these choices for validation. The input is case-insensitive.
            Defaults to None.

    Returns:
        str or None: If `choices` is a single string, the user's input is returned if it matches the choice, or None if
        it doesn't. If `choices` is a list, the user's input is returned if it matches one of the choices, or None if it
        doesn't.
    """

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


def get_random_interval():
    """Generate random monitoring interval."""

    lower_bound = 60
    upper_bound = 60 * 60 * 24

    return random.randint(lower_bound, upper_bound)
