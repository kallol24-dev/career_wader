from rest_framework import serializers
from .models import Category, Question, TestType

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']




class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = ['id', 'name', 'category', 'category_id']
    
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'category', 'category_id', 'user_group', 'option_a_text', 'option_a_image',
                  'option_b_text', 'option_b_image', 'option_c_text', 'option_c_image',
                  'option_d_text', 'option_d_image', 'option_e_text', 'option_e_image',
                  'option_f_text', 'option_f_image']
    category = TestTypeSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TestType.objects.all(), source='category', write_only=True
    )