# -*- coding: utf-8 -*-
# Copyright (c) 2021, Greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from distutils.log import debug
import frappe
from frappe.model.document import Document
from erpnext import get_company_currency, get_default_company


class ItemReplacementCT(Document):
    def validate(self):
        msg = []
        for d in self.item_returned + self.item_issued:
            item = frappe.get_doc("Item", d.item_code)
            if item.has_serial_no and not d.serial_no:
                msg.append(
                    "Serial No missing for item %s" % (frappe.bold(item.item_name))
                )
            if item.has_batch_no and not d.batch_no:
                msg.append(
                    "Batch No missing for item %s" % (frappe.bold(item.item_name))
                )
            if d.serial_no:
                d.qty = d.serial_no and len(d.serial_no.split("\n")) or 0
                if d.doctype == "Item Issued":
                    self.validate_serial_numbers(d.serial_no, d.item_code)

        if msg:
            frappe.throw("\n".join(msg))

    def validate_serial_numbers(self, serial_no, item_code):
        serial_nos = serial_no.split("\n")
        valid_numbers = frappe.db.sql(
            """
            select name
            from `tabSerial No`
            where item_code = %s and status = 'Active' and name in (%s)
        """
            % ("%s", ", ".join(["%s"] * len(serial_nos))),
            tuple([item_code] + serial_nos),
            as_list=True,
        )
        valid_numbers = [d[0] for d in valid_numbers]
        for d in serial_nos:
            if not d in valid_numbers:
                frappe.throw(
                    "Invalid serial numbers %s for item %s"
                    % (frappe.bold(serial_no), frappe.bold(item_code))
                )

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
                        "serial_no": d.serial_no,
                        "batch_no": d.batch_no,
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
                        "serial_no": d.serial_no,
                        "batch_no": d.batch_no,
                    },
                )
        stock_entry.set_stock_entry_type()
        stock_entry.insert()
        stock_entry.submit()
        for d in self.item_issued:
            d.reference_ste = stock_entry.name
