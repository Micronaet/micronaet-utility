===============
web_m2x_options
===============

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fweb-lightgray.png?logo=github
    :target: https://github.com/OCA/web/tree/11.0/web_m2x_options
    :alt: OCA/web
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/web-11-0/web-11-0-web_m2x_options
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/162/11.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This modules modifies "many2one" and "many2manytags" form widgets so as to add some new display
control options.

Options provided includes possibility to remove "Create..." and/or "Create and
Edit..." entries from many2one drop down. You can also change default number of
proposition appearing in the drop-down. Or prevent the dialog box poping in
case of validation error.

If not specified, the module will avoid proposing any of the create options
if the current user has no permission rights to create the related object.

**Table of contents**

.. contents::
   :local:

Usage
=====

in the field's options dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``create`` *boolean* (Default: depends if user have create rights)

  Whether to display the "Create..." entry in dropdown panel.

``create_edit`` *boolean* (Default: depends if user have create rights)

  Whether to display "Create and Edit..." entry in dropdown panel

``m2o_dialog`` *boolean* (Default: depends if user have create rights)

  Whether to display the many2one dialog in case of validation error.

``limit`` *int* (Default: openerp default value is ``7``)

  Number of displayed record in drop-down panel

``search_more`` *boolean*

  Used to force disable/enable search more button.

``field_color`` *string*

  A string to define the field used to define color.
  This option has to be used with colors.

``colors`` *dictionary*

  A dictionary to link field value with a HTML color.
  This option has to be used with field_color.

``no_open_edit`` *boolean* (Default: value of ``no_open`` which is ``False`` if not set)

  Causes a many2one not to offer to click through in edit mode, but well in read mode

``open`` *boolean* (Default: ``False``)

  Makes many2many_tags buttons that open the linked resource

``no_color_picker`` *boolean* (Default: ``False``)

  Deactivates the color picker on many2many_tags buttons to do nothing (ignored if open is set)

ir.config_parameter options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you can disable "Create..." and "Create and Edit..." entry for all widgets in the odoo instance.
If you disable one option, you can enable it for particular field by setting "create: True" option directly on the field definition.

``web_m2x_options.create`` *boolean* (Default: depends if user have create rights)

  Whether to display the "Create..." entry in dropdown panel for all fields in the odoo instance.

``web_m2x_options.create_edit`` *boolean* (Default: depends if user have create rights)

  Whether to display "Create and Edit..." entry in dropdown panel for all fields in the odoo instance.

``web_m2x_options.m2o_dialog`` *boolean* (Default: depends if user have create rights)

  Whether to display the many2one dialog in case of validation error for all fields in the odoo instance.

``web_m2x_options.limit`` *int* (Default: openerp default value is ``7``)

  Number of displayed record in drop-down panel for all fields in the odoo instance

``web_m2x_options.search_more`` *boolean* (Default: default value is ``False``)

  Whether the field should always show "Search more..." entry or not.

To add these parameters go to Configuration -> Technical -> Parameters -> System Parameters and add new parameters like:

- web_m2x_options.create: False
- web_m2x_options.create_edit: False
- web_m2x_options.m2o_dialog: False
- web_m2x_options.limit: 10
- web_m2x_options.search_more: True


Example
~~~~~~~

Your XML form view definition could contain::

    ...
    <field name="partner_id" options="{'limit': 10, 'create': false, 'create_edit': false, 'search_more':true 'field_color':'state', 'colors':{'active':'green'}}"/>
    ...

Known issues / Roadmap
======================

Double check that you have no inherited view that remove ``options`` you set on a field !
If nothing works, add a debugger in the first line of ``_search method`` and enable debug mode in Odoo. When you write something in a many2one field, javascript debugger should pause. If not verify your installation.

- Instead of making the tags rectangle clickable, I think it's better to put the text as a clickable link, so we will get a consistent behaviour/aspect with other clickable elements (many2one...).
- In edit mode, it would be great to add an icon like the one on many2one fields to allow to open the many2many in a popup window.
- Include this feature as a configurable option via parameter to have this behaviour by default in all many2many tags.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/web/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/web/issues/new?body=module:%20web_m2x_options%0Aversion:%2011.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* ACSONE SA/NV
* 0k.io
* Tecnativa

Contributors
~~~~~~~~~~~~

* David Coninckx <davconinckx@gmail.com>
* Emanuel Cino <ecino@compassion.ch>
* Holger Brunn <hbrunn@therp.nl>
* Nicolas JEUDY <nicolas@sudokeys.com>
* Yannick Vaucher <yannick.vaucher@camptocamp.com>
* Zakaria Makrelouf <z.makrelouf@gmail.com>
* `Tecnativa <https://www.tecnativa.com>`_:

  * Jairo Llopis <jairo.llopis@tecnativa.com>
  * David Vidal <david.vidal@tecnativa.com>
  * Ernesto Tejeda <ernesto.tejeda87@gmail.com>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/web <https://github.com/OCA/web/tree/11.0/web_m2x_options>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.