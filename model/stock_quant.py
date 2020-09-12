from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class Quant(models.Model):
    _inherit = "stock.quant"

    cost = fields.Float(string="Total Cost") #, compute="count_cost"
    ship_cost = fields.Float(string="Shipping Cost", compute="count_cost") #
    total_cost = fields.Float(string="Cost per Product", compute="count_cost") #

    @api.one
    def count_cost(self):
        total_ship_cost = 0

        picking_name = self.history_ids.picking_id.name

        landed_cost = self.env['stock.landed.cost'].search([('picking_ids.name', '=', picking_name)])

        for line in landed_cost.valuation_adjustment_lines:
            if line.product_id.name == self.product_id.name:
                total_ship_cost = line.additional_landed_cost
        
        if total_ship_cost > 0:
            self.ship_cost = total_ship_cost/self.qty
        self.total_cost = (self.inventory_value-total_ship_cost)/self.qty