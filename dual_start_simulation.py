import time
import math
import connect_python
from datetime import datetime
import random

@connect_python.main
def main(client: connect_python.Client):
    
    # Stream initial status
    client.stream("status_text", datetime.now(), "Dual Simulation Running")
    
    # Simulation variables for both sensors
    cumulative_flow_1 = 0.0
    cumulative_flow_2 = 0.0
    start_time = time.time()
    point_counter = 0
    
    try:
        # Simulation parameters
        max_voltage = 5.0
        max_flow = 10.0  # Full scale flow rate in liters/min
        
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            point_counter += 1
            timestamp = datetime.now()

            # Update status every 10 points (5 seconds)
            if point_counter % 10 == 0:
                client.stream("status_text", timestamp, f"Running... {elapsed_time:.1f}s elapsed")

            # Simulate SENSOR 1 - sine wave pattern
            base_voltage_1 = 2.5 + 1.0 * math.sin(elapsed_time * 0.1)
            voltage_1 = base_voltage_1 + random.uniform(-0.1, 0.1)
            voltage_1 = max(0, min(5.0, voltage_1))
            flow_rate_1 = (voltage_1 / max_voltage) * max_flow

            # Simulate SENSOR 2 - cosine wave pattern (different phase/frequency)
            base_voltage_2 = 3.0 + 0.8 * math.cos(elapsed_time * 0.15)
            voltage_2 = base_voltage_2 + random.uniform(-0.1, 0.1)
            voltage_2 = max(0, min(5.0, voltage_2))
            flow_rate_2 = (voltage_2 / max_voltage) * max_flow

            # Update cumulative flows
            time_delta = 0.5  # 0.5 second intervals
            cumulative_flow_1 += (flow_rate_1 / 60.0) * time_delta
            cumulative_flow_2 += (flow_rate_2 / 60.0) * time_delta

            # Stream data for BOTH sensors
            client.stream("Flow Rate Sensor 1", timestamp, flow_rate_1)
            client.stream("Flow Rate Sensor 2", timestamp, flow_rate_2)
            client.stream("Cumulative Flow Sensor 1", timestamp, cumulative_flow_1)
            client.stream("Cumulative Flow Sensor 2", timestamp, cumulative_flow_2)
            client.stream("Elapsed Time", timestamp, elapsed_time)
            
            # Print to logs 
            print(f"Point {point_counter}:")
            print(f"  Sensor 1: V={voltage_1:.2f}V, Flow={flow_rate_1:.2f}L/min, Cum={cumulative_flow_1:.2f}L")
            print(f"  Sensor 2: V={voltage_2:.2f}V, Flow={flow_rate_2:.2f}L/min, Cum={cumulative_flow_2:.2f}L")
            print(flush=True)
           
            time.sleep(0.5)  # Update every 0.5 seconds

            # Stop after a certain time
            if elapsed_time >= 120:  # Run for 2 minutes
                client.stream("status_text", timestamp, "Time limit reached")
                break
            
    except Exception as e:
        print(f"Error in simulation: {e}")
        client.stream("status_text", datetime.now(), f"Error: {str(e)}")
    finally:
        client.stream("status_text", datetime.now(), "Simulation Complete")
        print("Simulation finished")

if __name__ == "__main__":
    main()
