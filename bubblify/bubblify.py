"""Welcome to Reflex!."""

from bubblify import styles
from dotenv import load_dotenv

# Import all the pages.
from bubblify.pages import *
import dotenv 
dotenv.load_dotenv()
import reflex as rx

load_dotenv()

# Create the app and compile it.
app = rx.App(styles=styles.base_style)
app.compile()
