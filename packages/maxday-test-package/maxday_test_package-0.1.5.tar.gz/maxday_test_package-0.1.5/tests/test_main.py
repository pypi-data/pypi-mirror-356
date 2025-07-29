from dummy_package import hello_world

def test_hello_world():
    assert hello_world() == "Hello, World!"
    assert hello_world("Python") == "Hello, Python!"
