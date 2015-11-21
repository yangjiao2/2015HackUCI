from database import *
FULL = 0
OPEN = 1
get_db()
print (get_notified_users(12000))
print (get_courses())
print (add_following_course("'hua@uci.edu'", 12000))
print (add_following_course("'huh@uci.edu'", 12000))
print (add_following_course("'hub@uci.edu'", 12000))
print (add_following_course("'hub@uci.edu'", 12001))
print (get_courses())
print (get_notified_users(12000))
print (get_notified_users(12001))
print (delete_following_course("'hub@uci.edu'", 12000))
print (get_courses())
print (get_notified_users(12000))
print (get_notified_users(12001))


print (is_status_changed(12000, FULL))
print get_courses_tuple()
print (is_status_changed(12000, OPEN))
print get_courses_tuple()
print (is_status_changed(12000, OPEN))
print get_courses_tuple()
