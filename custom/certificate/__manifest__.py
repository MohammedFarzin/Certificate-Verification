{
    'name': "Certificate Verification App",
    'author': "Farzin",
    'summary': "This module is defined for certicate verification of students",
    'depends': ['sale', 'base'],
    'data': [
        # 'security/ir.model.access.csv',
    #     'data/sequence.xml',
    #     'views/menu.xml',
        'views/student.xml',
        'reports/report.xml',
        'reports/report_template.xml',
    #     # 'views/search.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}