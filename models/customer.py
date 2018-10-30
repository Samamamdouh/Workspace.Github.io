from odoo import models, fields, api

class customer(models.Model):
    _name = 'regcustomer.customer'
    _description = 'New Description'

    name = fields.Char(required=True)
    phone = fields.Char(required=True, )
