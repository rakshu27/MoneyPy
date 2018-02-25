import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, exc
from moneypy.exporters.models import Base, ExpenseDetails, ExpenseLabels
from datetime import date, datetime
import os
 
class DatabaseTesting(unittest.TestCase):
    sampleRecords=[{
        'id':'23',
        'amount':500,
        'date':date(2017, 10, 17),
        'recipient':'Aircel',
        'description':'Aircel Prepaid Bill',
        'labels':['cellular', 'Entertainment']
    },
    {
        'id':'25',
        'amount':1000,
        'date':date(2017, 4, 11),
        'recipient':'Amazon',
        'description':'Python Book',
        'labels':['Education', 'Online shopping']
    },
    {
        'id':'27',
        'amount':2000,
        'date':date(2017, 11, 12),
        'recipient':'Netflix',
        'description':'Account Subscription to watch movies',
        'labels':['Entertainment']
    },
    {
        'id':'29',
        'amount':2000,
        'date':date(2017, 12, 22),
        'recipient':'Amazon',
        'description': 'Bought new dresses',
        'labels':['Entertainment','Online shopping']
    }]
    labelCount=0
    def populateSampleData(self):
        for record in DatabaseTesting.sampleRecords:
            expenseid = record['id']
            amount = record['amount']
            recipient = record['recipient']
            description = record['description']
            expenseDate = record['date']
            labels = record['labels']
            labelInstances = self.getLabelInstances(labels)
            expenseObject = ExpenseDetails(id=expenseid, date=expenseDate, amount=amount, recipient=recipient, description=description, labels=labelInstances)
            self.session.add(expenseObject)
    def getLabelInstances(self, labels):
        labelInstances = []
        for label in labels:
            try:
                labelInstance = self.session.query(ExpenseLabels).filter_by(label=label).one()
                labelInstances.append(labelInstance)
            except exc.NoResultFound:
                labelId = 'Label'+str(DatabaseTesting.labelCount)
                labelInstance = ExpenseLabels(id=labelId, label=label)
                DatabaseTesting.labelCount += 1
                labelInstances.append(labelInstance)
            except exc.MultipleResultsFound:
                raise
        return labelInstances
    def setUp(self):
        engine = create_engine('sqlite:///data/test_money_manager.db', echo=False)
        self.engine = engine
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.populateSampleData()
        self.session.commit()
    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)
        try:
            filename= '.\\data\\test_money_manager.db'
            os.remove(filename)
        except FileNotFoundError:
            pass
    def test_recordInsertionInExpenseDetailsTableByCheckingCount(self):
        count = self.session.query(ExpenseDetails).count()
        self.assertEqual(count, len(DatabaseTesting.sampleRecords), 'Given records are not inserted properly in ExpenseDetails table')
    def test_backPopulationInExpenseLabelsTableByCheckingCount(self):
        count = self.session.query(ExpenseLabels).count()
        self.assertEqual(count, DatabaseTesting.labelCount, 'Labels are not back populated correctly in ExpenseLabels Table') 
    def test_filterLabelsByExpenseId(self):
        record = DatabaseTesting.sampleRecords[3]
        recordId = record['id']
        expectedLabels = record['labels']
        actualLabels = []
        try:
            expenseInstance = self.session.query(ExpenseDetails).filter_by(id=recordId).one()
            for labelInstance in expenseInstance.labels:
                actualLabels.append(labelInstance.label)
            self.assertCountEqual(actualLabels, expectedLabels, 'Labels are not filtered correctly')
        except exc.NoResultFound:
            raise
        except exc.MultipleResultsFound:
            raise
    def test_filterExpensesByLabel(self):
        sampleLabel = 'Entertainment'
        expectedExpenseIds = ['23','27','29']
        actualExpenseIds = []
        try:
            labelInstance = self.session.query(ExpenseLabels).filter_by(label=sampleLabel).one()
            for expenseInstance in labelInstance.expenses:
                actualExpenseIds.append(expenseInstance.id)
            self.assertCountEqual(actualExpenseIds, expectedExpenseIds, 'Labels are not filtered correctly')
        except exc.NoResultFound:
            raise
        except exc.MultipleResultsFound:
            raise
        

    



    
