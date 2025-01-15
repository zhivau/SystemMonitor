from data.model import Usage


class DataService:
    def __init__(self, session):
        self.session = session

    def insert_usage(self, cpu, ram, disk):
        usage = Usage(cpu=cpu, ram=ram, disk=disk)
        self.session.add(usage)
        self.session.commit()
        self.session.refresh(usage)
        return usage

    def get_all_usage(self):
        return self.session.query(Usage).all()

    def close(self):
        self.session.close()
