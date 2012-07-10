

def get(name=None, context=None, request=None, *args):
    """Get a BrowserView object.

    :param name: [required] Name of the view.
    :type name: string
    :param context: [required] Context on which to get view.
    :type context: TODO: hm?
    :param request: [required] Request on which to get view.
    :type request: TODO: hm?
    :Example: :ref:`view_get_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not name:
        raise ValueError

    if not context:
        raise ValueError

    if not request:
        raise ValueError

    raise NotImplementedError


def localized_time(datetime=None, request=None, *args):
    raise NotImplementedError


def show_message(message=None, type='info', *args):
    """Display a status message.

    :param message: [required] Message to show.
    :type message: string
    :param type: Message type. Possible values: 'info', 'warn', 'error'
    :type type: string
    :Example: :ref:`show_message_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not message:
        raise ValueError

    raise NotImplementedError
