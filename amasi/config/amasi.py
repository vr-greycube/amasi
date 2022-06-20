from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
    config = [
        {
            "label": _("Documents"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Item Replacement CT",
                    "description": _("Item Replacement CT"),
                },
            ],
        },
        {
            "label": _("Reports"),
            "items": [
                {
                    "type": "report",
                    "name": "Item and Batch Sales Detail",
                    "description": _("Item and Batch Sales Detail"),
                    "is_query_report": True,
                },
            ],
        },
    ]
    return config
