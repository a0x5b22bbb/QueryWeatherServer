from flask import Blueprint, request, jsonify, current_app
import requests
from app import limiter
from flasgger import swag_from

# from app.config import global_rate_limit

api = Blueprint('api', __name__)

# 放弃使用redis, 使用 limiter 来限制访问次数
def rate_limit_exceeded():
    response = jsonify({
        "error": "rate_limit_exceeded",
        "message": "You have exceeded your rate limit. Please try again later."
    })
    response.status_code = 429
    return response




@api.route('/weather', methods=['GET'])
# 添加swagger
# 新增 服务器最大访问次数
# @global_rate_limit
# 使用redis 需要启动redis服务 暂时废弃
@limiter.limit("5 per minute")
@swag_from({
    'parameters': [
        {
            'name': 'location_id',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Location ID of the city'
        }
    ],
    'responses': {
        200: {
            'description': 'Weather information',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'string'},
                    'updateTime': {'type': 'string'},
                    'fxLink': {'type': 'string', 'descrption': '地图详情.'},
                    'now': {
                        'type': 'object',
                        'properties': {
                            'obsTime': {'type': 'string', 'description': '当前API更新时间'},
                            'temp': {'type': 'string', 'description': '时间戳'},
                            'feelsLike': {'type': 'string', 'description': '体感温度'},
                            'icon': {'type': 'string'},
                            'text': {'type': 'string', 'description': '天气状况的文字描述，包括阴晴雨雪等天气状态的描述'},         #
                            'wind360': {'type': 'string', 'description': '风向360角度'},
                            'windDir': {'type': 'string', 'description': '风向'},
                            'windScale': {'type': 'string', 'description': '风力等级'},
                            'windSpeed': {'type': 'string', 'description': '风速 公里/小时'},
                            'humidity': {'type': 'string', 'description': '相对湿度  百分比'},
                            'precip': {'type': 'string', 'description': '过去一小时降水'},
                            'pressure': {'type': 'string', 'description': '大气压强, 百帕'},
                            'vis': {'type': 'string', 'description': '能见度  公里'},
                            'cloud': {'type': 'string', 'description': '云量    百分比 可为空'},
                            'dew': {'type': 'string', 'description': '露点温度 可为空'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        404: {
            'description': 'City not found'
        },
        429: {
            'description': 'Reached max request limit'
        },
        500: {
            'description': 'Internal server error'
        }

    }
})
def get_weather():

    location_id = request.args.get("location_id")
    # 前端获取发送过来 我对其进行转化
    if not location_id:
        return jsonify({"error": "LocationID is required"}), 400

    mappings_locationid = current_app.config['city_ID_mappings']
    is_present = any(item['location_id'] == location_id for item in mappings_locationid)

    if not is_present:
        return jsonify({"error": "LocationID is invalid"}), 400

    try:
        response = requests.get(current_app.config['API_URL'], params={
            'location': location_id,
            'key': current_app.config['API_KEY']
        })
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), response.status_code
    except Exception as err:
        return jsonify({"error": f"An error occurred: {err}"}), 500

    return jsonify(response.json())

@api.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@api.app_errorhandler(429)
def not_found(error):
    return jsonify({"error": "Too Many Requests: 5 per 1 minute"}), 429



@api.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

@api.app_errorhandler(Exception)
def handle_exception(error):
    """Handle all other exceptions."""
    response = {
        "error": "An unexpected error occurred.",
        "message": str(error)
    }
    return jsonify(response), 500