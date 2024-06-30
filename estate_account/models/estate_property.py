from odoo import fields,models,Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_action(self):

        self.env["account.move"].create(
        {
            "partner_id": self.buyer.id,
            "move_type" : "out_invoice",
            "invoice_line_ids": [
                Command.create({
                    "name": self.name,
                    "quantity": "1",
                    "price_unit": ((self.selling_price*0.06)+100)
                })
            ],
        }
        )
        print("it's working")   
        return super().sold_action()