from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User

from restapi.models import Category, Groups, UserExpense, Expenses


class UserSerializer(ModelSerializer):
    """Serializer for the User model"""
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta(object):
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CategorySerializer(ModelSerializer):
    """Serializer for the Category model"""
    class Meta(object):
        model = Category
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    """Serializer for the Group model"""
    members = UserSerializer(many=True, required=False)

    class Meta(object):
        model = Groups
        fields = '__all__'


class UserExpenseSerializer(ModelSerializer):
    """Serializer for the UserExpense model"""
    class Meta(object):
        model = UserExpense
        fields = ['user', 'amount_owed', 'amount_lent']


class ExpensesSerializer(ModelSerializer):
    """Serializer for the Expenses model"""
    users = UserExpenseSerializer(many=True, required=True)

    def create(self, validated_data):
        """Creates expenses from validated_data"""
        expense_users = validated_data.pop('users')
        expense = Expenses.objects.create(**validated_data)
        for eu in expense_users:
            UserExpense.objects.create(expense=expense, **eu)
        return expense

    def update(self, instance, validated_data):
        """Updates an instance of expense"""
        user_expenses = validated_data.pop('users')
        instance.description = validated_data['description']
        instance.category = validated_data['category']
        instance.group = validated_data.get('group', None)
        instance.total_amount = validated_data['total_amount']

        if user_expenses:
            instance.users.all().delete()
            UserExpense.objects.bulk_create(
                [
                    user_expense(expense=instance, **user_expense)
                    for user_expense in user_expenses
                ],
            )
        instance.save()
        return instance

    def validate(self, attrs):
        """Validates the that a single user must appear single time"""
        user_ids = [user['user'].id for user in attrs['users']]
        if len(set(user_ids)) != len(user_ids):
            raise ValidationError('Single user appears multiple times')

        return attrs

    class Meta(object):
        model = Expenses
        fields = '__all__'
