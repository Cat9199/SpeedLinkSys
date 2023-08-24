from flask import Flask, redirect, url_for, request, send_file,jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
import random
import string
import pytz
from datetime import datetime
import requests
from pyzbar.pyzbar import decode
from datetime import datetime
from barcode_extractor import extract_barcode_data
import pytz


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speedlink.db'
app.config['UPLOAD_FOLDER'] = 'img/barcode' 
app.secret_key = 'speedlink'
db = SQLAlchemy(app)

class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    position = db.Column(db.String(100))

class Shippers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone1 = db.Column(db.String(11))
    phone2 = db.Column(db.String(11))
    city = db.Column(db.String(15))
    address = db.Column(db.String(300))
    wallet_code = db.Column(db.String(15), unique=True)
    dues = db.Column(db.Integer)
    shipments = db.Column(db.Integer)

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    

class AppLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    action = db.Column(db.String(100))
    created_at = db.Column(db.String(23))

class Wallets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_code = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(100))
    Shipper_id = db.Column(db.Integer)
    dues = db.Column(db.Integer)

class WalletsLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_code = db.Column(db.String(15))
    name = db.Column(db.String(100))
    Shipment_barcode = db.Column(db.String(15))
    amount = db.Column(db.Integer)
    created_at = db.Column(db.String(23))

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(15))
    shipper_username = db.Column(db.Integer)
    status = db.Column(db.String(50))
    delivery_id = db.Column(db.Integer)
    shipper_name = db.Column(db.String(100))
    shipper_phone_1 = db.Column(db.String(11))
    shipper_phone_2 = db.Column(db.String(11))
    shipper_address = db.Column(db.String(200))
    shipper_city = db.Column(db.String(100))
    shipper_wallet_code = db.Column(db.String(15))
    shipper_note = db.Column(db.Text)
    recipient_name = db.Column(db.String(100))
    recipient_phone_1 = db.Column(db.String(15))
    recipient_phone_2 = db.Column(db.String(15))
    recipient_address = db.Column(db.String(200))
    recipient_city = db.Column(db.String(100))
    recipient_note = db.Column(db.Text)
    pprice = db.Column(db.Integer)
    dprice = db.Column(db.Integer)
    tprice = db.Column(db.Integer)
    province = db.Column(db.String(100))
    date = db.Column(db.String(23))

class ShippingDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(15))
    shipment_id = db.Column(db.Integer)
    delivery_id = db.Column(db.Integer)
    state = db.Column(db.String(100))
    created_at = db.Column(db.String(23))

def generate_unique_code(length=15):
    characters = string.ascii_letters + string.digits
    unique_code = ''.join(random.choice(characters) for _ in range(length))
    return unique_code

def barcode_generator(n=15):
    random_numbers = [str(random.randint(0, 9)) for _ in range(n)]
    return "".join(random_numbers)
def get_current_time():
    url = "http://worldclockapi.com/api/json/utc/now"
    response = requests.get(url)
 
    if response.status_code == 200:
        data = response.json()
        utc_time = data['currentDateTime']
        utc_datetime = datetime.strptime(utc_time, '%Y-%m-%dT%H:%MZ')
        
        # Convert UTC time to Egypt timezone
        egypt_timezone = pytz.timezone('Africa/Cairo')
        egypt_time = utc_datetime.replace(tzinfo=pytz.utc).astimezone(egypt_timezone)
        
        egypt_time_str = egypt_time.strftime('%Y-%m-%d %H:%M:%S')
        return egypt_time_str
    else:
        return "Error fetching time data."


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/track/<int:barcode>')
def track(barcode):
    info = Shipment.query.filter_by(barcode=barcode).first()
    Detail = ShippingDetail.query.filter_by(barcode=barcode).all()
    Detail = Detail[::-1]
    return render_template('product.html',info=info,D=Detail)
@app.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        loginAdmin = Admins.query.filter_by(username=username, password=password).first()
        loginShipper = Shippers.query.filter_by(username=username, password=password).first()
        loginDelivery = Delivery.query.filter_by(username=username, password=password).first()
        
        if loginAdmin:
            session['user_type'] = 'admin'
            session['username'] = username
            return redirect('/dashboard')
        elif loginShipper:
            session['user_type'] = 'shipper'
            session['username'] = username
            return redirect('/dashboard')
        elif loginDelivery:
            session['user_type'] = 'delivery'
            session['username'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', mess='loginError')
    return render_template('login.html')
@app.route('/logout')
def logout():
    # جعل السيشنس فارغة
    session['user_type'] = None
    session['username'] = None
    # يمكنك أيضًا استخدام session.clear() لجعل جميع المتغيرات في السيشن فارغة

    return redirect('/login')
@app.route('/dashboard')
def dashboard():
    user_type = session.get('user_type')
    username = session.get('username')
    
    if user_type == 'admin':
        shinfo = Shipment.query.filter_by(shipper_username=username).all()
        return render_template('dashboard.html', paget= 'مرحبا بك في لوحة التحكم',user_type=user_type, username=username,infoL=shinfo)
    elif user_type == 'shipper':
         
        shinfo = Shipment.query.filter_by(shipper_username=username).all()
        shipper = Shippers.query.filter_by(username=username).first()
        return render_template('dashboard.html',  paget= 'مرحبا بك في لوحة التحكم',user_type=user_type, username=username,infoS=shipper,infoL=shinfo)
    elif user_type == 'delivery':
        return render_template('delivery-dashboard.html', user_type=user_type, username=username)
    else:
        return redirect('/login')
    
    return render_template('dashboard.html', user_type=user_type, username=username)
@app.route('/adds')
def adds():
    return render_template("adds.html",paget='اضافت حساب شاحن')
@app.route('/addd')
def addd():
    return render_template("addd.html",paget='اضافت حساب موصل')
@app.route('/addushipment')
def addushipment():
    return render_template('addushipment.html')
@app.route('/addfile')
def addfile():
    return render_template('addfile.html')
@app.route('/viweshipping')
def viweshipping():
    s = Shipment.query.filter_by(status='New Add').all()
    return render_template('allshipments.html',allS=s)
@app.route('/viwewallets/<wallet_code>')
def viwewallets(wallet_code):
    shipper = Shippers.query.filter_by(wallet_code=wallet_code).first()
    wallet = Wallets.query.filter_by(wallet_code=wallet_code).first()
    wallet_log = WalletsLog.query.filter_by(wallet_code=wallet_code).all()
    wallet_log = wallet_log[::-1]
    return render_template('wallet.html',infoS=shipper,infoW=wallet,infoL=wallet_log)
@app.route('/notifications')
def notifications():
    return 'this is notifications page'
@app.route('/extract_barcode', methods=['POST'])
def extract_barcode():
    if 'image' in request.files:
        image = request.files['image']
        barcode_data = extract_barcode_data(image)
        if barcode_data != "No barcode found.":
            global barcodeFound
            barcodeFound = True
        return barcode_data
    return "Error: No image provided."
@app.route('/changstates/<int:barcode>', methods=['POST'])
def changstates(barcode):
    if request.method == 'POST':
        shipment_status = request.form['shipment_status']
        s = Shipment.query.filter_by(barcode=barcode).first()
        if s:
            u = Shippers.query.filter_by(username=s.shipper_username).first()
            w = Wallets.query.filter_by(wallet_code=u.wallet_code).first()

            new_ac = ShippingDetail(
                barcode=barcode,
                state=shipment_status,
                created_at='19291329    '  
            )

            s.province = shipment_status

            if shipment_status == 'تم توصيل الشحنة':
                u.dues = int(u.dues) + int(s.pprice)
                w.dues = int(w.dues) + int(s.pprice)

                new_wl = WalletsLog(
                    wallet_code=w.wallet_code,
                    name=u.name,
                    Shipment_barcode=s.barcode,
                    amount=int(s.pprice),
                    created_at='39824'
                )

                s.status = 'archiv'

                # أضف وحدة الحالة الجديدة إلى قاعدة البيانات
                db.session.add(new_ac)

                # أضف وحدة تحديث الشحنة إلى قاعدة البيانات
                db.session.add(s)

                # أضف وحدة السجل الجديد للمحفظة إلى قاعدة البيانات
                db.session.add(new_wl)
                db.session.commit()
            
                return redirect(f'/track/{barcode}')
            else:
                db.session.add(new_ac)
                db.session.add(s)
                db.session.commit()
            
                return redirect(f'/track/{barcode}')
        else:
            return "الباركود غير موجود"
@app.route('/viwewallets')
def viwew():
    users = Shippers.query.all()
    total_assets=0
    for x in users:
        total_assets+=int(x.dues)
    return render_template('allw.html',users=users,m = total_assets)
@app.route('/submitS', methods=['POST'])
def submitS():
    if request.method == 'POST':
        try :
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            phone1 = request.form.get('phone1')
            phone2 = request.form.get('phone2')
            email = request.form.get('email')
            city = request.form.get('governorate')
            address = request.form.get('address')
            new_shipper = Shippers(
                name=name,
                username=username,
                password=password,
                phone1=phone1,
                phone2=phone2,
                city=city,
                email=email,
                address=address,
                wallet_code=generate_unique_code(),
                dues=0,
                shipments=0
            )
            new_wallet = Wallets(
                wallet_code = new_shipper.wallet_code,
                name = new_shipper.name,
                Shipper_id = new_shipper.id,
                dues = 0
            )
            
            # Add the new_shipper object to the database session
            db.session.add(new_shipper)
            db.session.add(new_wallet)
            db.session.commit()

            return render_template('adds.html',mes='ok')
        except :
            return render_template('adds.html',mes='error')
@app.route('/submit_delivery', methods=['POST'])
def submit_delivery_form():
    if request.method == 'POST':
        try:
            delivery_name = request.form.get('delivery_name')
            delivery_username = request.form.get('delivery_username')
            delivery_password = request.form.get('delivery_password')
            delivery_phone = request.form.get('delivery_phone')
            delivery_city = request.form.get('delivery_city')
            new_delivery = Delivery(
                name=delivery_name,
                username=delivery_username,
                password=delivery_password,
                phone=delivery_phone,
            )
            db.session.add(new_delivery)
            db.session.commit()
            return render_template('addd.html',mes='ok')
        except :
            return render_template('addd.html',mes='error')
@app.route('/adds1', methods=['POST'])
def adds1():
    try:
        charger = request.form.get('charger')
        name = request.form.get('name')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        charger_note = request.form.get('charger_note')
        receiver_note = request.form.get('receiver_note')
        governorate = request.form.get('governorate')
        address = request.form.get('address')
        price = request.form.get('price')
        shipping_price = request.form.get('shipping_price')
        delivery = request.form.get('delivery')
        charge_for_me = request.form.get('charge_for_me')

        shipper = Shippers.query.filter_by(username=charger).first()

        if shipper:
            shipment = Shipment(
                barcode = barcode_generator(),
                status = 'New Add',
                shipper_username=shipper.username,
                shipper_name=shipper.name,
                shipper_phone_1=shipper.phone1,
                shipper_phone_2=shipper.phone2,
                shipper_address=shipper.address,
                shipper_city = shipper.city,
                shipper_wallet_code = shipper.wallet_code,
                shipper_note = charger_note,
                recipient_name = name,
                recipient_phone_1 = phone1,
                recipient_phone_2 = phone2,
                recipient_address = address,
                recipient_city = governorate,
                recipient_note =receiver_note,
                pprice = price,
                dprice = shipping_price,
                tprice= int(price)+int(shipping_price),
                date=get_current_time()
            )
            print(get_current_time())
            db.session.add(shipment)
            db.session.commit()
            return render_template('addushipment.html',mes='ok')
    except :return render_template('addushipment.html',mes='error')
if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=1,port=2000,host="0.0.0.0")
