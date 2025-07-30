.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl
    :alt: License: AGPL-3

================================
Mail Block User Assigned Message
================================

This module allows to select multiple models in each user so they don't receive a notification from the documents related to those models when the users are assigned to them. This module works for both Odoo and email notifications.


Installation
============

To install this module, you need to:

* Only install


Configuration
=============

To configure this module, you need to:

#. Go to the "Preferences" tab in an internal user.
#. Activate the "Block Assigned Message" option.
#. Select the models for which assignation notifications don't have to be generated.

It is important to keep in mind that automatic assignment notifications are only created when a model meets the following requirements:

* The model is subclass of the abstract class mail.thread.
* The model has a user_id field.
* The tracking parameter of the user_id field is different to False.

This module will not work with models that do not meet all those three requirements. Also, notification methods can be overriden, so the module would not work in those cases either.

A particular example is project.task model. It doees not have a user_id field, but a Many2many user_ids field. Assignment notifications are created using a specific method for this model, so they cannot be blocked using this module.


Usage
=====

To use this module, you need to:

* No usage instructions needed.


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/sy-social/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/sy-social/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Sygel, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Manuel Regidor <manuel.regidor@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-social <https://github.com/sygel-technology/sy-social>`_.

To contribute to this module, please visit https://github.com/sygel.
