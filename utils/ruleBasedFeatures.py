import pandas as pd
import nltk
from IPython.core import debugger
breakpoint = debugger.set_trace



def prevWordIsThe(row):
    return 'the' in str(row['prev4']).lower() 


def prevStrIsInThe(row):
    prev_str = str(row['prev3']) + ' ' + str(row['prev4'])
    return 'in the' in prev_str.lower() 


# df = pd.read_pickle('../Data/data_window_ngram-5.pkl')

# row = df.iloc[0]
# print(row)

# pos_counts = posCounts(row)
# print(pos_counts)
# pos_counts_ngram = posCountsNGram(row, ngram=6)
# print(pos_counts_ngram)

