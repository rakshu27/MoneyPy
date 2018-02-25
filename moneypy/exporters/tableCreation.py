from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from moneypy.exporters.models import Base

engine = create_engine('sqlite:///data/moneyManager.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
