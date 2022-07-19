## Author Aurora Software

from odoo import api, fields, models, _
from datetime import timedelta,datetime, date



class SalesSummaryReport(models.TransientModel):
    _name = 'sales.summary.report'
    _description = 'Sales Summary Order Wise and Product Wise'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    product_id = fields.Many2one("product.product", "Product Name")
    product_category_id = fields.Many2one("product.category", "Product Category")
    customer_id = fields.Many2one("res.partner", "Customer Name")


    def print_sales_summary_report(self):
        search_list =[]


        query_param =[]

        st_date =str(self.date_start) + str(' 23:59:59')
        en_date =str(self.date_end) + str(' 00:00:00')

        query_param.append(st_date)
        query_param.append(en_date)
        q_string=""
        if self.product_id:
            query_param.append(self.product_id.id)
            q_string = q_string + " and product_product.id =%s"

        if self.product_category_id:
            query_param.append(self.product_category_id.id)
            q_string =q_string + " and product_template.categ_id =%s"

        if self.customer_id:
            query_param.append(self.customer_id.id)
            q_string = q_string + " and sale_order.partner_id =%s"

        q_string = q_string + " group by product_template.name,product_category.name"

        tmp_dict ={
            'st_date':self.date_start,
            'end_date':self.date_end,
            'p_name':self.product_id.name if self.product_id else '',
            'p_categ':self.product_category_id.name if self.product_category_id else '',
            'c_name':self.customer_id.name if self.customer_id else '',
        }

        search_list.append(tmp_dict)

        sales_query = """
        select sum(sale_order_line.price_subtotal) as total_b_tax,
        sum(sale_order_line.price_total) as total_with_tax,
        sum(sale_order_line.price_tax) as total_tax,
        sum(sale_order_line.product_uom_qty) as total_qty,
        product_template.name,product_category.name
        from sale_order_line,sale_order,product_product, product_template,product_category
        where sale_order_line.order_id= sale_order.id and 
        sale_order_line.product_id = product_product.id and 
        product_product.product_tmpl_id = product_template.id and product_template.categ_id=product_category.id
        and sale_order.state not in ('draft', 'cancel') and sale_order.confirmation_date >=%s and sale_order.confirmation_date <=%s 
        """

        sales_query = sales_query + q_string

        self.env.cr.execute(sales_query,query_param)
        sales_list = self.env.cr.fetchall()

        result_list = []


        for items in sales_list:
            result_list.append({
                'p_name':items[4],
                'p_categ':items[5],
                't_qty':items[3],
                't_sale_without_tax':items[0],
                't_tax':items[2],
                't_with_tax':items[1]
            })


        data = {
            'form_data': result_list,
            'search_data': search_list,
            'docs': result_list,

        }
        # return True
        return self.env.ref('sales_summary_report.action_report_sales_summary').report_action(self, data=data)

