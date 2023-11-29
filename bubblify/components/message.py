from bubblify import styles
from bubblify.state import State

import reflex as rx
import random


def message(msg) -> rx.Component:
    return rx.square(
        rx.text(msg[0]),
        rx.text(msg[1]),
        rx.text(msg[2]),
        rx.text(msg[3]),
        font_size=16,
    )
