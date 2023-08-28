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
import requests
import json
import datetime
import pytz
import random 

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
    CompanyID = db.Column(db.String(100))
    AccessToken =  db.Column(db.String(200))
    Language  =  db.Column(db.String(200))
    Content_Type = db.Column(db.String(200))
    city=db.Column(db.String(200))
    address = db.Column(db.String(200))
    phone1=db.Column(db.String(100))
    phone2 = db.Column(db.String(100))
    
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
    shipment_status = db.Column(db.String(100))
    date = db.Column(db.String(23))
    accepted = db.Column(db.Boolean)  
    delivery_date = db.Column(db.String(20)) 
    aws_code = db.Column(db.String(25))  
    how = db.Column(db.String(25)) 

class ShippingDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(15))
    shipment_id = db.Column(db.Integer)
    delivery_id = db.Column(db.Integer)
    state = db.Column(db.String(100))
    created_at = db.Column(db.String(23))
class Dprice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer)
    Cairo = db.Column(db.Integer)
    Alexandria = db.Column(db.Integer)
    Giza = db.Column(db.Integer)
    SharmElSheikh = db.Column(db.Integer)
    Luxor = db.Column(db.Integer)
    Aswan = db.Column(db.Integer)
    Hurghada = db.Column(db.Integer)
    Ismailia = db.Column(db.Integer)
    Tanta = db.Column(db.Integer)
    Mansoura = db.Column(db.Integer)
    PortSaid = db.Column(db.Integer)
    Suez = db.Column(db.Integer)
    Banha = db.Column(db.Integer)
    AlMahallaAlKubra = db.Column(db.Integer)
    Sohag = db.Column(db.Integer)
    Qena = db.Column(db.Integer)
    Asyut = db.Column(db.Integer)
    Damietta = db.Column(db.Integer)
    Zagazig = db.Column(db.Integer)
    ElArish = db.Column(db.Integer)
    MarsaMatruh = db.Column(db.Integer)
    KafrElSheikh = db.Column(db.Integer)
    Fayoum = db.Column(db.Integer)
    BeniSuef = db.Column(db.Integer)
    Minya = db.Column(db.Integer)
def save_shipment(payload):
    reqUrl = "https://vsoftapi.com-eg.net/api/ClientUsers/V6/SaveShipment"
    user=session['username']
    info = Admins.query.filter_by(username=user).first()
    headersList = {
        "CompanyID": info.CompanyID,
        "AccessToken": info.AccessToken,
        "Language": info.Language ,
        "Content-Type": info.Content_Type   
    }
    payload['fromCityID'] = 4
    payload['fromAddress'] = info.address
    payload['fromPhone'] = info.phone1
    print(payload)
    response = requests.post(reqUrl, json=payload, headers=headersList)
    return response.text

def generate_unique_code(length=15):
    characters = string.ascii_letters + string.digits
    unique_code = ''.join(random.choice(characters) for _ in range(length))
    return unique_code

def barcode_generator(n=15):
    random_numbers = [str(random.randint(0, 9)) for _ in range(n)]
    return "".join(random_numbers)
def get_current_time():
    egypt_timezone = pytz.timezone('Africa/Cairo')
    current_time = datetime.datetime.now(egypt_timezone)
    return current_time
@app.route('/setting')
def setting():
    username = session['username']
    admin = Admins.query.filter_by(username=username).first()

    return render_template('setting.html',info=admin)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/users')
def test():
    users = Shippers.query.all()
    return render_template('users.html',users=users)
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
            session['wellat'] = loginShipper.wallet_code
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
        shinfo = Shipment.query.filter_by(status='New Add').all()
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
    return render_template('notifications.html')
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

            s.shipment_status = shipment_status

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
                db.session.add(new_ac)
                db.session.add(s)
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
@app.route('/profile')
def profile():
    username = session['username']
    shippers = Shippers.query.filter_by(username=username).first()
    return render_template('profile.html', info=shippers, paget='الملف الشخصي')
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
            newp = Dprice(sid=new_shipper.id)
            # Add the new_shipper object to the database session
            db.session.add(new_shipper)
            db.session.add(new_wallet)
            db.session.add(newp)
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
    # try:
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
        how = request.form.get('how')
        shipper = Shippers.query.filter_by(username=charger).first()
        if how =='esh':
            if shipper:
                shipment = Shipment(
                    barcode=barcode_generator(),
                    status='New Add',
                    shipper_username=shipper.username,
                    shipper_name=shipper.name,
                    shipper_phone_1=shipper.phone1,
                    shipper_phone_2=shipper.phone2,
                    shipper_address=shipper.address,
                    shipper_city=shipper.city,
                    shipper_wallet_code=shipper.wallet_code,
                    shipper_note=charger_note,
                    recipient_name=name,
                    recipient_phone_1=phone1,
                    recipient_phone_2=phone2,
                    recipient_address=address,
                    recipient_city=governorate,
                    recipient_note=receiver_note,
                    pprice=price,
                    dprice=shipping_price,
                    date=get_current_time(),
                    shipment_status = 'في انتظار القبول',
                    how=how
                )
            

                shipment_payload = {
                    "fromAddress": "عنواني",
                    "fromPhone": "240932808923",
                    "fromContactPerson": "سبيد لنك",
                    "toCityID": 3,
                    "toConsigneeName":name,
                    "toAddress":address,
                    "toPhone": phone1,
                    "toMobile": phone2,
                    "toContactPerson": "احمد",
                    "price" : price
                }
                response_text = save_shipment(shipment_payload)
                response_list = json.loads(response_text)
                first_dict = response_list[0]
                awb_value = first_dict["awb"]
                print(awb_value)
                shipment.aws_code=awb_value
                db.session.add(shipment)
                
                shipper.shipments = shipper.shipments + 1 
                db.session.add(shipper)
                db.session.commit()

        else:
                shipment = Shipment(
                    barcode=barcode_generator(),
                    status='New Add',
                    shipper_username=shipper.username,
                    shipper_name=shipper.name,
                    shipper_phone_1=shipper.phone1,
                    shipper_phone_2=shipper.phone2,
                    shipper_address=shipper.address,
                    shipper_city=shipper.city,
                    shipper_wallet_code=shipper.wallet_code,
                    shipper_note=charger_note,
                    recipient_name=name,
                    recipient_phone_1=phone1,
                    recipient_phone_2=phone2,
                    recipient_address=address,
                    recipient_city=governorate,
                    recipient_note=receiver_note,
                    pprice=price,
                    dprice=shipping_price,
                    date=get_current_time(),
                    shipment_status = 'في انتظار القبول',
                    how=how
                    
                )
                db.session.add(shipment)
                shipper.shipments = shipper.shipments + 1 
                db.session.add(shipper)
                db.session.commit()

        return render_template('addushipment.html', mes='ok')
    # except:
    #     return render_template('addushipment.html', mes='error')
    
@app.route('/update_profile/<int:admin_id>', methods=['GET', 'POST'])
def update_profile(admin_id):
    admin = Admins.query.get(admin_id)

    if request.method == 'POST':
        admin.name = request.form['name']
        admin.username = request.form['username']
        admin.password = request.form['password']
        admin.position = request.form['position']
        admin.CompanyID = request.form['CompanyID']
        admin.AccessToken = request.form['AccessToken']
        admin.Language = request.form['Language']
        admin.Content_Type = request.form['Content_Type']
        admin.city = request.form['city']
        admin.address = request.form['address']
        admin.phone1 = request.form['phone']

        db.session.commit()
        return redirect(url_for('setting'))  # Assuming 'setting' is the route for the profile page

    return render_template('setting.html', admin=admin)
@app.route('/dprice/<int:sid>')
def dprice(sid):
    price = Dprice.query.filter_by(sid=sid).first()
    return render_template('dprice.html',price=price)
@app.route('/saveprice/<int:sid>', methods=['POST'])
def save_price(sid):
    price = Dprice.query.filter_by(sid=sid).first()
    if price is None:
            # Handle the case when the price object is not found
        return "Price not found", 404
    price.Cairo = request.form.get('cairo')
    price.Alexandria = request.form.get('Alexandria')
    price.Giza = request.form.get('giza')
    price.SharmElSheikh = request.form.get('sharm_el_sheikh')
    price.Luxor = request.form.get('luxor')
    price.Aswan = request.form.get('aswan')
    price.Hurghada = request.form.get('hurghada')
    price.Ismailia = request.form.get('ismailia')
    price.Tanta = request.form.get('tanta')
    price.Mansoura = request.form.get('mansoura')
    price.PortSaid = request.form.get('port_said')
    price.Suez = request.form.get('suez')
    price.Banha = request.form.get('banha')
    price.AlMahallaAlKubra = request.form.get('al_mahalla_al_kubra')
    price.Sohag = request.form.get('sohag')
    price.Qena = request.form.get('qena')
    price.Asyut = request.form.get('asyut')
    price.Damietta = request.form.get('damietta')
    price.Zagazig = request.form.get('zagazig')
    price.ElArish = request.form.get('el_arish')   
  
    db.session.commit()
    return redirect(f'/dprice/{sid}')
if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=1,port=2000,host="0.0.0.0")
