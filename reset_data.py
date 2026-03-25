import connect_python

@connect_python.main
def main(client: connect_python.Client):
    print("Resetting data", flush=True)
    
    client.clear_stream("Flow Rate")
    client.clear_stream("Cumulative Flow")
    client.clear_stream("Elapsed Time")
    client.clear_stream("Temperature")
    client.clear_stream("Pressure")
    client.clear_stream("Unfiltered CO2 ppm")
    client.clear_stream("Filtered CO2 ppm")
    client.set_value("status_text", "Data cleared")
    
    
    print("Reset complete", flush=True)
if __name__ == "__main__":
    # If the library handles the client connection automatically:
    main()