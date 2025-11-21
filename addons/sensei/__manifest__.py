{
    'name': 'Gestion des Utilisateurs',
    'version': '1.0',
    'category': 'Human Resources',
    'depends': ['base','mail'],
    'data': [
        'views/session_views.xml',
        'views/utilisateur_views.xml',
        'views/factures_views.xml',
        'views/menus.xml',
        'views/wizard_vue.xml',
        'security/ir.model.access.csv',
        'data/data_cron.xml',
        'data/ir_sequence.xml',
        'data/email_template.xml'
    ],
    'installable': True,
    'application': True,
}
