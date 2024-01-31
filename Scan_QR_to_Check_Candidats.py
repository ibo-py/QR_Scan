import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import os

entered_data_file_path = 'entered_data.csv'


# Set to store scanned QR codes
scanned_qr_codes = set()

# DataFrames to store CSV data  # Change this to your desired file path

# Change this to your desired file path,

qr_code_names_df = pd.read_csv('qr_code_names.csv') 
waittime = 900
ih, iw = 500, 640

hs1, hs2 = int(ih*(10/100)) , iw

folder_path = "status"


mylist = os.listdir(folder_path) 



#print(mylist)

overlaylist = []


for im_path in mylist:
    if ".jpg" in im_path:
        print(im_path)
        image = cv2.imread(f"{folder_path}/{im_path}")
        image = cv2.resize(image, (hs2, hs1))
        print(im_path)
        overlaylist.append(image)
        print(im_path)
    else:
        mylist.remove(im_path)
print(mylist)
print(len(mylist), len(overlaylist))



# Check if the file exists and is not empty
if os.path.isfile(entered_data_file_path) and os.path.getsize(entered_data_file_path) > 0:
    # Read the CSV file
    entered_data_df = pd.read_csv(entered_data_file_path)
else:
    # Create an empty DataFrame if the file is empty or doesn't exist
    entered_data_df = pd.DataFrame(columns=['QR_Code_Data', 'Timestamp'])

# Get the initial count of unique entries
initial_entered_count = entered_data_df['QR_Code_Data'].nunique()

# Counter for entered people
entered_count = initial_entered_count

def check_qr_code_in_katilimcilar(qr_data):
    # Check if QR code data is in the katilimcilar.csv
    if qr_data in qr_code_names_df["QR_Code_Names"].values:
        print(f"QR Code Data '{qr_data}' is in the katilimcilar.csv file!")
        return True
    else:
        print(f"QR Code Data '{qr_data}' is NOT in the katilimcilar.csv file.")
        return False

def store_entered_data(qr_data):
    global entered_data_df, entered_count

    # Check if the person is already entered
    if qr_data not in entered_data_df['QR_Code_Data'].values:
        # Create a new row of data
        new_data = {'QR_Code_Data': qr_data, 'Timestamp': pd.to_datetime('now')}

        # Append the new data to the DataFrame
        entered_data_df = pd.concat([entered_data_df, pd.DataFrame([new_data], columns=entered_data_df.columns)], ignore_index=True)

        print(f"Entered Data: {entered_data_df.iloc[-1]}")

        # Save the DataFrame to a CSV file
        entered_data_df.to_csv(entered_data_file_path, index=False)

        entered_count += 1
        print(f"Updated entered_data_df:\n{entered_data_df}")

def draw_border(frame, points, color=(0, 255, 0), thickness=2):
    # Draw border lines around the detected QR code
    cv2.line(frame, tuple(points[0]), tuple(points[1]), color, thickness)
    cv2.line(frame, tuple(points[1]), tuple(points[2]), color, thickness)
    cv2.line(frame, tuple(points[2]), tuple(points[3]), color, thickness)
    cv2.line(frame, tuple(points[3]), tuple(points[0]), color, thickness)

def calculate_brightness(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate the average pixel intensity
    return int(gray.mean())

def scan_qr_code_and_check_in_katilimcilar():
    global entered_count

    # Open the camera (you can specify 0 for the default camera)
    cap = cv2.VideoCapture(0)
    # Set the window size
    cv2.namedWindow("QR Code Scanner", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("QR Code Scanner", iw, ih)  # Adjust the size as needed
    
    current_focus = 0 
    while True:
        # Capture each frame
        header = overlaylist[mylist.index("scan.jpg")]
        entered_data_file_path = 'entered_data.csv'


        # Set to store scanned QR codes
        scanned_qr_codes = set()

        # DataFrames to store CSV data  # Change this to your desired file path

        # Change this to your desired file path,

        qr_code_names_df = pd.read_csv('qr_code_names.csv') 

        # Check if the file exists and is not empty
        if os.path.isfile(entered_data_file_path) and os.path.getsize(entered_data_file_path) > 0:
            # Read the CSV file
            entered_data_df = pd.read_csv(entered_data_file_path)
        else:
            # Create an empty DataFrame if the file is empty or doesn't exist
            entered_data_df = pd.DataFrame(columns=['QR_Code_Data', 'Timestamp'])

        # Get the initial count of unique entries
        initial_entered_count = entered_data_df['QR_Code_Data'].nunique()

        # Counter for entered people
        entered_count = initial_entered_count

        
        _, frame = cap.read()
            # Calculate average brightness
        brightness = calculate_brightness(frame)

        # Adjust the focus based on brightness
        current_focus = max(0, min(255, current_focus + (brightness - 128) // 10))

        # Set the focus property
        cap.set(cv2.CAP_PROP_EXPOSURE, current_focus)
        # Flip the frame horizontally to handle mirrored cameras
        frame = cv2.flip(frame, 1)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use pyzbar to decode QR codes
        decoded_objects = decode(gray)



        # Iterate over all decoded objects
        for i, obj in enumerate(decoded_objects):
            points = obj.polygon
            if len(points) == 4:
                # Draw border lines around the detected QR code
                draw_border(frame, points)

            qr_data = obj.data.decode('utf-8')
            qr_type = obj.type

            # Check if the QR code has been scanned earlier
            if qr_data in scanned_qr_codes:
                print(f"QR Code Data '{qr_data}' has already been scanned.")
                continue

            # Print the QR code data
            print(f"QR Code Type: {qr_type}, Data: {qr_data}")

            # Check if QR code data is in the katilimcilar.csv and not already scanned
            if check_qr_code_in_katilimcilar(qr_data):
                # Check if the person is already entered
                if qr_data not in entered_data_df['QR_Code_Data'].values:
                    # Perform some action if the QR code data is in the entered_data.csv and not entered
                    # Store entered data
                    store_entered_data(qr_data)

                    # Add the QR code data to the set of scanned codes
                    scanned_qr_codes.add(qr_data)

                    # Display validation and approval messages
                    
                    
                    header = overlaylist[mylist.index("can.jpg")]
                    text_size = cv2.getTextSize(qr_data, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                    
                    # Draw a filled rectangle behind the text
                    cv2.rectangle(frame, (20, 150 - text_size[1] - 5 ), (20 + text_size[0] , 150 +5), (94, 241, 67), cv2.FILLED)#rgb(67,241,94)
                    
                    # Write the text on the highlighted background
                    cv2.putText(frame, f"{qr_data}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

                    # cv2.putText(frame, f'can enter.', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    frame[0:hs1, 0:hs2] = header
                    cv2.imshow("QR Code Scanner", frame)

                    # Update the screen (this is crucial for the display to be updated)
                    cv2.waitKey(waittime)
                    continue
                else:
                    header = overlaylist[mylist.index("already.jpg")]
                    text_size = cv2.getTextSize(qr_data, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                    
                    # Draw a filled rectangle behind the text
                    cv2.rectangle(frame, (20, 150 - text_size[1] - 5 ),(20 + text_size[0] , 150 +5), (51, 188, 244), cv2.FILLED)#244,188,51
                    
                    # Write the text on the highlighted background
                    cv2.putText(frame, f"{qr_data}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
                    # cv2.putText(frame, f"{qr_data} is already entered ", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    # cv2.putText(frame, f"at {entered_data_df['Timestamp'][i]}.", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    print(entered_data_df['Timestamp'])
                    frame[0:hs1, 0:hs2] = header
                    cv2.imshow("QR Code Scanner", frame)

                    # Update the screen (this is crucial for the display to be updated)
                    cv2.waitKey(waittime)
            else:
                header = overlaylist[mylist.index("noenter.jpg")]
                # cv2.putText(frame, f'{qr_data}is not valid.', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                frame[0:hs1, 0:hs2] = header
                cv2.imshow("QR Code Scanner", frame)

                # Update the screen (this is crucial for the display to be updated)
                cv2.waitKey(waittime)

        # Display the entered count on the screen
        #cv2.putText(frame, f'Entered: {entered_count}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        # Display the frame
        frame[0:hs1, 0:hs2] = header
        cv2.imshow("QR Code Scanner", frame)
        
        

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    
    cap.release()
    cv2.destroyAllWindows()

# Print the initial count
print(f"Initial Entered Count: {initial_entered_count}")

# Run the QR code scanner and check in katilimcilar.csv
scan_qr_code_and_check_in_katilimcilar()
