
from flask import Flask
from flask import jsonify
from flask import json
import zeep
from flask import request

from flask_cors import CORS
import collections
orderedDict = collections.OrderedDict()


from collections import OrderedDict

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
@app.route('/test12')
def parseOFS():
     #a =",USER.NAME::USER.NAME/CIN::CIN/AGENCE::AGENCE/DATE::DATE,USER.NAME:1:1=BEN ROMDHANE MOHAMED ALI,CIN:1:1=07454400,AGENCE:1:1=Agence Hedi Chaker,DATE:1:1=03 DEC 2020"
     #a=",USER.NAME::USER.NAME/CIN::CIN/AGENCE::AGENCE/DATE::DATE,USER.NAME:1:1=SAADAOUI FIRAS,CIN:1:1=12662802,AGENCE:1:1=Agence Hedi Chaker,DATE:1:1=03 DEC 2020"
    #  a=",USER.NAME::USER.NAME/CIN::CIN/AGENCE::AGENCE/DATE::DATE,USER.NAME:1:1=BEN ROMDHANE MOHAMED ALI,CIN:1:1=07454400,AGENCE:1:1=Agence Hedi Chaker,DATE:1:1=03 DEC 2020"
     a = returnOFS()
     print("------------------>",str(a))
     b =a.split("/")
     c =b[3].split(":1=")
     nom = c[1].split(',')[0]
     CIN = c[2].split(',')[0]
     agence= c[3].split(',')[0]
     
     date= c[4].split(',')[0]
     data = OrderedDict([("nom", nom), ("CIN", CIN), ("agence",agence), ("date",date)])
     print(data)
     return  json.dumps([data] , sort_keys=False)


    #  data = OrderedDict([("nom", c[1].split(',')[0]), ("CIN", c[2].split(',')[0]), ("agence", c[3].split(',')[0])])
    #  return  json.dumps({
    #      data
    #    # "date": c[4].split(',')[0]
        

       
    # })
@app.route('/getjson' , methods=['POST'])
def returnOFS():
    account = "0117881011176281"
    print("------------------" ,getjson())
    request_data = {
        "OfsRequest": "ENQUIRY.SELECT,,EODUSER/123456,ATTESTATION.ENG.PP,@ID:EQ="
        +account
    }
    
    wsdl = 'http://172.16.40.115:9095/TWSEB/services?wsdl'
    client = zeep.Client(wsdl=wsdl)
    ofsResponse = client.service.callOfs(**request_data)
    #status = ofsResponse.Status.successIndicator
    ofsResponse = str(ofsResponse.OfsResponse)
    print("test >>>>>", ofsResponse)
    return ofsResponse


@app.route('/getjson' , methods=['POST'])
def getjson():
    cpt = request.args.get("cpt")
    # cpt = request.json["cpt"]
    print(cpt)
    return cpt

@app.route('/test')
def hello_world():
    request_data = {
        "OfsRequest": "ENQUIRY.SELECT,,EODUSER/123456,USER.AUTH,SIGN.ON.NAME:EQ=EODUSER"
    }

    #wsdl = 'http://172.16.40.115:9095/TWSEB/services?wsdl'
    #client = zeep.Client(wsdl=wsdl)
    #ofsResponse = client.service.callOfs(**request_data)

    return jsonify({
        #"data": ofsResponse.ofsResponse
        "data": "sid",
        "nom" : "firas",
        "piece d'identite": "12662803",
        "agence" : "hedi cheker",
        "date" : "29/01/2021"
    })

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)