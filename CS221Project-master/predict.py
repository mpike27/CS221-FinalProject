from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Activation, Dropout, Dense, Lambda
from tensorflow.keras.layers import BatchNormalization as BatchNorm
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from Data_Parser import getNotes
import numpy
import music21
from Data_Parser import getNotes
import pickle
import random

#CONSTANTS
OUTPUT_DIR = 'final_output_ep100_t7'
WEIGHTS_DIR = 'final_weights_ep100'
SEQUENCE_LEN = 20
LOADED = True  # must change if songs are added to training/testing data
#HYPERPARAMETERS
TEMP = 0.7
LSTM_LAYER_SIZE = 256
DROPOUT_RATE = 0.2
EPOCHS = 50
BATCH_SIZE = 64
N_NEW_NOTES = 200

def main():
    input, output, mapping = getNotes(SEQUENCE_LEN, False, LOADED)  # getNotes(int, bool train, bool loaded)
    test_input = [[mapping[note] for note in sequence] for sequence in input]

    model = rebuild_model(test_input, mapping)
    test_output = [mapping[note]for note in output]
    test_input_np = numpy.reshape(test_input, (len(test_input), len(test_input[0]), 1))
    test_output = to_categorical(test_output, num_classes = len(mapping))
    model.evaluate(test_input_np, test_output, batch_size=BATCH_SIZE)
    makeNotes(model, test_input, mapping)



def rebuild_model(test_input, mapping):
    test_input = numpy.reshape(test_input, (len(test_input), len(test_input[0]), 1))

    #New
    model = Sequential()
    model.add(LSTM(LSTM_LAYER_SIZE,  # num nodes
                   input_shape=(test_input.shape[1], test_input.shape[2]),   # Since this is the first layer, we know dimentions of input
                   return_sequences=True))  # creates recurrence
    model.add(LSTM(LSTM_LAYER_SIZE,
                   return_sequences=True,  # creates recurrence
                   recurrent_dropout=DROPOUT_RATE,))  # fraction to leave out from recurrence

    model.add(LSTM(LSTM_LAYER_SIZE))     # multiple LSTM layers create Deep Neural Network for greater accuracy
    model.add(BatchNorm())               # normalizes inputs to neural network layers to make training faster
    model.add(Dropout(DROPOUT_RATE))     # prevents overfitting
    model.add(Dense(len(mapping)))       # classification layer - output must be same dimentions as mapping
    model.add(Lambda(lambda x: x / TEMP))# adds temperature settings
    model.add(Activation('softmax'))     # transforms output into a probability distribution

    model.compile(loss='categorical_crossentropy', optimizer='adam')
    #load weights
    model.load_weights('%s.hdf5' %WEIGHTS_DIR)

    return model


def makeNotes(model, test_input, mapping):
    start = numpy.random.randint(0, len(test_input)-1)

    int_to_note = dict((mapping[note], note) for note in mapping.keys())
    initial_sequence = test_input[start]
    #output = [] we used this for error checking

    s = music21.stream.Stream()

    for i in range(N_NEW_NOTES):
        prediction_input = numpy.reshape(initial_sequence, (1, len(initial_sequence), 1))

        prediction = model.predict(prediction_input, verbose=0)
        index = numpy.random.choice(numpy.arange(len(prediction[0])), p = prediction[0])  # samples from distribution

        result = int_to_note[index]

        #add the note to output stream
        if "." in result:
            note = music21.chord.Chord(result.split("."))
            #print("created_chord")
        elif (result == 'R'):
            note = music21.note.Rest()
        else:
            note = music21.note.Note(result)
            #print("created_note")
        s.append(note)
        #output.append(result)

        initial_sequence.append(index)
        initial_sequence = initial_sequence[1:len(initial_sequence)]
    s.write('midi', fp="%s.mid" %OUTPUT_DIR)
    #print(output)

if __name__ == '__main__':
    main()
