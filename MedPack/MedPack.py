from flask import Flask, flash, redirect, render_template, \
     request, url_for
import requests
import json

app = Flask(__name__)
app.debug = True


#Getting current list of pharm classes
pharm_response = requests.get('https://api.fda.gov/drug/ndc.json?count=pharm_class.exact')
pharm_output = json.loads(pharm_response.content.decode('utf-8'))
pharm_class = [x['term'] for x in pharm_output['results']]
pharm_class.sort()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        data=pharm_class)

@app.route("/test" , methods=['GET', 'POST'])
def test():
    search = request.form.get('comp_select')
    base_url = 'https://api.fda.gov/drug/ndc.json?search=pharm_class.exact:"'
    limit = '"&limit=100&skip='
    query = base_url+search+limit
    response = requests.get(query)
    output = json.loads(response.content.decode('utf-8'))
    skip = 0

    flatten = lambda l: [item for sublist in l for item in sublist]

    results = []

    while skip <= output['meta']['results']['total'] and skip <= 5000:
        query = base_url+search+limit+str(skip)
        response = requests.get(query)
        output = json.loads(response.content.decode('utf-8'))
        results.append(list(set(flatten([[x['brand_name'],x['generic_name']] if ('brand_name' and 'generic_name' in output['results']) else [x['brand_name']] if ('brand_name' in output['results']) else [x['generic_name']] for x in output['results']]))))
        skip = skip + 100

    results = list(set(flatten(results)))
    results.sort()
    return str([x.upper() for x in results])

if __name__=='__main__':
    app.run(debug=True)