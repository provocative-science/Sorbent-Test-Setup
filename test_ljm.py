# from labjack import ljm
# import time


# try:
#     # Open the first found LabJack
#     handle = ljm.openS("ANY", "ANY", "ANY")

#     info = ljm.getHandleInfo(handle)
#     print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
#           "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
#           (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

#     # Configuration
#     name = "AIN5"
#     max_voltage = 5.0  # Full scale voltage of the sensor
#     max_flow = 30000.0  # Full scale flow rate in sccm

#     print("\nStarting continuous read. Press Ctrl+C to stop.\n")

#     # Continuous read loop
#     while True:
#         voltage = ljm.eReadName(handle, name)
#         flow_rate = (voltage / max_voltage) * max_flow

#         print("Voltage: %.3f V | Flow rate: %.2f sccm" % (voltage, flow_rate))

#         time.sleep(1)  # Wait for 1 second between readings

# except KeyboardInterrupt:
#     print("\nStopping continuous read...")

# finally:
#     # Always close the handle when done
#     try:
#         ljm.close(handle)
#         print("LabJack handle closed.")
#     except:
#         pass

import serial

PORT = "/dev/cu.usbserial-B0021TCS"
BAUD = 9600

with serial.Serial(PORT, BAUD, bytesize=8, parity="N", stopbits=1, timeout=2) as ser:
    # Put sensor in streaming mode
    ser.write(b"K 1\r\n")

    line = ser.readline().decode("ascii", errors="ignore").strip()
    filtered = line[18:23]     # chars 5..9
    unfiltered = line[26:31]  # chars 11..15

    if line:
            print(f'filtered: {filtered}    unfiltered: {unfiltered}')