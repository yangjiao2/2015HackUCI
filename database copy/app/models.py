from app import db
from . import db

FULL = 0
OPEN = 1

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    courses = db.relationship('Course', backref='courses', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    def follow(self, course):
    	#  calles when user want to change user's followed class list
        if not self.is_following(course):
            f = Follow(follower_id=self, followed_course_id =course)
            db.session.add(f)

    def unfollow(self, course):
    	#  calles when user want to change user's followed class list
        f = self.followed.filter_by(followed_course_id=course).first()
        if f:
            db.session.delete(f)

    def is_following(self, course):
    	# checks if user is following a particular couse
        return self.followed.filter_by(
            ffollowed_course_id=course).first() is not None


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                            primary_key=True)
    followed_course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'),
                            primary_key=True)

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)

    def is_available(self, check_course_id):
    	return Course.query.filter_by(course_id=check_course_id).first().status == OPEN

    def change_status(self, check_course_id, changed_status):
    	course = Course.query.filter_by(course_id=check_course_id).first()
    	course.status = changed_status

    def notify_user(self, changed_course_id):
    	# get all the user's email that follows changed_course_id
    	# calls email-sending function


    def is_status_changed(self, course_id)):
    	# get the course's status by given course_id


