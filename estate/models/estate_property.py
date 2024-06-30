from odoo import api,fields, models
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_is_zero, float_compare
from datetime import timedelta, date
 
class TestModel(models.Model):
    _name = "estate.property"
    _description = "Test Model"
    _order = "id desc"

    name = fields.Char(string='title', required=True)
    postcode = fields.Text(string="PostCode")
    description = fields.Text(string="Description")
    date_availability = fields.Date(string="Avalibility", copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)) #add the default today+3month
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="NO. bedrooms", default=2)
    living_area = fields.Integer(string="living areas")
    facades = fields.Integer(string="facades")
    garage = fields.Boolean(string="garage")
    garden = fields.Boolean(string="garden")
    garden_area = fields.Integer(string="Garden Area")
    active_id = fields.Boolean(string='Active', default=True)
    _sql_constraints = [
        ('check_expected_price','CHECK(expected_price > 0)','A property expected price must be strictly positive'),
        ('check_selling_price','CHECK(selling_price >= 0)','A property expected selling must be strictly positive'),
    ]

    garden_orientation = fields.Selection(
        [
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West')
            ])
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    sales_person = fields.Many2one("res.users",string="Sales Person", default= lambda self: self.env.user)
    buyer = fields.Many2one("res.partner",string="Buyer",copy=False)
    type_id = fields.Many2one('estate.property.type', string="Property Type",options={'no_create_edit': True}) #This field will be a many-to-one relation to the estate.property.type model
    tag_id = fields.Many2many('estate.property.tag',string="Tags")
    offer_id = fields.One2many("estate.property.offer",'property_id',string="Offers")
    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_id.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_id:
                record.best_price = max(record.offer_id.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden_true(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold_action(self):
        for record in self:
            if record.state == "canceled":
                exceptions.UserError("This Property is already Canceled")
            else:
                record.state = "sold"            
            return True

    def cancel_action(self):
        for record in self:
            if record.state == "sold":
                exceptions.UserError("This Property is already Sold")
            else:
                record.state = "canceled"            
            return True
        
    @api.onchange('expected_price','selling_price')
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if (not float_is_zero(record.selling_price,precision_digits=2)) and (float_compare(record.selling_price , record.expected_price*0.9, precision_digits = 2) == -1):
                raise ValidationError("selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def on_delete_check_state(self):
        for record in self:
            if record.state in ['new','canceled']:
                raise UserError("you can't delete New or Canceld Property")
    
