View
====


.. _view_show_message_example:

Show notification message
-------------------------

This is how to show a notification message to the user.

.. code-block:: python

    from plone import api
    api.view.show_message(message='Blueberries!')

.. invisible-code-block:: python

    from Products.statusmessages.interfaces import IStatusMessage
    messages = IStatusMessage(self.request)
    self.assertEquals(len(messages), 1)

    message = messages.show()[0].message
    self.assertIn('Blueberries!.', message)


