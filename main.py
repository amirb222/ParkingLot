from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

parking_lot = {}


def calculate_charge(entry_time):
    exit_time = datetime.now()
    parked_time = exit_time - entry_time
    parked_hours = parked_time.total_seconds() / 3600
    charged_hours = int(parked_hours) + 1 if parked_hours % 1 > 0 else int(parked_hours)
    charge = charged_hours * 10
    return charge


@app.route('/entry', methods=['POST'])
def entry():
    plate = request.args.get('plate')
    parking_lot_id = request.args.get('parkingLot')
    entry_time = datetime.now()

    ticket_id = len(parking_lot) + 1
    parking_lot[ticket_id] = {'plate': plate, 'entry_time': entry_time, 'parking_lot_id': parking_lot_id}

    return jsonify({'ticketId': ticket_id}), 200


@app.route('/exit', methods=['POST'])
def exit():
    ticket_id = int(request.args.get('ticketId'))

    if ticket_id in parking_lot:
        ticket = parking_lot[ticket_id]
        entry_time = ticket['entry_time']
        charge = calculate_charge(entry_time)

        response = {
            'licensePlate': ticket['plate'],
            'parkedTime': str(datetime.now() - entry_time),
            'parkingLotId': ticket['parking_lot_id'],
            'charge': charge
        }

        del parking_lot[ticket_id]

        return jsonify(response), 200
    else:
        return jsonify({'error': 'Invalid ticketId'}), 404


if __name__ == '__main__':
    app.run()

