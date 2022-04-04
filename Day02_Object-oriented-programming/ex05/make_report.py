#!/usr/local/bin/python3

import config
import analytics

def main():
    """Main function"""
    research = analytics.Research(config.DATA_FILENAME)

    try:
        data = research.file_reader(has_header=config.DATA_HAS_HEADER)
    except Exception as err:
        print(type(err).__name__, err, sep=': ')
        return
    
    handler = analytics.Research.Analytics(data)

    counts = handler.counts()
    fractions = handler.fractions(counts)
    predict_random = handler.predict_random(config.PREDICT_NUMBER_OF_STEPS)

    report = config.REPORT_FORMAT_TEXT.format(sum(counts), counts[1], counts[0],
                                            fractions[1], fractions[0],
                                            config.PREDICT_NUMBER_OF_STEPS,
                                            predict_random.count([1, 0]),
                                            predict_random.count([0, 1]))
    handler.save_file(report, 'report', 'txt')


if __name__ == '__main__':
    main()
