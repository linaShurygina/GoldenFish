from passlib.hash import bcrypt

from backend.config import session
from backend.storage.BaseStorage import BaseStorage
from backend.models.User import User
from backend.models.Friend import friends_association
from backend.models.FriendRequest import friend_requests_association


class UserStorage(BaseStorage):
    model = User

    def is_friends(self, user1_id, user2_id):
        try:
            res = self.model.query.join(friends_association).filter(friends_association.c.friend_one_id == user1_id,
                                                                    friends_association.c.friend_two_id == user2_id).count()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return res > 0

    @classmethod
    def add_friend(cls, user, friend):
        try:
            user.friends.append(friend)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def delete_friend(cls, user, friend):
        try:
            user.friends.remove(friend)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def delete_request(cls, recipient, sender):
        try:
            recipient.friend_requests.remove(sender)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def get_all(self):
        try:
            users = self.model.query.all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return users

    def search_by_username(self, username):
        try:
            search_list = self.model.query.filter(self.model.username.like('%' + username + '%')).all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return search_list

    def get_friends(self, user_id):
        try:
            user_friends = self.model.query.join(friends_association, (friends_association.c.friend_one_id == user_id))\
                                            .filter(self.model.id == friends_association.c.friend_two_id)\
                                            .all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return user_friends

    def get_friend_requests(self, user_id):
        try:
            user_friend_requests = self.model.query.join(friend_requests_association, (friend_requests_association.c.recipient_id == user_id))\
                                            .filter(self.model.id == friend_requests_association.c.sender_id)\
                                            .all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return user_friend_requests

    def get_by_id(self, user_id):
        try:
            user = self.model.query.filter_by(id=user_id).first()
            if not user:
                raise Exception('Not found user')
            session.commit()
        except Exception:
            session.rollback()
            raise
        return user

    def get_by_username(self, username):
        try:
            user = self.model.query.filter_by(username=username).first()
            if not user:
                raise Exception('Not found user')
            session.commit()
        except Exception:
            session.rollback()
            raise
        return user

    def authenticate(self, email, password):
        user = self.model.query.filter_by(email=email).first()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this email or/and password')
        return user