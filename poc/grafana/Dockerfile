FROM grafana/grafana:latest

COPY src /etc/grafana/provisioning/
COPY grafana.ini /etc/grafana/grafana.ini

ENTRYPOINT [ "/run.sh" ]
