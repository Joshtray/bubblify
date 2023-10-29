"""Welcome to Reflex!."""

from bubblify import styles

# Import all the pages.
from bubblify.pages import *
import dotenv 
dotenv.load_dotenv()
import reflex as rx

# Create the app and compile it.
app = rx.App()
app.compile()
