# estate/__manifest__.py
{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Muhammad Wael",
    'category': 'Real State',
    'description': """
    Description text
    """,
    
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_sales_view.xml',
        'views/estate_property_menus.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
