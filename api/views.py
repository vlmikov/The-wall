from rest_framework.response import Response
from .models import ConfigWall
from .serializer import ConfigWallSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404     
from .services import Wall


class CreateWallConfiguration(APIView):
    """"
    This endpoint is for get and post new configuration input
    Valid input for conf: {"conf": "10 10"}
    Accepts: sting with numbers separated by " " and "\n"
    Every new line represents profile
    Every number - section with height
    """
    @staticmethod
    def get(request):
        """"
        The get method accepts all get requested get requests
        and return all valid configuration stored in db
        """
        confs = ConfigWall.objects.all()
        serializer = ConfigWallSerializer(confs, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        """
        The post method accepts all post requests, validate data
        and save

        Response :
        - Validation Error or
        - return stored data and response status 201
        """
        serializer = ConfigWallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

       
class ListWallConfiguration(APIView):
    """
    This endpoint is for get update or delete conf
    """
    @staticmethod
    def get_object(pk):
        try:
            return ConfigWall.objects.get(pk=pk)
        except (Exception,):
            raise Http404
        
    def get(self, request, pk):
        """
        Get method accepts pk, query db and return the record
        """
        conf = self.get_object(pk)
        serializer = ConfigWallSerializer(conf)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Put method accepts pk and update the record with requested data
        """
        conf = self.get_object(pk)
        serializer = ConfigWallSerializer(conf, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete method accepts pk and delete the record
        """
        conf = self.get_object(pk)
        conf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class ProfileDay(APIView):
    """
    Endpoint that accepts profile number and day and returns
    day, ice_amount for the input profile till the provided day.
    """
    @staticmethod
    def get(request, profile, day):

        conf = ConfigWall.objects.all()[0].conf
        wall_ = Wall(conf)
        if profile > len(wall_.profiles):
            return Response({"error": f"There is no  with number {profile}. "
                                      f"Provide number less than {len(wall_.profiles) + 1}"},
                            status=status.HTTP_404_NOT_FOUND)
        res = wall_.get_profiles_day(profile, day)
        res = {
            "day": day,
            "ice_amount": res[1]
        }

        return Response(res)


class ProfileOverview(APIView):
    """
    Endpoint that accepts profile number and day and returns
    day, cost for the input profile till the provided day
    """
    @staticmethod
    def get(request, profile, day):
        conf = ConfigWall.objects.all()[0].conf
        wall_ = Wall(conf)
        if profile > len(wall_.profiles):
            return Response({"error": f"There is no  with number {profile}. "
                                      f"Provide number less than {len(wall_.profiles) + 1}"},
                            status=status.HTTP_404_NOT_FOUND)
        res = wall_.get_profiles_day(profile, day)
        res = {
            "day": day,
            "cost": res[2]
        }

        return Response(res)
    

class ProfileOverviewDay(APIView):
    """
    Endpoint that accepts day and return overview of the wall
    till the input day
    """
    @staticmethod
    def get(request, day):
        conf = ConfigWall.objects.all()[0].conf
        wall_ = Wall(conf)
        day, ice_amount, cost = wall_.wall_overview(day)
        res = {
            "day": day,
            "cost": cost
        }
        return Response(res)
    

class WallOverview(APIView):
    """
    Endpoint that return wall overview.
    cost needed to complete all sections.
    """
    @staticmethod
    def get(request):
        conf = ConfigWall.objects.all()[0].conf
        wall_ = Wall(conf)
        day, ice_amount, cost = wall_.wall_overview()
        res = {
            "day": day,
            'cost': cost
        }
        return Response(res)
