import unittest
from net_scanner import Network


class TestNetScanner(unittest.TestCase):

    # if function name does not start with test, the test will not run correctly
    def test_network(self):

        ipCIDR = ["221.8.159.37/28","96.179.53.57/23","47.16.101.151/17","71.42.102.58/20","2.217.42.73/19","82.251.71.209/15","52.124.252.192/13","158.241.19.144/23","108.216.184.244/28","23.57.46.204/8"]
        ipNetwork = ["221.8.159.32","96.179.52.0","47.16.0.0","71.42.96.0","2.217.32.0","82.250.0.0","52.120.0.0","158.241.18.0","108.216.184.240","23.0.0.0"]
        
        for index, ip in enumerate(ipCIDR):
            networkTest = Network(ip)
            network = networkTest.get_network()
            self.assertEqual(network,ipNetwork[index])

    def test_get_octet_block(self):
        CIDR1 = [1,2,3,4,5,6,7,8]
        CIDR2 = [9,10,11,12,13,14,15,16]
        CIDR3 = [17,18,19,20,21,22,23,24]
        CIDR4 = [25,26,27,28,29,30,31,32]

        for CIDR in CIDR1:
            networkTest = Network("172.27.131.1/" + str(CIDR))
            block = networkTest.get_octet_block()
            self.assertEqual(block,0)

        for CIDR in CIDR2:
            networkTest = Network("172.27.131.1/" + str(CIDR))
            block = networkTest.get_octet_block()
            self.assertEqual(block,1)

        for CIDR in CIDR3:
            networkTest = Network("172.27.131.1/" + str(CIDR))
            block = networkTest.get_octet_block()
            self.assertEqual(block,2)

        for CIDR in CIDR4:
            networkTest = Network("172.27.131.1/" + str(CIDR))
            block = networkTest.get_octet_block()
            self.assertEqual(block,3)

    def test_get_broadcast(self):

        ipCIDR = ["221.8.159.37/28","96.179.53.57/23","47.16.101.151/17","71.42.102.58/20","2.217.42.73/19","82.251.71.209/15","52.124.252.192/13","158.241.19.144/23","108.216.184.244/28","23.57.46.204/8"]
        ipBroadcast = ["221.8.159.47","96.179.53.255","47.16.127.255","71.42.111.255","2.217.63.255","82.251.255.255","52.127.255.255","158.241.19.255","108.216.184.255","23.255.255.255"]

        for index, ip in enumerate(ipCIDR):
            networkTest = Network(ip)
            broadcast = networkTest.get_broadcast()
            self.assertEqual(broadcast,ipBroadcast[index])

if __name__ == '__main__':
    unittest.main()
