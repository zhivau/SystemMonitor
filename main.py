import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from data.model import Base
from data.data_service import DataService


def main():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    Base.metadata.create_all(bind=engine)

    data_service = DataService(session)

    app = QApplication(sys.argv)
    window = MainWindow(data_service)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
