import packages

def test_retrieve_pacakges():
    test = packages.retrieve_packages()
    assert test is not None
