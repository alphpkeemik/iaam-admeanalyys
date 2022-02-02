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


SELECT 
e.registered,
e.selected,
e.event,
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
(SELECT country FROM iplocation WHERE iplocation.ip=b.ip LIMIT 1) as "registration_country"
FROM band b
JOIN bandevent e on e.band=b.id
WHERE b.status="active"
AND b.name!='KukeProtest'
AND e.event!=''
;