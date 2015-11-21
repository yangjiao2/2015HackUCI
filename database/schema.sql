drop table if exists entries;
create table users (
  user_id integer primary key autoincrement,
  email text not null
);


create table follows (
  id integer primary key autoincrement,
  follower_user_id integer not null foreign key references users(user_id),
  followed_course_id integer not null foreign key references course(course_id)
  # foreign key
);


create table course (
  course_id integer primary key autoincrement,
  status integer not null
);