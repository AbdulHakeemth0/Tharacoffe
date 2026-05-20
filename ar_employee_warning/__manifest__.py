{
    "name": "Employee Warning",
    "version": "17.0.0.1",
    "summary": """ Employee Warning """,
    "description": """ Employee Warning """,
    "author": "AR",
    "depends": ["hr"],
    "category": "HR",
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/employee_warning_views.xml",
        "views/employee_views.xml",
        "report/paperformat.xml",
        "report/report_employee_warning.xml",
        "report/employee_warning_report_template.xml",
    ],
}
