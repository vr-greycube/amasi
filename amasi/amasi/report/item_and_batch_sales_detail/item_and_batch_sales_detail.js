// Copyright (c) 2016, Greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item and Batch Sales Detail"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "sales_partner",
			"label": __("Sales Partner"),
			"fieldtype": "Link",
			"options": "Sales Partner",
		},
		{
			"label": "Customer",
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"label": "Item Code",
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"label": "Batch No",
			"fieldname": "batch_no",
			"fieldtype": "Link",
			"options": "Batch"
		},
	]
};
