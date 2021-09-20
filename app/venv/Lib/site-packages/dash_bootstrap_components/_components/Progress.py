# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Progress(Component):
    """A Progress component.
A component for creating progress bars just with CSS. Control the current
progress with a callback and the `value` prop.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- animated (boolean; optional):
    Animate the bar, must have striped set to True to work.

- bar (boolean; optional):
    Apply progress-bar class, for use inside a multi progress bar.

- barClassName (string; optional):
    CSS classes to apply to the bar.

- bar_style (dict; optional):
    Style arguments to pass to the bar.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- color (string; optional):
    Set color of the progress bar, options: primary, secondary,
    success, warning, danger, info or any valid CSS color of your
    choice (e.g. a hex code, a decimal code or a CSS color name).

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- max (string | number; optional):
    Upper limit for value, default: 100.

- multi (boolean; optional):
    Create container for multiple progress bars.

- striped (boolean; optional):
    Use striped progress bar.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tag (string; optional):
    HTML tag to use for the progress bar, default: div.

- value (string | number; optional):
    Specify progress, value from 0 to max inclusive."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, key=Component.UNDEFINED, tag=Component.UNDEFINED, bar=Component.UNDEFINED, multi=Component.UNDEFINED, max=Component.UNDEFINED, value=Component.UNDEFINED, animated=Component.UNDEFINED, striped=Component.UNDEFINED, color=Component.UNDEFINED, barClassName=Component.UNDEFINED, bar_style=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'animated', 'bar', 'barClassName', 'bar_style', 'className', 'color', 'key', 'loading_state', 'max', 'multi', 'striped', 'style', 'tag', 'value']
        self._type = 'Progress'
        self._namespace = 'dash_bootstrap_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'animated', 'bar', 'barClassName', 'bar_style', 'className', 'color', 'key', 'loading_state', 'max', 'multi', 'striped', 'style', 'tag', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Progress, self).__init__(children=children, **args)
