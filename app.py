import os
from datetime import datetime

from flask import Flask, render_template, request, send_from_directory

from models.bookingDemand import BookingDemand
from models.room import Room
from models.team import Team

app = Flask(__name__)

ROOMS = {
}

TEAMS = {
}


# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


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
        for bd, team_id in r.schedule:
            main_schedule.append((team_id,
                                  room_id,
                                  datetime.strftime(bd.start_time, '%d/%m/%Y'),
                                  datetime.strftime(bd.start_time, '%H:%M'),
                                  datetime.strftime(bd.end_time, '%H:%M')))

    return render_template('result.html', schedule=main_schedule)


@app.route('/api/teams', methods=['POST'])
def add_team():
    payload = dict(request.get_json())
    try:
        team_id = int(payload['team_id'])
    except ValueError as e:
        return {"Status": f"Team ID ({payload['team_id']}) is not a number.", "error": e}, 501

    if team_id not in TEAMS.keys():
        preferred_rooms = list()
        for i in range(4):
            preferred = payload['favorite_' + str(i)]
            if preferred and (preferred not in preferred_rooms):
                preferred_rooms.append(preferred)

        TEAMS[int(team_id)] = Team(preferred_rooms)
        return {"status": f"Team '{team_id}' was add successfully."}, 204
    else:
        return {"status": f"Team '{team_id}' already exists."}, 305


@app.route('/api/teams/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    try:
        if int(team_id) in TEAMS.keys():
            TEAMS.pop(int(team_id))
            return {"status": f"Team '{team_id}' was deleted successfully."}, 202
        else:
            return {"status": f"Team '{team_id}' does not exist."}, 304
    except ValueError as e:
        return {"status": f"Team ID '{team_id}' is invalid because it's not a number.", "error": e}, 501


@app.route('/api/rooms', methods=['POST'])
def add_room():
    payload = dict(request.get_json())
    try:
        room_id = int(payload['room_id'])
    except ValueError as e:
        return {"status": f"RoomID ('{payload['room_id']}') is invalid because it's not a number.", "error": e}, 501

    if room_id not in ROOMS.keys():
        try:
            ROOMS[int(room_id)] = Room(bool(payload['has_projector']), bool(payload['has_board']),
                                       int(payload['chairs_num']))
        except ValueError as e:
            return {"Status": f"Details are invalid.", "error": e}, 500

        return {"status": f"Room '{room_id}' was add successfully."}, 204
    else:
        return {"status": f"Room '{room_id}' already exists."}, 305


@app.route('/api/rooms/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    try:
        if int(room_id) in ROOMS.keys():
            ROOMS.pop(int(room_id))
            return {"status": f"Team '{room_id}' was deleted successfully."}, 202
        else:
            return {"status": f"Team '{room_id}' does not exist."}, 304
    except ValueError as e:
        return {"status": f"Room ID '{room_id}' is invalid because it's not a number.", "error": e}, 501


@app.route("/api/validate-password", methods=['POST'])
def validate_password():
    payload = dict(request.get_json())
    if 'PASSWORD' in os.environ.keys() and payload['PASSWORD'] == os.environ['PASSWORD']:
        return {"status": 'true'}, 200
    return {"status": 'false'}, 400


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
        except ValueError as e:
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


@app.route('/teams')
def all_teams():
    return render_template('all_teams.html', teams=TEAMS)


@app.route('/rooms')
def all_rooms():
    return render_template('all_rooms.html', rooms=ROOMS)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
