from extensions import db


class WebStarInfo(db.Model):
    __tablename__ = 'star_photos'

    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.String(64), nullable=True, comment='明星')
    release_time = db.Column(db.Date, nullable=True, comment='照片发布时间')
    star_img_path = db.Column(db.String(3000), nullable=True, comment='照片地址')
    star_url = db.Column(db.String(3000), nullable=True, comment='图片链接地址')
    star_update_time = db.Column(db.DateTime, nullable=True, comment='照片更新时间')

