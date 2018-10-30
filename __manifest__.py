# -*- coding: utf-8 -*-
{
    'name': "workingspace",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/reservation_view.xml',
        'views/company_setting_view.xml',
        'views/wizard.xml',
        'views/report.xml',
        'views/reservation_report.xml',
        'views/regcustomer_report.xml',
         ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}