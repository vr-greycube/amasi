# -*- coding: utf-8 -*-
# Copyright (c) 2021, Greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext import get_company_currency, get_default_company


class ItemReplacementCT(Document):
    def on_submit(self):
        if self.item_returned:
            self.make_stock_entry_for_item_returned()

        if self.item_issued:
            self.make_stock_entry_for_item_issued()

    def make_stock_entry_for_item_returned(self):
        company = get_default_company()
        difference_account = frappe.db.get_value(
            "Company", company, "stock_adjustment_account"
        )

        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.company = company
        stock_entry.purpose = "Material Receipt"
        for d in self.item_returned:
            if d.qty > 0:
                stock_entry.append(
                    "items",
                    {
                        "item_code": d.item_code,
                        "t_warehouse": d.warehouse,
                        "qty": d.qty,
                        "expense_account": difference_account,
                        "allow_zero_valuation_rate": 1,
                    },
                )
        stock_entry.set_stock_entry_type()
        stock_entry.insert()
        stock_entry.submit()
        for d in self.item_returned:
            d.reference_ste = stock_entry.name


    def make_stock_entry_for_item_issued(self):
        company = get_default_company()
        difference_account = frappe.db.get_value(
            "Company", company, "stock_adjustment_account"
        )

        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.company = company
        stock_entry.purpose = "Material Issue"
        for d in self.item_issued:
            if d.qty > 0:
                stock_entry.append(
                    "items",
                    {
                        "item_code": d.item_code,
                        "s_warehouse": d.warehouse,
                        "qty": d.qty,
                        "expense_account": difference_account,
                        "allow_zero_valuation_rate": 1,
                    },
                )
        stock_entry.set_stock_entry_type()
        stock_entry.insert()
        stock_entry.submit()
        for d in self.item_issued:
            d.reference_ste = stock_entry.name



