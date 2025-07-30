"""
The UI module for WinUp.

This package exposes all the available UI widgets, layouts, and dialogs
through a factory system to allow for custom widget implementations.
"""
from .widget_factory import register_widget, create_widget, create_component
from .layouts import Row, Column, Stack, Grid
from .utils import clear_layout
from winup.style.styler import merge_props

# Low-level Layouts (usually not overridden)
from .layout_managers import VBox, HBox

# Dialogs
from . import dialogs

# Import widgets
from .widgets.button import Button
from .widgets.calendar import Calendar
from .widgets.checkbox import Checkbox
from .widgets.combobox import ComboBox
from .widgets.deck import Deck
from .widgets.frame import Frame
from .widgets.image import Image
from .widgets.input import Input
from .widgets.label import Label
from .widgets.link import Link
from .widgets.progress_bar import ProgressBar
from .widgets.radio_button import RadioButton
from .widgets.scroll_view import ScrollView
from .widgets.slider import Slider
from .widgets.switch import Switch
from .widgets.tabview import TabView
from .widgets.textarea import Textarea

# --- Public API ---
# These are factory functions, not classes. They create widgets from the registry.
# This makes the API user-friendly, e.g., ui.Button("Click me").

def Button(*args, **kwargs): return create_widget("Button", *args, **kwargs)
def Calendar(*args, **kwargs): return create_widget("Calendar", *args, **kwargs)
def Checkbox(*args, **kwargs): return create_widget("Checkbox", *args, **kwargs)
def ComboBox(*args, **kwargs): return create_widget("ComboBox", *args, **kwargs)
def Deck(*args, **kwargs): return create_widget("Deck", *args, **kwargs)
def Frame(*args, **kwargs): return create_widget("Frame", *args, **kwargs)
def Image(*args, **kwargs): return create_widget("Image", *args, **kwargs)
def Input(*args, **kwargs): return create_widget("Input", *args, **kwargs)
def Label(*args, **kwargs): return create_widget("Label", *args, **kwargs)
def Link(*args, **kwargs): return create_widget("Link", *args, **kwargs)
def ProgressBar(*args, **kwargs): return create_widget("ProgressBar", *args, **kwargs)
def RadioButton(*args, **kwargs): return create_widget("RadioButton", *args, **kwargs)
def ScrollView(*args, **kwargs): return create_widget("ScrollView", *args, **kwargs)
def Slider(*args, **kwargs): return create_widget("Slider", *args, **kwargs)
def Switch(*args, **kwargs): return create_widget("Switch", *args, **kwargs)
def TabView(*args, **kwargs): return create_widget("TabView", *args, **kwargs)
def Textarea(*args, **kwargs): return create_widget("Textarea", *args, **kwargs)

# Expose all factory functions and the registration function for discoverability.
__all__ = [
    "register_widget",
    "create_component",
    "Button",
    "Calendar",
    "Checkbox",
    "ComboBox",
    "Deck",
    "Frame",
    "Image",
    "Input",
    "Label",
    "Link",
    "ProgressBar",
    "RadioButton",
    "ScrollView",
    "Slider",
    "Switch",
    "TabView",
    "Textarea",
    "Row",
    "Column",
    "Stack",
    "Grid",
    "clear_layout",
    "dialogs",
    "VBox",
    "HBox",
] 