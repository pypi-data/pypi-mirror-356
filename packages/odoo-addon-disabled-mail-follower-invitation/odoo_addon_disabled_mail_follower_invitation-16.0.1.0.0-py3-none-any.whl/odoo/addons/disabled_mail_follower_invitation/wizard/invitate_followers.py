# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class InvitateFollowers(models.TransientModel):
    _inherit = "mail.wizard.invite"

    send_mail = fields.Boolean(default=False)
