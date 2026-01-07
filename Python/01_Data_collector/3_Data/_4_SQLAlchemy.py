import _0_Coin_Data_getter as coin_data
import time
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/test_db"  # username, password, test_db를 적절히 변경하세요.
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Data(Base):
    __tablename__ = 'coin'

    dt = Column(DateTime, primary_key=True, default=datetime.utcnow)
    current_info = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def insert_data(curr_point, percentage):
    new_coin = Data(curr_info=curr_point, percentage=percentage)
    session.add(new_coin)
    session.commit()
    print(f"Inserted coin information.")


def read_data():
    coins = session.query(Data).all()
    for coin in coins:
        print(f"Datetime: {coin.dt}, Current: {coin.current_info}, Persent: {coin.percentage}")


if __name__ == "__main__":
    coin_name = "BTCUSDC"

    current_info = 0.0
    past_info = 0.0
    percentage = 0.0

    while True:
        time.sleep(5)  # 60 * 60 * 24)  # Daily
        past_info = current_info
        current_info = coin_data.get_altcoin_current_price(coin_name)
        if 0.0 != past_info:
            percentage = (current_info - past_info) / current_info * 100

        insert_data(current_info, percentage)

        read_data()

        # Add your own abort conditions.

    session.close()
