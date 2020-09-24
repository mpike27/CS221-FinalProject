import music21
import os
import pickle

training_dir = 'CS221_Training_Data'
testing_dir = 'CS221_Testing_Data'

'''Function takes in a music21.note object and parses it into its string form'''
def convertToString(elem):
    if isinstance(elem, music21.note.Note):
        #print(elem.nameWithOctave)
        return elem.nameWithOctave
    elif isinstance(elem, music21.chord.Chord):
        return '.'.join(n.name for n in elem.pitches)
    return 'R'

'''Function parses songs in training and testing data in midi form to training
   and testing inputs and outputs.'''
def extractSequences(dir, unique_notes, maxlen):
    print("Parsing ", dir)
    inputs = []
    outputs = []
    song_count = 0
    song_list = os.listdir(dir)
    for song in song_list:
        print("%d / %d" %(song_count, len(song_list)))
        song_count += 1
        print("Parsing %s..." %(str(song)))
        try:
            midi = music21.converter.parse(dir + '/' + song)
            raw_notes = None
            try:
                s2 = music21.instrument.partitionByInstrument(midi)
                raw_notes = s2.parts[0].recurse()  # Selects first instrument from every file
            except:
                raw_notes = midi.flat.notes
            for i in range(len(raw_notes) - maxlen - 1):
                sequence = []
                for j in range(i, i + maxlen):
                    note = convertToString(raw_notes[j])
                    if note not in unique_notes:
                        unique_notes.append(note)
                    sequence.append(note)
                inputs.append(sequence)
                output = convertToString(raw_notes[i + maxlen + 1])
                if output not in unique_notes:
                    unique_notes.append(output)
                outputs.append(output)
        except:
            continue
    return inputs, outputs

def getNotes(maxlen, train, loaded):
    print('Parsing...')
    if loaded:
        with open('Data_Note_OBJECT_Parsing/mapping', 'rb') as filepath:
            mapping = pickle.load(filepath)
        with open('Data_Note_OBJECT_Parsing/training_input', 'rb') as filepath:
            training_input = pickle.load(filepath)
        with open('Data_Note_OBJECT_Parsing/training_output', 'rb') as filepath:
            training_output = pickle.load(filepath)
        with open('Data_Note_OBJECT_Parsing/testing_input', 'rb') as filepath:
            testing_input = pickle.load(filepath)
        with open('Data_Note_OBJECT_Parsing/testing_output', 'rb') as filepath:
            testing_output = pickle.load(filepath)
    else:
        unique_notes =[]
        training_input, training_output = extractSequences(training_dir, unique_notes, maxlen)
        testing_input, testing_output = extractSequences(testing_dir, unique_notes, maxlen)
        mapping = {note: num for num, note in enumerate(unique_notes)}

        with open('Data_Note_OBJECT_Parsing/training_input', 'wb') as filepath:
            pickle.dump(training_input, filepath)
        with open('Data_Note_OBJECT_Parsing/training_output', 'wb') as filepath:
            pickle.dump(training_output, filepath)
        with open('Data_Note_OBJECT_Parsing/testing_input', 'wb') as filepath:
            pickle.dump(testing_input, filepath)
        with open('Data_Note_OBJECT_Parsing/testing_output', 'wb') as filepath:
            pickle.dump(testing_output, filepath)
        with open('Data_Note_OBJECT_Parsing/mapping', 'wb') as filepath:
            pickle.dump(mapping, filepath)


    if train:
        return training_input, training_output, mapping
    return testing_input, testing_output, mapping
