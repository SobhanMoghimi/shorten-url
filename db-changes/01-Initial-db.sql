CREATE DATABASE url_shortener;

CREATE TABLE urls
(
    "url_uuid"         uuid                     NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    "created_at"       timestamp with time zone NOT NULL             DEFAULT transaction_timestamp(),
    "url"              VARCHAR                  NOT NULL,
    "shortened_url"    CHAR(6) UNIQUE           NOT NULL
);

CREATE TABLE urls_access_logs (
    "log_uuid"         uuid                     NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    "created_at"       timestamp with time zone NOT NULL DEFAULT transaction_timestamp(),
    "url_uuid"         uuid                     NOT NULL REFERENCES urls(url_uuid) ON DELETE CASCADE
);

CREATE INDEX "urls_url" ON "urls" ("url" varchar_pattern_ops);
CREATE INDEX "urls_shortened_url" ON "urls" ("shortened_url");

CREATE OR REPLACE PROCEDURE add_log(url_id UUID)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO urls_access_logs (url_uuid)
    VALUES (url_id);
END;
$$;


CREATE OR REPLACE FUNCTION get_url(short_url CHAR(6))
RETURNS TABLE (
    url_uuid UUID,
    created_at TIMESTAMP WITH TIME ZONE,
    url VARCHAR,
    shortened_url CHAR(6)
) AS $$
DECLARE
    url_id UUID;
BEGIN
    SELECT urls.url_uuid INTO url_id
    FROM urls
    WHERE urls.shortened_url = short_url;

    IF url_id IS NOT NULL THEN
        CALL add_log(url_id);

        RETURN QUERY
        SELECT urls.url_uuid, urls.created_at, urls.url, urls.shortened_url
        FROM urls
        WHERE urls.shortened_url = short_url;
    ELSE
        RETURN;
    END IF;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_short_url(long_url VARCHAR)
RETURNS CHAR(6) AS $$
DECLARE
    url_id UUID;
    short_url CHAR(6);
BEGIN
    SELECT url_uuid, shortened_url INTO url_id, short_url
    FROM urls
    WHERE url = long_url;

    IF url_id IS NOT NULL THEN
        CALL add_log(url_id);
        RETURN short_url;
    ELSE
        RETURN null;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION gen_new_short_url()
RETURNS VARCHAR AS $$
DECLARE
new_url VARCHAR(6);
BEGIN
    LOOP
        new_url := (
            SELECT string_agg(substr('abcdefghijklmnopqrstuvwxyz0123456789', floor(random() * 36)::int + 1, 1), '')
            FROM generate_series(1, 6)
        );

        IF NOT EXISTS (
            SELECT 1
            FROM urls
            WHERE shortened_url = new_url
        ) THEN
            RETURN new_url;
        END IF;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION assign_shortened_url()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM urls WHERE url = NEW.url) THEN
        RAISE NOTICE 'URL already exists: %', NEW.url;
        RETURN NULL;
    END IF;

    IF NEW.shortened_url IS NULL THEN
        NEW.shortened_url := gen_new_short_url();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_assign_shortened_url
BEFORE INSERT ON urls
FOR EACH ROW
EXECUTE FUNCTION assign_shortened_url();


CREATE OR REPLACE VIEW urls_time_since_last_access AS
SELECT
    urls.shortened_url,
    COUNT(logs.log_uuid) AS accessed_count,
    NOW() - MAX(logs.created_at) AS time_since_last_access
FROM urls
LEFT JOIN urls_access_logs logs ON urls.url_uuid = logs.url_uuid
GROUP BY urls.shortened_url;


CREATE OR REPLACE VIEW top_3_accessed_urls AS
SELECT
    urls.shortened_url,
    urls.url AS long_url,
    COUNT(logs.log_uuid) AS access_count
FROM urls
JOIN urls_access_logs logs ON urls.url_uuid = logs.url_uuid
GROUP BY urls.shortened_url, urls.url
ORDER BY access_count DESC
LIMIT 3;


CREATE OR REPLACE VIEW registered_urls_each_day AS
SELECT
    created_at::DATE AS registration_date,
    COUNT(*) AS total_new_urls
FROM urls
GROUP BY registration_date
ORDER BY registration_date DESC;

CREATE OR REPLACE VIEW accesses_per_day_per_url AS
SELECT
    u.shortened_url,
    l.created_at::DATE AS access_date,
    COUNT(*) AS total_accesses
FROM urls_access_logs l
JOIN urls u ON l.url_uuid = u.url_uuid
GROUP BY u.shortened_url, access_date
ORDER BY access_date DESC, total_accesses DESC;


CREATE OR REPLACE PROCEDURE delete_inactive_urls()
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM urls
    WHERE url_uuid IN (
        SELECT urls.url_uuid
        FROM urls
        LEFT JOIN urls_access_logs l ON urls.url_uuid = l.url_uuid
        GROUP BY urls.url_uuid
        HAVING COALESCE(MAX(l.created_at), urls.created_at) < NOW() - INTERVAL '7 days'
    );
    RAISE NOTICE 'Inactive URLs older than 7 days have been deleted.';
END;
$$;

