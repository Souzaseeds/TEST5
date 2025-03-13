{
    'name': 'Gestion des Artisans',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Gestion des artisans et leurs interventions',
    'description': """
        Module de gestion des artisans et leurs interventions.
        Fonctionnalités :
        - Gestion des artisans (plombiers, électriciens, etc.)
        - Gestion des compétences
        - Suivi des interventions
        - Gestion des documents
    """,
    'author': 'KNSAI',
    'website': 'https://www.knsai.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/artisan_views.xml',
        'views/menu.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 