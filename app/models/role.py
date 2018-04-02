from app import db


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):

    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True) # 是否为默认角色
    permissions = db.Column(db.Integer) # 用户权限
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = dict(
            User=[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
            ],
            Moderator=[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE,
            ],
            Administrator=[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE,
                Permission.ADMIN,
            ],
        )
        default_role = 'User'
        # 遍历保存所有 role 的字典
        for role in roles:
            # 在数据库中查询这个 role
            r = Role.query.filter_by(name=role).first()
            # 如果数据库中没有储存这个 role
            if r is None:
                # 新建一个此 role 的对象
                r = Role(name=role)
            # 如果数据库中储存这个 role
            else:
                # 重置这个 role 的权限
                role.reset_permissions()
            # 更新这个 role 的权限
            for permission in roles[role]:
                role.add_permission(permission)
            # 判断这个 role 是否为默认, 并赋值
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission):
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, permission):
        return self.permissions

    def __repr__(self):
        return '<Role {0}>'.format(self.name)
