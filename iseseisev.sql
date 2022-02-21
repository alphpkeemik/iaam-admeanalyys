-- IP riik
DROP VIEW IF EXISTS ipcountry;
CREATE VIEW ipcountry AS
SELECT distinct(country), ip
FROM (
        SELECt ip, country
        FROM iplocation
        UNION
        SELECT ip,
            CASE
                riik
                WHEN 'ESTONIA' THEN "EE"
                WHEN 'LATVIA' THEN "LV"
                WHEN 'SWEDEN' THEN "SE"
                WHEN 'FINLAND' THEN "FI"
                ELSE riik
            END AS country
        FROM la_ip_riik
    ) t;
-- 2007
DROP VIEW IF EXISTS la07;
CREATE view la07 AS SELECT 1 AS "registered",
                           if(valitud, 1, null) AS "selected",
                           REPLACE(bandinimi, '\\', '') AS name,
                           kodukoht AS place,
                           tegutsemisiga AS activesincetext,
                           ip,
                           concat('07-', id) AS id
                    FROM la_bandid2007_tulemused;
DROP VIEW IF EXISTS la08_and_la09;
-- 2008 ja 2009
CREATE view la08_and_la09 AS SELECT id,
    event,
    selected,
    REPLACE(CONVERT(CAST(CONVERT(bandinimi USING LATIN1) AS BINARY) USING UTF8), '\\', '') COLLATE utf8_general_ci AS name,
    REPLACE(CONVERT(CAST(CONVERT(kodukoht USING LATIN1) AS BINARY) USING UTF8), '\\', '') AS place,
    REPLACE(CONVERT(CAST(CONVERT(tegutsemisiga USING LATIN1) AS BINARY) USING UTF8), '\\', '') AS activesincetext,
    REPLACE(CONVERT(CAST(CONVERT(muusikastiil USING LATIN1) AS BINARY) USING UTF8), '\\', '') AS stylespecify,
    ip COLLATE utf8_general_ci AS ip,
    unplugged
FROM (
        SELECT concat('08-', id) AS id,
            bandinimi,
            kodukoht,
            tegutsemisiga,
            muusikastiil,
            ip,
            'LA08' AS "event",
            (
                SELECT 1
                FROM la_valitudbandid2008
                WHERE band_id = la_bandid2008.id
            ) AS selected,
            null AS unplugged
        FROM la_bandid2008
        UNION ALL
        SELECT concat('09-', id) AS id,
            bandinimi,
            kodukoht,
            tegutsemisiga,
            muusikastiil,
            ip,
            'LA09' AS "event",
            (
                SELECT 1
                FROM la_valitudbandid2009
                WHERE band_id = la_bandid2009.id
            ) AS selected,
            unplugged
        FROM la_bandid2009
    ) t;
-- Andmete valimine
DROP VIEW IF EXISTS selected_data;
CREATE VIEW selected_data AS SELECT a.selected,
    'LA07' AS "event",
    a.id,
    a.name,
    if(a.place, a.place, b.place) AS "place",
    b.activesinceyear,
    b.activesincemonth,
    activesincetext,
    (
        SELECT value
        FROM classifierlang
        WHERE classifier = b.style
            AND lang = 'et'
    ) AS style,
    b.stylespecify,
    b.unplugged,
    b.singer,
    (
        SELECT country
        FROM ipcountry
        WHERE ipcountry.ip = a.ip
            or ipcountry.ip = b.ip
        LIMIT 1
    ) AS "registration_country"
FROM la07 a
    LEFT JOIN band b ON b.name = a.name
WHERE a.name != 'KukeProtest'
UNION ALL
SELECT a.selected,
    event,
    a.id,
    a.name,
    if(a.place, a.place, b.place) AS "place",
    b.activesinceyear,
    b.activesincemonth,
    activesincetext,
    (
        SELECT value
        FROM classifierlang
        WHERE classifier = b.style
            AND lang = 'et'
    ) AS style,
    if(
        a.stylespecify,
        a.stylespecify,
        b.stylespecify
    ) AS "stylespecify",
    if(a.unplugged, a.unplugged, b.unplugged) AS "unplugged",
    b.singer,
    (
        SELECT country
        FROM ipcountry
        WHERE ipcountry.ip = a.ip
            or ipcountry.ip = b.ip
        LIMIT 1
    ) AS "registration_country"
FROM la08_and_la09 a
    LEFT JOIN band b ON b.name = a.name
WHERE a.name != 'KukeProtest'
UNION ALL
SELECT e.selected,
    e.event,
    concat('band-',b.id) as id,
    b.name,
    b.place,
    b.activesinceyear,
    b.activesincemonth,
    null AS activesincetext,
    (
        SELECT value
        FROM classifierlang
        WHERE classifier = b.style
            AND lang = 'et'
    ) AS style,
    b.stylespecify,
    b.unplugged,
    b.singer,
    (
        SELECT country
        FROM iplocation
        WHERE iplocation.ip = b.ip
        LIMIT 1
    ) AS "registration_country"
FROM band b
    JOIN bandevent e on e.band = b.id
WHERE b.status = "active"
    AND b.name != 'KukeProtest'
    AND e.event != ''
    AND e.registered = 1
    AND e.event LIKE 'LA%';