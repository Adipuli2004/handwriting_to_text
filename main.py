import serial
import sys
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Provide the path to the directory containing the saved model
model_path = 'model_1.h5'

# Load the model
loaded_model = tf.keras.models.load_model(model_path)

max_length = 415

# Now you can use the loaded_model for prediction or further training
index_to_char = {i: chr(ord('a') + i) for i in range(26)}

# Create a MinMaxScaler object (you can replace this with the scaler you used during training)
scaler = MinMaxScaler()

def predict_data(data):
    # Pad sequences
    padded_sequences = pad_sequences(data, maxlen=max_length, padding='post', dtype='float32')

    # Make predictions
    predictions = loaded_model.predict(padded_sequences)
    return predictions

# Function to convert predictions to characters
def predictions_to_characters(predictions):
    # Get the index of the maximum predicted value
    max_index = np.argmax(predictions)

    # Map the index to a character using the index_to_char dictionary
    character = index_to_char[max_index]
    return character

try:
    # Configure serial port
    ser = serial.Serial('COM14', 9600)  # Change 'COM14' to your Arduino's serial port
    all_data = []  # List to hold all the rows of data

    while True:
        # Read data from serial port
        data = ser.readline().decode().strip()

        # Split the received data
        split_data = data.split('\t')

        # Check if split_data contains valid values
        if all(value != '' for value in split_data):
            try:
                # Convert each value to float and append to the row data list
                row_data = [float(value) for value in split_data]
                # Append the row data to the list of all rows
                all_data.append(row_data)
                print(all_data)

            except ValueError:
                print("Received invalid data:", split_data)
                if len(all_data) > 0:
                    break

    if len(all_data) > 0:
        print(all_data)
        # Make predictions
        predictions = predict_data([all_data])
        predicted_character = predictions_to_characters(predictions)
        print("Predicted character:", predicted_character)

except serial.SerialException as e:
    print("Serial port error:", e)
    sys.exit(1)
except KeyboardInterrupt:
    if 'ser' in locals():
        ser.close()
