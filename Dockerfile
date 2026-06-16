FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-c","import subprocess; subprocess.run(['python','src/extract.py']); subprocess.run(['python','src/transform.py']); subprocess.run(['python','data/mart/load.py']); subprocess.run(['python','scripts/quality_check.py'])"]