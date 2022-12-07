FROM python:3.8
ADD okteto-stack.yaml /okteto-stack.yaml
EXPOSE 8000
COPY . .
WORKDIR ./
RUN pip install -r ./requirements.txt
CMD ["python3", "backend/main.py"]