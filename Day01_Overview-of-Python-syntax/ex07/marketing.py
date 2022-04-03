#!/usr/local/bin/python3

import sys

######################
#   Subject's data   #
######################

def get_subjects_data() -> list:
    """Get prepared by subject dictionary of counters and codes

    Returns:
        dict[str, str]: dictionary with `contry: code` pairs
    """
    # basic lists
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com', 'john@snow.is',
               'bill_gates@live.com', 'mark@facebook.com', 'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru', 'pinkman@yo.org',
                    'jessica@gmail.com', 'elon@paypal.com', 'pinkman@yo.org', 'mr@robot.gov',
                    'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    # return sets
    return set(clients), set(participants), set(recipients)



######################
#   Subject's data   #
######################

def call_center_request(clients: set, recipients: set) -> list:
    """Returns clients that are not recipients of emails.
    They will be called by the call center.
    """
    return list(clients - recipients)


def potential_clients_request(clients: set, participants: set) -> list:
    """Returns participants of the most recent event
    that are not clients yet
    """
    return list(participants - clients)


def loyalty_program_request(clients: set, participants: set) -> list:
    """Returns clients that are not participants of the most recent event.
    They will receive link to the video.
    """
    return list(clients - participants)


def interactive_request_handler(task: str) -> None:
    """Handle one task and print the result to stdout
    """
    clients, participants, recipients = get_subjects_data()

    if task == 'call_center':
        print(call_center_request(clients, recipients))
    elif task == 'potential_clients':
        print(potential_clients_request(clients, participants))
    elif task == 'loyalty_program':
        print(loyalty_program_request(clients, participants))
    else:
        raise ValueError('Invalid argument: argument must be one of: ' +
                            '["call_center", "potential_clients", "loyalty_program"]')



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    if len(sys.argv) == 2:
        interactive_request_handler(sys.argv[1])


if __name__ == '__main__':
    main()
