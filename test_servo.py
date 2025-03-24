#!/usr/bin/env python3

import time
import pigpio

# --- User Configurations ---
SERVO_PIN = 18        # GPIO pin used for servo signal
MIN_PULSE_WIDTH = 500  # microseconds (typical minimum pulse width)
MAX_PULSE_WIDTH = 2500 # microseconds (typical maximum pulse width)
SWEEP_DEGREE_START = 0
SWEEP_DEGREE_END = 270
STEP_SIZE = 10        # Degrees to move per step
DWELL_TIME = 1.0      # Seconds to wait at each position

def angle_to_pulsewidth(angle, min_pulse=MIN_PULSE_WIDTH, max_pulse=MAX_PULSE_WIDTH):
    """
    Convert an angle in degrees to a pulse width in microseconds.
    Assumes angle in [0,180].
    """
    # Ensure angle is within 0-270
    angle = max(0, min(270, angle))
    # Linear mapping from [0..270] -> [min_pulse..max_pulse]
    pulse_width_range = max_pulse - min_pulse
    pulsewidth = min_pulse + (pulse_width_range * angle / 270.0)
    return pulsewidth

def main():
    # Initialize pigpio library
    pi = pigpio.pi()
    if not pi.connected:
        print("Could not connect to pigpio daemon.")
        return
    
    try:
        print("Starting servo test on GPIO {}.".format(SERVO_PIN))
        
        # Set servo pin as servo output
        # (pigpio automatically handles hardware-timed PWM for the servo)
        pi.set_mode(SERVO_PIN, pigpio.OUTPUT)
        
        # Sweep from SWEEP_DEGREE_START to SWEEP_DEGREE_END
        for angle in range(SWEEP_DEGREE_START, SWEEP_DEGREE_END + 1, STEP_SIZE):
            pulsewidth = angle_to_pulsewidth(angle)
            pi.set_servo_pulsewidth(SERVO_PIN, pulsewidth)
            print(f"Moving to {angle} degrees -> pulse width = {pulsewidth:.1f} μs")
            time.sleep(DWELL_TIME)

        # Then sweep back from SWEEP_DEGREE_END down to SWEEP_DEGREE_START
        for angle in range(SWEEP_DEGREE_END, SWEEP_DEGREE_START - 1, -STEP_SIZE):
            pulsewidth = angle_to_pulsewidth(angle)
            pi.set_servo_pulsewidth(SERVO_PIN, pulsewidth)
            print(f"Moving to {angle} degrees -> pulse width = {pulsewidth:.1f} μs")
            time.sleep(DWELL_TIME)

        # Turn off servo signals (optional)
        pi.set_servo_pulsewidth(SERVO_PIN, 0)
        print("Servo test complete.")

    finally:
        # Clean up and close pigpio connection
        pi.stop()

if __name__ == "__main__":
    main()
