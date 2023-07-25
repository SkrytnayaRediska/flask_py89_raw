from flask import Flask, render_template, url_for, \
    request, redirect, flash
import psycopg2


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'


def get_connection(db_name):
    connection = psycopg2.connect(
        dbname=db_name,
        host='127.0.0.1',
        port='5432',
        user='postgres',
        password='12345'
    )
    return connection


def get_post(post_id):
    with get_connection('py89_blog_raw') as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM posts WHERE id = {post_id}")
            post = cursor.fetchone()
    return {
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'created': post[3]
            }


@app.route('/')
def index():
    with get_connection('py89_blog_raw') as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM posts""")
            posts = cursor.fetchall()

    posts_data = list()
    for post in posts:
        posts_data.append(
            {
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'created': post[3]
            }
        )
    return render_template('index.html', posts=posts_data)


@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    post = get_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Title and content are both required')
        else:
            with get_connection('py89_blog_raw') as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""UPDATE posts 
                                        SET title = '{title}',
                                        content = '{content}'
                                        WHERE id = {post_id}""")
                    conn.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/<int:post_id>/delete', methods=['POST',])
def delete(post_id):
    post = get_post(post_id)
    with get_connection('py89_blog_raw') as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"""DELETE FROM posts 
                               WHERE id = {post_id}""")
            conn.commit()
    flash(f"Post {post['title']} was successfully deleted")
    return redirect(url_for('index'))


@app.route('/create-post', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Title and content are both required')
        else:
            with get_connection('py89_blog_raw') as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                            INSERT INTO posts (title, content) 
                            VALUES ('{title}', '{content}')
                    """)
                    conn.commit()
            return redirect(url_for('index'))
    return render_template('create.html', post=post)


app.run(debug=True)
