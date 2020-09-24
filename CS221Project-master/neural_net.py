from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Activation, Dropout, Dense
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from Data_Parser import getNotes
import numpy

#CONSTANTS
WEIGHTS_DIR = 'final_weights_ep50'
SEQUENCE_LEN = 20
LOADED = True # must change if songs are added to training/testing data
#HYPERPARAMETERS
LSTM_LAYER_SIZE = 256
DROPOUT_RATE = 0.2
EPOCHS = 50
BATCH_SIZE = 64


def main():
    input, output, mapping = getNotes(SEQUENCE_LEN, True, LOADED)  # getNotes(int, bool train, bool loaded)
    training_input = [[mapping[note] for note in sequence] for sequence in input]
    training_output = [mapping[note]for note in output]
    training_input = numpy.reshape(training_input, (len(training_input), len(training_input[0]), 1))
    training_output = to_categorical(training_output, num_classes = len(mapping))
    # print(training_input.shape)
    # print(training_output.shape)
    model = Sequential()
    model.add(LSTM(LSTM_LAYER_SIZE,  # num nodes
                   input_shape=(training_input.shape[1], training_input.shape[2]),   # Since this is the first layer, we know dimentions of input
                   return_sequences=True))  # creates recurrence

    model.add(LSTM(LSTM_LAYER_SIZE,
                   return_sequences=True,  # creates recurrence
                   recurrent_dropout= DROPOUT_RATE,))  # fraction to leave out from recurrence

    model.add(LSTM(LSTM_LAYER_SIZE))            # multiple LSTM layers create Deep Neural Network for greater accuracy
    model.add(BatchNorm())          # normalizes inputs to neural network layers to make training faster
    model.add(Dropout(DROPOUT_RATE))         # prevents overfitting
    model.add(Dense(len(mapping)))  # classification layer - output must be same dimentions as mapping
    model.add(Activation('softmax'))# transforms output into a probability distribution

    model.compile(loss='categorical_crossentropy', optimizer='adam')  # try changing optimizer to adam - adpative moment estimation

    #model.summary()
    #TRAINING TIME
    filepath = "%s.hdf5" %WEIGHTS_DIR

    checkpoint = ModelCheckpoint( # used for training loss
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    model_callbacks = [checkpoint]


    model.fit(training_input, training_output, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=model_callbacks)


if __name__ == '__main__':
    main()
