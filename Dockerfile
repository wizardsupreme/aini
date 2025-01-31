FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ansible \
    curl \
    git \
    ssh \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

# Install Python dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install Ansible requirements
COPY ansible/requirements.yml /ansible/
RUN ansible-galaxy install -r /ansible/requirements.yml

WORKDIR /***REMOVED***

# Copy API and configurations
COPY cli/api.py /***REMOVED***/cli/
COPY cli/static /***REMOVED***/cli/static
COPY ansible /***REMOVED***/ansible

CMD ["python", "cli/api.py"]