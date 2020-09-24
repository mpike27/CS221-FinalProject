import music21
import random
from Data_Parser import getNotes


"""
clear goal for baseline:

1. make a list of notes along 2 consecutive octaves (the 2 middle octaves
or sum else, or within 1 key)
1b. add "rest" to our list of notes so the thing rests...

2. program something that picks randomly from this set of notes for however
many notes we want baseline song to go for
2b. create stream object and append notes to the stream

DONT NEED: actual midi files/songs yet
"""

NOTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_NOTES = 50
NUM_OCTAVES = 2
START_OCTAVE = 4
SEQUENCE_LEN = 20

# def generateBaselineNotes():
#     midi = music21.converter.parse(FILE_NAME)
#     baseLineNotes = []
#     notes_to_parse = None
#     s = music21.stream.Stream()
#     try: # file has instrument parts
#         s2 = music21.instrument.partitionByInstrument(midi)
#         notes_to_parse = s2.parts[0].recurse()
#     except: # file has notes in a flat structure
#         notes_to_parse = midi.flat.notes
#
#     for element in notes_to_parse:
#         if isinstance(element, music21.note.Note):
#             # baseLineNotes.append(str(element.pitch))
#             baseLineNotes(element.name)
#         elif isinstance(element, music21.chord.Chord):
#             # baseLineNotes.append('.'.join(str(n) for n in element.normalOrder))
#             baseLineNotes('.'.join(n.name for n in element.pitches))
#         s.append(element)
#     # print(baseLineNotes)
#
#     return s
#     # for i in range(START_OCTAVE,START_OCTAVE + NUM_OCTAVES):
#     #     for j in range(len(NOTES)):
#     #         baselineNotes.append(NOTES[j] + str(i))
#     # # baselineNotes.append('R')
#     # return baselineNotes
#
# def main():
#     stream = generateBaselineNotes()
#     # s = music21.stream.Stream()
#     # for i in range(NUM_NOTES):
#     #     note = music21.note.Note(random.choice(baseLineNotes))
#     #     s.append(note)
#     #     # note.show('midi')
#     stream.write('midi', fp='output.mid')
#     # s.show('midi')

    # TODO: try making a distribution and sampling from there?


def main():
    input, output, mapping = getNotes(SEQUENCE_LEN)
    input, output = getNotes(SEQUENCE_LEN)
    print('Input: ' + str(len(input)))
    print('Output: ' + str(len(output)))
    baseline = random.choice(input)
    for i in range(NUM_NOTES - SEQUENCE_LEN):
        baseline.append(random.choice(output))
    print(baseline)

if __name__ == '__main__':
    main()
