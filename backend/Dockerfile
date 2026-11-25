FROM python:3.12-slim

WORKDIR /app

# Cài dependencies trước để tận dụng cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn
COPY app/ ./app/

# Khai báo cổng (chỉ ghi nhận, chưa mở ra ngoài)
EXPOSE 8000

# Lệnh chạy khi container khởi động
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]