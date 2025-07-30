# winup/router/router.py
from typing import Dict, Callable, Optional
import winup
from winup import ui
from winup.core.component import Component
from winup.ui import clear_layout
import re

class Router:
    """Manages navigation and application state for different UI views."""
    def __init__(self, routes: Dict[str, Callable[..., Component]]):
        if not routes:
            raise ValueError("Router must be initialized with at least one route.")
        
        self.routes = self._compile_routes(routes)
        initial_path = list(routes.keys())[0]
        
        # Use WinUp's state manager to make the current route reactive.
        self.state = winup.state.create("router_current_path", initial_path)

    def _compile_routes(self, routes: Dict[str, Callable[..., Component]]):
        """Compiles route strings into regex for path matching."""
        compiled_routes = []
        for path, component_factory in routes.items():
            param_keys = re.findall(r":(\w+)", path)
            # Replace /:param with a regex capture group
            regex_path = re.sub(r":\w+", r"([^/]+)", path) + "$"
            compiled_routes.append((re.compile(regex_path), param_keys, component_factory))
        return compiled_routes

    def navigate(self, path: str):
        """Navigates to the given path, matching against registered routes."""
        if self.get_component_for_path(path):
            self.state.set(path)
        else:
            print(f"Error: Route for '{path}' not found.")

    def get_component_for_path(self, path: str) -> Optional[tuple[Callable[..., Component], dict]]:
        """
        Finds the component factory for a given path and extracts route parameters.
        Returns a tuple of (component_factory, params) or None if no match is found.
        """
        for regex, param_keys, component_factory in self.routes:
            match = regex.match(path)
            if match:
                param_values = match.groups()
                params = dict(zip(param_keys, param_values))
                return component_factory, params
        return None

@winup.component
def RouterView(router: Router) -> Component:
    """
    A component that displays the view for the current route.
    It listens to route changes and updates its content automatically.
    """
    # Create a container that will hold the routed components.
    view_container = ui.Frame()
    view_container.set_layout("vertical")

    def _update_view(path: str):
        """Clears the container and renders the new component with route params."""
        result = router.get_component_for_path(path)
        if result:
            component_factory, params = result
            # Clear previous component from the container
            if view_container.layout() is not None:
                ui.clear_layout(view_container.layout())
            
            # Instantiate and add the new component, passing params to it
            new_component = component_factory(**params)
            view_container.add_child(new_component)

    # Subscribe to changes in the router's state.
    router.state.subscribe(_update_view)
    
    # Perform the initial render for the starting route.
    _update_view(router.state.get())

    return view_container

@winup.component
def RouterLink(router: Router, to: str, text: str, props: Dict = None) -> Component:
    """
    A navigational component that looks like a hyperlink and triggers a route change on click.
    """
    def handle_click():
        router.navigate(to)

    # Use a Button styled as a link for better control and consistency.
    link_props = {
        "font-family": "Segoe UI",
        "text-decoration": "none",
        "color": "#0078D4",
        "border": "none",
        "background-color": "transparent",
        "cursor": "PointingHandCursor",
        "text-align": "left",
        "padding": "0"
    }
    
    # Merge user-defined props
    if props:
        link_props.update(props)

    return ui.Button(text, on_click=handle_click, props=link_props) 