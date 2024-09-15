from flask import Flask, render_template, request, redirect, url_for, flash
from database_manager import DbManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong, unique secret key

dbm = DbManager("fpgas.json", "gunshots.json")

@app.route("/")
def index():
    gunshot = dbm.get_gunshot()
    fpga = dbm.get_fpgas()
    reverse_sorted_gunshot = dict(sorted(gunshot.items(), key=lambda item: int(item[0]), reverse=True))

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

if __name__ == "__main__":
    app.run(port=3000, debug=True)
