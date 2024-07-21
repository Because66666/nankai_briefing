from init import db




class Lecture(db.Model):
    id = db.Column(db.Integer,primary_key=True,unique = True,nullable=False)
    title = db.Column(db.Text,index = True)
    type = db.Column(db.Text)
    time_set = db.Column(db.Integer)
    time_begin = db.Column(db.Text)
    place = db.Column(db.Text)
    url = db.Column(db.Text)

class Dean(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.Text, index=True) # 文章标题
    time_push = db.Column(db.Text)
    push_time = db.Column(db.DateTime) # 发布时间
    url = db.Column(db.Text) # 链接
    from_place = db.Column(db.Text) # 来源
    type = db.Column(db.Text) # 类型



class user_sub(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    place = db.Column(db.Text) # 平台支持-发送到哪个平台上,可选：qq,fs
    group = db.Column(db.Integer,default=None) # 群组
    sub_place = db.Column(db.Text) # 订阅信息,确定渠道网站
    sub_type = db.Column(db.Text) # 订阅类型


    # 飞书字段设置
    user_phone = db.Column(db.Text) # 用户手机号
    user_email = db.Column(db.Text) # 用户邮箱
    user_open_id = db.Column(db.Text) # 用户openid
    user_open_id_ts = db.Column(db.Integer) # 用户openid时间戳（到什么时候失效）

class fs_app_info(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    tenant_access_token = db.Column(db.Text) # 企业内部应用的access_token
    token_expires = db.Column(db.Integer) # access_token过期时间