{
    'name': 'Gestion Locative',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Gestion complète de la location immobilière',
    'description': """
        Module de gestion locative permettant de :
        - Gérer les contrats de bail
        - Suivre les paiements et relances
        - Générer les documents légaux
        - Automatiser les factures et relances
    """,
    'author': 'KNSAI',
    'website': 'https://www.knsai.com',
    'depends': ['base', 'mail', 'knsai_logement', 'knsai_artisan'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/cron.xml',
        'data/mail_template.xml',
        'views/bail_views.xml',
        'views/paiement_views.xml',
        'views/relance_views.xml',
        'views/menu.xml',
        'report/quittance_report.xml',
        'report/relance_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 