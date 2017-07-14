FROM python:3.6-alpine

WORKDIR /build

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "/build/update-windows-release-json.py" ]
