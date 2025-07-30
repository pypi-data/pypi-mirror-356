.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl
    :alt: License: AGPL-3

==============================
Mail Hide Header Portal Button
==============================

This module allows to hide the button automatically attached to the email's header
which gives access to the documents in the portal.


Installation
============

To install this module, you need to:

* Only install


Configuration
=============

To configure this module, you need to:

#. Go to Settings > Technical > System Parameters
#. Add the comma separated list of models which have not to attach the portal button
   in the email header as the value for the parameter
   "mail_hide_header_portal_button.models". For example, if the button needs to be hidden
   in sale orders and purchase orders, the value for the parameter has to be as follows:
   sale.order,purchase.order


Usage
=====

To use this module, you need to:

* No usage instructions needed.


ROADMAP
=======

* ...


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
* Valentín Vinagre <valentin.vinagre@sygel.es>
* Harald Panten <harald.panten@sygel.es>
* Juan Alberto Raja<juan.raja@sygel.es>


Maintainer
~~~~~~~~~~

This module is maintained by Sygel.

.. image:: https://www.sygel.es/logo.png
   :alt: Sygel
   :target: https://www.sygel.es

This module is part of the `Sygel/sy-social <https://github.com/sygel-technology/sy-social>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
