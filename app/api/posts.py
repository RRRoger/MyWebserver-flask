from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Post, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden
from app.main.common import try_except_log, response


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id)}


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())

############################################# ERP ###################################### 

import requests
import json

eepromModel ={ 
    "MAC":"",
    "SN":"",
    "AngleOffset":"",
    "AccurityAngleOffsetPeak":0,
    "AccurityAngleOffsetPhase":0,
    "DataFormat": 0,
    "MoterType": 1,
    "ProductDate":"",
    "CalibrationFilePath":"calibrationFile",
    "HardwareInfo":{},
    "SAES":""}
base_url = 'http://172.31.0.63:8069'



def print_error_info(response_json):
    print(response_json['code'] + response_json['message'])

def Save2File(file, data):
    with open(file, 'w') as f:
        f.write(data)

def jsonSave(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)


################ mac/sn/production date ########################
def GetMac_SN_ProductDate(base_url, lidarID, eepromModel):
    data = {
        "lidarid": lidarID, 
    }
    req_url='/erp/get/lidar/info'
    response_info = requests.post(base_url + req_url, data=data)
    response_json = json.loads(response_info.content.decode())
    if response_json['code'] == 0:
        eepromModel['MAC'] = response_json['result']['mac_address']
        eepromModel['SN'] = response_json['result']['sn']
        eepromModel['ProductDate'] = response_json['result']['production_date']
        
        return 0
    else:
        print_error_info(response_json)
        return -1

################# get angle file file #########################
def GetCalibrationFile(base_url, lidarID, eepromModel):
    data = {
        'lidar_name': lidarID
    }
    req_url = '/erp/lidar/workstation/get_angle_file'
    response_info = requests.get(base_url + req_url, params=data )
    response_json = json.loads( response_info.content.decode())
    if response_json['code'] == 0:
        req_url = response_json['result']['url']
        angle_respose = requests.get(req_url)
        Save2File(eepromModel['CalibrationFilePath'],str(angle_respose.content.decode()))
        return 0
    else:
        print_error_info(response_json)
        return -1

#################  angle offset #########################
def GetAngleOffset(base_url, lidarID, eepromModel):
    data = {
        "lidarid": lidarID, 
        "assembly_item_codes": "adjustment_angle_offset;adjustment_A;adjustment_C"
    }
    req_url =  "/erp/get/lidar/assembly/info"
    response_info = requests.post(base_url + req_url, data=data)
    response_json = json.loads( response_info.content.decode())
    if response_json['code'] == 0:
        eepromModel['AngleOffset'] =  response_json['result']['adjustment_angle_offset']['content']
        eepromModel['AccurityAngleOffsetPeak'] = response_json['result']['adjustment_A']['content']
        eepromModel['AccurityAngleOffsetPhase'] = response_json['result']['adjustment_C']['content']
        return 0
    else:
        print_error_info(response_json)
        return -1
@api.route('/get_e2prom/', methods=['POST'])
def get_e2prom():
    GetMac_SN_ProductDate(base_url=base_url, lidarID='ARES-007',eepromModel=eepromModel)
    GetCalibrationFile(base_url=base_url, lidarID='WR36-500-66-44', eepromModel=eepromModel)
    GetAngleOffset(base_url=base_url, lidarID="ARES-003", eepromModel=eepromModel)
    return eepromModel
############################################# HSM ###################################### 


@api.route('/posts/test', methods=['POST', 'GET'])
@permission_required(Permission.WRITE)
@try_except_log(add_log=True)
def post_test():
    return response({})

