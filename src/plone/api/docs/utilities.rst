Utilities
=========

Getting the plone site
----------------------

Getting the Plone site object goes like this:

.. code-block:: python

    from plone import api
    site = api.get_site()

.. invisible-code-block:: python

    self.assertEquals(site.getPortalTypeName(), 'Plone Site')
    self.assertEquals(site.getId(), 'plone')



Getting the current request
---------------------------

You can get the current request like that:

.. code-block:: python

   request = api.get_request()

.. invisible-code-block:: python

   import pdb; pdb.set_trace()
   #self.assertEquals()


Sending an E-Mail
-----------------

To send an e-mail just use send_email:

.. Todo: Add example for creating a mime-mail

.. code-block::

   api.send_email(
       subject="hello world",
       sender="admin@mysite.com",
       recipients=["arthur.dent@gmail.com"],
       body="hello, arthur",
   )

.. invisible-code-block::

   None

