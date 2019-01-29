from sqlalchemy import *

engine = create_engine('sqlite:///satyam.db')

metadata = MetaData()

user = Table('user', metadata,
             Column('user_id', Integer, primary_key=True),
             Column('user_name', String(16), nullable=False),
             Column('email_address', String(60), key='email'),
             Column('password', String(20), nullable=False)
             )

user_prefs = Table('user_prefs', metadata,
                   Column('pref_id', Integer, primary_key=True),
                   Column('user_id', Integer, ForeignKey(
                       "user.user_id"), nullable=False),
                   Column('pref_name', String(40), nullable=False),
                   Column('pref_value', String(100))
                   )

metadata.create_all(engine)
