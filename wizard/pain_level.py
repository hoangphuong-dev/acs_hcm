from odoo import models, api, fields

class MatePainLevel(models.TransientModel):
    _name = 'mate.pain.level'
    _description = "Pain Level Diagram"

    name = fields.Char()