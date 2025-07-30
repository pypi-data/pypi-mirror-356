# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _message_auto_subscribe_notify(self, partner_ids, template):
        self = self.with_context(subscribe_notify=True)
        return super()._message_auto_subscribe_notify(partner_ids, template)

    def message_notify(
        self,
        *,
        partner_ids=False,
        parent_id=False,
        model=False,
        res_id=False,
        author_id=None,
        email_from=None,
        body="",
        subject=False,
        **kwargs,
    ):
        if self and self.env.context.get("subscribe_notify") and partner_ids:
            partner_ids = (
                self.env["res.partner"]
                .search(
                    [
                        ("id", "in", partner_ids),
                        "|",
                        ("block_assigned_message", "=", False),
                        (
                            "block_assigned_message_model_ids",
                            "not in",
                            self.env["ir.model"]._get(self._name).id,
                        ),
                    ]
                )
                .ids
            )
        return super().message_notify(
            partner_ids=partner_ids,
            parent_id=parent_id,
            model=model,
            res_id=res_id,
            author_id=author_id,
            email_from=email_from,
            body=body,
            subject=subject,
            **kwargs,
        )
