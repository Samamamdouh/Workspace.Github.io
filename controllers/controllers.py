# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class Workingspace(http.Controller):
    @http.route('/workingspace/workingspace/', auth='public',website=True)
    def index(self, **kw):
        res = request.env['workingspace.regcustomer'].sudo()
        res.create({
            'customer_name': kw.get('customer_name'),
            'arrive_time': kw['arrive_time'],
            'leave_time': kw['leave_time'],
            'total_hours': kw['total_hours'],
            'product_orders_ids': kw['product_orders_ids'],
            'total_fees': kw['total_fees'],
        })
        # return json.dumps(res)

    # @http.route('/workingspace/workingspace/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('workingspace.listing', {
    #         'root': '/workingspace/workingspace',
    #         'objects': http.request.env['workingspace.workingspace'].search([]),
    #     })
    #
    # @http.route('/workingspace/workingspace/objects/<model("workingspace.workingspace"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('workingspace.object', {
    #         'object': obj
    #     })