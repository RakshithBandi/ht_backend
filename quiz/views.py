from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Question, UserResponse, UserScore, QuizSettings
from .serializers import QuestionSerializer, UserResponseSerializer, UserScoreSerializer, QuizSettingsSerializer
from api.permissions import IsAdminOrManagerOrReadOnly

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManagerOrReadOnly]

    def get_queryset(self):
        year = self.request.query_params.get('year')
        queryset = Question.objects.all().order_by('-created_at')
        if year:
            queryset = queryset.filter(year=year)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def answer(self, request, pk=None):
        question = self.get_object()
        user = request.user
        selected_answer = request.data.get('selected_answer')

        if not selected_answer:
            return Response({'error': 'selected_answer is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already answered
        if UserResponse.objects.filter(user=user, question=question).exists():
            return Response({'error': 'You have already answered this question'}, status=status.HTTP_400_BAD_REQUEST)

        # Check expiration
        from django.utils import timezone
        import datetime
        expiration_time = question.created_at + datetime.timedelta(minutes=30)
        if timezone.now() > expiration_time:
             return Response({'error': 'Time limit expired for this question'}, status=status.HTTP_400_BAD_REQUEST)

        is_correct = (selected_answer == question.correct_answer)

        try:
            response = UserResponse.objects.create(
                user=user,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct
            )
            
            # Update score - ensure UserScore exists for every participant
            score, created = UserScore.objects.get_or_create(user=user)
            if is_correct:
                score.total_points += 1
                score.save()
            # If incorrect, we still created the score record with default=0 if it didn't exist

            return Response({
                'is_correct': is_correct,
                'correct_answer': question.correct_answer, # Return correct answer for feedback
                'message': 'Correct answer!' if is_correct else 'Incorrect answer'
            })

        except IntegrityError:
             return Response({'error': 'Duplicate answer submission'}, status=status.HTTP_400_BAD_REQUEST)

class UserScoreViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='my-score')
    def my_score(self, request):
        try:
            score, created = UserScore.objects.get_or_create(user=request.user)
            serializer = UserScoreSerializer(score)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        try:
            # Check permissions
            is_admin = request.user.groups.filter(name__in=['Admin', 'Manager']).exists() or request.user.is_superuser
            
            # Get settings
            settings = QuizSettings.objects.first()
            if not settings:
                settings = QuizSettings.objects.create(is_leaderboard_visible=False)
                
            if not settings.is_leaderboard_visible and not is_admin:
                return Response({"detail": "Leaderboard is currently hidden"}, status=status.HTTP_403_FORBIDDEN)

            scores = UserScore.objects.select_related('user').order_by('-total_points')[:10]
            serializer = UserScoreSerializer(scores, many=True)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def get_quiz_settings(self, request):
        try:
            settings = QuizSettings.objects.first()
            if not settings:
                settings = QuizSettings.objects.create(is_leaderboard_visible=False)
            return Response(QuizSettingsSerializer(settings).data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='toggle-leaderboard')
    def toggle_leaderboard(self, request):
        try:
            # Only admin/manager
            is_admin = request.user.groups.filter(name__in=['Admin', 'Manager']).exists() or request.user.is_superuser
            if not is_admin:
                 return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

            settings = QuizSettings.objects.first()
            if not settings:
                settings = QuizSettings.objects.create(is_leaderboard_visible=False)
            
            settings.is_leaderboard_visible = not settings.is_leaderboard_visible
            settings.save()
            return Response(QuizSettingsSerializer(settings).data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
