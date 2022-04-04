"""Config parametrs
"""

import logging

logging.basicConfig(filename = 'analytics.log',
                    filemode = 'w',
                    format = '%(asctime)s %(message)s',
                    level = logging.DEBUG)


DATA_FILENAME = '../data.csv'
DATA_HAS_HEADER = True

PREDICT_NUMBER_OF_STEPS = 3

REPORT_FORMAT_TEXT="""Report
We have made {} observations from tossing a coin: {} of them were tails and {} of \
them were heads. 
The probabilities are {:.2f}% and {:.2f}%, respectively.
Our forecast is that in the next {} observations we will have: {} tail and {} heads."""

SLACKBOT_TOKEN='xoxb-3332818006950-3339553072178-rzPR4il50tj2c5xDLm2bHdHx'
SLACKBOT_CHANNEL_ID='C039SQ31E5C'
