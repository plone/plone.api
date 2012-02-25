Utilities
=========

Getting the plone site
----------------------

.. code-block:: python
   :linenos:

   from plone import api
   site = api.get_site(context=None)


Getting the current request
---------------------------

The request will be fetched from a thread local

.. testcode:: python
   api.get_request()

.. testoutput::
   None


Sending an E-Mail
-----------------

Todo: Add example for creating a mime-mail

.. testcode::
   api.send_email(
       subject="hello world",
       sender="admin@mysite.com",
       recipients=["arthur.dent@gmail.com"],
       body="hello, arthur",
   )

.. testoutput::
   None

