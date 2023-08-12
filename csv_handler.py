import pandas as pd
class CSV:
    def __init__(self,fileName, ports):
        self.table_columns = ["Date/Time","Host","Ping"]
        tcp_data = pd.read_csv("default_tcp_ports.csv", sep=",")
        
        for _, row in tcp_data.iterrows():
            if str(row["port"]) in ports:
                self.table_columns.append("TCP" + str(row["port"]))
 
        self.df = pd.DataFrame(columns=self.table_columns)
        self.fileName = fileName
        self.rows = []
    
    def write_to_dataframe(self):
        self.df.loc[len(self.df)] = self.rows 
        self.rows = []
    
    def write_to_csv(self):
        self.df.to_csv(self.fileName, sep=",", index=False)

