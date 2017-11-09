from api.views import ProfileAuthedAPIView
from db_models.models.food_log import FoodLog
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from utils.models import get_model_for_profile


class FoodLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodLog
        fields = (
            'id',
            'name',
            'created',
            'calories',
        )


class CreateFoodLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodLog
        fields = (
            'id',
            'profile',
            'name',
            'week',
            'day',
            'created',
            'calories',
            'meal',
        )


class FoodLogsView(ProfileAuthedAPIView):

    def get(self, request):
        """Get all of your food logs

        #### Sample Response
        ```
        {
            "1": {
                "1": {
                    "DINNER": [
                        {
                            "id": 1,
                            "name": "Pizza",
                            "created": "2017-11-09T04:04:24.927630Z",
                            "calories": 1000
                        }
                    ]
                }
            }
        }
        ```
        """
        food_logs = FoodLog.objects.filter(
            profile=request.profile,
        ).all()

        result = {}

        for food_log in food_logs:
            if food_log.week not in result:
                result[food_log.week] = {}
            if food_log.day not in result[food_log.week]:
                result[food_log.week][food_log.day] = {}
            if food_log.meal not in result[food_log.week][food_log.day]:
                result[food_log.week][food_log.day][food_log.meal] = []

            result[food_log.week][food_log.day][food_log.meal].append(
                FoodLogSerializer(food_log).data,
            )

        return Response(result)

    def post(self, request):
        """Create a food log

        #### Body Parameters
        * name: string
        * week: string
        * day: string
        * calories: string
        * meal: string

        #### Sample Response
        ```
        {
            "id": 7,
            "profile": 1,
            "name": "asd",
            "week": 1,
            "day": 1,
            "created": "2017-11-09T04:21:04.122415Z",
            "calories": 1,
            "meal": "DINNER"
        }
        ```
        """
        if request.data:
            request.data._mutable = True
            request.data['profile'] = request.profile.pk
            request.data._mutable = False

        serializer = CreateFoodLogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        errors = dict(serializer.errors)
        errors.pop('profile', None)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class FoodLogView(ProfileAuthedAPIView):

    def delete(self, request, pk):
        """Delete a food log
        """
        food_log = get_model_for_profile(FoodLog, request.profile, pk=pk)

        food_log.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
