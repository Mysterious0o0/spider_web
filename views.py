import datetime
from logs import web_log_info
from db.db_mysql import session, func
from models.spider_model import StarInfo
from models.web_models import WebStarInfo
from flask import Blueprint, render_template, redirect, url_for, request


from utility.util_config import get_config_value
from utility.util_star_map import star_pinyin_dict, star_name_dict, encode_name, decode_name


star = Blueprint('star', __name__)


# 蓝本配置元组
DEFAULT_BLUEPRINT = (
    # 蓝本 前缀
    (star, '/'),
    (star, '/star'),
    (star, '/star/date')

)

star_list = get_config_value('STAR_INFO', 'STAR_LIST').split(',')
time_str = (datetime.datetime.today() - datetime.timedelta(1)).__format__('%Y-%m-%d')


# 蓝本启动配置
def config_blueprint(app):
    for blue_print, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blue_print, url_prefix=url_prefix)


# 404
def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        data = {'star_dict': {name: encode_name(name) for name in star_list}}
        return render_template('error404.html', **data)


@star.route('/')
def index():
    return redirect(url_for('star.show_star'))


@star.route('/star')
def show_star():

    star_db = session.query(StarInfo.star, func.count(StarInfo.star)).group_by(StarInfo.star).order_by(
        func.count(StarInfo.star).desc()).all()[:3]

    img_path_list = [session.query(StarInfo.star_img_path).filter(StarInfo.star == name).first()[0]
                     for name, _ in star_db]
    data = {
        'star_dict': {name: encode_name(name) for name in star_list},
        'star_name': [star_pinyin_dict[name] for name, _ in star_db],
        'img_path_list': img_path_list,
        'encode_name': [encode_name(star_pinyin_dict[name]) for name, _ in star_db],
    }

    return render_template('index.html', **data)


@star.route('/star/<name>', methods=['GET'])
def show_star_one(name):
    return redirect(url_for('star.show_star_page', name=name, page=1))


@star.route('/star/<name>&<page>', methods=['GET'])
def show_star_page(name, page):
    data = {
        'name': name,
        'star_dict': {name: encode_name(name) for name in star_list}
    }
    try:
        name_pinyin = star_name_dict[decode_name(name)]
    except Exception as e:
        web_log_info('error-------show_star_page :{}'.format(e))
        return render_template('error404.html', **data)

    img_date_list = session.query(StarInfo.star_img_path, StarInfo.release_time).filter(
        StarInfo.star == name_pinyin).order_by(StarInfo.star_update_time.desc()).limit(6).offset((int(page)-1)*6).all()

    data['name_ch'] = decode_name(name)
    data['url_date'] = [_ for _ in img_date_list]
    paginate = WebStarInfo.query.filter(WebStarInfo.star == name_pinyin).paginate(
            page=int(page), per_page=6, error_out=False)
    data['paginate'] = paginate
    # print(paginate)

    return render_template('star_page.html', **data)


@star.route('/star/date', methods=['GET', 'POST'])
def show_images_for_time():
    data = {
        'star_dict': {name: encode_name(name) for name in star_list}
    }
    try:
        if request.method == 'POST':
            page = request.args.get('page', 1)
            select_date = request.form.get('time', None)
            if select_date is None or datetime.datetime.strptime(select_date, '%m/%d/%Y %H:%M %p') > (
                    datetime.datetime.today() - datetime.timedelta(1)):
                select_date = time_str
            else:
                select_date = datetime.datetime.strptime(select_date, '%m/%d/%Y %H:%M %p').__format__('%Y-%m-%d')

            data['select_date'] = {'select_date': select_date, 'encode': encode_name(select_date)}

        else:
            page = request.args.get('page', 1)
            select_date = decode_name(request.args.get('date', None)) \
                if request.args.get('date', None) else None

            data['select_date'] = {'select_date': select_date, 'encode': encode_name(select_date)} \
                if select_date else {'select_date': None}
            print(data['select_date'])
        if data.get('select_date').get('select_date') is None:
            data['select_date'] = {'select_date': None}
            img_date_list = session.query(StarInfo.star_img_path, StarInfo.release_time, StarInfo.star).order_by(
                StarInfo.star_update_time.desc()).limit(6).offset((int(page) - 1) * 6).all()
            paginate = WebStarInfo.query.paginate(page=int(page), per_page=6, error_out=False)
        else:
            img_date_list = session.query(StarInfo.star_img_path, StarInfo.release_time, StarInfo.star).filter(
                StarInfo.release_time == select_date).order_by(StarInfo.star_update_time.desc()).limit(6).offset(
                (int(page) - 1) * 6).all()
            paginate = WebStarInfo.query.filter(WebStarInfo.release_time == select_date).paginate(
                page=int(page), per_page=6, error_out=False)
            data['select_date'] = {'select_date': select_date, 'encode': encode_name(select_date)}
        data['paginate'] = paginate
        data['url_date_star'] = [[url, date, star_pinyin_dict[_]] for url, date, _ in img_date_list]
    except Exception as e:
        web_log_info('error---------select data by date error: {}'.format(e))

    return render_template('date_page.html', **data)










