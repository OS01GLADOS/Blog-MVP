FROM python:3.8

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV SECRET_KEY=9pI_6H7XRgBYxY_4JKjY6Dt7Px6aSZ5zJMaHX7LvD13FEbdqwAKA64IG5YqumZsBnDUaGZNwFZrcfWqIEi8Fw

ENV DB_ENGINE=django.db.backends.postgresql_psycopg2
ENV DB_NAME=os01glados_blog_db
ENV DB_USER=postgres
ENV DB_PASSWORD=tyuiyrfu2617
ENV DB_HOST=os01glados-blog-db.cjkkfc9cffpn.us-east-1.rds.amazonaws.com
ENV DB_PORT=5432

ENV EMAIL_USER=djangotutorialblog.t@gmail.com
ENV EMAIL_PASS=mnbvcxz0987

COPY ./ /code
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
