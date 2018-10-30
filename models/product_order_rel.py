from odoo import models,fields,api

class productorder(models.Model):
    _name = 'product.order.line'

    name = fields.Char()
    orderd_qty = fields.Integer()

    product_order_id = fields.Many2one(comodel_name="workingspace.regcustomer", )
    product_id = fields.Many2one(comodel_name="workingspace.product",)

    @api.model
    def create(self, vals):
        res = self.env['workingspace.product'].search([('id', '=', vals['product_id'])])
        res.qty -= vals['orderd_qty']
        rec = super(productorder, self).create(vals)
        return rec

