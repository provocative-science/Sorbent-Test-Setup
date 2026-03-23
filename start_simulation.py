import time
import math
import connect_python
from datetime import datetime

@connect_python.main
def main(client: connect_python.Client):
    # Clear any existing data   # Can't decide if I want to keep this in, bc of reset_data
    client.clear_stream("flow_rate")
    client.clear_stream("cumulative_flow") 
    
    # Update status
    client.set_value("status_text", "Simulation Running")
    
    print("Starting flow meter simulation...\n")
    
    # Simulation variables
    cumulative_flow = 0.0
    start_time = time.time()
    point_counter = 0
    
    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            point_counter += 1
            
            # Simulate varying flow rate
            base_flow = 5.0
            variation = 1.0 * math.sin(elapsed_time * 0.5)
            flow_rate = base_flow + variation
            
            # Update cumulative flow
            time_delta = 0.1  # 0.1 second intervals
            cumulative_flow += (flow_rate / 60.0) * time_delta

            #calculate voltage
            voltage = flow_rate/2

            temp = flow_rate/4
            pressure = flow_rate 
            co2_ppm = flow_rate

            client.stream("Temperature", datetime.now(), temp)
            client.stream("Pressure", datetime.now(), pressure)
            client.stream("CO2 ppm", datetime.now(), co2_ppm)



            
            # Stream the data using positional arguments
            client.stream("Flow Rate", datetime.now(), flow_rate)
            client.stream("Cumulative Flow", datetime.now(), cumulative_flow)
            client.stream("Elapsed Time", datetime.now(), elapsed_time)

            
            # Print to console (like your example)
            print(f"Point {point_counter}: \n Flow = {flow_rate:.2f}, Cumulative = {cumulative_flow:.2f}", flush=True)
            print(f' Pressure = {pressure:.2f} Temp = {temp:.2f} \n')
            time.sleep(0.25)  # Update every 0.25 seconds

            # if cumulative_flow >= 1: 
            #     break
            # if elapsed_time >= 10:
            #      break
            
    except KeyboardInterrupt: 
        print("\nSimulation stopped by user")
        client.set_value("status_text", "Simulation Stopped")
    except Exception as e:
        print(f"Error in simulation: {e}")
        client.set_value("status_text", f"Error: {str(e)}")
    # finally:
    #     client.set_value("status_text", "Simulation Complete")


if __name__ == "__main__":
    main()

