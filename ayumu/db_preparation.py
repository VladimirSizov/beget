# https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27/amp/
from db_connect import *


create_dictionary_words = """
INSERT INTO
training_translation (eng, rus)
VALUES
('be', 'быть'),
('of', 'из'),
('of', 'о'),
('and', 'и'),
('in', 'в'),
('in', 'на'),
('to', 'к'),
('to', 'в'),
('to', 'до'),
('to', 'на'),
('to', 'для'),
('have', 'иметь'),
('it', 'это'),
('it', 'он'),
('it', 'она'),
('it', 'него'),
('for', 'для'),
('for', 'за'),
('for', 'на'),
('I', 'я'),
('that', 'тот'),
('that', 'что'),
('you', 'ты'),
('you', 'вы'),
('you', 'тебя'),
('you', 'вас'),
('you', 'вам'),
('you', 'вами'),
('he', 'он'),
('on', 'на'),
('on', 'по'),
('on', 'о'),
('on', 'в'),
('with', 'с'),
('do', 'делать'),
('at', 'на'),
('at', 'в'),
('at', 'при'),
('by', 'по'),
('by', 'на'),
('not', 'не'),
('not', 'нет'),
('this', 'это'),
('this', 'этот'),
('this', 'эта'),
('but', 'но'),
('but', 'а'),
('from', 'из'),
('from', 'от'),
('from', 'с'),
('they', 'они'),
('his', 'его'),
('his', 'свой'),
('his', 'своё'),
('she', 'она'),
('or', 'или'),
('which', 'который'),
('which', 'какой'),
('as', 'как'),
('as', 'в качестве'),
('we', 'мы'),
('say', 'сказать'),
('say', 'говорить'),
('say', 'слово'),
('say', 'мнение');
"""

execute_query(connection, create_dictionary_words)

'''

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER,
	gender TEXT,
	nationality TEXT
);
"""

create_posts_table = """
CREATE TABLE IF NOT EXISTS posts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
description TEXT NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

create_comments_table = """
CREATE TABLE IF NOT EXISTS comments (
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT NOT NULL,
user_id INTEGER NOT NULL,
post_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

create_likes_table = """
CREATE TABLE IF NOT EXISTS likes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
post_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

# делаем запрос в БД на создание таблиц
execute_query(connection, create_users_table)
execute_query(connection, create_posts_table)
execute_query(connection, create_comments_table)
execute_query(connection, create_likes_table)


""" ВСТАВКА ЗАПИСЕЙ """

create_users = """
INSERT INTO
users (name, age, gender, nationality)
VALUES
('James', 25, 'male', 'USA'),
('Leila', 32, 'female', 'France'),
('Brigitte', 35, 'female', 'England'),
('Mike', 40, 'male', 'Denmark'),
('Elizabeth', 21, 'female', 'Canada');
"""

create_posts = """
INSERT INTO
posts (title, description, user_id)
VALUES
("Happy", "I am feeling happy today", 1),
("Hot water", "The weather is very hot today", 2),
("Help", "I need some help with my work", 2),
("Great News", "I am getting married", 1)
("Interesting game", "It was a fantastic game of tennis", 5),
("Party", "Anyone up for a late-night party today?", 3);
"""

create_comments = """
INSERT INTO
comments (text, user_id, post_id)
VALUES
("Count me in", 1, 6),
("Whats sort of help?", 5, 3),
("I was rooting for Nadal though", 4, 5),
("Help with your thesis?", 2, 3),
("Many congratulations", 5, 4);
"""

create_likes = """
INSERT INTO
likes (user_id, post_id)
VALUES
(1, 6),
(2, 3),
(1, 5),
(5, 4),
(2, 4),
(4, 2),
(3, 6);
"""

execute_query(connection, create_users)
execute_query(connection, create_posts)
execute_query(connection, create_comments)
execute_query(connection, create_likes)



# SELECT

print()
select_users = "SELECT * from users"
users = execute_read_query(connection, select_users)
for user in users:
	print(user)

# JOIN

print()
select_users_posts = """
SELECT
	users.id,
	users.name,
	posts.description
FROM
	posts
	INNER JOIN users ON users.id = posts.user_id
"""
users_posts = execute_read_query(connection, select_users_posts)
for user_post in users_posts:
	print(user_post)


print()
select_posts_comments_users = """
SELECT
	posts.description as post,
	text as comment,
	name
FROM
	posts
	INNER JOIN comments ON posts.id = comments.post_id
	INNER JOIN users ON users.id = comments.user_id
"""
posts_comments_users = execute_read_query(connection, select_posts_comments_users)
for posts_comments_user in posts_comments_users:
	print(posts_comments_user)

print()
cursor = connection.cursor()
cursor.execute(select_posts_comments_users)
cursor.fetchall()
column_names = [description[0] for description in cursor.description]
print(column_names)

# WHERE
# мы выполним SELECT-запрос, который возвращает текст поста
# и общее количество лайков, им полученных

print()
select_post_likes = """
SELECT
	description as Post,
	COUNT(likes.id) as Likes
FROM
	likes,
	posts
WHERE
	posts.id = likes.post_id
GROUP BY
	likes.post_id
"""
post_likes = execute_read_query(connection, select_post_likes)
for post_like in post_likes:
	print(post_like)


""" ОБНОВЛЕНИЕ ЗАПИСЕЙ ТАБЛИЦЫ """

print()
# запрашиваем результат содержания статьи id=2
select_post_description = "SELECT description FROM posts WHERE id = 2"
post_description = execute_read_query(connection, select_post_description)
print(post_description)
# обновляем содержание статьи id=2
update_post_description = """
UPDATE
	posts
SET
	description = 'The weather is very hot today'
WHERE
id = 2
"""
#description = 'The weather has become pleasant now'
#description = 'The weather is very hot today'
execute_query(connection, update_post_description)
# проверяем новое содержание статьи id=2
select_post_description = "SELECT description FROM posts WHERE id = 2"
post_description = execute_read_query(connection, select_post_description)
for description in post_description:
	print(description)


""" УДАЛЕНИЕ ЗАПИСЕЙ ИЗ ТАБЛИЦЫ """

print("---")
# создаем комментарий id=5

create_comments = """
INSERT INTO
comments (id, text, user_id, post_id)
VALUES
(5, "Many congratulations", 1, 4);
"""
execute_query(connection, create_comments)

# получаем комментарий id=5
select_comment = """
SELECT
	text
FROM
	comments
WHERE
	id = 5"""
text_comment = execute_read_query(connection, select_comment)
print(text_comment)
# удаляем комментарий id=5

delete_comment = "DELETE FROM comments WHERE id = 5"
execute_query(connection, delete_comment)
# перепроверяем остался ли комментарий id=5
select_comment = "SELECT text FROM comments WHERE id = 5"
text_comment = execute_read_query(connection, select_comment)
print(text_comment)
'''