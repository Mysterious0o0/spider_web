import os
from flask_script import Manager
from flask_bootstrap import Bootstrap

from flask import Flask

from config import config
from extensions import config_extensions
from views import config_blueprint, config_errorhandler


def create_app(config_name):
    # 创建应用实例
    app = Flask(__name__)
    # 通过类初始化配置
    app.config.from_object(config[config_name])
    # 调用初始化函数
    config[config_name].init_app(app)
    # 配置相关扩展
    config_extensions(app)
    # 配置相关蓝本
    config_blueprint(app)
    # 配置错误显示
    config_errorhandler(app)
    # 返回应用实例
    return app


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
# 添加命令行启动控制
manager = Manager(app)
# 创建对象
bootstrap = Bootstrap(app)


if __name__ == '__main__':
    manager.run()

