"""Config parametrs
"""

DATA_FILENAME = 'data.csv'
DATA_HAS_HEADER = True

PREDICT_NUMBER_OF_STEPS = 3

REPORT_FORMAT_TEXT="""Report
We have made {} observations from tossing a coin: {} of them were tails and {} of \
them were heads. 
The probabilities are {:.2f}% and {:.2f}%, respectively.
Our forecast is that in the next {} observations we will have: {} tail and {} heads."""

SLACKBOT_TOKEN=''
SLACKBOT_CHANNEL_ID=''
