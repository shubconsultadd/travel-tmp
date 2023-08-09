

class Middleware:

    def __int__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        print("MiddleWare Called")
        response = self.get_response(request)

        return response

