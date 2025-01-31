FROM hashicorp/consul:latest

# Install required packages
RUN apk add --no-cache gettext

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"] 