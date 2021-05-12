FROM public.ecr.aws/lambda/python:3.7
LABEL maintainer="Luis Enrique Fuentes Plata"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY app.py requirements.txt ./
RUN python3.7 -m pip install -r requirements.txt -t .

COPY src ./src

CMD ["app.lambda_handler"]
