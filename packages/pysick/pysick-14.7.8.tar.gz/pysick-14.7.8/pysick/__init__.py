"""
pysick: A beginner-friendly graphics module with future-ready video & canvas features.
"""

from .pysick_main import InGine, MessageBox
from . import image
from . import graphics  # if you have this module

__all__ = ["InGine", "MessageBox", "image", "graphics"]

