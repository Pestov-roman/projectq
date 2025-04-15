from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from src.rooms.serializers import CreateRoomSerializer, RoomSerializer
from src.core.services.room_services import RoomServices


class RoomCreateView(APIView):
    """
    POST /rooms/create
    Принимает: description, price
    Возвращает {"room_id": <id>}
    """

    def post(self, request, *args, **kwargs):
        serializer = CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            room_data = serializer.validated_data
            room = RoomServices.create_room(
                description=room_data["description"], price=room_data["price"]
            )
            return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDeleteView(APIView):
    """
    DELETE /rooms/delete?room_id=123
    Удаляет комнату и все её брони
    """

    def delete(self, request, *args, **kwargs):
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response(
                {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            RoomServices.delete_room(room_id=int(room_id))
            return Response({"status": "OK"})
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RoomListView(APIView):
    """
    GET /rooms/list?order_by=price&asc=0
    По умолчанию сортировка по created_at (asc)
    """

    def get(self, request, *args, **kwargs):
        order_by = request.query_params.get("order_by", "created_at")
        asc_param = request.query_params.get("asc", "1")
        ascending = asc_param != "0"

        rooms = RoomServices.list_rooms(order_by=order_by, ascending=ascending)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
