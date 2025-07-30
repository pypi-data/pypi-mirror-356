# Copyright 2025 Juan Alberto Raja<juan.raja@sygel.es>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest.mock import patch

from odoo.tests.common import TransactionCase


class TestMailThreadNotifyRecipients(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model = cls.env["mail.thread"]
        cls.ir_config = cls.env["ir.config_parameter"].sudo()
        cls.ir_config.set_param("mail_hide_header_portal_button.models", "")

    def test_has_button_access_only_customer_portal(self):
        """Only customer and portal have access to the button when model is not hidden."""
        result_super = [
            {"notification_group_name": "customer"},
            {"notification_group_name": "portal"},
            {"notification_group_name": "internal"},
            {"notification_group_name": "other"},
        ]
        with patch(
            "odoo.addons.mail.models.mail_thread.MailThread._notify_get_recipients_classify",
            return_value=result_super,
        ):
            result = self.model._notify_get_recipients_classify([], "res.partner", {})

        for group in result:
            if group["notification_group_name"] in ["customer", "portal"]:
                # Para customer y portal: has_button_access debe ser True
                self.assertTrue(group.get("has_button_access", False))
            else:
                # Para otros grupos: has_button_access debe ser False
                self.assertFalse(group.get("has_button_access", False))

    def test_no_should_hide_button_when_no_hidden_models(self):
        """If there are no hidden models, no group has should_hide_button."""
        self.ir_config.set_param("mail_hide_header_portal_button.models", "")

        result_super = [
            {"notification_group_name": "customer"},
            {"notification_group_name": "portal"},
            {"notification_group_name": "internal"},
        ]
        with patch(
            "odoo.addons.mail.models.mail_thread.MailThread._notify_get_recipients_classify",
            return_value=result_super,
        ):
            result = self.model._notify_get_recipients_classify([], "res.partner", {})

        for group in result:
            # Ningún grupo debe tener should_hide_button cuando no hay modelos ocultos
            self.assertNotIn("should_hide_button", group)

    def test_has_button_access_false_when_model_in_hidden_models(self):
        self.ir_config.set_param(
            "mail_hide_header_portal_button.models", "res.partner,sale.order"
        )

        result_super = [
            {"notification_group_name": "customer"},
            {"notification_group_name": "portal"},
            {"notification_group_name": "internal"},
            {"notification_group_name": "other"},
        ]

        with patch(
            "odoo.addons.mail.models.mail_thread.MailThread._notify_get_recipients_classify",
            return_value=result_super,
        ):
            result = self.model._notify_get_recipients_classify([], "res.partner", {})

        # Todos los grupos deben tener has_button_access=False cuando el modelo está oculto
        for group in result:
            self.assertFalse(group.get("has_button_access", False))
