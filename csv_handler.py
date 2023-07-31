import pandas as pd
class CSV:
    def __init__(self,fileName):
        self.df = pd.DataFrame(columns=["Date/Time","Host","Ping","TCP/19","TCP/21","TCP/22","TCP/23",
                                        "TCP/25","TCP/80","TCP/110","TCP/137","TCP/138","TCP/139","TCP/143",
                                        "TCP/179","TCP/389","TCP/443","TCP/445","TCP/902","TCP/903",
                                        "TCP/993","TCP/995","TCP/1080","TCP/1433","TCP/3306","TCP/3389","TCP/5900"])
        self.fileName = fileName
        self.csvRows = []
    
    def write_to_dataframe(self):
        self.df.loc[len(self.df)] = self.csvRows 
        self.csvRows = []
    
    def write_to_csv(self):
        self.df.to_csv(self.fileName, sep=",", index=False)

