from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
    config = [
        {
            "label": _("Documents"),
            "items": [
                # {
                #     "type": "doctype",
                #     "name": "",
                #     "description": _(""),
                # },
            ],
        },
    ]
    return config
