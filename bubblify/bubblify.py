"""Welcome to Reflex!."""

from bubblify import styles
from dotenv import load_dotenv

# Import all the pages.
from bubblify.pages import *

import reflex as rx

load_dotenv()

# Create the app and compile it.
app = rx.App()
app.compile()
