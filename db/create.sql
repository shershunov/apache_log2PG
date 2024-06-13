-- PostgreSQL

CREATE TABLE apache_logs (
    id_apache_logs BIGSERIAL NOT NULL CONSTRAINT PK_apache_logs PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    log_name TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    request TEXT NOT NULL,
    status_code INT NOT NULL,
    response_size INT NOT NULL
);
CREATE INDEX IF NOT EXISTS index_id_apache_logs on apache_logs (id_apache_logs);

CREATE OR REPLACE PROCEDURE apache_log_Insert(
    p_ip_address VARCHAR,
    p_log_name TEXT,
    p_timestamp TIMESTAMPTZ,
    p_request TEXT,
    p_status_code INT,
    p_response_size INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO apache_logs (ip_address, log_name, timestamp, request, status_code, response_size)
    VALUES (p_ip_address, p_log_name, p_timestamp, p_request, p_status_code, p_response_size);
END;
$$;

CREATE OR REPLACE PROCEDURE apache_log_Update(
    p_id_apache_logs BIGINT,
    p_ip_address VARCHAR,
    p_log_name TEXT,
    p_timestamp TIMESTAMPTZ,
    p_request TEXT,
    p_status_code INT,
    p_response_size INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE apache_logs
    SET ip_address = p_ip_address,
        log_name = p_log_name,
        timestamp = p_timestamp,
        request = p_request,
        status_code = p_status_code,
        response_size = p_response_size
    WHERE id_apache_logs = p_id_apache_logs;
END;
$$;

CREATE OR REPLACE PROCEDURE apache_log_Delete(
    p_id_apache_logs BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM apache_logs
    WHERE id_apache_logs = p_id_apache_logs;
END;
$$;

CREATE ROLE watchdog_agent WITH LOGIN PASSWORD 'Pa$$w0rd';
GRANT INSERT, UPDATE, SELECT ON TABLE apache_logs TO watchdog_agent;
grant usage, select on sequence apache_logs_id_apache_logs_seq to watchdog_agent;
GRANT EXECUTE ON PROCEDURE apache_log_insert TO watchdog_agent;

CREATE ROLE api_agent WITH LOGIN PASSWORD 'Pa$$w0rd';
GRANT SELECT ON TABLE apache_logs TO api_agent;