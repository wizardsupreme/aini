FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ansible \
    curl \
    git \
    ssh \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install Ansible requirements
COPY ansible/requirements.yml /ansible/
RUN ansible-galaxy install -r /ansible/requirements.yml

WORKDIR /***REMOVED***

# Copy AINI CLI tool and configurations
COPY cli /***REMOVED***/cli
COPY ansible /***REMOVED***/ansible

# Make CLI executable
RUN chmod +x /***REMOVED***/cli/***REMOVED***

# Add to PATH
ENV PATH="/***REMOVED***/cli:${PATH}"

# Default command shows help
CMD ["***REMOVED***", "--help"]