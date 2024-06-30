from odoo import fields,models,api

class EstatePropertyType(models.Model):
    _name ="estate.property.type"
    _description = "estate property type"
    _order = "name"

    name = fields.Char(string="name", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many("estate.property","type_id", string="Partner")
    offer_ids = fields.One2many("estate.property.offer","type_id")
    _sql_constraints =[
        ('check_type','UNIQUE(type)','A property type name must be unique')
    ]
    offer_count = fields.Integer(compute="_calc_offer_count")

    @api.depends("offer_ids")
    def _calc_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
