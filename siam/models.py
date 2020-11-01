from uuid import uuid4
import boto3
from boto3.dynamodb.conditions import Key, Attr

from .config import TABLE, DYNAMODB_CONFIG

dynamodb = boto3.resource("dynamodb", **DYNAMODB_CONFIG)
table = dynamodb.Table(TABLE)


class Model:

    @classmethod
    def build_id(cls, source_id: str):
        return f"{cls.__name__.upper()}#{source_id}"


class User(Model):

    @classmethod
    def get_policies(cls, user_id):
        response = table.query(KeyConditionExpression=cls.build_id(user_id))
        return response["Items"]


class Group(Model):

    @classmethod
    def add_user(cls, group_id, user_id):
        table.put_item(
            Item=dict(PK=User.build_id(user_id), SK=cls.build_id(group_id))
        )

    @classmethod
    def remove_user(cls, group_id, user_id):
        table.delete_item(
            Key=dict(PK=User.build_id(user_id), SK=cls.build_id(group_id))
        )

    @classmethod
    def add_policy(cls, group_id, policy_id):
        table.put_item(
            Item=dict(PK=cls.build_id(group_id), SK=Policy.build_id(policy_id))
        )

    @classmethod
    def remove_policy(cls, group_id, policy_id):
        table.delete_item(
            Key=dict(PK=cls.build_id(group_id), SK=Policy.build_id(policy_id))
        )


class Policy(Model):

    @classmethod
    def create(cls, statements):
        policy_id = cls.build_id(str(uuid4()))
        table.put_item(
            Item=dict(PK=policy_id, SK=policy_id, data=statements)
        )

    @classmethod
    def delete(cls, policy_id):
        policy_id = cls.build_id(policy_id)
        table.delete_item(
            Key=dict(PK=policy_id, SK=policy_id)
        )
