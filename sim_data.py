import time
import math
import connect_python
from labjack import ljm
from datetime import datetime
import serial



# def voltage_to_temperature(therm_voltage, supply_voltage, R_fixed, R_nominal, T_nominal, beta):
#     """Convert AIN voltage to temperature in Celsius using Beta equation."""
#     if therm_voltage <= 0 or therm_voltage >= supply_voltage:
#         return None  # Guard against divide-by-zero at rail voltages
#     # Voltage divider → thermistor resistance
#     R_thermistor = R_fixed * therm_voltage / (supply_voltage - therm_voltage)
#     # Beta equation → temperature in Kelvin
#     temp_K = 1.0 / (1.0 / T_nominal + (1.0 / beta) * math.log(R_thermistor / R_nominal))
#     return temp_K - 273.15  # Convert to Celsius

#     temp_K = pressure_fs_temp * (supply_voltage / pressure_fs_voltage)


    
   
def voltage_to_pressure(pressure_voltage, pressure_fs_voltage, full_scale_torr):
    torr = pressure_voltage*(full_scale_torr/pressure_fs_voltage)
    return torr


@connect_python.main
def main(client: connect_python.Client):
    
    # Update status
    client.set_value("status_text", "Simulation Running")
    
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

        PORT = "/dev/cu.usbserial-B0021TCS"
        BAUD = 9600

        with serial.Serial(PORT, BAUD, bytesize=8, parity="N", stopbits=1, timeout=2) as ser:
    # Put sensor in streaming mode
            ser.write(b"K 1\r\n")       


    ##### FLOW Variables #####
        flow_name = "AIN5"
        flow_fs_voltage = 5.0  # Full scale voltage of the sensor
        max_flow = 10.0    # Full scale flow rate in liters/min; 10,000 SCCM

    # ##### THERMISTOR ##### --- these values needs to be upated with accurate values once thermistor is chosen
    #     thermistor_name = "AIN1"
    #     R_fixed = 1000.0        # Fixed resistor in voltage divider (ohms)
    #     R_nominal = 10000.0     # Thermistor resistance at 25°C
    #     T_nominal = 298.15      # 25°C in Kelvin
    #     beta = 3892             # Beta coefficient (check your thermistor datasheet)
    #     supply_voltage = 2.5    # Voltage divider voltage

    ##### PRESSURE #####
        pressure_name = "AIN7"
        pressure_fs_voltage = 10
        full_scale_torr = 100
        

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
            

            # # Read thermistor
            # therm_voltage = ljm.eReadName(handle, thermistor_name)
            # temperature = voltage_to_temperature(therm_voltage, supply_voltage, R_fixed, R_nominal, T_nominal, beta)

            


            # Read Pressure Sensor
            pressure_voltage = ljm.eReadName(handle, pressure_name)
            pressure = voltage_to_pressure(pressure_voltage, pressure_fs_voltage, full_scale_torr)

            line = ser.readline().decode("ascii", errors="ignore").strip()
            filtered = line[18:23]     # chars 5..9
            unfiltered = line[26:31]  # chars 11..15


            # Stream the flow data using positional arguments
            client.stream("Pressure", datetime.now(), pressure)
            client.stream("Flow Rate", datetime.now(), flow_rate)
            client.stream("Cumulative Flow", datetime.now(), cumulative_flow)
            client.stream("Elapsed Time", datetime.now(), elapsed_time)
            client.stream("Filtered CO2 ppm", datetime.now(), filtered)
            client.stream("Unfiltered CO2 ppm", datetime.now(), unfiltered)

            #if temperature is not None:
                #client.stream("Temperature", datetime.now(), temperature)
            
            
            # Print to logs 
            print(f"Point {point_counter}: \n Flow = {flow_rate:.2f}, Cumulative = {cumulative_flow:.2f}", flush=True)
            #print(f' Pressure = {pressure:.2f} Temp = {temperature:.2f} \n')
            #print(f'{pressure_voltage}')



            # while True:
            #         line = ser.readline().decode("ascii", errors="ignore").strip()
            #         filtered = line[18:23]     # chars 18-23
            #         unfiltered = line[26:31]  # chars 26-31
            time.sleep(0.5)  # Update every 0.5 seconds
            #         client.stream("Unfiltered CO2 ppm", datetime.now(), unfiltered)
            #         client.stream("Filtered CO2 ppm", datetime.now(), filtered)



            #if elapsed_time >= 20:
                        #break
            
    except KeyboardInterrupt: #not printing with nominal bc no keyboard interrupt, figure out the equivlent for hitting stop
        print("\nSimulation stopped by user")
        client.set_value("status_text", "Simulation Stopped") 
    except Exception as e:
        print(f"Error in simulation: {e}")
        client.set_value("status_text", f"Error: {str(e)}")

if __name__ == "__main__":
    main()

