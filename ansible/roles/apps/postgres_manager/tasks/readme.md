GRANT pg_signal_backend TO postgres;
GRANT nocodb TO postgres;
ALTER DATABASE nocodb OWNER TO postgres;
drop database nocodb;
drop role nocodb;
