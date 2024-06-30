from odoo import fields,models,api,exceptions
from datetime import timedelta


class EsatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status= fields.Selection(
        [
            ('accepted','Accepted'),
            ('refused','Refused')
        ],
        copy = False,
        string="Status"
    )
    
    partner_id = fields.Many2one("res.partner", required=True, string="Partner") #buyer
    property_id = fields.Many2one("estate.property")
    type_id = fields.Many2one(related="property_id.type_id")
    
    validity = fields.Integer(string="Validity",default = 7)
    date_deadline = fields.Date(compute="_compute_deadline",inverse = "_inverse_deadline",string = "Deadline")
    
    _sql_constraints =[
        ('check_offer_price','CHECK(price >= 0)','offer price must be positive')
    ]
    
    @api.depends("validity","create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days = record.validity)
   
    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date).days()

    def accept_action(self):
        for record in self:
            if record.property_id.state == "sold":
                raise exceptions.UserError("This property already Sold")
            elif record.status == "accepted" :
                raise exceptions.UserError("This offer already Accepted")
            else:
                record.status = "accepted"
                record.property_id.write({
                    'selling_price': record.price,
                    'buyer':record.partner_id
                })


    def refuse_action(self):
        for record in self:
            if record.status == "refused":
                raise exceptions.UserError("This offer already refused")
            elif record.status == "accepted":
                raise exceptions.UserError("This offer already Accepted")
            else:
                record.status = "refused"
 
    @api.model
    def create(self, vals):

        property_id = vals.get('property_id')
        property = self.env['estate.property'].browse(property_id)
        
        if property:
            property.state = 'offer_received'
        
        higher_price_offer = self.search([('property_id','=',property_id), ('price','>=',vals.get('price'))])
        if higher_price_offer:
            raise exceptions.ValidationError("The offer's price must be higher than the existing ones")
        return super().create(vals) # Then call super to execute the parent method