"""
Author: Eero Rinne

Description (Hayden Mann): Sanity check to see if the original 
radar-running code is working as expected.
"""

import pickle

count = 0
with open("storage/01_03_2026_1/data.pkl", "rb") as f:
    while True:
        try:
            pickle.load(f)
            count += 1
        except EOFError:
            break
        except Exception as e:
            print("Corrupted at frame", count)
            break
print("Total good frames:", count)
