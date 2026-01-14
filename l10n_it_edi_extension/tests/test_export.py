# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command

from .common import Common


class TestExport(Common):
    def test_narration(self):
        """The narration included in the invoice
        is exported to the XML in Causale nodes."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        invoice.narration = "first line\n\nsecond line"
        invoice.action_post()
        self._assert_export_invoice(invoice, "narration.xml")

    def test_invoice_causale_non_latin(self):
        narration = """
            <p> </p>
            <p>```</p>
            <p>L’impresa è un’attività economica organizzata ai fini della produzione
             o dello scambio di beni o servizi.</p>
            <p>Importo totale fattura è 976,49 €.</p>
            <p>```</p>
        """
        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": "2022-03-24",
                    "invoice_date_due": "2022-03-24",
                    "partner_id": self.italian_partner_a.id,
                    "narration": narration,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "line1",
                                "price_unit": 800.40,
                                "tax_ids": [Command.set(self.default_tax.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        invoice.action_post()
        self._assert_export_invoice(invoice, "test_invoice_causale_non_latin.xml")

    def test_partner_shipping(self):
        """The partner shipping included in the invoice
        is exported to the XML in IndirizzoResa node."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        invoice.partner_shipping_id = self.italian_shipping_partner_a
        invoice.action_post()
        self._assert_export_invoice(invoice, "partner_shipping.xml")
