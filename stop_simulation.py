import connect_python
from datetime import datetime

# Import the global variable from start_simulation
try:
    import start_simulation
except ImportError:
    print("Could not import start_simulation module", flush=True)
    start_simulation = None

@connect_python.main
def main(client: connect_python.Client):
    client.set_value("simulation_active", False)
    print("Sent stop signal to server.")
    
    timestamp = datetime.now()
    
    if start_simulation and hasattr(start_simulation, 'simulation_running'):
        if start_simulation.simulation_running:
            start_simulation.simulation_running = False
            
            # Wait a moment for the thread to finish
            if (hasattr(start_simulation, 'simulation_thread') and 
                start_simulation.simulation_thread and 
                start_simulation.simulation_thread.is_alive()):
                start_simulation.simulation_thread.join(timeout=1.0)
            
            final_flow = getattr(start_simulation, 'cumulative_flow', 0.0)
            status_text = f"Stopped - Final total: {final_flow:.2f} L"
            client.stream(stream_id="status_stream", timestamp=timestamp, value=status_text)
            print(f"Flow meter simulation stopped. Total flow: {final_flow:.2f} L", flush=True)
        else:
            client.stream(stream_id="status_stream", timestamp=timestamp, value="Simulation not running")
            print("Simulation was not running", flush=True)
    else:
        client.stream(stream_id="status_stream", timestamp=timestamp, value="Error: Could not access simulation")
        print("Error: Could not access simulation state", flush=True)

if __name__ == "__main__":
    # If the library handles the client connection automatically:
    main()