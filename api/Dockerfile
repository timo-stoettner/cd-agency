FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY api/requirements.txt /app/api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Copy the full project (runtime, tools, content-design, presets, api)
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
