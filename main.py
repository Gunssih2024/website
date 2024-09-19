from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_manager import DbManager
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

dbm = DbManager("fpgas.json", "test_gunshots.json")



def get_datetime(item):
    date_str = item['date']
    time_str = item['time']
    datetime_str = f"{date_str} {time_str}"
    return datetime.strptime(datetime_str, "%d-%m-%Y %H:%M:%S")


@app.route("/")
def index():
    gunshot = dbm.get_gunshot()
    fpga = dbm.get_fpgas()
    reverse_sorted_gunshot = dict(sorted(
    gunshot.items(),
    key=lambda item: get_datetime(item[1]),
    reverse=True
    ))
    
    # print(dbm.gunshot_counter())
    # dbm.get_gunshot_specific()
    # print(gunshot,"hasdhfahsdfhasd",reverse_sorted_gunshot, fpga)
    return render_template("index.html", reverse_sorted_gunshot=reverse_sorted_gunshot, fpga=fpga)


@app.route("/settings")
def settings_page():
    fpga = dbm.get_fpgas()
    print(fpga)
    return render_template("settings.html", fpgas=fpga)


@app.route("/save_fpga_settings", methods=['POST'])
def save_fpga_settings():
    fpga_id = request.form['fpga_id']
    name = request.form['name']
    uid = request.form['uid']
    region = request.form['region']
    coordinates = request.form['coordinates']

    # Call the update_fpga method to update FPGA settings

    dbm.update_fpga(fpga_id, name, uid, region, coordinates)

    return redirect(url_for('settings_page'))


@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        uid = request.form.get('uid')
        region = request.form.get('region')
        coordinates = request.form.get('coordinates')
        
        # Add the FPGA with the additional fields
        response_add_fpga = dbm.add_fpga(name, uid, region, coordinates)
        
        if response_add_fpga == "error":
            flash('There was an Unknown error.', 'error')
        else:
            flash(f'Successfully added new FPGA with ID: {response_add_fpga}.', 'success')

        # Redirect to the same page or another page after submission
        return redirect(url_for('add_new'))
    
    # Handle GET request: Render the form page
    return render_template('add_new.html')


@app.route('/data', methods=['GET'])
def get_data():

    data = dbm.get_gunshot_specific_elevation()
    return jsonify(data)

@app.route('/gundata', methods=['GET'])
def gun_data():

    data = dbm.gunshot_counter()
    print(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=3000, debug=True)
