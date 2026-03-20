import connect_python

@connect_python.main
def test(client: connect_python.Client):
    print("Test button clicked!", flush=True)
