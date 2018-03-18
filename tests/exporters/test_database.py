import unittest
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, exc

from moneypy.exporters.models import Base, ExpenseDetails, ExpenseLabels
from moneypy.exporters.mixin import CRUDMixin

# This path creates the DB in memory. So no file is actually created
TEST_DB_PATH = "sqlite://"


class TestDatabase(unittest.TestCase, CRUDMixin):

    sample_records = [{
        'id': '23',
        'amount': 500,
        'date': date(2017, 10, 17),
        'recipient': 'Aircel',
        'description': 'Aircel Prepaid Bill',
        'labels': ['cellular', 'Entertainment']
    },
        {
            'id': '25',
            'amount': 1000,
            'date': date(2017, 4, 11),
            'recipient': 'Amazon',
            'description': 'Python Book',
            'labels': ['Education', 'Online shopping']
    },
        {
            'id': '27',
            'amount': 2000,
            'date': date(2017, 11, 12),
            'recipient': 'Netflix',
            'description': 'Account Subscription to watch movies',
            'labels': ['Entertainment']
    },
        {
            'id': '29',
            'amount': 2000,
            'date': date(2017, 12, 22),
            'recipient': 'Amazon',
            'description': 'Bought new dresses',
            'labels': ['Entertainment', 'Online shopping']
    }]

    def __create_test_data(self):
        for record in self.sample_records:
            self.insert(record=record)

    def setUp(self):
        self.engine = create_engine(TEST_DB_PATH, echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_record_insertion_in_expense_details_table(self):
        self.__create_test_data()
        count = self.get_rows_count()
        self.assertEqual(count, len(self.sample_records),
                         'Given records are not inserted properly in ExpenseDetails table')

    def test_back_population_in_expense_labels_table(self):
        self.__create_test_data()
        count = self.session.query(ExpenseLabels).count()
        self.assertEqual(count, 4,
                         'Labels are not back populated correctly in ExpenseLabels Table')

    def test_filter_labels_by_expense_id(self):
        self.__create_test_data()
        record = self.sample_records[3]
        actual_labels = []
        expected_instance = self.read_by_id(id=record['id'])
        for label_instance in expected_instance.labels:
            actual_labels.append(label_instance.label)
        self.assertCountEqual(actual_labels, record['labels'],
                              'Labels are not filtered correctly')

    def test_filter_expense_by_label(self):
        self.__create_test_data()
        sample_label = 'Entertainment'
        expected_expense_ids = ['23', '27', '29']
        actual_expense_ids = []
        label_instance = self.read_by_label(label=sample_label)
        for expense_instance in label_instance.expenses:
            actual_expense_ids.append(expense_instance.id)
        self.assertCountEqual(
            actual_expense_ids, expected_expense_ids, 'Labels are not filtered correctly')

    def test_update_expense_by_id(self):
        self.__create_test_data()
        sample_id = '29'
        new_data = 'Flipkart'
        self.update(id=sample_id, newdata={
            'recipient': new_data
        })
        expense_instance = self.read_by_id(id=sample_id)
        self.assertEqual(expense_instance.recipient, new_data)

    def test_remove_expense_by_id(self):
        self.__create_test_data()
        sample_id = '29'
        self.delete(sample_id)
        self.assertRaises(exc.NoResultFound, self.session.query(ExpenseDetails).filter_by(id=sample_id).one)




