from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

parking_lot = {}
ticketId_counter = 0


def calculate_charge(entry_time):
    """
    Calculates the parking charge based on the entry time.
    """
    exit_time = datetime.now()
    total_time = (exit_time - entry_time).total_seconds() / 60  # calculate total time in minutes and
    # round down to the nearest integer
    periods = (total_time // 15) + 1  # calculate the number of 15-minute periods
    charge = periods * 2.5  # update charge to 2.5 dollars per 15 minutes
    return round(charge, 2)


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    """
    Record the entry time, license plate, and parking lot number.
    Returns a ticket ID.
    """
    global ticketId_counter
    plate = request.args.get('plate')
    parking_lot_id = request.args.get('parkingLot')
    entry_time = datetime.now()
    ticket_id = str(ticketId_counter)
    parking_lot[ticket_id] = {'plate': plate, 'parking_lot_id': parking_lot_id, 'entry_time': entry_time}
    ticketId_counter += 1
    return jsonify({'ticket_id': ticket_id})


@app.route('/exit', methods=['GET', 'POST'])
def exit():
    """
    Record the exit time and calculate the parking charge.
    Returns the license plate, total parked time, parking lot ID, and charge.
    """
    ticket_id = request.args.get('ticketId')
    enter = parking_lot.get(ticket_id)
    if not enter:
        return jsonify({'error': 'Ticket not found'}), 404
    exit_time = datetime.now()
    charge = calculate_charge(enter['entry_time'])
    del parking_lot[ticket_id]
    return jsonify({'plate': enter['plate'], 'total_time': str(exit_time - enter['entry_time']),
                    'parking_lot_id': enter['parking_lot_id'], 'charge': charge})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
