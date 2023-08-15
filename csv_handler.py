import pandas as pd
class CSV:
    def __init__(self,fileName, ports, tcpPortsFile = "default_tcp_ports.csv"):
        print("______")
        print(len(ports))
        print("______")
        
        self._tcpData = self.__load_tcp_data(tcpPortsFile)
        self._tableColumns = self.__set_table_columns(ports)
        self.df = pd.DataFrame(columns=self._tableColumns)
        self.fileName = fileName
        self.row = []
    
    def __load_tcp_data(self, filepath):
        return pd.read_csv(filepath, sep=",")
    
    def __set_table_columns(self, ports):
        baseColumns = ["Date/Time", "Host", "Ping"]

        relevantPorts = []
        for _, row in self._tcpData.iterrows():
            if str(row["port"]) in ports:
                print("true")
                relevantPorts.append(str(row["port"]))

        portColumns = ["TCP" + str(port) for port in relevantPorts]
        return baseColumns + portColumns
    
    def write_to_dataframe(self):
        print("in write to data frame")
        print(len(self.df))
        print(self.row)

        print("in write to data frame")
        self.df.loc[len(self.df)] = self.row 
        self.row = []
    
    def write_to_csv(self):
        self.df.to_csv(self.fileName, sep=",", index=False)

