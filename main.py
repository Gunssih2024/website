from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_manager import DbManager
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, unique secret key

dbm = DbManager("fpgas.json", "test_gunshots.json")
# dbm = DbManager("fpgas.json", "gunshots.json")


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

    dbm.get_gunshot_specific()
    # print(gunshot,"hasdhfahsdfhasd",reverse_sorted_gunshot, fpga)
    return render_template("index.html", reverse_sorted_gunshot=reverse_sorted_gunshot, fpga=fpga)




@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    # print(dbm.add_gunshot("100004", 100, 39))
    # print(dbm.add_gunshot("100004", 80, 135))
    # print(dbm.add_gunshot("100004", 0, 45))
    # print(dbm.add_gunshot("100005", 55, 90))
    # print(dbm.add_gunshot("100005", 27, 192))
    # print(dbm.get_gunshot("100003"))
    if request.method == 'POST':
        # Handle form submission

        
        name = request.form.get('name')
        response_add_fpga = dbm.add_fpga(name)
        if response_add_fpga == "error":
            flash('There was an Unknown error.', 'error')
        else:
            flash(f'Successfully added new FPGA with ID: {response_add_fpga}.', 'success')

        # Create an instance of FPGAHandler and add the new FPGA
        # dbm.add_fpga(name)
        # Redirect to the same page or another page after submission
        return redirect(url_for('add_new'))
    
    # Handle GET request: Render the form page
    return render_template('add_new.html')






data = {
    "dates":
    {
        "today":
        {
            "total": 102831,
            "upDown": 2.2,
            "data": {
    'labels': ['12am', '01am', '02am', '03am', '04am', '05am', '06am', '07am', '08am', '09am', '10am', '11am', '12pm', '01pm', '02pm', '03pm', '04pm', '05pm', '06pm', '07pm', '08pm', '09pm', '10pm', '11pm'],
    '100001': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    '100002': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0],
    '100003': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 0, 0],
    '100004': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0],
    '100005': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0],
    '100006': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    '100007': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
        },
        "7days":
        {
            "total": 213180,
            "upDown": 1,
            "data": {
                "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "income": [33120, 31578, 31549, 26435, 26307, 33391, 30800],
                "expenses": [12254, 12947, 4417, 7137, 12364, 3339, 11704]
            }
        },
        "30days":
        {
            "total": 3982743,
            "upDown": 1.3,
            "data": {'labels': ['18-08-2024', '19-08-2024', '20-08-2024', '21-08-2024', '22-08-2024', '23-08-2024', '24-08-2024', '25-08-2024', '26-08-2024', '27-08-2024', '28-08-2024', '29-08-2024', '30-08-2024', '31-08-2024', '01-09-2024', '02-09-2024', '03-09-2024', '04-09-2024', '05-09-2024', '06-09-2024', '07-09-2024', '08-09-2024', '09-09-2024', '10-09-2024', '11-09-2024', '12-09-2024', '13-09-2024', '14-09-2024', '15-09-2024', '16-09-2024'], '100001': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0], '100002': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 75, 0], '100003': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0], '100004': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 180, 0], '100005': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 82, 0], '100006': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], '100007': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}  
        },
        "6months":
        {
            "total": 790546,
            "upDown": -1,
            "data": {
                "labels": ["Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                "income": [129086, 114855, 138390, 141537, 122422, 144256],
                "expenses": [28399, 51685, 65043, 50953, 23260, 28851]
            }
        },
        "year":
        {
            "total": 1586266,
            "upDown": 9.8,
            "data": {
                "labels": ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                "income": [119081, 122160, 146259, 147543, 116608, 141801, 137770, 125591, 146268, 114010, 136872, 132303],
                "expenses": [51205, 42756, 42415, 29509, 54806, 55302, 66130, 38933, 17552, 49024, 26006, 64828]
            }
        }
    }
}




# data = {
#     'labels': ['12am', '01am', '02am', '03am', '04am', '05am', '06am', '07am', '08am', '09am', '10am', '11am', '12pm', '01pm', '02pm', '03pm', '04pm', '05pm', '06pm', '07pm', '08pm', '09pm', '10pm', '11pm'],
#     '100001': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     '100002': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0],
#     '100003': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 0, 0],
#     '100004': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0],
#     '100005': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0],
#     '100006': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     '100007': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# }

@app.route('/data', methods=['GET'])
def get_data():
    data = dbm.get_gunshot_specific()
    return jsonify(data)



if __name__ == "__main__":
    app.run(port=3000, debug=True)
