from app_mail.celery import app
@app.task
def prueba_suma(x, y):
    return x + y

@app.task
def prueba_resta(x, y):
    return x - y
