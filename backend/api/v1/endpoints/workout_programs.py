from api.views import ProfileAuthedAPIView


class WorkoutProgramsView(ProfileAuthedAPIView):

    def get(self, request):
        """Get a list of workout programs available to the user

        #### Sample Response
        ```

        ```
        """
        raise Exception()
