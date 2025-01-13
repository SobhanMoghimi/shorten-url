CREATE
DATABASE url_shortener;

-- CREATE
-- USER url_shortener_app WITH PASSWORD '4*GB%!VjCF7K48Vh';
-- GRANT ALL
-- ON DATABASE url_shortener TO url_shortener_app;
-- ALTER
-- DATABASE url_shortener OWNER TO url_shortener_app;

CREATE TABLE urls
(
    "url_uuid"         uuid                     NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    "created_at"       timestamp with time zone NOT NULL             DEFAULT transaction_timestamp(),
    "last_accessed_at" timestamp with time zone NOT NULL             DEFAULT transaction_timestamp(),
    "accessed_count"   INT                      NOT NULL             DEFAULT 0,
    "url"              VARCHAR                  NOT NULL,
    "shortened_url"    CHAR(6) UNIQUE           NOT NULL
);

CREATE INDEX "urls_url" ON "urls" ("url" varchar_pattern_ops);
CREATE INDEX "urls_last_accessed_at" ON "urls" ("last_accessed_at" DESC NULLS LAST);
CREATE INDEX "urls_accessed_count" ON "urls" ("accessed_count" DESC NULLS LAST);
CREATE INDEX "urls_shortened_url" ON "urls" ("shortened_url");

CREATE OR REPLACE FUNCTION get_url(short_url CHAR(6))
RETURNS TABLE (
    url_uuid UUID,
    created_at TIMESTAMP WITH TIME ZONE,
    last_accessed_at TIMESTAMP WITH TIME ZONE,
    accessed_count INT,
    url VARCHAR,
    shortened_url CHAR(6)
) AS $$
BEGIN
    UPDATE urls
    SET accessed_count = urls.accessed_count + 1,
        last_accessed_at = transaction_timestamp()
    WHERE urls.shortened_url = short_url;

    RETURN QUERY SELECT *
    FROM urls
    WHERE urls.shortened_url = short_url;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION gen_new_short_url()
RETURNS VARCHAR AS $$
DECLARE
new_url VARCHAR(6);
BEGIN
    LOOP
        -- Generate a random 6-character string
new_url := (
            SELECT string_agg(substr('abcdefghijklmnopqrstuvwxyz0123456789', floor(random() * 36)::int + 1, 1), '')
            FROM generate_series(1, 6)
        );

        -- Check if it already exists in the table
        IF
NOT EXISTS (
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
