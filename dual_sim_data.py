import time
import math
import connect_python
from labjack import ljm
from datetime import datetime
#import threading

@connect_python.main
def main(client: connect_python.Client):
    
    # Update status
    client.set_value("status_text", "Dual LabJack Simulation Running")
    
    # Simulation variables
    cumulative_flow_1 = 0.0
    cumulative_flow_2 = 0.0
    start_time = time.time()
    point_counter = 0
    
    # Configuration for both LabJacks
    max_voltage = 5.0  # Full scale voltage of the sensor
    max_flow = 10.0    # Full scale flow rate in liters/min
    
    try:
        
        
        #Open specific LabJacks by serial number
        handle1 = ljm.openS("T7", "ANY", "SERIAL_NUMBER_1")
        handle2 = ljm.openS("T7", "ANY", "SERIAL_NUMBER_2")
        
        # Get info for both devices
        info1 = ljm.getHandleInfo(handle1)
        info2 = ljm.getHandleInfo(handle2)
        
        print("LabJack 1 - Device type: %i, Serial: %i, IP: %s" % 
              (info1[0], info1[2], ljm.numberToIP(info1[3])))
        print("LabJack 2 - Device type: %i, Serial: %i, IP: %s" % 
              (info2[0], info2[2], ljm.numberToIP(info2[3])))

        # Channel names for each LabJack
        channel1 = "AIN5"  # Channel on LabJack 1
        channel2 = "AIN5"  # Channel on LabJack 2 

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            point_counter += 1
            timestamp = datetime.now()

            # Read from both LabJacks
            voltage1 = ljm.eReadName(handle1, channel1)
            voltage2 = ljm.eReadName(handle2, channel2)
            
            # Calculate flow rates
            flow_rate1 = (voltage1 / max_voltage) * max_flow
            flow_rate2 = (voltage2 / max_voltage) * max_flow

            # Update cumulative flows
            time_delta = 0.5  # 0.5 second intervals
            cumulative_flow_1 += (flow_rate1 / 60.0) * time_delta
            cumulative_flow_2 += (flow_rate2 / 60.0) * time_delta

            # Stream data from both LabJacks with descriptive names
            client.stream("Flow Rate LJ1", timestamp, flow_rate1)
            client.stream("Flow Rate LJ2", timestamp, flow_rate2)
            client.stream("Cumulative Flow LJ1", timestamp, cumulative_flow_1)
            client.stream("Cumulative Flow LJ2", timestamp, cumulative_flow_2)
            client.stream("Elapsed Time", timestamp, elapsed_time)
            
            # Print to logs 
            print(f"Point {point_counter}:")
            print(f"  LJ1: V={voltage1:.2f}V, Flow={flow_rate1:.2f}L/min, Cum={cumulative_flow_1:.2f}L")
            print(f"  LJ2: V={voltage2:.2f}V, Flow={flow_rate2:.2f}L/min, Cum={cumulative_flow_2:.2f}L")
            print(flush=True)
           
            time.sleep(0.5)  # Update every 0.5 seconds

            if elapsed_time >= 20:
                break
            
    except Exception as e:
        print(f"Error in simulation: {e}")
        client.set_value("status_text", f"Error: {str(e)}")
    finally:
        # Close both LabJack connections
        try:
            ljm.close(handle1)
            ljm.close(handle2)
            print("LabJack connections closed")
        except:
            pass
        client.set_value("status_text", "Simulation Complete")

if __name__ == "__main__":
    main()





#-----YAML Configuration for two labjacks-----

# title: Dual LabJack Flow Monitoring

# python:
#   packages:
#     - labjack-ljm

# bottom_panel:
#   layout:
#     - controls: script_table
#       scripts:
#         - label: Start Dual LabJack Reading
#           path: dual_labjack_flow.py
#     - id: status_text
#       display: text
#       default: "Ready"

# left_panel:
#   width: 0.6
#   tabs:
#     - name: Flow Rates
#       layout:
#         - title: Real-time Flow Rates (Both LabJacks)
#           plot: line
#           stream_id: ["Flow Rate LJ1", "Flow Rate LJ2"]
#           x_label: Time
#           x_format: timestamp
#           y_label: Flow Rate (L/min)
#           legend: true
#         - title: Cumulative Flow Comparison
#           plot: line
#           stream_id: ["Cumulative Flow LJ1", "Cumulative Flow LJ2"]
#           x_label: Time
#           x_format: timestamp
#           y_label: Cumulative Flow (L)
#           legend: true

# right_panel:
#   width: 0.4
#   tabs:
#     - name: Current Values
#       layout:
#         - title: LJ1 Flow Rate
#           display: stream_value
#           stream_id: "Flow Rate LJ1"
#           units: L/min
#           color: rgb(76,140,43)
#         - title: LJ2 Flow Rate
#           display: stream_value
#           stream_id: "Flow Rate LJ2"
#           units: L/min
#           color: rgb(255,99,71)
#         - title: LJ1 Cumulative
#           display: stream_value
#           stream_id: "Cumulative Flow LJ1"
#           units: L
#           color: rgb(76,140,43)
#         - title: LJ2 Cumulative
#           display: stream_value
#           stream_id: "Cumulative Flow LJ2"
#           units: L
#           color: rgb(255,99,71)

