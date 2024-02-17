from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)

class Barangay:
    def __init__(self, name):
        self.name = name
        self.residents = {}

    def add_resident(self, name):
        self.residents[name] = True
        return f"{name} has been added to {self.name}."

    def remove_resident(self, name):
        if name in self.residents:
            del self.residents[name]
            return f"{name} has been removed from {self.name}."
        else:
            return f"{name} is not found in {self.name}."

    def search_resident(self, name):
        if name in self.residents:
            return f"{name} is found in {self.name}."
        else:
            return f"{name} is not found in {self.name}."

    def display_residents(self):
        if self.residents:
            residents_list = [resident for resident in self.residents]
            return residents_list
        else:
            return None


class Municipality:
    def __init__(self, name):
        self.name = name
        self.barangays = {}

    def add_barangay(self, name):
        self.barangays[name] = Barangay(name)
        return f"{name} has been added to {self.name}."

    def remove_barangay(self, name):
        if name in self.barangays:
            del self.barangays[name]
            return f"{name} has been removed from {self.name}."
        else:
            return f"{name} is not found in {self.name}."

    def search_resident(self, name):
        for barangay_name, barangay in self.barangays.items():
            if name in barangay.residents:
                return f"{name} is found in {barangay_name}."
        return f"{name} is not found in any barangays."

    def display_residents(self):
        residents = {}
        for barangay_name, barangay in self.barangays.items():
            residents[barangay_name] = barangay.display_residents() or ["No residents found"]
        return residents

municipality_name = "Clarin Municipality"
municipality = Municipality(municipality_name)

@app.route('/')
def index():
    return render_template('index.html', municipality_name=municipality_name, barangays=municipality.barangays)

@app.route('/add_barangay', methods=['POST'])
def add_barangay():
    name = request.form['name']
    message = municipality.add_barangay(name)
    return redirect(url_for('index'))  # Redirect to index after adding barangay

@app.route('/remove_barangay', methods=['POST'])
def remove_barangay():
    name = request.form['name']
    message = municipality.remove_barangay(name)
    return redirect(url_for('index'))  # Redirect to index after removing barangay

@app.route('/add_resident', methods=['POST'])
def add_resident():
    barangay_name = request.form['barangay']
    name = request.form['name']
    message = municipality.barangays[barangay_name].add_resident(name)
    return redirect(url_for('index'))  # Redirect to index after adding resident

@app.route('/remove_resident', methods=['POST'])
def remove_resident():
    barangay_name = request.form['barangay']
    name = request.form['name']
    message = municipality.barangays[barangay_name].remove_resident(name)
    return redirect(url_for('index'))  # Redirect to index after removing resident

@app.route('/search_resident', methods=['POST'])
def search_resident():
    name = request.form['name']
    message = municipality.search_resident(name)
    return message

@app.route('/display_residents', methods=['GET'])
def display_residents():
    barangay_name = request.args.get('barangay')
    residents = municipality.barangays.get(barangay_name).display_residents()
    return render_template('display_residents.html', barangay_name=barangay_name, residents=residents)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
