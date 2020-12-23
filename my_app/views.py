from django.shortcuts import render
from django.http import request, JsonResponse, Http404
from my_app.models import Employee
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EmployeeSerializer

#Normally when you make a request via a form you want the form being submitted 
#to your view to originate from your website and not come from some other domain. 
#To ensure that this happens, you can put a csrf token in your form for your view to recognize. 
#If you add @csrf_exempt to the top of your view, 
#then you are basically telling the view that it doesn't need the token. 
#This is a security exemption that you should take seriously.

#Decorator marks a view as being exempt from the protection ensured by the middleware.
@csrf_exempt
@api_view(["GET"])
#do something very specific/custom
def EmployeeDetails(request):
    if request.method == "GET":
        obj = Employee.objects.all()
        data = {
            "response":list(obj.values("id","name"))
        }
        return JsonResponse(data)

    elif request.method == "POST":
        name = request.POST["name"]
        obj = Employee(name=name)
        obj.save()
        data = {
            "response": {
                "id":obj.id,
                "name":obj.name
            }
        }
        return JsonResponse(data)


class ListEmployee(APIView):
    def get(self,request):
        obj = Employee.objects.all()
        # data = {
        #     "response":list(obj.values("id","name"))
        # }   
        serializer_obj = EmployeeSerializer(obj, many=True)     
        return Response(serializer_obj.data)
        #data - serialized data for response
        #status - return status code of response
        #headers - dictionary for http headers example (passing token to authenticated API)
        #template_name - html renderer is selected
        #content_type - set content type of response

    def post(self,request):
        #name = request.data["name"]
        data = request.data
        # obj = Employee(name=name)
        # obj.save()
        serializer_obj = EmployeeSerializer(data=data)
        # data = {
        #     "response": {
        #         "id":obj.id,
        #         "name":obj.name
        #     }
        # }
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        return Response(serializer_obj.errors)


class UpdateEmployee(APIView):
    def get_object(self, id):
        try:
            obj = Employee.objects.get(id=id)
            return obj
        except Employee.DoesNotExist:
            raise Http404

    def put(self, request, id):
        data = request.data
        obj = Employee.objects.get(id=id)
        serializer_obj = EmployeeSerializer(obj, data=data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        return Response(serializer_obj.errors)
        
    def delete(self, request, id):
        obj = Employee.objects.get(id=id)
        obj.delete()
        return Response({"response": "Employee is successfully completed"})