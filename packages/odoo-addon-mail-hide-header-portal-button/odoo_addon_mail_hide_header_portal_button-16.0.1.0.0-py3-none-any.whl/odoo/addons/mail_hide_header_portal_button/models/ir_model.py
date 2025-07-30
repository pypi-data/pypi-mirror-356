# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo import api, models


class IrModel(models.Model):
    _inherit = "ir.model"

    @api.model
    def get_hidden_mail_portal_access_models(self):
        hidden_mail_models = []
        hidden_mail_models_param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("mail_hide_header_portal_button.models")
        )
        if hidden_mail_models_param:
            hidden_mail_models = hidden_mail_models_param.replace(" ", "").split(",")
        return hidden_mail_models
