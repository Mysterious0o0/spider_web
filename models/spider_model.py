import os

from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date


# 乱码
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
# 创建对象的基类
Base = declarative_base()


# 产品类别链接
class StarInfo(Base):
    __tablename__ = 'star_photos'

    id = Column(Integer, Sequence('seq_star_photos'), primary_key=True, autoincrement=True)
    star = Column(String(64), nullable=True, comment='明星')  # 明星
    release_time = Column(Date, nullable=True, comment='照片发布时间')  # 照片发布时间
    star_img_path = Column(String(3000), nullable=True, comment='照片地址')  # 照片地址
    star_url = Column(String(3000), nullable=True, comment='图片链接地址')  # 图片链接地址
    star_update_time = Column(DateTime, nullable=True, comment='照片更新时间')  # 照片更新时间
