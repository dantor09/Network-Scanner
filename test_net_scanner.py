from net_scanner import Network



    # if function name does not start with test, the test will not run correctly
def test_get_network():

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
        assert network == expected_network

def test_get_octet_index():

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
            assert octetIndex == expected_octet_index

def test_decode_ip():

    test_data = [
                ("3633769907", "216.150.237.179"),
                ("1758202136", "104.204.9.24"),
                ("3573630627", "213.1.70.163"),
                ("3468956643", "206.196.19.227"),
                ("1511687121", "90.26.131.209"),
                ("2944128678", "175.123.214.166"),
                ("3277952363", "195.97.149.107"),
                ("2525154599", "150.130.205.39"),
                ("3544356109", "211.66.149.13"),
                ("2198693254", "131.13.101.134")
                ]

    for ipInteger, expectedIP in test_data:
        dummyNetwork = Network(expectedIP + "/1")
        decodedIP = dummyNetwork.decode_ip(ipInteger)
        assert decodedIP == expectedIP

def test_get_range():
    """Test that the IP range is correct for a given IP. This should 
    return the start integer of the network block the ip lands on 
    and the broadcast(end) integer for the block too"""
    
    test_data = ["221.8.159.37/28","96.179.53.57/23",
                "47.16.101.151/17","71.42.102.58/20",
                "2.217.42.73/19","82.251.71.209/15",
                "52.124.252.192/13","158.241.19.144/23",
                "108.216.184.244/28","23.57.46.204/8"
                ]

    start_stop_data = [("3708329761", "3708329774"),
                ("1622356993", "1622357502"),
                ("789577729", "789610494"),
                ("1193959425", "1193963518"),
                ("47783937", "47792126"),
                ("1392115713", "1392246782"),
                ("880279553", "880803838"),
                ("2666598913", "2666599422"),
                ("1826142449", "1826142462"),
                ("385875969", "402653182")
                ]

    for index, ip_cidr in enumerate(test_data):
        dummyNetwork = Network(ip_cidr)
        start, stop = dummyNetwork.get_range()
        expected_start, expected_stop = start_stop_data[index]
        assert (start, stop) == (int(expected_start), int(expected_stop))

def test_get_broadcast():
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
                ("23.57.46.204/8", "23.255.255.255")
                ]

    for ip_cidr, expected_broadcast in test_data:
        dummyNetwork = Network(ip_cidr)
        broadcast = dummyNetwork.get_broadcast()
        assert broadcast == expected_broadcast


def test_get_ip_address():

    test_data = [
        ("221.8.159.37/28", "221.8.159.37"),
        ("96.179.53.57/23", "96.179.53.57"),
        ("47.16.101.151/17", "47.16.101.151"),
        ("71.42.102.58/20", "71.42.102.58"),
        ("2.217.42.73/19", "2.217.42.73"),
        ("82.251.71.209/15", "82.251.71.209"),
        ("52.124.252.192/13", "52.124.252.192"),
        ("158.241.19.144/23", "158.241.19.144"),
        ("108.216.184.244/28", "108.216.184.244"),
        ("23.57.46.204/8", "23.57.46.204"),
        ]

    for ip_cidr, expected_ip in test_data:
        dummyNetwork = Network(ip_cidr)
        ipAddress = dummyNetwork.get_ip_address()
        assert ipAddress == expected_ip
