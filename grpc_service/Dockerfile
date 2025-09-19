# 1. Base Image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Install uv, our package manager
RUN pip install uv

# 4. Copy and install dependencies
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# 5. Copy protobuf definition
COPY proto/ /app/proto

# 6. Generate gRPC code from .proto file
RUN python -m grpc_tools.protoc \
    -I/app/proto \
    --python_out=. \
    --grpc_python_out=. \
    /app/proto/availability.proto

# 7. Copy the application server
COPY server.py .

# 8. Expose ports
EXPOSE 50051
EXPOSE 8000

# 9. Run the server
CMD ["python", "-u", "server.py"]
