# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_get_recipients_classify(
        self, recipient_data, model_name, msg_vals=None
    ):
        result = super()._notify_get_recipients_classify(
            recipient_data, model_name, msg_vals=msg_vals
        )

        technical_model_name = (
            msg_vals.get("model") if msg_vals and "model" in msg_vals else model_name
        )
        hidden_mail_models = self.env["ir.model"].get_hidden_mail_portal_access_models()

        for group in result:
            if technical_model_name in hidden_mail_models:
                group["has_button_access"] = False
            else:
                if group.get("notification_group_name") in [
                    "customer",
                    "portal",
                    "portal_customer",
                ]:
                    group["has_button_access"] = True
                else:
                    group["has_button_access"] = False

        return result
