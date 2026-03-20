title: Dual Flow Simulation

# Remove the labjack-ljm package since we're not using real hardware
python:
  packages: []

bottom_panel:
  layout:
    - controls: script_table
      scripts:
        - label: Start Flow Simulation
          path: flow_simulation.py
    - id: status_text
      display: text
      default: "Ready"

left_panel:
  width: 0.6
  tabs:
    - name: Flow Rates
      layout:
        - title: Simulated Flow Rates (Both Sensors)
          plot: line
          stream_id: ["Flow Rate LJ1", "Flow Rate LJ2"]
          x_label: Time
          x_format: timestamp
          y_label: Flow Rate (L/min)
          legend: true
        - title: Cumulative Flow Comparison
          plot: line
          stream_id: ["Cumulative Flow LJ1", "Cumulative Flow LJ2"]
          x_label: Time
          x_format: timestamp
          y_label: Cumulative Flow (L)
          legend: true

right_panel:
  width: 0.4
  tabs:
    - name: Current Values
      layout:
        - title: Sensor 1 Flow Rate
          display: stream_value
          stream_id: "Flow Rate LJ1"
          units: L/min
          color: rgb(76,140,43)
        - title: Sensor 2 Flow Rate
          display: stream_value
          stream_id: "Flow Rate LJ2"
          units: L/min
          color: rgb(255,99,71)
        - title: Sensor 1 Cumulative
          display: stream_value
          stream_id: "Cumulative Flow LJ1"
          units: L
          color: rgb(76,140,43)
        - title: Sensor 2 Cumulative
          display: stream_value
          stream_id: "Cumulative Flow LJ2"
          units: L
          color: rgb(255,99,71)
