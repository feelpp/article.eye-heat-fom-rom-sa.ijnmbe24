import os
import pandas as pd
import sys


def convert_csv_to_kelvin(dir_file):

    files = os.listdir(dir_file)

    keys = ['O', 'A', "B", "B1", "C", "D", "D1", "F", "G"]

    it = iter(files)
    for file in it:
        if file.endswith(".csv"):
            print("Looking for file: ", file)
            file_path = os.path.join(dir_file, file)
            new_file_path = os.path.join(dir_file, os.path.splitext(file)[0] + "_K.csv")
            if os.path.isfile( new_file_path ):
                print("\tfile already converted: ", new_file_path )
            else:
                try:
                    df = pd.read_csv(file_path, sep=',')
                except:
                    print("Error: ", file_path)
                    continue

                toSave = False

                for l in df:
                    if l in keys:
                        toSave = True
                        df[l+'K'] = df[l] + 273.15

                if toSave:
                    print("\tFile saved :", new_file_path)
                    df.to_csv(new_file_path, index=False)

if __name__ == "__main__":
    dir_file = os.path.dirname( __file__ )
    convert_csv_to_kelvin(dir_file)