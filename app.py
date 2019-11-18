from flask import Flask, escape, render_template, request
from werkzeug import secure_filename
import csv, os

UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(secure_filename(f.filename))
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        mid = request.form['merchant_id']
        vid = request.form['vanity_id']

        create_sql = csv_reader(mid, vid, f.filename )

    return render_template(
        'result.html',
        sql=create_sql,
        mid=mid,
        vid=vid
    )


def csv_reader(merchant, vanity_config_id, filename ):
    with open('files/' + filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        row_count = sum(1 for rec in read_csv)

    with open('files/' + filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        sql = 'INSERT INTO ip."VanityPricingConfig" ("MerchantId","Currency","Fixed","Round","Charm","Tariff","MerchantFee","ConsumerFee","VanityPricingGroupId") VALUES '
        iterrow = iter(read_csv)
        next(iterrow)
        cnt = 1
        for row in iterrow:
            record = row
            record_value = "(" + merchant + ",'" + row[0] + "'," + "0," + row[1] + "," + str(int(float(row[3]))) + ",0,0,0," + vanity_config_id + ")"
            cnt += 1
            if cnt < row_count:
                sql = sql + record_value + ","
            else:
                sql = sql + record_value + ";"

    return sql


if __name__ == '__main__':
    app.run(host='0.0.0.0')
