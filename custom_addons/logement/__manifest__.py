{
    'name': 'Gestion des Logements',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Gestion des biens immobiliers avec leurs propriétaires, diagnostics, adresses, état du logement et photos',
    'description': """
        Module de gestion des logements permettant de :
        - Gérer les biens immobiliers
        - Suivre les diagnostics
        - Gérer les adresses
        - Suivre l'état du logement
        - Gérer les photos
    """,
    'author': 'KNSAI',
    'website': 'https://github.com/yourusername/KNSAI',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/logement_views.xml',
        'views/menu_views.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 