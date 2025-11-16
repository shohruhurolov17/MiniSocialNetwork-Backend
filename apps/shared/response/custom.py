from rest_framework import response, status
from typing import Union, List, Dict


class CustomResponse(response.Response):

    def __init__(
            self, 
            success: bool = True, 
            message: Union[str, None] = None, 
            data: Union[Dict, List, None] = None, 
            status: status = status.HTTP_200_OK,
            **kwargs
        ):

        response = {
            'success': success,
            **({'message': message} if message else {}),
            **({'data': data} if data else {})
        }

        super().__init__(
            response,
            status=status,
            **kwargs
        )
        