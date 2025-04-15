from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .serializers import CreateBookingSerializer, BookingSerializer
from src.core.services.booking_services import BookingServices


class BookingCreateView(APIView):
    """
    POST /booking/create
    Принимает: room, date_start, date_end
    Возвращает: {"booking_id": <id>}
    """

    def post(self, request):
        serializer = CreateBookingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                booking = BookingServices.create_booking(
                    room_id=data["room"].id,
                    date_start=data["date_start"],
                    date_end=data["date_end"],
                )
                return Response(
                    {"booking_id": booking.id}, status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDeleteView(APIView):
    """
    DELETE /booking/delete?booking_id=<id>
    """

    def delete(self, request):
        booking_id = request.query_params.get("booking_id")
        if not booking_id:
            return Response(
                {"error": "booking_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            BookingServices.delete_booking(booking_id)
            return Response({"status": "OK"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookingListView(APIView):
    """
    GET /bookings/list?room_id=<id>
    """

    def get(self, request):
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response(
                {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        bookings = BookingServices.get_bookings_for_room(int(room_id))
        serializer = BookingSerializer(bookings, many=True)
        data = [
            {
                "booking_id": b["id"],
                "date_start": b["date_start"],
                "date_end": b["date_end"],
            }
            for b in serializer.data
        ]
        return Response(data)
