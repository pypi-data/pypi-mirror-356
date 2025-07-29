from PySide6.QtWidgets import QTabWidget, QWidget
from ... import style
from typing import Dict

class TabView(QTabWidget):
    def __init__(self, tabs: Dict[str, QWidget], props: dict = None, **kwargs):
        super().__init__(**kwargs)
        for title, widget in tabs.items():
            self.addTab(widget, title)
        if props:
            style.styler.apply_props(self, props)
