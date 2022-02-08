from select import select
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
#class model for controller
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name=data['first_name']
        self.last_name= data['last_name']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.friends=[]
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        result= connectToMySQL('friendships').query_db(query)
        users=[]
        for user in result:
            users.append(cls(user))
        return users
    @classmethod
    def get_one(cls, data):
        query= "SELECT * FROM users where id=%(id)s;"
        return connectToMySQL('friendships').query_db(query, data)

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , NOW() , NOW() );"
        return connectToMySQL('friendships').query_db( query, data )
    @classmethod
    def new_friend(cls, data ):
        query = "INSERT INTO friendships (user_id, friend_id, created_at, updated_at) VALUES ( %(user)s , %(friend)s, NOW(), NOW() );"
        return connectToMySQL('friendships').query_db( query, data )
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = (%(id)s);"
        return connectToMySQL('friendships').query_db(query, data)
    @classmethod
    def get_all_friendships(cls):
        query = """
            SELECT * 
            FROM friendships
            LEFT JOIN users 
            ON friendships.user_id = users.id
            LEFT JOIN users friend 
            ON friendships.friend_id = friend.id
            ORDER BY users.last_name ASC;
        """
        result = connectToMySQL('friendships').query_db(query)
        all_friendships=[]
        for row in result:
            user=cls(row)    
            print(["users.id"])
            friend_data = {
                "id" : row["friend.id"],
                "first_name" : row["friend.first_name"],
                "last_name" : row["friend.last_name"],
                "created_at": row["friend.created_at"],
                "updated_at": row["friend.updated_at"]
            }
            user.friends.append(User(friend_data))
            all_friendships.append(user)
        return all_friendships
    @staticmethod
    def validate_friendship ( data ):
        is_valid = True
        friendships=User.get_all_friendships()
        print(friendships[0].id)
        if data["user"]==data["friend"]:
            is_valid=False
            flash("User cannot be friends with themselves")
        for user in friendships:
            if user.id == int(data["user"]):
                print("yes!!!!!!")
                for friend in user.friends:
                    if friend.id==int(data["friend"]):
                        flash("this friendship already exists")
                        is_valid=False        
        return is_valid

        # @classmethod
        # def update(cls, data):
        #     query = "UPDATE users SET first_name=%(fname)s, last_name=%(lname)s WHERE id = %(id)s;"
        #     return connectToMySQL('friendships').query_db( query, data )

