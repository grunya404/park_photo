-- upgrade --
CREATE TABLE IF NOT EXISTS "camera"
(
    "id"                    SERIAL       NOT NULL PRIMARY KEY,
    "camera_title_location" VARCHAR(255) NOT NULL UNIQUE,
    "camera_url"            VARCHAR(255) NOT NULL UNIQUE,
    "is_active"             BOOL         NOT NULL DEFAULT False,
    "created_at"            TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_at"             TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
);;
CREATE TABLE IF NOT EXISTS "parking"
(
    "id"         SERIAL       NOT NULL PRIMARY KEY,
    "file"       VARCHAR(255) NOT NULL UNIQUE,
    "camera_id"  VARCHAR(55) UNIQUE,
    "created_at" TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_at"  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO public.camera (camera_title_location, camera_url, is_active, created_at, update_at)
VALUES ('Парковка вид с балкона', 'rtsp://admin:q12345678@10.0.132.227:554', true, '2022-06-07 07:14:05.351712 +00:00',
        '2022-06-07 07:14:05.351733 +00:00');
INSERT INTO public.camera (camera_title_location, camera_url, is_active, created_at, update_at)
VALUES ('Камера установленная на складе', 'rtsp://admin:q12345678@10.0.41.231:554', true,
        '2022-06-09 08:31:01.266315 +00:00', '2022-06-09 08:31:01.266336 +00:00');
INSERT INTO public.camera (camera_title_location, camera_url, is_active, created_at, update_at)
VALUES ('Вид на шлагбаум', 'rtsp://admin:q12345678@10.0.133.4:554', true, '2022-06-09 08:31:50.252576 +00:00',
        '2022-06-09 08:31:50.252613 +00:00');
-- downgrade --
DROP TABLE IF EXISTS "camera";
DROP TABLE IF EXISTS "parking";

