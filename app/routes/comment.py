# from flask import (
#     render_template,
#     flash,
#     redirect,
#     url_for,
#     request,
#     Blueprint,
# )
# from flask_login import (
#     current_user,
#     login_user,
#     logout_user,
#     login_required,
# )
# from app import db
# from app.forms.post import NewPostForm, EditPostForm
# from app.forms.comment import PostCommentForm
# from app.models.role import Permission
# from app.models.user import User
# from app.models.post import Post
# from app.models.comment import PostComment
#
#
# main = Blueprint('comment', __name__)
#
#
# @main.route('/add/<int:post_id>', methods=['POST'])
# @login_required
# def new_comment(post_id):
#     form = PostCommentForm()
#     comment = PostComment(
#         body=form.body.data,
#         author_id=current_user(),
#         post_id=post_id,
#     )
#     db.session.add(comment)
#     db.session.commit()
#     return url_for('post.view_post', id=post_id)