from odoo import models, fields, api
from odoo.exceptions import ValidationError



class Wizard(models.TransientModel):
    _name = 'workingspace.wizard'

    choose = fields.Selection(string="", selection=[('room', 'Room'), ('regcustomer', 'Regular Customer'), ] )
    date_from = fields.Datetime(string="", required=False, )
    date_to = fields.Datetime(string="", required=False, )
    room_id = fields.Many2one(comodel_name="workingspace.room", )
    regcustomer_name = fields.Many2one(comodel_name="regcustomer.customer", )


    @api.multi
    def print_report(self, data):
        self.ensure_one()
        data['form'] = self.read()

        return self.env.ref('workingspace.workingspace_report').report_action(self, data=data)


class reservation_report(models.AbstractModel):
    _name = 'report.workingspace.workingspace_template'

    @api.model
    def get_report_values(self, docids, data=None):
        val=data['form'][0]['choose']
        if  data['form'][0]['choose'] == 'room':
            docs = self.env['workingspace.reservation'].browse(self.env.context.get('active_ids', []))
            data2 = {'form': self.env['workingspace.reservation'].search(
                [('time_from', '>=', data['form'][0]['date_from']),
                 ('time_to', '<=', data['form'][0]['date_to'])])}

            if not data2['form']:
                raise ValidationError("No Reservations in this duration")

            return {
                'doc_ids': docids,
                'doc_model': 'workingspace.reservation',
                'docs': docs,
                'data': data2,
                'val': val
            }
        elif data['form'][0]['choose'] == 'regcustomer':
            docs = self.env['workingspace.regcustomer'].browse(self.env.context.get('active_ids', []))
            data2 = {'form': self.env['workingspace.regcustomer'].search(
                [('customer_name', '=', data['form'][0]['regcustomer_name'][0])])}

            if not data2['form']:
                raise ValidationError("No Reservations in this duration")

            return {
                'doc_ids': docids,
                'doc_model': 'workingspace.regcustomer',
                'docs': docs,
                'data': data2,
                'val':val
            }