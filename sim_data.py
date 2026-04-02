import time
import math
import connect_python
from labjack import ljm
from datetime import datetime
import serial

 
   
def voltage_to_pressure(pressure_voltage, pressure_fs_voltage, full_scale_torr):
    torr = pressure_voltage*(full_scale_torr/pressure_fs_voltage)
    return torr/7.6


@connect_python.main
def main(client: connect_python.Client):
    
    # Update status
    client.set_value("status_text", "Simulation Running")

    #CO2 Sensor Serial reading
    PORT = "/dev/cu.usbserial-B0021TCS" 
    BAUD = 9600 

    ser = serial.Serial(PORT, BAUD, timeout=2)
    ser.reset_input_buffer()



    # Simulation variables
    cumulative_flow = 0.0
    start_time = time.time()
    point_counter = 0
    
    try:
        # Open LabJack
        handle = ljm.openS("ANY", "ANY", "ANY")
        info = ljm.getHandleInfo(handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
                  "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
                (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

    except Exception as e:
        print(f"Error in simulation: {e}")
        client.set_value("status_text", f"Error: {str(e)}")
         


    ##### FLOW Variables #####
    flow_name = "AIN5"
    flow_fs_voltage = 5.0  # Full scale voltage of the sensor
    max_flow = 10.0    # Full scale flow rate in liters/min; 10,000 SCCM


    ##### PRESSURE #####
    pressure_name = "AIN7"
    pressure_fs_voltage = 10
    full_scale_torr = 760
        
    
    while True:
                current_time = time.time()
                elapsed_time = current_time - start_time
                point_counter += 1

            # Continuous read loop
            
                flow_voltage = ljm.eReadName(handle, flow_name)
                flow_rate =  (flow_voltage / flow_fs_voltage) * (max_flow)


            # Update cumulative flow
                time_delta = 0.5  # 0.5 second intervals
                cumulative_flow += (flow_rate / 60.0) * time_delta #subtracting the negative (reverse direction)
            # cumulative_flow += (abs(flow_rate) / 60.0) * time_delta #adding the abs(negative) (reverse direction)
            
                ser.reset_input_buffer()
                raw = ser.readline()
                if not raw:
                    continue
                line = raw.decode("ascii", "ignore").strip()
                if not line:
                    continue

                try:
            
                    filtered = float(line[18:23]) 
                    unfiltered = float(line[26:31])
            # Stream 
                    client.stream("Filtered CO2 ppm", datetime.now(), filtered)
                    client.stream("Unfiltered CO2 ppm", datetime.now(), unfiltered)
                except (ValueError, IndexError):

                    continue



            # Read Pressure Sensor
                pressure_voltage = ljm.eReadName(handle, pressure_name)
                pressure = voltage_to_pressure(pressure_voltage, pressure_fs_voltage, full_scale_torr)

            # Stream the flow data
                client.stream("Pressure", datetime.now(), pressure)
                client.stream("Flow Rate", datetime.now(), flow_rate)
                client.stream("Cumulative Flow", datetime.now(), cumulative_flow)
                client.stream("Elapsed Time", datetime.now(), elapsed_time)
                

            
            
            # Print to logs 
                print(f"Point {point_counter}: \n Flow = {flow_rate:.2f}, Cumulative = {cumulative_flow:.2f}", flush=True)


                time.sleep(0.5)  # Update every 0.5 seconds
     

            #if elapsed_time >= 20:
                        #break
            
if __name__ == "__main__":
    main()

