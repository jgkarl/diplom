ALTER ROLE diplom_admin SET client_encoding TO 'utf8';
ALTER ROLE diplom_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE diplom_admin SET timezone TO 'Europe/Tallinn';
CREATE ROLE diplom_manager WITH LOGIN;
ALTER ROLE diplom_manager SET client_encoding TO 'utf8';
ALTER ROLE diplom_manager SET default_transaction_isolation TO 'read committed';
ALTER ROLE diplom_manager SET timezone TO 'Europe/Tallinn';

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO diplom_manager;
ALTER DEFAULT PRIVILEGES GRANT SELECT, INSERT, UPDATE ON TABLES TO diplom_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO diplom_manager;
ALTER DEFAULT PRIVILEGES GRANT USAGE, SELECT ON SEQUENCES TO diplom_manager;
REVOKE GRANT OPTION FOR ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM diplom_manager;
ALTER DEFAULT PRIVILEGES REVOKE GRANT OPTION FOR ALL PRIVILEGES ON TABLES FROM diplom_manager;

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT CREATE ON SCHEMA public TO diplom_admin;
ALTER DATABASE diplom OWNER TO diplom_admin;
