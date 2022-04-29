import os
def generate_negative_description_file():
    #open output file for writing. will overwrite all existing data in there

    with open('neg.txt', 'w') as f:

        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')