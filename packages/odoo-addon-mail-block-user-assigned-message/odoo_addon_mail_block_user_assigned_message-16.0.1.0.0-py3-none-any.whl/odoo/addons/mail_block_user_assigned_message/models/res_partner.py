# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResParter(models.Model):
    _inherit = "res.partner"

    block_assigned_message = fields.Boolean()
    block_assigned_message_model_ids = fields.Many2many(
        comodel_name="ir.model", domain="[('is_mail_thread', '=', True)]"
    )
