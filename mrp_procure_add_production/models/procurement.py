# Copyright 2018 Comunitea Servicios Tecnológicos S.L.
#   (https://comunitea.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    @api.multi
    def _run_manufacture(self, product_id, product_qty, product_uom,
                         location_id, name, origin, values):
        active_prods = self.env['mrp.production'].search([
            ('product_id', '=', product_id.id),
            ('state', 'in', ['confirmed', 'planned'])
            ])
        if active_prods:
            prod = active_prods[0]
            prod.change_production_qty(product_qty)
            return True
        else:
            return super(ProcurementRule, self).\
                _run_manufacture(product_id, product_qty, product_uom,
                                 location_id, name, origin, values)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def change_production_qty(self, new_qty):
        change_qty = self.env['change.production.qty'].\
            create(
            {
                'mo_id':  self.id,
                'product_qty': self.product_qty + new_qty
            }
        )
        return change_qty.change_prod_qty()
