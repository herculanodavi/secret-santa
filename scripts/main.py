from person import Person
import scrambler
import mail
import argparse
import json
import logging


def main(user, password, input_file):
    with open(input_file, 'r') as f:
        j = json.load(f)
        people = [Person.from_json(el) for el in j]
        
    server = mail.DummySender(mail.User(user, password))
    solution = scrambler.solve(people, 'groups', int(1e6))
    for s in solution:
        server.send_mail(s['giver'], s['receiver'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Secret Santa 2022',
        description='Does a Secret Santa shuffle that guarantees people that the giver knows the receiver.')
    
    logging.basicConfig(level=logging.DEBUG)

    parser.add_argument('-user', required=True)
    parser.add_argument('-password', required=True)
    parser.add_argument('-input', required=True)
    args = parser.parse_args()
    print(args.user, args.password, args.input)
    main(args.user, args.password, args.input)
