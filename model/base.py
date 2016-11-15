from __future__ import unicode_literals
from orm.base import Entity
from orm import types


class Customer(Entity):
    __table_name__ = 'Customer'
    __primary_key__ = 'CustomerId'
    __fields__ = {
        'CustomerId': int,
        'FirstName': unicode,
        'LastName': unicode,
        'Company': unicode,
        'Address': unicode,
        'City': unicode,
        'State': unicode,
        'Country': unicode,
        'PostalCode': unicode,
        'Phone': unicode,
        'Fax': unicode,
        'Email': unicode,
        'SupportRepId': types.nullable_int,
    }


class Invoice(Entity):
    __table_name__ = 'Invoice'
    __primary_key__ = 'InvoiceId'
    __fields__ = {
        'InvoiceId': int,
        'CustomerId': int,
        'InvoiceDate': types.date_time,
        'BillingAddress': unicode,
        'BillingCity': unicode,
        'BillingState': unicode,
        'BillingCountry': unicode,
        'BillingPostalCode': unicode,
        'Total': float,
    }
