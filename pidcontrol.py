# basic pid concept code from Digikey: https://www.youtube.com/watch?v=tFVAaUcOm4I
# to be fleshed out and implemented hopefully soon

k_p = 1
k_i = 0
k_d = 0
interval = 0.001 # interval should be replaced with current time - previoustime (which is stored in a variable in the while loop

# Tune this
# Tune this
# Tune this
# e.g. 1 ms

# Loop forever
error_prev = 0
integral = 0
while True: #use timers

  # Get value from sensor (feedback)
  val = readfromsensor()

  # Calculate the PID terms
  error = setpoint - val
  integral = integral + (error * interval)
  derivative = (error - error_prev) / interval
  output = (k_p * error) + (k_i * integral) + (k_d * derivative)

  # Save value for next iteration
  error_prev = error

  # Wait for interval time
  sleep(interval)

#filler stuff for now
def readfromsensor():
  # Get the position of the turtle
  return 50.0
