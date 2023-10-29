"""Bubble component for the app."""

from bubblify import styles
from bubblify.state import State

import reflex as rx
import random

def bubble(cluster) -> rx.Component:
    """The bubble.

    Returns:
        The bubble component.
    """
    colors = ["#D27CBF", "#D2BF7C", "#7cb3d2", "#7cd2be", "#d27c7c", "#7cd2b3", "#d27cbf", "#7cbfd2"]

    return rx.hstack(
            rx.circle(
                rx.text(cluster[State.size_index], 
                    font_size=40,
                    font_weight="bold"
                    ),
                rx.text(cluster[State.name_index],
                    text_transform="uppercase",
                    font_size=16,
                    font_weight=600),
                rx.cond(cluster[State.unread_count_index], rx.circle(
                    rx.text(cluster[State.unread_count_index], 
                            font_size=20,
                            font_weight="bold"
                            ),
                    width="40px",
                    height="40px",
                    background_color="#EE3B3B",
                    position="absolute",
                    top="10%",
                    right="10%",
                    border_radius="50%",
                    color="white",
                ), rx.text("", display="none")),
                display="flex",
                flex_direction="column",
                justify_content="center",
                padding="20px",
                align_items="center",
                width=cluster[State.diameter_index],
                height=cluster[State.diameter_index],
                position="absolute",
                top="calc(50% + " + cluster[State.positiony_index] + ")",
                left="calc(50% + " + cluster[State.positionx_index] + ")",
                background_color=cluster[State.color_index],
                transition="all 0.5s ease",
                on_mouse_enter=State.mouse_enter(cluster),
                on_mouse_leave=State.mouse_leave(cluster),
                on_click=State.bubble_click(cluster),
                z_index=cluster[State.z_index_index],
            ),
            width="100%",
            height="100%",
    )
