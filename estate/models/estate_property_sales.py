from odoo import models,fields

class SalesPerson(models.Model):
    _inherit = "res.users"

    property_id = fields.One2many("estate.property","sales_person",
                                  domain="[('state', 'in', ('offer_recived','offer_accepted','new'))]")