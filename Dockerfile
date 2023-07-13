FROM python:3.11
ADD .env .
ADD app.py .
ADD requirements.txt .
ADD /index .
RUN pip install -r requirements.txt
EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# CMD ["python", "streamlit run ./app.py"]