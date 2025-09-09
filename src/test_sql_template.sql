-- 测试SQL模板
SELECT 
    city_name,
    qqt_amt,
    pzqqt_amt,
    qqt_cnt
FROM anaylsis_qqt_lzgx_st_mm 
WHERE op_month = {op_month}
  AND (last_month IS NULL OR last_month = {last_op_month})
ORDER BY qqt_amt DESC
LIMIT 10;