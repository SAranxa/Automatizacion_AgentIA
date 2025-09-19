import grpc
from concurrent import futures
import os
from datetime import datetime
import logging
import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


import availability_pb2
import availability_pb2_grpc


from google.oauth2 import service_account
from googleapiclient.discovery import build


logging.basicConfig(level=logging.INFO)


GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS',
                                    '/app/credentials/google_credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class AvailabilityServicer(availability_pb2_grpc.AvailabilityServicer):
    """Proporciona métodos que implementan la funcionalidad del servidor de disponibilidad."""

    def __init__(self):
        try:
            self.creds = service_account.Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS_PATH, scopes=SCOPES)
            self.calendar_service = build('calendar', 'v3', credentials=self.creds)
            logging.info("Successfully connected to Google Calendar API.")
        except Exception as e:
            logging.error(f"Failed to initialize Google Calendar service: {e}")
            self.calendar_service = None


    def CheckAvailability(self, request, context):
        """
        Verifica si un rango de tiempo dado está disponible en el Calendario de Google.
        """
        if not self.calendar_service:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Google Calendar service not available.")
            return availability_pb2.AvailabilityResponse()

        start_time_str = request.start_time
        end_time_str = request.end_time
        calendar_id = request.calendar_id or 'primary'

        logging.info(f"Checking availability for calendar '{calendar_id}' "
                     f"from {start_time_str} to {end_time_str}")

        try:
            start_time_dt = datetime.fromisoformat(start_time_str).isoformat() + 'Z'
            end_time_dt = datetime.fromisoformat(end_time_str).isoformat() + 'Z'

            events_result = self.calendar_service.events().list(
                calendarId=calendar_id,
                timeMin=start_time_dt,
                timeMax=end_time_dt,
                maxResults=1,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            if not events:
                logging.info("Slot is available.")
                return availability_pb2.AvailabilityResponse(is_available=True)
            else:
                logging.info(f"Slot is not available. Found event: {events[0]['summary']}")
                return availability_pb2.AvailabilityResponse(is_available=False)

        except Exception as e:
            logging.error(f"Error checking calendar availability: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error communicating with Google Calendar: {e}")
            return availability_pb2.AvailabilityResponse()


app = FastAPI()


class AvailabilityRequestModel(BaseModel):
    start_time: str
    end_time: str
    calendar_id: str = 'primary'


availability_servicer = AvailabilityServicer()


@app.post("/check-availability")
async def check_availability_endpoint(request_model: AvailabilityRequestModel):
    if not availability_servicer.calendar_service:
        raise HTTPException(status_code=503, detail="Google Calendar service not available.")

    class MockContext:
        def set_code(self, code):
            pass

        def set_details(self, details):
            pass

    context = MockContext()
    grpc_request = availability_pb2.AvailabilityRequest(
        start_time=request_model.start_time,
        end_time=request_model.end_time,
        calendar_id=request_model.calendar_id
    )

    try:
        response = availability_servicer.CheckAvailability(grpc_request, context)
        return {"is_available": response.is_available}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")


def run_fastapi():
    """Ejecuta el servidor FastAPI."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


def serve():
    """Inicia el servidor gRPC y el servidor FastAPI en hilos separados."""
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    logging.info("FastAPI server starting in a background thread on port 8000...")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    availability_pb2_grpc.add_AvailabilityServicer_to_server(availability_servicer, server)
    server.add_insecure_port('[::]:50051')
    logging.info("gRPC server starting on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
