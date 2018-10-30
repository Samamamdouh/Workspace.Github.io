from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import requests



class RegCustomer(models.Model):
    _name = 'workingspace.regcustomer'
    _description = 'This model for regular customer'

    customer_name = fields.Many2one(comodel_name="regcustomer.customer" )
    arrive_time = fields.Datetime()
    leave_time = fields.Datetime()
    total_hours = fields.Integer(compute="_total_hours")
    product_orders_ids = fields.One2many(comodel_name="product.order.line",
                                         inverse_name="product_order_id", )

    # quantity = fields.Integer()
    total_fees = fields.Float(compute="_total_fees")
    state = fields.Selection(selection=[('running', 'Running'), ('closed', 'Closed')], default='running')


    @api.one
    def running(self):
        for rec in self:
            rec.state = "running"

    @api.one
    def closed(self):
        for rec in self:
            rec.state = "closed"

    @api.one
    @api.depends('arrive_time', 'leave_time')
    def _total_hours(self):
        if self.arrive_time and self.leave_time:
            start_dt = fields.Datetime.from_string(self.arrive_time)
            finish_dt = fields.Datetime.from_string(self.leave_time)
            differance = relativedelta(finish_dt, start_dt)
            self.total_hours = differance.hours

    @api.one
    @api.depends('product_orders_ids', 'total_hours')
    def _total_fees(self):
        total_price = 0
        for product in self.product_orders_ids:
            res = self.env["workingspace.product"].\
                search([('id', '=', product.product_id.id)])
            total_price += (res.product_price * product.orderd_qty)

        self.total_fees = (self.total_hours * 5) + total_price

    @api.one
    def creaturl(self):
        data = self.read()[0]
        r = requests.get('http://localhost:7777/workingspace/workingspace/', params=data, timeout=5)
        return r