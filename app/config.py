# from functools import wraps
# from flask import jsonify, current_app
#
#
#
# def global_rate_limit(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         key = "global_rate_limit"
#         redis_client = current_app.redis_client
#         # 获取当前访问次数
#         current_requests = redis_client.get(key)
#         # 最大访问次数
#         MAX_GLOBAL_REQUESTS = current_app.config['MAX_GLOBAL_REQUESTS'] # 风向api 默认每天最大1000个
#
#         # 访问次数重置时间（秒）
#         TIME_WINDOW = current_app.config['TIME_WINDOW']  # 24 hour
#         if current_requests is None:
#             # 如果没有记录，初始化访问次数
#             redis_client.set(key, 1, ex=TIME_WINDOW)
#         else:
#             current_requests = int(current_requests)
#             if current_requests >= MAX_GLOBAL_REQUESTS:
#                 # 超过最大访问次数，返回503状态码
#                 return jsonify({"error": "Service Unavailable: Too many requests"}), 503
#             else:
#                 # 增加访问次数
#                 redis_client.incr(key)
#
#         return func(*args, **kwargs)
#     return wrapper

