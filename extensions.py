# 导入相关扩展类库
from flask_sqlalchemy import SQLAlchemy


# 创建相关扩展对象
db = SQLAlchemy()


# 配置函数
def config_extensions(app):
    db.init_app(app)
