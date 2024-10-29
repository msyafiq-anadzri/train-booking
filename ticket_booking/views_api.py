from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Origin, Destination, Train, Coach
from .serializers import OriginSerializer, DestinationSerializer, TrainSerializer, CoachSerializer

@api_view(['POST'])
def bulk_upload(request):
    data = request.data

    # Process Origins
    if 'origins' in data:
        for origin_data in data['origins']:
            serializer = OriginSerializer(data=origin_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Process Destinations
    if 'destinations' in data:
        for destination_data in data['destinations']:
            serializer = DestinationSerializer(data=destination_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Process Trains
    if 'trains' in data:
        for train_data in data['trains']:
            serializer = TrainSerializer(data=train_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Process Coaches
    if 'coaches' in data:
        for coach_data in data['coaches']:
            serializer = CoachSerializer(data=coach_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Bulk upload successful."}, status=status.HTTP_201_CREATED)
