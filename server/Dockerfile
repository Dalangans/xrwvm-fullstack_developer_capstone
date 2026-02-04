FROM node:16 as builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM python:3.12.0-slim-bookworm
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app
# Change the workdir.
WORKDIR $APP
# Install the requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt
# Copy the rest of the files
COPY . $APP
# Copy React build from builder stage
COPY --from=builder /app/frontend/build $APP/frontend/build
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
