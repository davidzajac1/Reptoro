# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Toast(Component):
    """A Toast component.
Toasts can be used to push messages and notifactions to users. Control
visibility of the toast with the `is_open` prop, or use `duration` to set a
timer for auto-dismissal.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- bodyClassName (string; optional):
    Often used with CSS to style elements with common properties. The
    classes specified with this prop will be applied to the body of
    the toast.

- body_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the body of the toast.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- dismissable (boolean; optional):
    Set to True to add a dismiss button to the header which will close
    the toast on click.

- duration (number; optional):
    Duration in milliseconds after which the Alert dismisses itself.

- fade (boolean; optional):
    Set to False for a Toast that simply appears rather than fades
    into view.

- header (string; optional):
    Text to populate the header with.

- headerClassName (string; optional):
    Often used with CSS to style elements with common properties. The
    classes specified with this prop will be applied to the header of
    the toast.

- header_style (dict; optional):
    Defines CSS styles which will override styles previously set. The
    styles set here apply to the header of the toast.

- icon (string; optional):
    Add a contextually coloured icon to the header of the toast.
    Options are: \"primary\", \"secondary\", \"success\", \"warning\",
    \"danger\", \"info\", \"light\" or \"dark\".

- is_open (boolean; default True):
    Whether Toast is currently open.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- n_dismiss (number; default 0):
    An integer that represents the number of times that the dismiss
    button has been clicked on.

- n_dismiss_timestamp (number; default -1):
    Use of *_timestamp props has been deprecated in Dash in favour of
    dash.callback_context. See \"How do I determine which Input has
    changed?\" in the Dash FAQs https://dash.plot.ly/faqs.  An integer
    that represents the time (in ms since 1970) at which n_dismiss
    changed. This can be used to tell which button was changed most
    recently.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tag (string; optional):
    HTML tag to use for the Toast, default: div."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, header_style=Component.UNDEFINED, headerClassName=Component.UNDEFINED, body_style=Component.UNDEFINED, bodyClassName=Component.UNDEFINED, tag=Component.UNDEFINED, is_open=Component.UNDEFINED, key=Component.UNDEFINED, fade=Component.UNDEFINED, header=Component.UNDEFINED, dismissable=Component.UNDEFINED, duration=Component.UNDEFINED, n_dismiss=Component.UNDEFINED, n_dismiss_timestamp=Component.UNDEFINED, icon=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'bodyClassName', 'body_style', 'className', 'dismissable', 'duration', 'fade', 'header', 'headerClassName', 'header_style', 'icon', 'is_open', 'key', 'n_dismiss', 'n_dismiss_timestamp', 'style', 'tag']
        self._type = 'Toast'
        self._namespace = 'dash_bootstrap_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'bodyClassName', 'body_style', 'className', 'dismissable', 'duration', 'fade', 'header', 'headerClassName', 'header_style', 'icon', 'is_open', 'key', 'n_dismiss', 'n_dismiss_timestamp', 'style', 'tag']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Toast, self).__init__(children=children, **args)
