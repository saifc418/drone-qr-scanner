# Import libraries
from pyzbar.pyzbar import decode
import cv2
import numpy as np
from djitellopy import Tello
import time

# The following code lets you read a QR code from tello drone stream

# Initialize tello drone object
drone = Tello()

# Connect the drone
drone.connect()

# Print the drone battery
print(drone.get_battery())

# Turn the stream off and on
drone.streamoff()
drone.streamon()

# Initialize running as True
running = True

# Initialize the list of URLs linked to the QR Code(s)
qrCodes = []

# Create a window named Tello Stream 
cv2.namedWindow("Tello Stream", cv2.WINDOW_NORMAL)

# Initialize the takeoff variable
takeoff = 0

# If takeoff is 1, the drone will take flight
if takeoff == 1:
    drone.takeoff()

# Loop while running is true
while running:
    
    # Read the video stream
    img = drone.get_frame_read().frame
    
    # Convert the drone video stream to the correct colors
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  
    # Loop for the number of QR codes in frame
    for code in decode(img):

        # Uncomment this to visualize all the decoded elements from the QR code
        #print(code)

        # Get the URL
        url = code.data.decode()

        # Initialize the add variable
        addQRCode = 1

        # Loop for the length of URLs in the list
        for i in range(len(qrCodes)):

            # If the URL is already in the list, run this code
            if qrCodes[i] == url:

                # Set add to 0
                addQRCode = 0

                # Teriminate the loop
                break
        
        # If add is 1, add the URL to the list of QR codes
        if addQRCode == 1:
            qrCodes.append(url)

        # The four points for the bounding box around the QR code
        rectanglePoints = code.rect

        # Uncomment this to visualize all four points
        #print(rectanglePoints)

        # Run this block if there is a URL
        if url:

            # Create a list of the Point objects and turn it into an array
            points = np.array(code.polygon)

            # Draw the bounding box
            cv2.polylines(img, [points], True, (0, 255, 0), 3)

            # Put the URL on the frame
            cv2.putText(img, str(url), (rectanglePoints[0], rectanglePoints[1]), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
        
        # Calculate the center x and y value of the QR code
        centerX = rectanglePoints[0] + (rectanglePoints[2] / 2)
        centerY = rectanglePoints[1] + (rectanglePoints[3] / 2)

        # Convert to integer
        centerX = int(centerX)
        centerY = int(centerY)

        # Uncomment to ensure that calculation of center x and y values are correct
        #cv2.putText(img, "CENTER", (centerX, centerY), cv2.FONT_HERSHEY_COMPLEX_SMALL, 
        #            1, (0, 255, 0), 3)
           
        # The following sequence of if statements determines the location of the QR code on the screen
        # and moves the drone as necessary to bring the QR code to the middle of the screen
        if centerX > 0 and centerX < 320: 
            
            if centerY > 0 and centerY < 240:

                #cv2.imshow("Tello Stream", img)
                drone.rotate_counter_clockwise(15)
                #print(1)

        if centerX > 320 and centerX < 640:

            if centerY > 0 and centerY < 240:

                #cv2.imshow("Tello Stream", img)
                drone.move_up(20)
                #print(2)

        if centerX > 640 and centerX < 960:

            if centerY > 0 and centerY < 240:

                #cv2.imshow("Tello Stream", img)
                drone.rotate_clockwise(15)
                #print(3)

        if centerX > 0 and centerX < 320:

            if centerY > 240 and centerY < 480:

                #cv2.imshow("Tello Stream", img)
                drone.rotate_counter_clockwise(15)
                #print(4)

        if centerX > 320 and centerX < 640:

            if centerY > 240 and centerY < 480:

                #cv2.imshow("Tello Stream", img)
                #print(5)
                pass

        if centerX > 640 and centerX < 960:

            if centerY > 240 and centerY < 480:

                #cv2.imshow("Tello Stream", img)
                drone.rotate_clockwise(15)
                #print(6)

        if centerX > 0 and centerX < 320:

            if centerY > 480 and centerY < 720:

                #cv2.imshow("Tello Stream", img)
                drone.rotate_counter_clockwise(15)
                #print(7)

        if centerX > 320 and centerX < 640:

            if centerY > 480 and centerY < 720:

                #cv2.imshow("Tello Stream", img)
                drone.move_down(20)
                #print(8)
                    

        if centerX > 640 and centerX < 960:

            if centerY > 480 and centerY < 720:

                #cv2.imshow("Tello Stream", img)
                drone.rotate_clockwise(15)
                #print(9)
                
    # Resize the video stream
    cv2.resizeWindow("Tello Stream", 960, 720)

    # Draw a 3x3 grid on the frame
    cv2.line(img, (320, 0), (320, 720), (255, 0, 0), 3)
    cv2.line(img, (640, 0), (640, 720), (255, 0, 0), 3)
    cv2.line(img, (0, 240), (960, 240), (255, 0, 0), 3)
    cv2.line(img, (0, 480), (960, 480), (255, 0, 0), 3)

    # Display the frame to the stream
    cv2.imshow("Tello Stream", img)

    # End the loop if the user enters 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Land the drone if it is in flight
if takeoff == 1:
    drone.land()

# Turn of the stream
drone.streamoff()

# Close the video stream window
cv2.destroyAllWindows()

# Display the QR codes
if len(qrCodes) == 1:

    print(f"The QR code: {qrCodes}")

elif len(qrCodes) == 0:
    
    print("No QR codes found.")

else:

    print(f"The QR codes: {qrCodes}")
