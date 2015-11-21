drop table if exists users;
create table users (
  user_id integer primary key autoincrement,
  email text not null
);


drop table if exists courses;
create table courses (
  course_id integer primary key autoincrement,
  status integer not null
);

drop table if exists follows;
create table follows (
  id integer primary key autoincrement,
  follower_user_id integer not null references users(user_id),
  followed_course_id integer not null references course(course_id)
);

