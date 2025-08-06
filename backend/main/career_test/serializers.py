from rest_framework import serializers #type: ignore
from .models import Category, Question, Option
import bleach #type: ignore

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'label', 'text', 'match_text', 'image', 'is_correct']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        # Hide 'is_correct' for unauthenticated or non-admin users
        if not (user and user.is_authenticated and getattr(user, 'role', '') == 'Admin'):
            data.pop('is_correct', None)
        return data


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    category_name = serializers.CharField(source='category.name', read_only=True)
    correct_answer = serializers.CharField(write_only=True, required=False, allow_null=True)
    true_false_answer = serializers.BooleanField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'user_group',
            'category', 'category_name', 'explanation', 'options',
            'correct_answer', 'true_false_answer', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'correct_answer', 'true_false_answer','created_at', 'updated_at']  # These are write-only
        # ordering = ['id']

    def validate(self, data):
        options = self.initial_data.get("options", [])
        question_type = data.get("question_type")

        # Validate based on question type
        if question_type == Question.QuestionType.MCQ:
            if not options:
                raise serializers.ValidationError("MCQ must have options.")
            if not any(opt.get("is_correct") for opt in options):
                raise serializers.ValidationError("MCQ must have at least one correct answer.")

        elif question_type == Question.QuestionType.MATCHING:
            if len(options) < 2:
                raise serializers.ValidationError("Matching questions must have at least 2 pairs.")
            for opt in options:
                if not opt.get("text") or not opt.get("match_text"):
                    raise serializers.ValidationError(
                        "Matching questions must have both 'text' and 'match_text'."
                    )
                if not opt.get("is_correct"):
                    raise serializers.ValidationError(
                        "All matching pairs must be marked as correct (is_correct=True)."
                    )

        elif question_type == Question.QuestionType.TRUE_FALSE:
            if 'true_false_answer' not in data:
                raise serializers.ValidationError("True/False questions require a true_false_answer.")
            if options:
                raise serializers.ValidationError("True/False questions should not have options.")

        elif question_type in [Question.QuestionType.SHORT_ANSWER, Question.QuestionType.FILL_BLANK]:
            if 'correct_answer' not in data:
                raise serializers.ValidationError(
                    f"{question_type} questions require a correct_answer field."
                )
            if options:
                raise serializers.ValidationError(
                    f"{question_type} questions should not have options."
                )

        return data

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        correct_answer = validated_data.pop('correct_answer', None)
        true_false_answer = validated_data.pop('true_false_answer', None)
        question_type = validated_data.get('question_type')

        if correct_answer:
            correct_answer = bleach.clean(correct_answer, tags=[], attributes={}, strip=True)
        
        question = Question.objects.create(
            **validated_data,
            correct_answer=correct_answer,
            true_false_answer=true_false_answer
        )
        
        if question_type == Question.QuestionType.MATCHING:
            # For matching questions, we'll create pairs differently
            for i in range(0, len(options_data), 1):
                option_data = options_data[i]
                # Create the left item option
                Option.objects.create(
                    question=question,
                    label=option_data['label'],
                    text=option_data['text'],
                    match_text=option_data['match_text'],
                    is_correct=True
                )
                # The reverse matching will be handled by querying the options
        else:
            # Handle other question types normally
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)

        return question

        # # Only create options for question types that need them
        # if validated_data['question_type'] in [
        #     Question.QuestionType.MCQ,
        #     Question.QuestionType.MATCHING
        # ]:
        #     for option_data in options_data:
        #         Option.objects.create(question=question, **option_data)

        # return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', None)
        correct_answer = validated_data.pop('correct_answer', None)
        true_false_answer = validated_data.pop('true_false_answer', None)

        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if correct_answer is not None:
            instance.correct_answer = bleach.clean(correct_answer, tags=[], attributes={}, strip=True)
        
        # Update correct answer fields
        if correct_answer is not None:
            instance.correct_answer = correct_answer
        if true_false_answer is not None:
            instance.true_false_answer = true_false_answer
        
        instance.save()

        # Handle options update
        if options_data is not None:
            instance.options.all().delete()
            if validated_data['question_type'] in [
                Question.QuestionType.MCQ,
                Question.QuestionType.MATCHING
            ]:
                for option_data in options_data:
                    Option.objects.create(question=instance, **option_data)

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Include correct answer for certain question types in the response
        if instance.question_type in [
            Question.QuestionType.TRUE_FALSE,
            Question.QuestionType.SHORT_ANSWER,
            Question.QuestionType.FILL_BLANK
        ]:
            request = self.context.get('request')
            user = getattr(request, 'user', None)
            
            # Only show correct answers to admins
            if user and user.is_authenticated and getattr(user, 'role', '') == 'Admin':
                if instance.question_type == Question.QuestionType.TRUE_FALSE:
                    data['true_false_answer'] = instance.true_false_answer
                else:
                    data['correct_answer'] = instance.correct_answer
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']