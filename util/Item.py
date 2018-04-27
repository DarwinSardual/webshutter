class Item:

    def __init__(self, dbId, link, status, isChecked = False):
        self.dbId = dbId
        self.link = link
        self.status = status
        self.isChecked = isChecked
