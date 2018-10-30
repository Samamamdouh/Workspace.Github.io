from odoo import models, fields, api


class product(models.Model):
    _name = 'workingspace.product'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()
    product_price = fields.Float(required = True)
    qty = fields.Integer()
