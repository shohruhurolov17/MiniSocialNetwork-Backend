from rest_framework.views import APIView
from apps.users.serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserDetailSerializer
)
from apps.shared.response import CustomResponse
from rest_framework import status
from apps.users.models import CustomUser
from django.core import signing
from rest_framework.exceptions import NotFound
from apps.users.tasks import send_verification_url_to_email


class LoginView(APIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = CustomUser.objects \
                .filter(email=email) \
                .first()
            
            if user and user.check_password(password):

                data = UserDetailSerializer(user).data

                return CustomResponse(
                    message='Login successful',
                    data=data
                )

            else:

                return CustomResponse(
                    success=False,
                    message='Incorrect email or password.',
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        else:

            error_message = str(serializer.errors)

            return CustomResponse(
                success=False,
                message=error_message,
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = LogoutSerializer

    def post(self, request):

        pass


class RegisterView(APIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            data = UserDetailSerializer(user).data

            return CustomResponse(
                message='Register successful',
                data=data,
                status=status.HTTP_201_CREATED
            )

        else:

            error_message = str(serializer.errors)

            return CustomResponse(
                success=False,
                message=error_message,
                status=status.HTTP_200_OK
            )


class VerifyEmailView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get_object(self, id):

        try:

            return CustomUser.objects \
                .get(id=id)
        
        except CustomUser.DoesNotExist:
            raise NotFound('User not found')

    def get(self, request, signed_data):

        try:

            data = signing.loads(signed_data, max_age=60 * 15)

            id = data.get('user_id')

            user = self.get_object(id)

            if not user.is_verified:

                user.is_verified = True

                user.save(update_fields=['is_verified'])

            return CustomResponse(message='Email verified')

        except signing.BadSignature:

            return CustomResponse(
                success=False,
                message='Invalid link',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except signing.SignatureExpired:

            return CustomResponse(
                success=False,
                message='Link expired',
                status=status.HTTP_410_GONE
            )


class SendVerificationEmailView(APIView):

    def post(self, request):

        user = request.user

        if not user.is_verified:

            send_verification_url_to_email.apply_async([
                user.email,
                user.id
            ])

            return CustomResponse(message='Confirmation email sent')

        return CustomResponse(
            message='Email already verified',
            status=status.HTTP_400_BAD_REQUEST
        )