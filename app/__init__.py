import os

import yaml
from flask import Flask
from flask_cors import CORS

from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# import redis

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["900 per day", "200 per hour"],
    storage_uri="memory://"
)

def create_app():
    app = Flask(__name__)
    swagger_config = {
        "swagger": "2.0",
        "info": {
            "title": "Weather API",
            "description": "API for getting weather information.",
            "version": "1.0.0"
        },
        "host": "localhost:8000",
        "basePath": "/api",
        "schemes": ["http", "https"],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "headers": []  # 添加空的 headers 配置 防止报错
    }
    Swagger(app, config=swagger_config)



    # 初始化速率限制器
    limiter.init_app(app)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))

    # 加载配置文件, 目前存放 api_url  api_key
    with open(project_root + '/config.yml', 'r', encoding='utf8') as config_file:
        config = yaml.safe_load(config_file)
    app.config.update(config)
    # 加载city_name 和location_id 的mappings
    with open(project_root + '/city_name_locationID.yml', 'r', encoding='utf8') as mappings_file:
        mappings = yaml.safe_load(mappings_file)
    app.config["city_ID_mappings"] = mappings

    # 导入并注册蓝图.
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'https://source-cn.net:8000').split(',')
    # allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:9000').split(',')
    CORS(app, origins=allowed_origins, supports_credentials=True)
    # 初始化swagger
    # swagger_config = {
    #     "header": [],
    #     "specs": [
    #         {
    #             "endpoint": "api"
    #         }
    #     ]
    # }

    return app
