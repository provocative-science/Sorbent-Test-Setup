import time
import math
import random
import nominal

# -----------------------------
# Connect to Nominal
# -----------------------------
client = nominal.connect()
flow_topic = client.topic("flow/sccm")
voltage_topic = client.topic("flow/voltage")

print("\nRunning Flow Meter Simulation (Nominal connected)\n")

max_voltage = 5.0
max_flow = 30000.0

start_time = time.time()

try:
    while True:
        t = time.time() - start_time

        true_flow = 15000 + 10000 * math.sin(0.2 * t)

        voltage = (true_flow / max_flow) * max_voltage
        voltage += random.uniform(-0.02, 0.02)
        voltage = max(0.0, min(max_voltage, voltage))

        flow_rate = (voltage / max_voltage) * max_flow

        # ✅ SEND DATA TO NOMINAL
        flow_topic.publish(flow_rate)
        voltage_topic.publish(voltage)

        print(
            f"Voltage: {voltage:5.3f} V | "
            f"Flow rate: {flow_rate:8.1f} sccm"
        )

        time.sleep(1)

except KeyboardInterrupt:
    print("\nSimulation stopped.")
