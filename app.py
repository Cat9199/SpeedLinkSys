from flask import Flask,redirect,url_for, request, send_file,jsonify, session, render_template
from modules.barcode_extractor import extract_barcode_data
from modules.sendmail import send_daily_report_email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date
import requests
import datetime
import random
import string
import json
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
    p1 = db.Column(db.Integer)
    p2 = db.Column(db.Integer)
    p3 = db.Column(db.Integer)
    p4 = db.Column(db.Integer)
    p5 = db.Column(db.Integer)
    p6 = db.Column(db.Integer)
    p7 = db.Column(db.Integer)
    p8 = db.Column(db.Integer)
    p9 = db.Column(db.Integer)
    p10 = db.Column(db.Integer)
    p11 = db.Column(db.Integer)
    p12 = db.Column(db.Integer)
    p13 = db.Column(db.Integer)
    p14 = db.Column(db.Integer)
    p15 = db.Column(db.Integer)
    p16 = db.Column(db.Integer)
    p17 = db.Column(db.Integer)
    p18 = db.Column(db.Integer)
    p19 = db.Column(db.Integer)
    p20 = db.Column(db.Integer)
    p21 = db.Column(db.Integer)
    p22 = db.Column(db.Integer)
    p23 = db.Column(db.Integer)
    p24 = db.Column(db.Integer)
    p25 = db.Column(db.Integer)
    p26 = db.Column(db.Integer)
class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    ntype = db.Column(db.Integer)
    messaget = db.Column(db.Integer)
    state = db.Column(db.String(100))
    created_at = db.Column(db.String(23))
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
    payload['fromCityID'] = 3
    payload['fromAddress'] = info.address
    payload['fromPhone'] = info.phone1
    
    
    print(payload)
    response = requests.post(reqUrl, json=payload, headers=headersList)
    return response.text
def get_data_value(city_name):
  
    city_data = {
        "القاهرة": 1,
        "البحيرة": 2,
        "الاسكندرية": 3,
        "الدلتا": 4,
        "الاسماعيلية": 5,
        "بورسعيد": 6,
        "السويس": 7,
        "الشرقية": 8,
        "بنى سويف": 9,
        "المنيا": 10,
        "اسيوط": 11,
        "سوهاج": 12,
        "الساحل الشمالي": 13,
        "مطروح": 14,
        "قنا": 15,
        "الاقصر": 16,
        "اسوان": 17,
        "شرم الشيخ": 18,
        "الغردقة": 19,
        "مدن البحر الاحمر": 20,
        "الفيوم": 21,
        "خارج التغطية": 22,
        "موقوف": 23,
        "ش": 24,
        "منصورة": 25,
        "قليوب": 26
    }

    data_value = city_data.get(city_name)
    if data_value is not None:
        return data_value
    else:
        return None
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
    current_time = current_time.replace(microsecond=0, tzinfo=None)
    return current_time
@app.route('/download_database')
def download_database():
    try:
        # Replace 'your_database.db' with the actual path to your database file
        db_file_path = './instance/speedlink.db'
        day = date.today()
        # Provide a name for the downloaded file (shown to the user)
        download_filename = f'db{day}.db'
        
        return send_file(db_file_path, as_attachment=True, download_name=download_filename)
    except Exception as e:
        return str(e)
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
@app.route('/print')
def t():
    user = Shippers.query.all()
    return render_template('printform.html',u=user)
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
    session['user_type'] = None
    session['username'] = None
    return redirect('/login')
@app.route('/del/<int:id>')
def delete(id):
    student = Shipment.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/req')
@app.route('/pa',methods=['POST'])
def printq():
    info = Shipment.query.all()
    num_pages = (len(info) + 2) // 3
    info_chunks = [info[i:i+3] for i in range(0, len(info), 3)]
    return render_template('print.html', info_chunks=info_chunks, num_pages=num_pages)

@app.route('/dashboard')
def dashboard():
    user_type = session.get('user_type')
    username = session.get('username')
    if user_type == 'admin':
        s1 = Shipment.query.filter_by(shipment_status='شحنة جديدة').all()
        s2 = Shipment.query.filter_by(shipment_status='لم يتم استلامها').all()
        s3 = Shipment.query.filter_by(shipment_status='تم استلامها').all()
        s4 = Shipment.query.filter_by(shipment_status='تم توصيل الشحنة').all()
        
        shinfo = Shipment.query.filter_by(status='New Add').all()
        shinfo = shinfo[::-1]
        notnum = Notifications.query.filter_by(state='0').all()
        y = 0
        for x in notnum:
            y += 1
        session['numn'] = y
        return render_template('dashboard.html', paget= 'مرحبا بك في لوحة التحكم',user_type=user_type, username=username,infoL=shinfo)
    elif user_type == 'shipper':
        shinfo = Shipment.query.filter_by(shipper_username=username).all()
        shinfo = shinfo[::-1]
        shipper = Shippers.query.filter_by(username=username).first()
        return render_template('dashboard.html',  paget= 'مرحبا بك في لوحة التحكم',user_type=user_type, username=username,infoS=shipper,infoL=shinfo)
    elif user_type == 'delivery':
        de = Delivery.query.filter_by(username=username).first()
        sh = Shipment.query.filter_by(delivery_id=de.id,status='New Add',delivery_date=date.today()).all()
        
        return render_template('delivery-dashboard.html', user_type=user_type, username=username,sh=sh)
    else:
        return redirect('/login')
@app.route('/stopshipping/<int:id>')
def stopshipping(id):
    s = Shipment.query.filter_by(id=id).first()
    s.status = 'stop'
    s.delivery_date = None
    s.delivery_id = None
    db.session.commit()
    return redirect('/dashboard')
@app.route('/stop')
def stop():
    log = Shipment.query.filter_by(delivery_date=None,status='stop').all()
    u = Delivery.query.all()
    
    return render_template('sendtodelivery.html',infoL=log,u=u)
@app.route('/makeasreed/<int:id>')
def makeasreed(id):
    notf = Notifications.query.filter_by(id=id).first()
    notf.state = '1'
    db.session.commit()
    notnum = Notifications.query.filter_by(state='0').all()
    y = 0
    for x in notnum:
        y += 1
    session['numn'] = y
    return redirect('/notifications')
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
@app.route('/sendtodelivery')
def sendtodelivery():
    log = Shipment.query.filter_by(delivery_date=None)
    u = Delivery.query.all()
    return render_template('sendtodelivery.html',infoL=log,u=u)
@app.route('/setship', methods=['POST'])
def setship():
    Deliveryid = request.form.get('dvid')
    data = request.form.get('date')
    sid = request.form.get('sid')
    s = Shipment.query.filter_by(id=sid).first()
    s.delivery_id = Deliveryid
    s.delivery_date = data
    db.session.commit()
    return redirect('/sendtodelivery')

@app.route('/viweshipping')
def viweshipping():
    s = Shipment.query.filter_by(status='New Add').all()
    s =s[::-1]
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
    n = Notifications.query.filter_by(state='0',ntype='n').all()
    w = Notifications.query.filter_by(state='0',ntype='w').all()
    n = n[::-1]
    w = w[::-1]
    return render_template('notifications.html', n = n,w=w)
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
                    created_at=get_current_time()
                )

                s.status = 'archiv'
                db.session.add(new_ac)
                db.session.add(s)
                db.session.add(new_wl)
                db.session.commit()
                send_daily_report_email(x=s.barcode,y=s.recipient_name,z=s.pprice,receiver_email=u.email,name=u.name)
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
        # try :
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
            
            db.session.add(new_shipper)
            db.session.add(new_wallet)
            db.session.commit()
            newp = Dprice(sid=new_shipper.id)
            db.session.add(newp)
            db.session.commit()
            return render_template('adds.html',mes='ok')
        # except :
        #     return render_template('adds.html',mes='error')
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
@app.route('/req')
def req():
    req = Shipment.query.filter_by(status="what").all()
    return render_template('req.html',infoL=req)
@app.route('/ac/<int:id>')
def ac(id):
    s = Shipment.query.filter_by(id=id).first()
    s.status = 'New Add'
    s.shipment_status = 'شحنة جديدة'
    db.session.commit()
    return redirect('/req')
@app.route('/acs/<int:id>')
def acs(id):
    s = Shipment.query.filter_by(id=id).first()
    s.status = 'New Add'
    s.shipment_status = 'شحنة جديدة'
    s.how = 'esh'
    shipment_payload = {
                    "fromAddress": "عنواني",
                    "fromPhone": "240932808923",
                    "fromContactPerson": "سبيد لنك",
                    "toCityID": int(s.recipient_city),
                    "toConsigneeName":s.recipient_name,
                    "toAddress":s.recipient_address,
                    "toPhone": s.recipient_phone_1,
                    "toMobile": s.recipient_phone_2,
                    "toContactPerson": "احمد",
                    "price" : s.pprice
                }
    response_text = save_shipment(shipment_payload)
    response_list = json.loads(response_text)
    first_dict = response_list[0]
    awb_value = first_dict["awb"]
    s.aws_code=awb_value
    db.session.commit()
    return redirect('/req')
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
        print(get_data_value(governorate))
        address = request.form.get('address')
        price = request.form.get('price')
        how = request.form.get('how')
        shipping_price = 100
        shipper = Shippers.query.filter_by(username=charger).first()
        dpricee = Dprice.query.filter_by(sid=shipper.id).first()
        if governorate == '1' :
            shipping_price = dpricee.p1
        elif governorate == '2' :
            shipping_price = dpricee.p2
        elif governorate == '3' :
            shipping_price = dpricee.p3
        elif governorate == '4' :
            shipping_price = dpricee.p4
        elif governorate == '5' :
            shipping_price = dpricee.p5
        elif governorate == '6' :
            shipping_price = dpricee.p6
        elif governorate == '7' :
            shipping_price = dpricee.p7
        elif governorate == '8' :
            shipping_price = dpricee.p8
        elif governorate == '9' :
            shipping_price = dpricee.p9
        elif governorate == '10' :
            shipping_price = dpricee.p10
        elif governorate == '11' :
            shipping_price = dpricee.p11
        elif governorate == '12' :
            shipping_price = dpricee.p12
        elif governorate == '13' :
            shipping_price = dpricee.p13
        elif governorate == '14' :
            shipping_price = dpricee.p14
        elif governorate == '15' :
            shipping_price = dpricee.p15
        elif governorate == '16' :
            shipping_price = dpricee.p16
        elif governorate == '17' :
            shipping_price = dpricee.p17
        elif governorate == '18' :
            shipping_price = dpricee.p18
        elif governorate == '19' :
            shipping_price = dpricee.p19
        elif governorate == '20' :
            shipping_price = dpricee.p20
        elif governorate == '21' :
            shipping_price = dpricee.p21
        elif governorate == '22' :
            shipping_price = dpricee.p22
        elif governorate == '23' :
            shipping_price = dpricee.p23
        elif governorate == '24' :
            shipping_price = dpricee.p24
        elif governorate == '25' :
            shipping_price = dpricee.p25
        elif governorate == '26' :
            shipping_price = dpricee.p26
        tprice = price+shipping_price
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
                    tprice=tprice,
                    date=get_current_time(),
                    shipment_status = 'في انتظار القبول',
                    how=how
                )
            

                shipment_payload = {
                    "fromContactPerson": "سبيد لنك",
                    "toCityID": int(governorate),
                    "toConsigneeName":name,
                    "toAddress":address,
                    "toPhone": phone1,
                    "toMobile": phone2,
                    "toContactPerson": name,
                    "price" : tprice
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
                if session['user_type'] == 'admin':
                    st='New Add'
                    sh = 'شحنة جديدة'
                else:
                    st='what'
                    sh = 'في انتظار القبول'
                shipment = Shipment(
                    barcode=barcode_generator(),
                    status=st,
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
                    tprice = tprice,
                    date=get_current_time(),
                    shipment_status = sh,
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
    username= session['username']
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
        newn= Notifications(username=username,ntype='n',messaget='تم التعديل علي اعدادات البرنامج',state='0',created_at=get_current_time())
        db.session.add(newn)
        db.session.commit()
        return redirect(url_for('setting'))  

    return render_template('setting.html', admin=admin)
@app.route('/dprice/<int:sid>')
def dprice(sid):
    price = Dprice.query.filter_by(sid=sid).first()
    return render_template('dprice.html',price=price)
@app.route('/saveprice/<int:sid>', methods=['POST'])
def save_price(sid):
    price = Dprice.query.filter_by(sid=sid).first()
    if price is None:
        return "Price not found", 404
    price.p1 = request.form.get('1')
    price.p2 = request.form.get('2')
    price.p3 = request.form.get('3')
    price.p4 = request.form.get('4')
    price.p5 = request.form.get('5')
    price.p6 = request.form.get('6')
    price.p7 = request.form.get('7')
    price.p8 = request.form.get('8')
    price.p9 = request.form.get('9')
    price.p10 = request.form.get('10')
    price.p11 = request.form.get('11')
    price.p12 = request.form.get('12')
    price.p13 = request.form.get('13')
    price.p14 = request.form.get('14')
    price.p15 = request.form.get('15')
    price.p16 = request.form.get('16')
    price.p17 = request.form.get('17')
    price.p18 = request.form.get('18')
    price.p19 = request.form.get('19')
    price.p20 = request.form.get('20')
    price.p21 = request.form.get('21')
    price.p22 = request.form.get('22')
    price.p23 = request.form.get('23')
    price.p24 = request.form.get('24')
    price.p25 = request.form.get('25')
    price.p26 = request.form.get('26')
    db.session.commit()
    return redirect(f'/dprice/{sid}')
if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=1,port=8001,host='0.0.0.0')