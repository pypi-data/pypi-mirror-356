from spyre.spire import Spire
from spyre.Models.sales_models import *
import json
from spyre.utils  import *
from spyre.customers import customer

"""
Tested
> Get Order
> Pydantic Model
> Creating Order
> Deleting Order
> Updating Order
> Processing a order
> Invoicing a order
> Reversing a invoice(Check with eric)
> Get Invoice
> Update Invoice
> Get Customer
> Create Customer
> Update Customer
> Delete Customer
> Querying
> Filtering
> Sorting


Todo


>Exceptions (Duplicate , Processing quotes, Invalid inPuts)
>Documentation
>Response handling/ object -> Replace Riase_for_status
>Invoice Items/ Sales Order Item
>Payments, Deposit on Sales Order
>get by orderNo/invoiceNo etc

# >Querying
# >filtering and sorting
# >Create returns the item created
# >Customer
# >Make Wrapper class and implemement Oob type classes & methods
# >Create a model for Orders
# >Test Create,Update,
# >Processing Orders
# >Cancel/Delete
# >Return
"""


spire = Spire('intertest' , 'david1' , 'david')




order = spire.orders.get_sales_order(51247)
order.model.location = "01"
print(order.update())

# order = spire.orders.get_sales_order(51245)
# print(order.invoice())

TAXES = {
    0.05 : 1,

    0.08 : 2,
    0.13 : 3,
    0.15 : 4,
    0.14 : 5,
    0.12 : 6,
    0.11 : 7 
}

order = {
    "amazon-order-id": "702-6212155-2707463",
    "merchant-order-id": "3045",
    "purchase-date": "5/31/2025 23:22",
    "last-updated-date": "6/2/2025 11:08",
    "order-status": "Shipped",
    "fulfillment-channel": "Merchant",
    "sales-channel": "Amazon.ca",
    "order-channel": "WebsiteOrderChannel",
    "url": "",
    "ship-service-level": "Standard",
    "product-name": "20V MAX 1/2IN Compact Impact WR- HR",
    "sku": "DEWDCF921B",
    "asin": "B09M3TL9BB",
    "number-of-items": 1,
    "item-status": "Shipped",
    "tax-collection-model": "",
    "tax-collection-responsible-party": "",
    "quantity": 1,
    "currency": "CAD",
    "item-price": 195,
    "item-tax": 21.45,
    "shipping-price": "",
    "shipping-tax": "",
    "gift-wrap-price": "",
    "gift-wrap-tax": "",
    "item-promotion-discount": "",
    "ship-promotion-discount": "",
    "address-type": "",
    "ship-city": "Maple Creek",
    "ship-state": "Saskatchewan",
    "ship-postal-code": "S0N 1N0",
    "ship-country": "CA",
    "promotion-ids": "",
    "is-business-order": False,
    "purchase-order-number": "",
    "price-designation": "",
    "fulfilled-by": "",
    "default-ship-from-address-name": "Interline Wholesale Hardware Distributors North",
    "default-ship-from-address-field-1": "399 Confederation Parkway",
    "default-ship-from-address-field-2": "",
    "default-ship-from-address-field-3": "",
    "default-ship-from-city": "Vaughan",
    "default-ship-from-state": "Ontario",
    "default-ship-from-country": "CA",
    "default-ship-from-postal-code": "L4K 4S1",
    "actual-ship-from-address-name": "Interline Wholesale Hardware Distributors North",
    "actual-ship-from-address-field-1": "399 Confederation Parkway",
    "actual-ship-from-address-field-2": "",
    "actual-ship-from-address-field-3": "",
    "actual-ship-from-city": "Vaughan",
    "actual-ship-from-state": "Ontario",
    "actual-ship-from-country": "CA",
    "actual-ship-from-postal-code": "L4K 4S1",
    "serial-numbers": ""
}

from datetime import datetime

def convert_order_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return ""
    

def get_tax_code(order: dict) -> int:
    try:
        item_price = float(order.get('item-price', 0))
        item_tax = float(order.get('item-tax', 0))

        if item_price == 0:
            raise ValueError("Item price cannot be zero.")

        tax_rate = item_tax / item_price
        print(tax_rate)
        # Find the closest tax rate key
        closest_rate = min(TAXES.keys(), key=lambda r: abs(r - tax_rate))
        print(closest_rate)
        return TAXES[closest_rate]

    except (TypeError, ValueError):
        return None  # or raise an error if preferred


def convert_order_to_sales_order(order: dict) -> SalesOrder:

    amazn_id = order.get('amazon-order-id')
    udf = {
        "shopid" : amazn_id,
        "shipped" : order.get('order-status') == 'shipped'
    }

    status = "O"
    # if order.get('order-status') == 'shipped':
    #     status = "H"
    
    tax_code = get_tax_code(order)

    shipping_address = Address(city=order.get('ship-city'), provState= order.get('ship-state'), postalCode = order.get('ship-postal-code'), country=order.get('ship-country'),
                               salesTaxes=[ { "code" : tax_code } ]
                               )

    items = []
    item = SalesOrderItem(
        inventory=Inventory(partNo=order.get("sku"), whse='00'),
        partNo=order.get("sku"),
        orderQty=str(order.get("quantity")),
        unitPrice=str( float(order.get("item-price")) /float(order.get("quantity"))   ),
        taxFlags= [True,True,True,True],
        committedQty=str(order.get("quantity")),

    )
    
    items.append(item)
    freight = str(
        float(order.get('shipping-tax', '0') or 0) - 
        float(order.get('ship-promotion-discount', '0') or 0)
    )

    customer = Customer(customerNo="AMAZON")

    return SalesOrder(
        orderNo= "AMZN3" + amazn_id[-5:]  ,
        orderDate=convert_order_date(order.get("purchase-date")),
        type = "O",
        referenceNo= amazn_id,
        status=status,
        currency=Currency(code=order.get("currency")) if order.get("currency") else None,
        shippingAddress=shipping_address,
        items=items,
        udf=udf,
        freight=freight,
        customer=customer,

    )

sales_order = convert_order_to_sales_order(order)
print(sales_order.model_dump_json(indent=2 , exclude_none= True))



# order.model.payments = [ {"method" : "06" , "amount" : "216.45" , "layawayFlag" : False}]
# order.update()
# print(order.invoice())



# uoms = spire.inventory.items.get_item_uoms(id = 811)
# test_uom = uoms[2]
# print(test_uom.description)


# inv = spire.invoices.get_invoice(206363)
# order_converted.
# order_converted = create_sales_order_from_invoice(inv.model)
# print(order_converted.model_dump_json(exclude_none=True, exclude_unset=True, indent=2))


# cust = spire.customers.get_customer(1)

# ord = spire.orders.get_sales_order(31319)
# ord.customer = cust.model

# print(ord.update())


# order_test = json.loads("""
                        
# {
#   "customer": {
#     "id" : 3143
#   },
#   "currency": {
#     "code": "CAD"
                        
#   },
#   "address": {
#     "country": "Can",
#     "defaultWarehouse": "00",
#     "line1": "629 Daintry Crescent",
#     "line2": "Cobourg ON K9A 4X9",
#     "email": "beatty731@yahoo.com",
#     "contacts": [
#       {
#         "phone": {
#           "number": "+1 905-207-1116"
#         }
#       }
#     ]
#   },
#   "contact": {
#     "phone": {
#       "number": "+1 905-207-1116"
#     },
#     "name": "safdasd"
#   },
#   "shippingCarrier": "1",
#   "referenceNo": "1",
#   "trackingNo": "1",
#   "shipDate": null,
#   "items": [
#     {
#       "inventory": {
#         "id": 12345,
#         "whse": "00"
#       }
#     }
#   ],
#   "freight": "1",
#   "discount": "1",
#   "surcharge": "1",
#   "status": "O",
#   "type": "Q",
#   "hold": false,
#   "customerPO": "1"
# }
                        
#                         """)



# order = SalesOrder(**order_test)
# print(order.model_dump(exclude_unset=True, ))



# spire.orders.get_sales_order
# invoice_test = spire.invoices.get_invoice(206362)
# response = invoice_test.reverse()
# print(response)

# order = spire.orders.get_sales_order(31312)
# response = order.invoice()

# response = order.update_sales_order

# order = spire.orders.get_sales_order(31307)
# response = order.delete()
# print(response)

# resp = spire.orders.delete_sales_order(31306)
# print(resp)



# response = spire.orders.create_sales_order(order_test)
# print(response)



# orders_client = OrdersClient(client)
# order = orders_client.get_order(12334)
# order.invoice()


# invoice_client = InvoiceClient(client)

# response = invoice_client.reverse_invoice(206354)
# print(response)

# invoice_em = invoice_client.get_invoice(206355)
# invoice_model = Invoice(**invoice_em)

# print(invoice_model.model_dump_json(indent=2))

# order_converted = create_sales_order_from_invoice(invoice_model)
# print(order_converted.model_dump_json(indent=2, exclude_unset=True, exclude_none=True))

# response = orders_client.create_order(order_converted.model_dump(exclude_unset=True, exclude_none=True))
# print(response)


# Get an order by ID
# order_1001 = orders_client.get_order(1001)
# try:
#     orderModel = SalesOrder(**order_1001)  
# except Exception as e:
#     print(e.errors())

# print(order)
# print(orderModel.model_dump_json(indent=2))

#Create an ORder



# response = orders_client.create_order(order_test)
# print(response)

# deleting An order
# response = orders_client.delete_order(31299)
# print(response)

# Updating an order
# orderModel.location = "01"
# print(orderModel.model_dump_json(indent=2))

# response = orders_client.update_order(1001, orderModel.model_dump_json())
# print(response)


# order_test_model = SalesOrder(**order_test)
# print(order_test_model.model_dump(exclude_none=True))


 