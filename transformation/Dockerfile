# Luis Enrique Fuentes Plata
FROM public.ecr.aws/lambda/python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY app.py requirements.txt ./
COPY src ./src

RUN python3.7 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
