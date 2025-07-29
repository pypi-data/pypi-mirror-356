"""
The WinUp Trait System.

Traits are modular, reusable behaviors that can be dynamically attached to any
widget to give it new functionality without subclassing.
"""
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QMenu
from .style import styler as style_manager

# --- 1. Trait Base Class and Manager ---

class Trait:
    """Base class for all traits. Defines the interface."""
    def __init__(self, **kwargs):
        self.options = kwargs
        self.widget = None

    def apply(self, widget: QWidget):
        """Logic to apply the trait's behavior to a widget."""
        self.widget = widget

    def remove(self):
        """Logic to clean up and remove the trait's behavior."""
        self.widget = None

class _TraitManager:
    """Internal class to manage traits attached to widgets."""
    def __init__(self):
        self._widget_traits = {} # {widget_id: {trait_name: trait_instance}}

    def add(self, widget: QWidget, trait: Trait, trait_name: str):
        widget_id = id(widget)
        if widget_id not in self._widget_traits:
            self._widget_traits[widget_id] = {}
        
        # If a trait of the same type already exists, remove it first
        if trait_name in self._widget_traits[widget_id]:
            self._widget_traits[widget_id][trait_name].remove()

        self._widget_traits[widget_id][trait_name] = trait
        trait.apply(widget)

    def get(self, widget: QWidget, trait_name: str) -> Trait | None:
        return self._widget_traits.get(id(widget), {}).get(trait_name)

    def remove(self, widget: QWidget, trait_name: str):
        widget_id = id(widget)
        if widget_id in self._widget_traits and trait_name in self._widget_traits[widget_id]:
            self._widget_traits[widget_id][trait_name].remove()
            del self._widget_traits[widget_id][trait_name]

# --- 2. Public API Functions ---

_manager = _TraitManager()

_available_traits = {} # Registry for trait classes

def register_trait(name: str, trait_class: type[Trait]):
    """Registers a new trait class for use with add_trait."""
    _available_traits[name] = trait_class

def add_trait(widget: QWidget, trait_name: str, **kwargs):
    """Adds a trait to a widget by its registered name."""
    if trait_name not in _available_traits:
        raise ValueError(f"Trait '{trait_name}' is not registered.")
    trait_instance = _available_traits[trait_name](**kwargs)
    _manager.add(widget, trait_instance, trait_name)

def remove_trait(widget: QWidget, trait_name: str):
    _manager.remove(widget, trait_name)

def get_trait(widget: QWidget, trait_name: str) -> Trait | None:
    return _manager.get(widget, trait_name)

# --- 3. Built-in Trait Implementations ---

class TooltipTrait(Trait):
    """Adds a simple tooltip on hover."""
    def apply(self, widget: QWidget):
        super().apply(widget)
        text = self.options.get("text", "No tooltip text provided.")
        widget.setToolTip(text)
    
    def remove(self):
        self.widget.setToolTip("")
        super().remove()

class ContextMenuTrait(Trait):
    """Adds a right-click context menu."""
    def apply(self, widget: QWidget):
        super().apply(widget)
        menu_items = self.options.get("items", {})
        if not menu_items: return

        self.menu = QMenu(widget)
        for name, handler in menu_items.items():
            if name == "---":
                self.menu.addSeparator()
            else:
                action = QAction(name, widget)
                action.triggered.connect(handler)
                self.menu.addAction(action)

        widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        widget.customContextMenuRequested.connect(self._show_menu)

    def _show_menu(self, pos: QPoint):
        self.menu.exec(self.widget.mapToGlobal(pos))
    
    def remove(self):
        self.widget.customContextMenuRequested.disconnect(self._show_menu)
        super().remove()

class DraggableTrait(Trait):
    """Makes a widget draggable within its parent."""
    def apply(self, widget: QWidget):
        super().apply(widget)
        self._drag_start_position = None
        self._original_mousePressEvent = widget.mousePressEvent
        self._original_mouseMoveEvent = widget.mouseMoveEvent
        self._original_mouseReleaseEvent = widget.mouseReleaseEvent

        widget.mousePressEvent = self._mousePressEvent
        widget.mouseMoveEvent = self._mouseMoveEvent
        widget.mouseReleaseEvent = self._mouseReleaseEvent

    def _mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_position = event.pos()
        self._original_mousePressEvent(event)

    def _mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_start_position:
            self.widget.move(self.widget.mapToParent(event.pos() - self._drag_start_position))
        self._original_mouseMoveEvent(event)

    def _mouseReleaseEvent(self, event):
        self._drag_start_position = None
        self._original_mouseReleaseEvent(event)
    
    def remove(self):
        self.widget.mousePressEvent = self._original_mousePressEvent
        self.widget.mouseMoveEvent = self._original_mouseMoveEvent
        self.widget.mouseReleaseEvent = self._original_mouseReleaseEvent
        super().remove()

class HoverEffectTrait(Trait):
    """
    Applies a dynamic property on hover that can be targeted by the stylesheet.
    This provides a more robust way to handle hover effects than direct manipulation.
    """
    def apply(self, widget: QWidget):
        super().apply(widget)
        
        # Store the original event handlers
        self._original_enterEvent = widget.enterEvent
        self._original_leaveEvent = widget.leaveEvent

        # Monkey-patch the widget's event handlers
        widget.enterEvent = self._enterEvent
        widget.leaveEvent = self._leaveEvent

    def _enterEvent(self, event):
        # Set a dynamic property when the mouse enters
        self.widget.setProperty("hover", True)
        # Ask the style manager to re-evaluate the widget's style
        style_manager.repolish(self.widget)
        # Call the original handler, if it exists
        self._original_enterEvent(event)

    def _leaveEvent(self, event):
        # Unset the dynamic property when the mouse leaves
        self.widget.setProperty("hover", False)
        # Re-evaluate the style again
        style_manager.repolish(self.widget)
        self._original_leaveEvent(event)

    def remove(self):
        if self.widget:
            # Restore original event handlers
            self.widget.enterEvent = self._original_enterEvent
            self.widget.leaveEvent = self._original_leaveEvent
            # Ensure the property is removed
            self.widget.setProperty("hover", False)
            style_manager.repolish(self.widget)
        super().remove()

class HighlightableTrait(Trait):
    """
    Allows the text in a widget (like a Label) to be selected and copied.
    """
    def apply(self, widget: QWidget):
        super().apply(widget)
        # Check if the widget supports text interaction flags (like QLabel)
        if hasattr(widget, 'setTextInteractionFlags'):
            self._original_flags = widget.textInteractionFlags()
            widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)

    def remove(self):
        if self.widget and hasattr(self.widget, 'setTextInteractionFlags'):
            # Restore the original interaction flags
            self.widget.setTextInteractionFlags(self._original_flags)
        super().remove()

# Register the built-in traits for use
register_trait("tooltip", TooltipTrait)
register_trait("context_menu", ContextMenuTrait)
register_trait("draggable", DraggableTrait)
register_trait("hover_effect", HoverEffectTrait)
register_trait("highlightable", HighlightableTrait) 