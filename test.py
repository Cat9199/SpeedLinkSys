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
    db.session.commit()
    return redirect('/req')