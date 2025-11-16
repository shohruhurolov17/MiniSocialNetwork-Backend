from rest_framework.views import APIView
from apps.users.serializers import UserDetailSerializer
from apps.shared.response import CustomResponse
from rest_framework import status


class UserDetailView(APIView):

    serializer_class = UserDetailSerializer

    def get(self, request):

        user = request.user

        serializer = self.serializer_class(user)

        return CustomResponse(data=serializer.data)

    def patch(self, request):

        user = request.user

        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return CustomResponse(
                message='Successfully updated',
                data=serializer.data
            )
        
        else:

            error_message = str(serializer.error_messages)
            
            return CustomResponse(
                success=False,
                message=error_message,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):

        user = request.user

        user.delete()

        return CustomResponse(status=status.HTTP_204_NO_CONTENT)