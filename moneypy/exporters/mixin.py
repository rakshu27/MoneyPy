
from moneypy.exporters.models import ExpenseDetails, ExpenseLabels
from sqlalchemy.orm import sessionmaker, exc


class CRUDMixin(object):
    label_count = 1
    def __get_label_instance(self, labels):
        label_instances = []
        for label in labels:
            try:
                label_instance = self.session.query(
                    ExpenseLabels).filter_by(label=label).one()
                label_instances.append(label_instance)
            except exc.NoResultFound:
                label_id = 'Label' + str(CRUDMixin.label_count)
                label_instance = ExpenseLabels(id=label_id, label=label)
                CRUDMixin.label_count += 1
                label_instances.append(label_instance)
        return label_instances

    def insert(self, record):
        record = dict(record)
        record['labels']=self.__get_label_instance(record['labels'])
        self.session.add(ExpenseDetails(**record))
        self.session.commit()

    def delete(self, id):
        self.session.query(ExpenseDetails).filter_by(id=id).delete()
        self.session.commit()

    def update(self, id, newdata):
        record = self.session.query(ExpenseDetails).filter_by(id=id)
        for key, value in newdata.items():
            if key == 'labels':
                value = self.__get_label_instance(value)
            record.update({key: value})
        self.session.commit()

    def read_by_id(self, id):
        record = self.session.query(ExpenseDetails).filter_by(id=id).one()
        return record

    def read_by_label(self, label):
        label_instance = self.session.query(ExpenseLabels).filter_by(label=label).one()
        return label_instance

    def get_rows_count(self):
        return self.session.query(ExpenseDetails).count()

    def read_rows(self):
        return self.session.query(ExpenseDetails).all()



