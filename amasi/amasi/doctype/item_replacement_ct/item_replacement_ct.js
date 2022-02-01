// Copyright (c) 2021, Greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item Replacement CT", {
  setup: function (frm) {
    // allow only stock items in item_returned child table
    frm.set_query("item_code", "item_returned", function (doc, cdt, cdn) {
      let row = locals[cdt][cdn];
      return {
        filters: {
          is_stock_item: 1,
        },
      };
    });

    frm.set_query("batch_no", "item_returned", function (doc, cdt, cdn) {
      let row = locals[cdt][cdn];
      return {
        filters: {
          item: row['item_code'],
        },
      };
    });

    frm.set_query("batch_no", "item_issued", function (doc, cdt, cdn) {
      let row = locals[cdt][cdn];
      return {
        filters: {
          item: row['item_code'],
        },
      };
    });

  },

  validate: function (frm) {
    // 
  },


});


frappe.ui.form.on(
  "Item Returned",
  "item_code",
  function (frm, cdt, cdn) {
    let row_item = locals[cdt][cdn];
    frappe.model.with_doc("Item", row_item.item_code, function () {
      let item = frappe.get_doc("Item", row_item.item_code);
      var grid_row = frm.open_grid_row() || frm.get_field('item_returned').grid.get_row(cdn);
      grid_row.toggle_reqd("serial_no", item.has_serial_no == 0 ? false : true);
      grid_row.toggle_reqd("batch_no", item.has_batch_no == 0 ? false : true);
    });
  }
);

frappe.ui.form.on(
  "Item Issued",
  "item_code",
  function (frm, cdt, cdn) {
    let row_item = locals[cdt][cdn];
    frappe.model.with_doc("Item", row_item.item_code, function () {
      let item = frappe.get_doc("Item", row_item.item_code);
      var grid_row = frm.open_grid_row() || frm.get_field('item_returned').grid.get_row(cdn);
      grid_row.toggle_reqd("serial_no", item.has_serial_no == 0 ? false : true);
      grid_row.toggle_reqd("batch_no", item.has_batch_no == 0 ? false : true);
    });
  }
);

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
