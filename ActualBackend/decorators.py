from functools import wraps
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from datetime import datetime, timedelta
import jwt


def user_check(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        #         token = args[0].headers["Authorization"].split("Bearer ")[1]
        #         print("args and kwargs", args[0].headers["Authorization"].split("Bearer ")[1], type(args))
        #         if token:
        #             try:
        #                 decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
        #                 expiration_timestamp = decoded_token.get('exp')
        #                 if expiration_timestamp:
        #                     expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
        #                     if datetime.utcnow() > expiration_datetime:
        #                         return JsonResponse({'error': 'Token has expired.'}, status=401)
        #                 request.decoded_token = decoded_token  # for further processing if needed
        #             except jwt.ExpiredSignatureError:
        #                 return JsonResponse({'error': 'Token has expired.'}, status=401)
        #             except jwt.InvalidTokenError:
        #                 return JsonResponse({'error': 'Invalid token.'}, status=401)
        #         else:
        #             return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)
        #         return view_func(request, *args, **kwargs)
        #
        # return _wrapped_view
        authorization_header = request.headers.get("Authorization", None)
        print(request.headers)
        print(request.headers.get("Authorization", None))
        if authorization_header:
            try:
                token = authorization_header.split("Bearer ")[1]
                decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
                expiration_timestamp = decoded_token.get('exp')
                # if expiration_timestamp:
                #     expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
                #     if datetime.utcnow() > expiration_datetime:
                #         return JsonResponse({'error': 'Token has expired.'}, status=401)
                # request['decoded_token'] = decoded_token
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired.'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token.'}, status=401)
        else:
            return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        #     token = args[0].headers["Authorization"].split("Bearer ")[1]
        #     print("args and kwargs", args[0].headers["Authorization"].split("Bearer ")[1], type(args))
        #     if token:
        #         decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
        #         role = decoded_token.role
        #         if role != 'admin':
        #             return JsonResponse({'error': 'User not permissible!'}, status=401)
        #     else:
        #         return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)
        #     return view_func(request, *args, **kwargs)
        #
        # return _wrapped_view
        authorization_header = request.headers.get("Authorization", None)
        if authorization_header:
            try:
                token = authorization_header.split("Bearer ")[1]
                decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
                role = decoded_token.get("role", None)
                print(role)

                if role != "admin":
                    return JsonResponse({'error': 'Insufficient Permissions!'}, status=401)
            except:
                return JsonResponse({'error': 'Invalid token.'}, status=401)
        else:
            return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def is_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        authorization_header = request.headers.get("Authorization", None)
        print(authorization_header)
        if authorization_header:
            try:
                token = authorization_header.split(" ")[1]
                decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
                role = decoded_token.get("role", None)

                if role != "user":
                    return JsonResponse({'error': 'Insufficient Permissions!'}, status=401)

            except:
                return JsonResponse({'error': 'Invalid Token!'}, status=401)
        else:
            return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def is_any_user(view_func):
    wraps(view_func)

    def _wrapped_view(request, *args, **kwargs):
        #     token = args[0].headers["Authorization"].split("Bearer ")[1]
        #     print("args and kwargs", args[0].headers["Authorization"].split("Bearer ")[1], type(args))
        #     if token:
        #         decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
        #         role = decoded_token.role
        #         if role != 'admin':
        #             return JsonResponse({'error': 'User not permissible!'}, status=401)
        #     else:
        #         return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)
        #     return view_func(request, *args, **kwargs)
        #
        # return _wrapped_view
        authorization_header = request.headers.get("Authorization", None)
        if authorization_header:
            try:
                token = authorization_header.split(" ")[1]
                decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
                role = decoded_token.get("role", None)

                if role != "user" and role != "admin":
                    return JsonResponse({'error': 'Insufficient Permissions!'}, status=401)
            except:
                return JsonResponse({'error': 'Invalid token!'}, status=401)
        else:
            return JsonResponse({'error': 'Token not found in the request headers.'}, status=401)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
