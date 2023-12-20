from .serializers import *
from rest_framework import status, generics, response
from django.contrib.auth import authenticate


# Create your views here.
class RegisterAPI(generics.GenericAPIView):
    """
    User Register
    """

    def post(self, request):
        serializer = RegisterSerializer(
            data=self.request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(
                {
                    "status": True,
                    "message": "Registered successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )


class LoginAPI(generics.GenericAPIView):
    """
    User Register
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            response_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                # "tokens": user.tokens,
            }
            return response.Response(
                {
                    "status": True,
                    "message": "Login successfully",
                    "data": response_data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return response.Response(
                {
                    "status": True,
                    "message": "Invalid username or password",
                    "data": {},
                },
                status=status.HTTP_201_CREATED,
            )

class GetUserDataAPI(generics.GenericAPIView):
    """
    User Register
    """
    def get(self, request):
        users = UserModel.objects.all()
        if users:
            response_list = []
            for user in users:
                response_data = {
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                }
                response_list.append(response_data)
                
            return response.Response(
                {
                    "status": True,
                    "message": "successfully",
                    "data": response_list,
                },
                status=status.HTTP_201_CREATED,
            )
            

class ProductDataAPI(generics.GenericAPIView):
    serializer_class = ProductSerializer 

    def get(self, request):
        product_data = Product.objects.all()
        serializer = self.get_serializer(product_data, many=True)

        if product_data.exists():
            total_price = sum(item['product_price'] for item in serializer.data)
            
            return response.Response(
                {
                    "status": True,
                    "message": "successfully",
                    "data": serializer.data,
                    "total_price": total_price,
                },
                status=status.HTTP_200_OK,
            )
        
        return response.Response(
            {
                "status": False,
                "message": "Something went wrong",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    
    def post(self, request):
        product_name = request.data.get("product_name")
        product_price = request.data.get("product_price")
        if product_name is not None and product_price is not None:
            Product.objects.create(
                product_name = product_name,
                product_price = product_price,
            )
            return response.Response(
                {
                    "status": True,
                    "message": "Product add successfully"
                },
                status=status.HTTP_201_CREATED,
            )
        return response.Response(
                {
                    "status": False,
                    "message": "Somthing wont's wrong",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProductDataUpdateAPI(generics.GenericAPIView):
    def put(self,request,id):
        product_name = request.data.get("product_name")
        product_price = request.data.get("product_price")
        
        product_data = Product.objects.get(pk=id)
        if (product_data) and (product_name is not None and product_price is not None):
            product_data.product_name = product_name
            product_data.product_price = product_price
            product_data.save()
            return response.Response(
                {
                    "status": True,
                    "message": "Update Successfully",
                    "data": {
                        "id" : product_data.pk,
                        "product name" :product_data.product_name,
                        "product price" :product_data.product_price,
                    }
                },
                status=status.HTTP_200_OK,
            )
        return response.Response(
                {
                    "status": False,
                    "message": "Somthing wont's wrong",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        