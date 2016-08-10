SELECT
  nth(51, quantiles(download_speed_mbps, 101)) AS download_speed_mbps_median,
  nth(51, quantiles(upload_speed_mbps, 101)) AS upload_speed_mbps_median,

  -- AVG(download_speed_mbps) AS download_speed_mbps_avg,
  -- AVG(upload_speed_mbps) AS upload_speed_mbps_avg,

  -- MIN(download_speed_mbps) AS download_speed_mbps_min,
  -- MAX(download_speed_mbps) AS download_speed_mbps_max,

  -- MIN(upload_speed_mbps) AS upload_speed_mbps_min,
  -- MAX(upload_speed_mbps) AS upload_speed_mbps_max,

  -- STDDEV(download_speed_mbps) AS download_speed_mbps_stddev,
  -- STDDEV(upload_speed_mbps) AS upload_speed_mbps_stddev,

  COUNT(*) AS count,

client_continent_code,
client_country_code,
client_asn_number,
client_continent,
client_country,
client_asn_name,
STRFTIME_UTC_USEC(TIMESTAMP_TO_USEC([test_date]), "%Y-%m") as date,
HOUR(test_date) AS hour

FROM
  {0}
WHERE LENGTH(client_country_code) > 0 AND LENGTH(client_continent_code) > 0 AND LENGTH(client_asn_number) > 0 AND LENGTH(client_asn_name) > 0

GROUP BY
client_continent_code,
client_country_code,
client_asn_number,
date,
hour,
client_continent,
client_country,
client_asn_name
