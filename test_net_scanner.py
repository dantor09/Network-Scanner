import unittest
from net_scanner import Network


# inheriting from test case will give you a lot of the functionality 
# that comse with test case
class TestNetScanner(unittest.TestCase):

    # if function name does not start with test, the test will nto run correctly
    def test_network(self):

        ipCIDR = ["221.8.159.37/28","96.179.53.57/23","47.16.101.151/17","71.42.102.58/20","2.217.42.73/19","82.251.71.209/15","52.124.252.192/13","158.241.19.144/23","108.216.184.244/28","23.57.46.204/8"]
        ipNetwork = ["221.8.159.32","96.179.52.0","47.16.0.0","71.42.96.0","2.217.32.0","82.250.0.0","52.120.0.0","158.241.18.0","108.216.184.240","23.0.0.0"]
        
        for index, ip in enumerate(ipCIDR):
            networkTest = Network(ip)
            network = networkTest.get_network()
            self.assertEqual(network,ipNetwork[index])

if __name__ == '__main__':
    unittest.main()
