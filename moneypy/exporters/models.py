from sqlalchemy import Column, ForeignKey, String, Date, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

association_table = Table('association', Base.metadata,
                                Column('expenseid', String, ForeignKey('expense_details.id')),
                                Column('labelid', String, ForeignKey('expense_labels.id')),
                          )

class ExpenseDetails(Base):
    __tablename__ = 'expense_details'
    id = Column(String, primary_key=True)
    date = Column(Date, nullable=True)
    amount = Column(Float, nullable=False)
    recipient = Column(String, nullable=False)
    description = Column(String, nullable=True)
    labels = relationship('ExpenseLabels', secondary=association_table, backref='expenses')

class ExpenseLabels(Base):
    __tablename__ ='expense_labels'
    id= Column(String, primary_key=True)
    label = Column(String, nullable=False)
