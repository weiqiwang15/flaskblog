from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    Blueprint,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from app import db
from app.forms.post import NewPostForm, EditPostForm
from app.forms.comment import PostCommentForm
from app.models.role import Permission
from app.models.user import User
from app.models.post import Post
from app.models.comment import PostComment


from app.models.role import Permission

main = Blueprint('post', __name__)


# 将 Permission 类加入模板上下文
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/<int:id>', methods=['GET', 'POST'])
def view_post(id):
    post = Post.query.get_or_404(id)
    form = PostCommentForm()
    comments = post.comments.order_by(PostComment.time_created.asc())
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = PostComment(
                body=form.body.data,
                post=post,
                author=current_user._get_current_object(),
            )
            db.session.add(comment)
            db.session.commit()
            flash('您已发表评论')
            return redirect(url_for('.view_post', id=id))
    else:
        return render_template('post/view_post.html', id=id, post=post, comments=comments, form=form)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                body=form.title.data,
                author=current_user._get_current_object(),
            )
            db.session.add(post)
            db.session.commit()
            flash('恭喜, 您已成功发表文章!')
            return redirect(url_for('.view_post', id=post.id))
        else:
            flash('您提交的表格有误, 请修改后重新发表!')
            return redirect(url_for('.new_post', form=form))
    else:
        return render_template('post/new_post.html', form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = EditPostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            db.session.add(post)
            db.session.commit()
            flash('恭喜, 您已成功修改文章!')
            return redirect(url_for('.view_post', id=post.id))
        else:
            flash('您提交的表格有误, 请修改后重新发表!')
            return redirect(url_for('.edit_post', form=form))
    else:
        form.title.data = post.title
        form.body.data = post.body
        return render_template('post/edit_post.html', form=form)


@main.route('/delete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    comments = post.comments
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home.index'))
