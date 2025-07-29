"""
The UI module for WinUp.

This package exposes all the available UI widgets, layouts, and dialogs
through a factory system to allow for custom widget implementations.
"""
from .widget_factory import create_widget, register_widget

# Low-level Layouts (usually not overridden)
from .layout_managers import VBox, HBox

# Dialogs
from . import dialogs

# --- Public API ---
# These are factory functions, not classes. They create widgets from the registry.

def Button(*args, **kwargs):
    return create_widget("Button", *args, **kwargs)

def Calendar(*args, **kwargs):
    return create_widget("Calendar", *args, **kwargs)

def Deck(*args, **kwargs):
    return create_widget("Deck", *args, **kwargs)

def Frame(*args, **kwargs):
    return create_widget("Frame", *args, **kwargs)

def Image(*args, **kwargs):
    return create_widget("Image", *args, **kwargs)

def Input(*args, **kwargs):
    return create_widget("Input", *args, **kwargs)

def Label(*args, **kwargs):
    return create_widget("Label", *args, **kwargs)

def Link(*args, **kwargs):
    return create_widget("Link", *args, **kwargs)

def ProgressBar(*args, **kwargs):
    return create_widget("ProgressBar", *args, **kwargs)

def ScrollView(*args, **kwargs):
    return create_widget("ScrollView", *args, **kwargs)

def Slider(*args, **kwargs):
    return create_widget("Slider", *args, **kwargs)

def Switch(*args, **kwargs):
    return create_widget("Switch", *args, **kwargs)

def TabView(*args, **kwargs):
    return create_widget("TabView", *args, **kwargs)

def Textarea(*args, **kwargs):
    return create_widget("Textarea", *args, **kwargs)

def Column(*args, **kwargs):
    return create_widget("Column", *args, **kwargs)

def Row(*args, **kwargs):
    return create_widget("Row", *args, **kwargs)

def ComboBox(*args, **kwargs):
    return create_widget("ComboBox", *args, **kwargs)

# Expose all factory functions and the registration function for discoverability.
__all__ = [
    "register_widget",
    "dialogs",
    "VBox", "HBox",
    "Button", "Calendar", "Deck", "Frame", "Image", "Input", "Label", "Link",
    "ProgressBar", "ScrollView", "Slider", "Switch", "TabView", "Textarea",
    "Column", "Row"
] 