from sqlmodel import create_engine, Session
from sqlmodel import SQLModel   

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/tp2_db"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

