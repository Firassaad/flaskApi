
from collections import OrderedDict
from flask import Flask
from flask import jsonify
from flask import json
import zeep
from flask import request
from flask_cors import CORS
import collections
orderedDict = collections.OrderedDict()

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
            r"/*": {"origins": ["http://localhost:4200"]}}, supports_credentials=True)
app.config['JSON_SORT_KEYS'] = False

# ----------PP-------------------------


@app.route('/frs', methods=['GET', 'POST'])
def parseOFS(a):
    # a = ',NOM::NOM/CIN::CIN/AGENCE::AGENCE/DATE::DATE/FT::FT/FISC::FISC/REGION::REGION,NOM:1:1=BEN ROMDHANE MOHAMED ALI,FT:1:1=FT2033872941//1/FUNDS.TRANSFER,AGENCE:1:1=Agence Hedi Chaker,CIN:1:1=07454400,FISC:1:1=,DATE:1:1=20201203'
    #  a = ',NOM::NOM/CIN::CIN/AGENCE::AGENCE/DATE::DATE/FT::FT/FISC::FISC/REGION::REGION,NOM:1:1=SAADAOUI FIRAS,CIN:1:1=12662802,AGENCE:1:1=Agence Hedi Chaker,DATE:1:1=20201203,FT:1:1=FT2033830095//1/FUNDS.TRANSFER,FISC:1:1=,REGION:1:1=Hedi Chake'
    print("----------a-------->", str(a))
    b = a.split("/")
    print("----------b-------->", str(b))
    c = b[6].split(":1=")
    print("----------c-------->", str(c))
    nom = c[1].split(',')[0]
    CIN = c[2].split(',')[0]
    agence = c[3].split(',')[0]
    date = c[4].split(',')[0]
    FT = c[5].split(',')[0]

    # build region & fisc
    b1 = a.split('/1/')
    c1 = b1[1].split(":1=")
    # print('b1>>>>>>>>>>>>>>>', b1)
    # print('c1>>>>>>>>>>>>>>>', c1)
    Fisc = c1[1].split(',')[0]
    Region = c1[2].split(',')[0]

    data = OrderedDict([("nom", nom), ("CIN", CIN),
                        ("agence", agence), ("date", date), ("FT", FT) ,("fisc",Fisc) , ("region",Region)])
    # print(data)
    return json.dumps([data], sort_keys=False)


@app.route('/getjson', methods=['GET', 'POST'])
def returnOFS():
    account = request.args.get("cpt")
    print("cpt recup  :",  request.args.get("cpt"))
    request_data = {
        "OfsRequest": "ENQUIRY.SELECT,,EODUSER/123456,ATTESTATION.ENG.PP,@ID:EQ="
        + account
    }

    wsdl = 'http://172.16.40.115:9095/TWSEB/services?wsdl'
    client = zeep.Client(wsdl=wsdl)
    ofsResponse = client.service.callOfs(**request_data)
    #status = ofsResponse.Status.successIndicator
    ofsResponse = str(ofsResponse.OfsResponse)
    # print("test >>>>>", ofsResponse)
    return parseOFS(ofsResponse)

# ----------end PP-------------------------

# ----------PM-------------------------


# @app.route('/test12PM', methods=['GET', 'POST'])
# def parseOFSPM(a):
#     print("------------------>", str(a))
#     b = a.split("/")
#     c = b[3].split(":1=")
#     nom = c[1].split(',')[0]
#     CIN = c[2].split(',')[0]
#     agence = c[3].split(',')[0]

#     date = c[4].split(',')[0]
#     data = OrderedDict([("nom", nom), ("CIN", CIN),
#                         ("agence", agence), ("date", date)])
#     print(data)
#     return json.dumps([data], sort_keys=False)


# @app.route('/getjsonPM', methods=['GET', 'POST'])
# def returnOFSPM():
#     account = request.args.get("cpt")
#     print("cpt recup  :",  request.args.get("cpt"))
#     request_data = {
#         "OfsRequest": "ENQUIRY.SELECT,,EODUSER/123456,ATTESTATION.ENG.PP,@ID:EQ="
#         + account
#     }

#     wsdl = 'http://172.16.40.115:9095/TWSEB/services?wsdl'
#     client = zeep.Client(wsdl=wsdl)
#     ofsResponse = client.service.callOfs(**request_data)
#     #status = ofsResponse.Status.successIndicator
#     ofsResponse = str(ofsResponse.OfsResponse)
#     # print("test >>>>>", ofsResponse)
#     //return parseOFS(ofsResponse)

#     # ----------end PM-------------------------


if __name__ == '__main__':
    # app.run(host="localhost", port=8080, debug=True )
    app.run(port=8080, debug=True, host='localhost', use_reloader=False)
