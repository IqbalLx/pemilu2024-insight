-- select partai_id, sum(jumlah_suara_total) as total 
-- from pdpr_tps_partai
-- group by partai_id
-- order by total desc

-- select * from pdpr_tps_list limit 10

with source as (
select 
	suara_paslon_1,
	suara_paslon_2,
	suara_paslon_3,
	(suara_paslon_1 + suara_paslon_2 +suara_paslon_3) as manual_total,
	suara_sah,
	suara_tidak_sah,
	pengguna_total_j,
	(pengguna_total_j - suara_tidak_sah) as manual_suara_sah,
	url_page
from ppwp_tps
where 
	psu is null and
	pengguna_total_j > 0 and
	suara_sah > 0 and
	provinsi_nama != 'Luar Negeri'
)
select * from source
where (manual_suara_sah > pengguna_total_j or
	manual_suara_sah > manual_total) and
	manual_total != suara_sah
order by manual_suara_sah desc
limit 10