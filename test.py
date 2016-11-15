"""
This presupposes you have loaded up a test DB matching the models provided in the model_test dir.

Please see README for setup.
"""

from __future__ import unicode_literals
import os
from unittest import TestCase, main
from random import randint
from datetime import datetime

from orm.base import Session
from model.base import Customer, Invoice


class TestORMBasics(TestCase):
    def setUp(self):
        """
        Set up and connect a quick session
        """
        self.session = Session(db_address=os.path.join(os.path.dirname(__file__), 'test.db'))
        self.session.connect()

    def tearDown(self):
        """
        Tidy things up after tests
        """
        self.session.disconnect()

    def test_single_item_by_id(self):
        """
        Get some item from the database by the primary key
        """
        customer = self.session.get(Customer, 1)
        self.assertEquals(customer.CustomerId, 1)

    def test_get_single_item_with_fields(self):
        """
        Get some item from the database by the primary key returning only selected fields
        """
        customer_w_name = self.session.get(Customer, 2, fields=["FirstName", "LastName"])
        self.assertTrue(hasattr(customer_w_name, "FirstName"))
        self.assertTrue(hasattr(customer_w_name, "LastName"))
        self.assertFalse(hasattr(customer_w_name, "Email"))

    def test_get_multiple_items(self):
        """
        Get multiple items from the database
        """
        customers = self.session.get_all(Customer)
        self.assertTrue(isinstance(customers, list))
        for cust in customers:
            self.assertTrue(isinstance(cust, Customer))

    def test_get_multiple_items_with_filter(self):
        """
        Get multiple items from the database given a filter
        """
        us_customers = self.session.get_all(Customer, filters={'Country': "USA"})
        self.assertTrue(isinstance(us_customers, list))
        for cust in us_customers:
            self.assertTrue(cust.Country == 'USA')

    def test_insert_item(self):
        """
        Add a new customer
        """
        test_email = "rick{}@birdperson.com".format(randint(0, 100000))
        new_customer = Customer(FirstName="Rick", LastName="Sanchez", Email=test_email)
        self.session.add(new_customer)
        self.session.commit()
        self.session.execute("""
        SELECT * FROM Customer WHERE EMAIL="{}";
        """.format(test_email))
        self.assertTrue(self.session.cursor.fetchone())

    def test_datetime_type_conversion(self):
        """
        Get an invoice since that has a datetime representation on it
        """
        invoice = self.session.get(Invoice, 1)
        self.assertEquals(type(invoice.InvoiceDate), datetime)

    def test_nullable_type_conversion(self):
        """
        Get an unassigned customers since those have None for SupportRepId
        """
        unassigned_customers = self.session.get_all(Customer, filters={'SupportRepId': None})
        for cust in unassigned_customers:
            self.assertEquals(cust.SupportRepId, None)
