from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from PyPDF2 import PdfReader, PdfWriter
from datetime import date
import os
import threading
import time

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
		if request.method == 'POST':
			name = request.form['name']
			business = request.form['business']
			classification = request.form['classification']
			individual = "/Off"
			ccorp = "/Off"
			scorp = "/Off"
			partnership = "/Off"
			trust = "/Off"
			llc = "/Off"
			otherfield = "/Off"
			other = ""
			tax = ""
			if classification == '0':
				individual = "/Yes"
			elif classification == '1':
				ccorp = "/Yes"
			elif classification == '2':
				scorp = "/Yes"
			elif classification == '3':
				partnership = "/Yes"
			elif classification == '4':
				trust = "/Yes"
			elif classification == '5':
				llc = "/Yes"
				tax = request.form['tax']
			elif classification == '6':
				otherfield = "/Yes"
				other = request.form['other']
			exempt = request.form['exempt']
			fatca = request.form['fatca']
			address = request.form['address']
			city = request.form['city']
			account = request.form['account']
			requester = request.form['requester']
			tin = request.form['tin']
			if tin == '0':
				ssn1 = request.form['ssn1']
				ssn2 = request.form['ssn2']
				ssn3 = request.form['ssn3']
				ein1 = ""
				ein2 = ""
			else:
				ein1 = request.form['ein1']
				ein2 = request.form['ein2']
				ssn1 = ""
				ssn2 = ""
				ssn3 = ""
			signature = request.form['signature']
			today = date.today()
			
			reader = PdfReader("fw9sig.pdf")
			writer = PdfWriter()
			
			page = reader.pages[0]
			writer.add_page(page)
			
			writer.update_page_form_field_values(
			    writer.pages[0], {
						"f1_1": name, 
						"f1_2": business,
						"c1_1_val1": individual, ##Individual
						"c1_1_val2": ccorp, ##C Corporation
						"c1_1_val3": scorp, ##S Corporation
						"c1_1_val4": partnership, ##Partnership
						"c1_1_val5": trust, ##Trust
						"c1_1_val6": llc, ##LLC
						"f1_3": tax,
						"c1_1_val7": otherfield,
						"f1_4": other,
						"FederalClassification[0]": "Unknown",
						"f1_5": exempt,
						"f1_6": fatca,
						"Exemptions[0]": exempt,
						"f1_7": address,
						"f1_8": city,
						"f1_9": requester,
						"f1_10": account,
						"f1_11": ssn1, ##SSN
						"f1_12": ssn2, ##SSN
						"f1_13": ssn3, ##SSN
						"f1_14": ein1, ##EIN
						"f1_15": ein2, ##EIN
						"EmployerID[0]": "Employer",
						"Page1[0]": "Page",
						"topmostSubform[0]": "Top Form",
						"signature": signature,
						"date": today
					}
			)
	
			file = name + "-w9.pdf"
			#write "output" to PyPDF2-output.pdf
			with open(file, "wb") as output_stream:
			  writer.write(output_stream)
			def long_running_task(**kwargs):
				time.sleep(2)
				os.remove(file)
			thread = threading.Thread(target=long_running_task)
			thread.start()
			return send_file(file, as_attachment=True)
		return render_template('index.html')


app.run(host='0.0.0.0', port=81, debug=True)
