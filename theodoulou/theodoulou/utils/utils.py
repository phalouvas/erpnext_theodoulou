import frappe
from webshop.webshop.doctype.website_item.website_item import make_website_item

def publish_all_items():

    # Delete all website items
    #print('Deleting all website items')
    #frappe.db.sql('DELETE FROM `tabWebsite Item`')
    #frappe.db.commit()

    #items = frappe.get_all('Item', filters={'published_in_website': 1}, fields=['name'])
    #for i, item in enumerate(items):
    #    frappe.db.set_value('Item', item.name, 'published_in_website', 0)
        # every 100 items, commit the changes
    #    if i % 100 == 0:
    #        print(f'Unpublishing item {item.name} on row {i}')
    #        frappe.db.commit()
    #frappe.db.commit()
    #return;

    # Get the names of all items that are not published_in_website
    items = frappe.get_all('Item', filters={'published_in_website': 0}, fields=['name'])

    # print the total number of items
    print(f'There are {len(items)} items to publish')
    
    # publish each item and print the name of the item and the row number of the array
    for i, item in enumerate(items):
        make_website_item(frappe.get_doc('Item', item.name), save=True)
        # every 100 items, commit the changes
        if i % 100 == 0:
            print(f'Publishing item {item.name} at row {i}')
            frappe.db.commit()
        
    frappe.db.commit()
    