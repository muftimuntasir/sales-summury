{
    "name": "Sales Summary Report",
    "version": "12.0.1.0",
    "author": "Mufti Muntasir Ahmed ",
    "category": "Sale",
    "license": "OPL-1",
    "depends": ['sale'],
    "price": 99.99,
    "currency": "USD",
    "data": [
        "security/ir.model.access.csv",
        "wizard/sales_summary_wizard.xml",
        'report/report_sales_summary_views.xml',
        'report/report_bind.xml',
        "views/menu.xml",

    ],
    "installable": True,
    'summary':"""
        Sales order summary
      This module is for sales summary for order date.
      It show the total sum of product quantity ,with tax data.
      Also can be filtered with product category , Product name and Customer Name with a date range.
       
    
    """


}
