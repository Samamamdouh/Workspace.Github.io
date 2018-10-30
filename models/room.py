from odoo import models, fields,api

class room(models.Model):
    _name = 'workingspace.room'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()
    price = fields.Integer()
    capacity = fields.Integer()
    responsible_id = fields.Many2one(comodel_name="res.users")
    reservations_ids = fields.One2many(comodel_name="workingspace.reservation", inverse_name="room_id")
    reservation_count = fields.Integer(compute='_get_reservation_count', store=True)

    @api.depends('reservations_ids')
    def _get_reservation_count(self):
        for r in self:
            r.reservation_count = len(r.reservations_ids)