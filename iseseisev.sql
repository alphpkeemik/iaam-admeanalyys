--  first skipped dataset
SELECT 
b.name,
b.lang, 
b.nonmusical, 
b.place, 
b.activesinceyear,
b.activesincemonth,
(SELECT value FROM classifierlang WHERE classifier=b.style AND lang='et') as style,
b.stylespecify,
b.unplugged,
b.singer,
(SELECT country FROM iplocation WHERE iplocation.ip=b.ip LIMIT 1) as "registration_country",
(SELECT count(*) FROM bandevent WHERE band=id AND selected=1) as "events_attended",
(SELECT count(*) FROM bandevent WHERE band=id AND registered=1) as "events_registered"
FROM band b
WHERE b.status="active";

-- dataset fixes and preparations
DROP view if exists la07;
CREATE view la07 as SELECT 
1 as "registered"
, if(valitud, 1, null) as "selected"
, REPLACE(bandinimi, '\\', '') as name
,kodukoht as place
,tegutsemisiga as activesincetext
,ip
,concat('07-', id) as id
 from la_bandid2007_tulemused;

DROP view if exists ipcountry;
CREATE VIEW ipcountry AS SELECT distinct(country), ip FROM(
SELECt  ip, country from iplocation
UNION 
SELECT ip, 
CASE riik
    WHEN 'ESTONIA' THEN "EE"
        WHEN 'LATVIA' THEN "LV"
        WHEN 'SWEDEN' THEN "SE"
        WHEN 'FINLAND' THEN "FI"
    ELSE riik
END
 AS country from la_ip_riik
) t;

DROP view if exists la08_and_la09;
CREATE view la08_and_la09 as SELECT 
id,
event,
selected
,REPLACE(CONVERT(CAST(CONVERT(bandinimi USING LATIN1) AS BINARY) USING UTF8), '\\', '') COLLATE utf8_general_ci as name 
,REPLACE(CONVERT(CAST(CONVERT(kodukoht USING LATIN1) AS BINARY) USING UTF8), '\\', '') as place
,REPLACE(CONVERT(CAST(CONVERT(tegutsemisiga USING LATIN1) AS BINARY) USING UTF8), '\\', '') as activesincetext
,REPLACE(CONVERT(CAST(CONVERT(muusikastiil USING LATIN1) AS BINARY) USING UTF8), '\\', '') as stylespecify
,ip COLLATE utf8_general_ci as ip
,unplugged
FROM (
 SELECT concat('08-', id) as id, bandinimi, kodukoht, tegutsemisiga,muusikastiil, ip,'LA08' as "event" ,
 (SELECT 1 FROM la_valitudbandid2008 WHERE band_id=la_bandid2008.id) as selected,
 null as unplugged
 from la_bandid2008
 UNION ALL 
 SELECT concat('09-', id) as id,bandinimi, kodukoht, tegutsemisiga,muusikastiil, ip,'LA09' as "event" ,
 (SELECT 1 FROM la_valitudbandid2009 WHERE band_id=la_bandid2009.id) as selected,
 unplugged
 from la_bandid2009
 ) t;

-- select data
SELECT 
a.selected,
'LA07' as "event",
a.id,
b.nonmusical,  
if(a.place,a.place, b.place) as "place", 
b.activesinceyear,
b.activesincemonth,
activesincetext,
(SELECT value FROM classifierlang WHERE classifier=b.style AND lang='et') as style,
b.stylespecify,
b.unplugged,
b.singer,
(SELECT country FROM ipcountry WHERE ipcountry.ip=a.ip or ipcountry.ip=b.ip LIMIT 1) as "registration_country"
FROM la07 a
LEFT JOIN band b ON b.name=a.name
WHERE a.name!='KukeProtest'
UNION ALL
SELECT 
a.selected,
event,
a.id,
b.nonmusical, 
if(a.place,a.place, b.place) as "place", 
b.activesinceyear,
b.activesincemonth,
activesincetext,
(SELECT value FROM classifierlang WHERE classifier=b.style AND lang='et') as style,
if(a.stylespecify, a.stylespecify, b.stylespecify) as "stylespecify",
if(a.unplugged, a.unplugged, b.unplugged) as "unplugged",
b.singer,
(SELECT country FROM ipcountry WHERE ipcountry.ip=a.ip or ipcountry.ip=b.ip LIMIT 1) as "registration_country"
FROM la08_and_la09 a
LEFT JOIN band b ON b.name=a.name
WHERE a.name!='KukeProtest'
UNION ALL
SELECT 
e.selected,
e.event,
concat('band-',b.id),
b.nonmusical, 
b.place, 
b.activesinceyear,
b.activesincemonth,
null as activesincetext,
(SELECT value FROM classifierlang WHERE classifier=b.style AND lang='et') as style,
b.stylespecify,
b.unplugged,
b.singer,
(SELECT country FROM iplocation WHERE iplocation.ip=b.ip LIMIT 1) as "registration_country"
FROM band b
JOIN bandevent e on e.band=b.id
WHERE b.status="active"
AND b.name!='KukeProtest'
AND e.event!=''
AND e.registered=1
;