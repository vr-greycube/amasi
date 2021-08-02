// Copyright (c) 2021, Greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item Replacement CT", {
  setup: function (frm) {
    frm.set_query("item_code", "item_returned", function (doc, cdt, cdn) {
      let row = locals[cdt][cdn];
      return {
        filters: {
          is_stock_item: 1,
        },
      };
    });
  },
});

frappe.ui.form.on(
  "Item Returned",
  "item_returned_add",
  function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    row.warehouse = frm.doc.warehouse;
  }
);

frappe.ui.form.on(
    "Item Issued",
    "item_issued_add",
    function (frm, cdt, cdn) {
      let row = locals[cdt][cdn];
      row.warehouse = frm.doc.warehouse;
    }
  );
  