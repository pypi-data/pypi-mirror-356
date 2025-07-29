from PySide6.QtWidgets import QFrame, QWidget
from ..layout_managers import VBox
from ... import style

class Frame(QFrame):
    def __init__(self, children: list = None, props: dict = None, **kwargs):
        # Intercept and remove our custom 'id' property so it's not passed to Qt
        widget_id = kwargs.pop("id", None)
        
        super().__init__(**kwargs)
        self._layout = None
        
        if props:
            style.styler.apply_props(self, props)
        
        # Now that the widget exists, set its object name if an ID was provided
        if widget_id:
            self.setObjectName(widget_id)
        
        # If children are provided, we must set a layout for them.
        # We'll use a VBox by default.
        if children:
            self.set_layout(VBox())
            for child in children:
                self.add_child(child)

    def set_layout(self, layout):
        # Clear any existing layout and its widgets before setting a new one.
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        
        self.setLayout(layout)
        self._layout = layout

    def add_child(self, child: QWidget):
        if self.layout() is None:
            raise RuntimeError("Cannot add child to a Frame without a layout. Call set_layout() first.")
        
        if hasattr(self._layout, 'addWidget'):
            self._layout.addWidget(child)
        else:
            raise TypeError("The layout for this Frame does not support adding widgets.")