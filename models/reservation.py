from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo import http
from odoo.http import request
import requests
import datetime


class Reservation(models.Model):
    _name = 'workingspace.reservation'
    _rec_name = 'room_id'
    _description = 'New Description'

    room_id = fields.Many2one(comodel_name="workingspace.room", )
    time_from = fields.Datetime(string="", required=False, )
    time_to = fields.Datetime(string="", required=False, )
    total_hours = fields.Integer(compute="_total_hours")
    customer_id = fields.Many2one(comodel_name="regcustomer.customer",)
    total_fees = fields.Float(compute="_total_fees")
    state = fields.Selection(selection=[('running', 'Running'), ('closed', 'Closed')], default='closed',compute="change_state")

    @api.multi
    def change_state(self):
        for rec in self:
            if rec.time_from <= fields.Datetime.now():
                rec.state='running'
            if fields.Datetime.now() >= rec.time_to:
                rec.state = 'closed'

    @api.model
    def create(self, vals):
        res=self.env['workingspace.room'].search([('id', '=', vals['room_id'])])
        print(vals['room_id'])
        for room in res.reservations_ids:
            if vals['time_from'] >= room.time_from and vals['time_from'] <= room.time_to:
                raise ValidationError("sorry this room not available")
            elif vals['time_to'] >= room.time_from and vals['time_to'] <= room.time_to:
                raise ValidationError("sorry this room not available")
            elif vals['time_from'] <= room.time_from and vals['time_to'] >= room.time_to :
                raise ValidationError("sorry this room not available")
        rec = super(Reservation, self).create(vals)
        return rec

    # @api.one
    # def running(self):
    #     for rec in self:
    #         rec.state = "running"
    #
    # @api.one
    # def closed(self):
    #     for rec in self:
    #         rec.state = "closed"

    @api.one
    @api.depends('time_from', 'time_to')
    def _total_hours(self):
        if self.time_from and self.time_to:
            start_dt = fields.Datetime.from_string(self.time_from)
            finish_dt = fields.Datetime.from_string(self.time_to)
            differance = relativedelta(finish_dt, start_dt)
            self.total_hours = differance.hours

    @api.one
    @api.depends('total_hours')
    def _total_fees(self):
        price = 0
        for room in self.room_id:
            res = self.env["workingspace.room"]. \
                search([('name', 'ilike', room.name)])
            price += res.price

        self.total_fees = self.total_hours * price

    # @api.one
    # def creaturl(self):
    #     data=self.read()[0]
    #     r = requests.get('http://localhost:7777/workingspace/workingspace/',params=data,timeout=5)
    #     return r


