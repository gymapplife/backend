import pytz
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
            'calories',
        )


class CreateFoodLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodLog
        fields = (
            'id',
            'profile',
            'name',
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
            "2017-11-14": {
                "BREAKFAST": [],
                "DINNER": [
                    {
                        "id": 1,
                        "name": "asd",
                        "calories": 1,
                        "time": "16:58:11.774818"
                    }
                ],
                "LUNCH": [],
                "SNACK": []
            }
        }
        ```
        """
        food_logs = FoodLog.objects.filter(
            profile=request.profile,
        ).order_by('created').all()

        result = {}

        timezone = pytz.timezone('US/Eastern')
        for food_log in food_logs:
            created = food_log.created.astimezone(timezone)
            date = str(created.date())
            time = str(created.time())
            if date not in result:
                result[date] = {k: [] for k in FoodLog.Meal._fields}
            data = FoodLogSerializer(food_log).data
            data['time'] = time
            result[date][food_log.meal].append(data)

        return Response(result)

    def post(self, request):
        """Create a food log

        #### Body Parameters
        * name: string
        * calories: string
        * meal: string

        #### Sample Response
        ```
        {
            "id": 1,
            "profile": 1,
            "name": "asd",
            "created": "2017-11-14T21:58:11.774818Z",
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
