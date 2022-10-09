# from sqlalchemy import Column, String
# from sqlalchemy.ext.declarative import declarative_base  
# from sqlalchemy.sql.schema import ForeignKey
# from configs.settings import SQL_ENGINE

# base = declarative_base()

# class ascorerisk(base):
#     __tablename__ = 'ascorerisk'
#     app_id = Column(String),
#     user_name = Column(String),
#     user_group = Column(String),
#     age = Column(int),
#     month_of_ocp = Column(int),
#     months_in_total_occupation = Column(int),
#     region = Column(String),
#     industry = Column(String),
#     type_of_house = Column(String),
#     gender = Column(String),            
#     verified_income = Column(int),
#     main_income = Column(int),
#     num_CIs_paid = Column(int),
#     num_CIs_approved = Column(int),
#     total_contracts_approved = Column(int),
#     ratio_living_contract = Column(int),
#     total_contracts_rejected = Column(int),
#     total_requires = Column(int),
#     pcb_score = Column(int)

# base.metadata.create_all(SQL_ENGINE)
