from datetime import datetime

from flask import Flask, render_template, request

from models.bookingDemand import BookingDemand
from models.room import Room
from models.team import Team

app = Flask(__name__)

ROOMS = {
    803: Room(True, True, 65),
    601: Room(True, True, 34),
    315: Room(False, True, 20)
}

TEAMS = {
    17: Team([803, 315]),
    18: Team([601, 803]),
    19: Team([315, 803]),
    20: Team([601, 803])
}


# APIs

@app.route('/api/booking-demand', methods=['POST'])
def add_booking_demand():
    payload = dict(request.get_json())
    team_id = int(payload['team_id'])
    if team_id not in TEAMS.keys():
        TEAMS[team_id] = Team([])

    demand_status = TEAMS[team_id].demand_booking(BookingDemand(
        datetime.strptime(payload['start_time'], "%Y-%m-%d %H:%M"),
        datetime.strptime(payload['end_time'], "%Y-%m-%d %H:%M"),
        payload['need_projector']
    ))
    if demand_status:
        status_code = 204
        message = "Booking demand was stores successfully."
    else:
        status_code = 304
        message = "It seems that the demand is invalid or it overlaps other demand."

    return {'status': demand_status, 'msg': message}, status_code


@app.route('/api/booking-demand', methods=['DELETE'])
def delete_booking_demand():
    payload = dict(request.get_json())
    team_id = int(payload['team_id'])
    if team_id not in TEAMS.keys():
        return {"status": "The team does not exist."}, 301

    return {"status": "Not working yet"}, 220


@app.route('/api/preferred-rooms/<team_id>', methods=['PUT'])
def update_team_preferred_rooms(team_id):
    if team_id not in TEAMS.keys():
        pass


@app.route("/results", methods=['GET'])
def calculate_api():
    for priority_index in range(10):
        for team_id, t in TEAMS.items():
            if len(t.preferred_rooms) > priority_index:
                for br in t.booking_remands:
                    ROOMS[t.preferred_rooms[priority_index]].book(br, team_id)

    # Random section
    for r in ROOMS.values():
        for id, t in TEAMS.items():
            for br in t.booking_remands:
                r.book(br, id)

    main_schedule = list()

    # Debug section
    for room_id, r in ROOMS.items():
        print('---')
        print(room_id)
        for bd, team_id in r.schedule:
            main_schedule.append((team_id,
                                  room_id,
                                  datetime.strftime(bd.start_time, '%d/%m/%Y'),
                                  datetime.strftime(bd.start_time, '%H:%M'),
                                  datetime.strftime(bd.start_time, '%H:%M')))

    return render_template('result.html', schedule=main_schedule)


# UIs

@app.route("/", methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/booking-demand/', methods=['GET'])
def booking_demand_ui():
    return render_template('booking_demand.html')


@app.route('/booking-demands/', methods=['GET'])
@app.route('/booking-demands/<team_id>', methods=['GET'])
def team_booking_demand(team_id=None):
    if team_id:
        try:
            int_team_id = int(team_id)
        except TypeError as e:
            return f"Error in team ID, it's not an int. ERROR: {e}", 301

        if int_team_id in TEAMS.keys():
            return render_template("demands.html", team_id=int_team_id, wishes=TEAMS[int_team_id].booking_remands,
                                   )
        else:
            return render_template("demands.html", team_id=int_team_id, wishes=[])
    else:
        return render_template("demands.html", team_id=None, wishes=[])


@app.route("/calculate", methods=['GET'])
def calculate():
    return render_template('calculate.html')


if __name__ == '__main__':
    import os

    os.environ['PORT'] = '5000'
    app.run(host='0.0.0.0')
