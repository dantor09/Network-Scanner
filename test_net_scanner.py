import unittest
from net_scanner import Network


class TestNetScanner(unittest.TestCase):

    # if function name does not start with test, the test will not run correctly
    def test_network(self):
        
        """Test that the network address is correct for a given IP/CIDR"""
        test_data = [
        ("221.8.159.37/28", "221.8.159.32"),
        ("96.179.53.57/23", "96.179.52.0"),
        ("47.16.101.151/17", "47.16.0.0"),
        ("71.42.102.58/20", "71.42.96.0"),
        ("2.217.42.73/19", "2.217.32.0"),
        ("82.251.71.209/15", "82.250.0.0"),
        ("52.124.252.192/13", "52.120.0.0"),
        ("158.241.19.144/23", "158.241.18.0"),
        ("108.216.184.244/28", "108.216.184.240"),
        ("23.57.46.204/8", "23.0.0.0"),
        ]

        for ip_cidr, expected_network in test_data:
            dummyNetwork = Network(ip_cidr)
            network = dummyNetwork.get_network()
            self.assertEqual(network, expected_network)

    def test_get_octet_index(self):
        
        """Test that the octet index is correct for a given CIDR"""
        cidr_octet_mapping = [
        (list(range(1, 9)), 0),
        (list(range(9, 17)), 1),
        (list(range(17, 25)), 2),
        (list(range(25, 33)), 3)
        ]

        for cidr_range, expected_octet_index in cidr_octet_mapping:
            for CIDR in cidr_range:
                dummyNetwork = Network("172.27.131.1/" + str(CIDR))
                octetIndex = dummyNetwork.get_octet_index()
                self.assertEqual(octetIndex, expected_octet_index)

    def test_get_broadcast(self):
        """Test that the broadcast address is correct for a given IP/CIDR"""
        test_data = [
        ("221.8.159.37/28", "221.8.159.47"),
        ("96.179.53.57/23", "96.179.53.255"),
        ("47.16.101.151/17", "47.16.127.255"),
        ("71.42.102.58/20", "71.42.111.255"),
        ("2.217.42.73/19", "2.217.63.255"),
        ("82.251.71.209/15", "82.251.255.255"),
        ("52.124.252.192/13", "52.127.255.255"),
        ("158.241.19.144/23", "158.241.19.255"),
        ("108.216.184.244/28", "108.216.184.255"),
        ("23.57.46.204/8", "23.255.255.255"),
        ]

        for ip_cidr, expected_broadcast in test_data:
            dummyNetwork = Network(ip_cidr)
            broadcast = dummyNetwork.get_broadcast()
            self.assertEqual(broadcast, expected_broadcast)

if __name__ == '__main__':
    unittest.main()
