from odoo import fields,models 

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description ="Estate Property Tag"
    _order = "name"

    name = fields.Char(string="name",required=True)
    color = fields.Integer()
    _sql_constraints =[
        ('check_tag_name','UNIQUE(name)','A property tag name must be unique')
    ]