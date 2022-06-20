# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext import get_default_company


def csv_to_columns(csv_str):
    props = ["label", "fieldname", "fieldtype", "options", "width"]
    return [
        zip(props, [x.strip() for x in col.split(",")])
        for col in csv_str.split("\n")
        if col.strip()
    ]


def execute(filters=None):
    return get_columns(filters), get_data(filters)


def get_columns(filters):
    return csv_to_columns(
        """
Date,posting_date,Date,,130
Sales Invoice,name,Link,Sales Invoice,150
Delivery Note,delivery_note,Link,Delivery Note,150
Customer,customer,Link,Customer,175
Item Code,item_code,Link,Item,180
Item name,item_name,,,180
Brand,brand,Link,Brand,145
Qty,qty,Float,,120
Price,rate,Currency,,120
Total,total,Currency,,130
Batch No,batch_no,Link,Batch,130
Expiration Date,expiry_date,Date,,120
Sales Partner,sales_partner,Link,Sales Partner,130
        """
    )


def get_data(filters=None):
    data = []
    where_conditions = get_conditions(filters)
    data = frappe.db.sql(
        """
    select 
        tsi.name , tsi.posting_date , tsii.delivery_note ,
		tsi.customer , tsii.item_code , tsii.item_name , tsii.brand ,
		tsii.qty , tsii.rate , tsii.qty * tsii.rate total ,
		tsii.batch_no , tb.expiry_date , tsi.sales_partner
    from 
        `tabSales Invoice` tsi
        inner join `tabSales Invoice Item` tsii on tsii.parent = tsi.name
        inner join tabItem ti on ti.item_code = tsii.item_code
		left outer join tabBatch tb on tb.name = tsii.batch_no
        {where_conditions} 
	-- limit 10
    """.format(
            where_conditions=where_conditions
        ),
        filters,
        as_dict=True,
        debug=0,
    )

    return data


def get_conditions(filters):
    where_conditions = [
        "tsi.docstatus = 1 and tsi.company = '{}' ".format(get_default_company())
    ]

    if filters.get("from_date"):
        where_conditions += ["tsi.posting_date >= %(from_date)s"]
    if filters.get("to_date"):
        where_conditions += ["tsi.posting_date <= %(to_date)s"]
    if filters.get("sales_partner"):
        where_conditions += ["tsi.sales_partner = %(sales_partner)s"]
    if filters.get("customer"):
        where_conditions += ["tsi.customer = %(customer)s"]
    if filters.get("item_code"):
        where_conditions += ["tsii.item_code = %(item_code)s"]
    if filters.get("batch_no"):
        where_conditions += ["tsii.batch_no = %(batch_no)s"]

    return where_conditions and " where {}".format(" and ".join(where_conditions)) or ""
