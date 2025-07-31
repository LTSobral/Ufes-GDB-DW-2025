class Connection:
    class Production:
        CONN_STAGE_MONGODB = "conn_stage_mongodb"

    class Development:
        CONN_STAGE_MONGODB = "conn_stage_mongodb"
    
    def __init__(self, deploy:bool=True):
        self.config = self.Production if deploy else self.Development

        self.conn_stage_mongodb = self.config.CONN_STAGE_MONGODB
