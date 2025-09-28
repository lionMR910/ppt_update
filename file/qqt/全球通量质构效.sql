----- 全省用户 打标签    3min 51sec 
drop table if exists temp_it_member_all_detail ; 
create table temp_it_member_all_detail DISTRIBUTE BY hash (user_id) as
select  a.user_id,kb_user_id,prod_bandwidth
       ,case when kd.kb_user_id is not null  and zw.user_id  is not null then 1 else 0 end  is_zw  -- 是否组网客户	20240818
	   ,case when kd.kb_user_id is not null  and mbh.user_id is not null then 1 else 0 end  is_mbh -- 是否电视客户	20240818
	   ,case when kd.kb_user_id is not null  and mbh.user_id is not null and vip.user_id is not null then 1 else 0 end  is_tv_vip -- 是否电视会员客户 20240818
  
	   ,case when lyh2.product_no is not null then 1 else 0 end is_lyh_active -- 是否辽友会活跃客户
	   ,case when kd.kb_user_id is not null  and af.user_id  is not null then 1 else 0 end is_anfang   -- 是否安防 20240818 强捆绑
       
	
	
 from  -- 全省正常用户，剔除物联网
  (select a.user_id,a.product_no,a.city_id,a.county_id from obdw.dw_product_detail_m202506 a  
     left join  obdw.dw_product_wlw_m202506 b  on a.user_id =b.user_id 
      where  b.user_id is null   ---  剔除物联网

     ) a  
 left join  --组网
     ( select user_id from OBDW.DW_HOME_ZNZW_m202506  group by 1 )zw
     on a.user_id =zw.user_id 
 left join  --魔百盒即高清
     (select  user_id ,sum(active_duration) as use_times  from obdw.dwv_home_mbh_m202506  group by 1 ) mbh
 	 on a.user_id =mbh.user_id 
 left join  -- 是否电视会员客户
      (select user_id  from obdw.dw_home_mbh_incre_m202506
 	     where is_arrive_mark =1
 		 group by 1)  vip 
 	 on a.user_id =vip.user_id 
 
 left join 
      (select product_no  from bdba.lyh_active_detail_dm  where op_time<=20250630 group by 1 
 	 ) lyh2 
 	 on a.product_no =lyh2.product_no
 left join -- 宽带到达表
    (select * from 
          (select  a.kb_user_id , a.cell_id ,a.cell_name ,a.attr_100025 , a.prod_bandwidth ,a.offer_id,a.offer_name ,a.mtd_flow --- 月累计流量
		   ,b.grid_id_3 , b.grid_name_3  ,a.account_id  
 		   ,row_number()over(partition by a.kb_user_id order by a.create_date desc) as rn 
            from  obdw.dwv_home_cable_m202506 a 
			 left join obdw.dw_home_cable_grid_m202506 b  on a.user_id =b.user_id
			 where a.is_group =0 
 		  ) where rn =1 ) kd
 	on a.user_id =kd.kb_user_id 

 left join   -- 安防
    ( select user_id 
					from (select user_id from obdw.dw_home_paxc_m202506
						   union all
						  select user_id from obdw.dw_home_hemu_m202506) group by 1 
						  )af 
   on a.user_id =af.user_id 
;



drop table if exists ins_offer_detail_m202506;
create table ins_offer_detail_m202506 AS
select user_id,max(case when b.offer_id is not null and to_char(create_date,'yyyymm')='202506' then 1 else 0 end) is_gm,
max(case when state=7 and to_char(done_date,'yyyymm')='202506' then 1 else 0 end) is_ywtd,
max(case when to_char(create_date,'yyyymm')='202506' and op_id like '10086%' and op_id<>'10086666' then 1 else 0 end) is_hdjx,
max(case when a.offer_id like '6%' and to_char(expire_date,'yyyymm')>202509 then 1 else 0 end) is_hyyh
from buff.ins_offer_m202506 a
left join tangds.temp_gm_offer_detail b on a.offer_id=b.offer_id
group by 1


;

drop table if exists tangds.temp_tongyong_bhd_202506;--饱和度
create table tangds.temp_tongyong_bhd_202506 as
select serv_id as user_id 
,sum(free_res_used)/1024 as tongyong_userd  ---流量使用量  单位m
,sum(free_res ) /1024 as free_res ---总的资源量M
,case when sum(free_res )=0 then 0 
      else  sum(free_res_used)/sum(free_res  ) end  ty_bhd
from obods.ods_convenient_exp_m202506 a
join buff.ggprs_day_tsj_m202506 b
 on a.prod_id = b.prod_id
and a.item_id = b.item_code
where region in ('国内')
and b.dx is null 
and b.is_nigth_pkg = '否'
and b.is_time_flash = '否'
group by serv_id
;



-- select a.city_id,qqt_amt,pzqqt_amt,a.qqt_cnt
-- ,普卡,银卡,金卡,白金卡,钻石卡,卓越钻石卡
-- ,a.qqt_cnt-qqt_cnt_online-qqt_cnt_lw qqt_jz-- a.qqt_cnt-b.qqt_cnt qqt_jz--全球通客户净增
-- ,qqt_new,qqt_cnt_online,qqt_cnt_lw,qqtzj,qqtkd,qqtjt,zd_online2yup,pzqqt_gm,pzqqt_jz,pzqqt_zh,ydapp_hy
-- ,gm_st,jc_10086,jc_10086_sy,jc_10086_wh,tsuser3mon_zb,ywtd_zb,hdjx_zb,gyrh_zb,yxrh_zb,ydkh_zb,old_zb,gjmy_zb,stu_zb
-- ,宽带1000,宽带500,宽带300,宽带200,宽带100,宽带100以下,宽带无宽带
-- ,tarpu_fc_0,tarpu_fc_0_30,tarpu_fc_0_50,tarpu_fc_50_100,tarpu_fc_100_150,tarpu_fc_150_200,tarpu_fc_200_300,tarpu_fc_300
-- ,dou_fc_0,dou_fc_0_1,dou_fc_1_5,dou_fc_5_10,dou_fc_15_20,dou_fc_20_30,dou_fc_30_50,dou_fc_50_100,dou_fc_100_200,dou_fc_200
-- ,online_fc_0_1,online_fc_1_5,online_fc_5_10,online_fc_10_15,online_fc_15_20,online_fc_20_30,online_fc_30
-- ,tarpu_dwn_cnt,tarpu_dwn_amt,tarpu_up_cnt,tarpu_up_amt,hyyh_cnt,plan_dwn_cnt
-- ,pzqqt_tarpu,pzqqt_dou,pzqqt_bhd,pzqqt_mou_zj,qqt_tarpu,qqt_dou,qqt_bhd,qqt_mou_zj
-- ,xdr_usercnt,qylq_usercnt,ajwlqqt_usercnt
-- 
-- 
-- 
-- from (select
-- nvl(a.city_id,999) city_id
-- ,round(sum(case when a.IS_GOTONE=1 then tarpu else 0 end)/10000,2) qqt_amt--全球通客户收入万元
-- ,round(sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end)/10000,2) pzqqt_amt--拍照全球通客户收入万元
-- ,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt--全球通客户规模
-- ,count(case when a.IS_GOTONE_PHO=1 then a.user_id else null end) pzqqt_cnt
-- ,count(case when a.GOTONE_NAME='全球通普卡' then a.user_id else null end) 普卡
-- ,count(case when a.GOTONE_NAME='全球通银卡' then a.user_id else null end) 银卡
-- ,count(case when a.GOTONE_NAME='全球通金卡' then a.user_id else null end) 金卡
-- ,count(case when a.GOTONE_NAME='全球通白金卡' then a.user_id else null end) 白金卡
-- ,count(case when a.GOTONE_NAME='全球通钻石卡' then a.user_id else null end) 钻石卡
-- ,count(case when a.GOTONE_NAME='全球通卓越钻石卡' then a.user_id else null end) 卓越钻石卡
-- ,count(case when b.IS_GOTONE=0 and a.IS_GOTONE=1 then a.user_id else null end) qqt_new--全球通客户当月新增
-- ,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_online--拍照全球通客户在网
-- ,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id not in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_lw--拍照全球通客户离网
-- ,count(case when a.IS_GOTONE=1 and c.is_zw=1 then a.user_id else null end) qqtzj--全球通组家客户
-- ,count(case when a.IS_GOTONE=1 and c.kb_user_id is not null then a.user_id else null end) qqtkd--全球通宽带客户
-- ,count(case when a.IS_GOTONE=1 and a.group_id is not null then a.user_id else null end) qqtjt--全球通集团客户
-- ,count(case when nvl(IMEI_LONG,0)>24 and a.IS_GOTONE=1 then a.user_id else null end) zd_online2yup--长机龄客户（2年以上）
-- ,round(count(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.user_id else null end)/pzqqt_cnt*100,2) pzqqt_gm--拍照全球通客户规模保有率
-- ,round(sum(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.tarpu else null end)/pzqqt_amt*100,2) pzqqt_jz--拍照全球通客户收入保有率
-- ,(pzqqt_gm+pzqqt_jz)/2 pzqqt_zh--拍照全球通客户综合保有率
-- ,round(count(case when a.IS_GOTONE=1 and e.serial_number is not null then a.user_id else null end)/qqt_cnt*100,2) ydapp_hy--中国移动APP次月活跃率
-- ,round(count(case when a.IS_GOTONE=1 and f.is_gm=1 then a.user_id else null end)/(count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end))*100,2) gm_st--国漫渗透率
-- ,round(count(case when a.IS_GOTONE=1 and g.product_no is not null then a.user_id else null end)/qqt_cnt*100,2) jc_10086--10088专席使用率
-- ,round(count(case when a.IS_GOTONE=1 and g.is_zxsy=1 then a.user_id else null end)/qqt_cnt*100,2) jc_10086_sy--10088专席使用率
-- ,round(count(case when a.IS_GOTONE=1 and g.is_zxwh=1 then a.user_id else null end)/qqt_cnt*100,2) jc_10086_wh--10088专席使用率
-- --低满
-- ,round(count(case when a.IS_GOTONE=1 and h.acpt_num is not null then a.user_id else null end)/qqt_cnt*100,2) tsuser3mon_zb--投诉用户占比
-- ,round(count(case when a.IS_GOTONE=1 and f.is_ywtd=1 then a.user_id else null end)/qqt_cnt*100,2) ywtd_zb--业务退订用户占比
-- ,round(count(case when a.IS_GOTONE=1 and f.is_hdjx=1 then a.user_id else null end)/qqt_cnt*100,2) hdjx_zb--活动接续用户占比
-- ,round(count(case when a.IS_GOTONE=1 and i.gyrhl=1 then a.user_id else null end)/qqt_cnt*100,2) gyrh_zb--全球通客户固移融合率
-- ,round(count(case when a.IS_GOTONE=1 and j.rxrhl=1 then a.user_id else null end)/qqt_cnt*100,2) yxrh_zb--全球通客户有效融合率
-- ,round(count(case when a.IS_GOTONE=1 and l.user_id is not null then a.user_id else null end)/qqt_cnt*100,2) ydkh_zb--异动客户占比
-- ,round(count(case when a.IS_GOTONE=1 and ((a.sex_id=1 and a.age>60) or (a.sex_id=2 and a.age>55) or (a.sex_id<>1 and a.sex_id<>2 and a.age>60)) then a.user_id else null end)/qqt_cnt*100,2) old_zb--银发用户占比
-- ,round(count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end)/qqt_cnt*100,2) gjmy_zb--国际用户占比
-- ,round(count(case when a.IS_GOTONE=1 and a.is_stu=1 then a.user_id else null end)/qqt_cnt*100,2) stu_zb--校园用户占比
-- 
-- ,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=1000 then a.user_id else null end) 宽带1000
-- ,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=500 then a.user_id else null end) 宽带500
-- ,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=300 then a.user_id else null end) 宽带300
-- ,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=200 then a.user_id else null end) 宽带200
-- ,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=100 then a.user_id else null end) 宽带100
-- ,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)<100 and a.prod_bandwidth>0 then a.user_id else null end) 宽带100以下
-- ,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=0 then a.user_id else null end) 宽带无宽带
-- 
-- ,count(case when a.IS_GOTONE=1 and nvl(tarpu,0)<=0 then a.user_id else null end) tarpu_fc_0
-- ,count(case when a.IS_GOTONE=1 and tarpu>0 and tarpu<30 then a.user_id else null end) tarpu_fc_0_30
-- ,count(case when a.IS_GOTONE=1 and tarpu>=30 and tarpu<50 then a.user_id else null end) tarpu_fc_0_50
-- ,count(case when a.IS_GOTONE=1 and tarpu>=50 and tarpu<100 then a.user_id else null end) tarpu_fc_50_100
-- ,count(case when a.IS_GOTONE=1 and tarpu>=100 and tarpu<150 then a.user_id else null end) tarpu_fc_100_150
-- ,count(case when a.IS_GOTONE=1 and tarpu>=150 and tarpu<200 then a.user_id else null end) tarpu_fc_150_200
-- ,count(case when a.IS_GOTONE=1 and tarpu>=200 and tarpu<300 then a.user_id else null end) tarpu_fc_200_300
-- ,count(case when a.IS_GOTONE=1 and tarpu>=300 then a.user_id else null end) tarpu_fc_300
-- 
-- ,count(case when a.IS_GOTONE=1 and nvl(dou,0)/1024=0 then a.user_id else null end) dou_fc_0
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=0 and dou/1024<1 then a.user_id else null end) dou_fc_0_1
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=1 and dou/1024<5 then a.user_id else null end) dou_fc_1_5
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=5 and dou/1024<10 then a.user_id else null end) dou_fc_5_10
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=10 and dou/1024<20 then a.user_id else null end) dou_fc_15_20
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=20 and dou/1024<30 then a.user_id else null end) dou_fc_20_30
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=30 and dou/1024<50 then a.user_id else null end) dou_fc_30_50
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=50 and dou/1024<100 then a.user_id else null end) dou_fc_50_100
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=100 and dou/1024<200 then a.user_id else null end) dou_fc_100_200
-- ,count(case when a.IS_GOTONE=1 and dou/1024>=200 then a.user_id else null end) dou_fc_200
-- 
-- ,count(case when a.IS_GOTONE=1 and USER_ONLINE>=0 and USER_ONLINE<1 then a.user_id else null end) online_fc_0_1--在网时长分层
-- ,count(case when a.IS_GOTONE=1 and USER_ONLINE>1 and USER_ONLINE<5 then a.user_id else null end) online_fc_1_5
-- ,count(case when a.IS_GOTONE=1 and USER_ONLINE>5 and USER_ONLINE<10 then a.user_id else null end) online_fc_5_10
-- ,count(case when a.IS_GOTONE=1 and USER_ONLINE>10 and USER_ONLINE<15 then a.user_id else null end) online_fc_10_15
-- ,count(case when a.IS_GOTONE=1 and USER_ONLINE>15 and USER_ONLINE<20 then a.user_id else null end) online_fc_15_20
-- ,count(case when a.IS_GOTONE=1 and USER_ONLINE>20 and USER_ONLINE<30 then a.user_id else null end) online_fc_20_30
-- ,count(case when a.IS_GOTONE=1 and USER_ONLINE>30 then a.user_id else null end) online_fc_30
-- 
-- ,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.user_id else null end) tarpu_dwn_cnt--价值下降客户
-- ,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_dwn_amt--价值下降客户下降总价值
-- ,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.user_id else null end) tarpu_up_cnt--价值提升客户
-- ,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_up_amt--价值提升客户提升总价值
-- ,count(case when a.IS_GOTONE=1 and f.is_hyyh=1 then a.user_id else null end) hyyh_cnt--合约客户
-- ,count(case when a.IS_GOTONE=1 and (PLAN_FEE-(ARPU-TARPU))<(PLAN_FEE-(ARPU_PRE1-TARPU_PRE1)) then a.user_id else null end) plan_dwn_cnt--套餐降档客户
-- 
-- ,round(sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end)/pzqqt_cnt,2) pzqqt_tarpu--拍照全球通客户TARPU
-- ,round(sum(case when a.IS_GOTONE_PHO=1 then dou/1024 else 0 end)/pzqqt_cnt,2) pzqqt_dou--拍照全球通客户DOU
-- ,round(sum(case when a.IS_GOTONE_PHO=1 then tongyong_userd else 0 end)/(sum(case when a.IS_GOTONE_PHO=1 then free_res else 0 end))*100,2) pzqqt_bhd--拍照全球通客户通用包月流量饱和度
-- ,round(sum(case when a.IS_GOTONE_PHO=1 then OUT_CALL_DURATION_M else 0 end)/pzqqt_cnt,2) pzqqt_mou_zj--拍照全球通客户主叫MOU
-- ,round(sum(case when a.IS_GOTONE=1 then tarpu else 0 end)/qqt_cnt,2) qqt_tarpu--当前全球通客户TARPU
-- ,round(sum(case when a.IS_GOTONE=1 then dou/1024 else 0 end)/qqt_cnt,2) qqt_dou--当前全球通客户DOU
-- ,round(sum(case when a.IS_GOTONE=1 then tongyong_userd else 0 end)/(sum(case when a.IS_GOTONE=1 then free_res else 0 end))*100,2) qqt_bhd--当前全球通客户通用包月流量饱和度
-- ,round(sum(case when a.IS_GOTONE=1 then OUT_CALL_DURATION_M else 0 end)/qqt_cnt,2) qqt_mou_zj--当前全球通客户主叫MOU
-- ,count(case when a.IS_GOTONE=1 and o.is_xdr=1 then a.user_id else null end) xdr_usercnt--星动日
-- ,count(case when a.IS_GOTONE=1 and o.user_id is not null then a.user_id else null end) qylq_usercnt--权益领取客户
-- ,count(case when a.IS_GOTONE=1 and p.user_id is not null then a.user_id else null end) ajwlqqt_usercnt--三大行动
-- 
-- 
-- 
-- 
-- 
-- from
-- bdba.MKT_USER_PROFILE_M202506 a
-- left join (select user_id,IS_GOTONE from bdba.MKT_USER_PROFILE_M202505) b on a.user_id=b.user_id
-- left join temp_it_member_all_detail c on a.user_id=c.user_id
-- --left join obdw.dwv_home_cable_m202506 d on a.user_id=d.user_id
-- left join tangds.JZYY_CMBHPT_10002_202506 e on a.product_no=e.serial_number--(select distinct serial_number from tangds.JZYY_CMBHPT_10002_202506)来源internetdb.JZYY_CMBHPT_10002_
-- left join ins_offer_detail_m202506 f on a.user_id=f.user_id
-- left join (select product_no,max(case when b.out_call_counts>0 then 1 else 0 end) is_zxsy
-- ,max(case when b.in_call_counts>0 then 1 else 0 end) is_zxwh--,count(1) cnt
-- from (select * from obdw.dw_call_opp_m202506) b --差异点
-- where (b.opposite_regular_no like '%10086' or
-- b.opposite_regular_no like '%10085')
-- and length(b.opposite_regular_no)<=9 group by 1) g on a.product_no=g.product_no
-- left join (select acpt_num from (select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202504 union all
-- select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202505 union all
-- select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202506) group by 1) h on a.product_no=h.acpt_num
-- left join (select user_id,case when is_gyrhhy=1 or is_tfkzcy=1 then 1 else 0 end gyrhl
-- from OBDW.DW_HOME_BASS1_GYRHL_M202506) i on a.user_id=i.user_id
-- left join (select user_id,case when (eff_fuse_id =1 or kd_act_id =1) then 1 else 0 end rxrhl
-- from obdw.dw_home_yxrhl_m202506) j on a.user_id=j.user_id
-- left join (select distinct user_id from obdw.dw_nb_roamuser_gj_dm where substr(op_time,1,6)='202506')k on a.user_id=k.user_id
-- left join (select user_id from xuzeshuai.temp_ydkh_detail_m202506 where is_qqt=1
-- and is_whyk_new+is_ywzk+is_dll+is_ywjc+is_ysgw_new+doumou_sj+dou_to0+dou_dwn+is_sjtc+is_oldplan>0 and nvl(gross_score,0)<3) l on a.user_id=l.user_id
-- left join (select user_id,OUT_CALL_DURATION_M,nvl(user_online,0)/12 user_online from obdw.dwv_nb_product_m202506) m on a.user_id=m.user_id
-- left join temp_tongyong_bhd_202506 n on a.user_id=n.user_id
-- left join (select user_id,max(case when fld07='星动日' then 1 else 0 end) is_xdr from OBDW.DW_VGOP_QYZX_70206_202506 group by 1) o on a.user_id=o.user_id
-- left join temp_ajwlqqt_user_m202506 p on a.user_id=p.user_id
-- group by rollup(a.city_id)
-- )a
-- -- left join (select nvl(city_id,999) city_id,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt from bdba.MKT_USER_PROFILE_M202505 a group by rollup(city_id)) b on a.city_id=b.city_id
-- 
-- order by decode(a.city_id,410,420,a.city_id)
-- ;







drop table temp_10086_call_202506;
create table temp_10086_call_202506 as
select product_no,max(case when b.out_call_counts>0 then 1 else 0 end) is_zxsy
,max(case when b.in_call_counts>0 then 1 else 0 end) is_zxwh--,count(1) cnt
from (select * from obdw.dw_call_opp_m202506) b --差异点
where (b.opposite_regular_no like '%10086' or
b.opposite_regular_no like '%10085')
and length(b.opposite_regular_no)<=9 group by 1
;






create table temp_test_101 as
select 202506 op_time,2025090001 rep_no,a.city_id,b.city_name,a.city_id county_id,b.city_name county_name,a.city_id grid_id_1,b.city_name grid_name_1
,qqt_amt,nullif(pzqqt_amt,0),a.qqt_cnt
,普卡,银卡,金卡,白金卡,钻石卡,卓越钻石卡
,a.qqt_cnt-qqt_cnt_online-qqt_cnt_lw qqt_jz-- a.qqt_cnt-b.qqt_cnt qqt_jz--全球通客户净增
,qqt_new,qqt_cnt_online,qqt_cnt_lw,qqtzj,qqtkd,qqtjt,zd_online2yup,pzqqt_gm,pzqqt_jz,pzqqt_zh,ydapp_hy
,gm_st,jc_10086_sy,jc_10086_wh,null,tsuser3mon_zb,ywtd_zb,hdjx_zb,gyrh_zb,yxrh_zb,ydkh_zb,old_zb,gjmy_zb,stu_zb
,宽带1000,宽带500,宽带300,宽带200,宽带100,宽带100以下,宽带无宽带
,tarpu_fc_0,tarpu_fc_0_30,tarpu_fc_0_50,tarpu_fc_50_100,tarpu_fc_100_150,tarpu_fc_150_200,tarpu_fc_200_300,tarpu_fc_300
,dou_fc_0,dou_fc_0_1,dou_fc_1_5,dou_fc_5_10,dou_fc_15_20,dou_fc_20_30,dou_fc_30_50,dou_fc_50_100,dou_fc_100_200,dou_fc_200
,online_fc_0_1,online_fc_1_5,online_fc_5_10,online_fc_10_15,online_fc_15_20,online_fc_20_30,online_fc_30
,tarpu_dwn_cnt,tarpu_dwn_amt,tarpu_up_cnt,tarpu_up_amt,hyyh_cnt,plan_dwn_cnt
,pzqqt_tarpu,pzqqt_dou,pzqqt_bhd,pzqqt_mou_zj,qqt_tarpu,qqt_dou,qqt_bhd,qqt_mou_zj
,xdr_usercnt,qylq_usercnt,ajwlqqt_usercnt



from (select
nvl(a.city_id,999) city_id
,sum(case when a.IS_GOTONE=1 then tarpu else 0 end) qqt_amt--全球通客户收入
,sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end) pzqqt_amt--拍照全球通客户收入
,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt--全球通客户规模
,count(case when a.IS_GOTONE_PHO=1 then a.user_id else null end) pzqqt_cnt
,count(case when a.GOTONE_NAME='全球通普卡' then a.user_id else null end) 普卡
,count(case when a.GOTONE_NAME='全球通银卡' then a.user_id else null end) 银卡
,count(case when a.GOTONE_NAME='全球通金卡' then a.user_id else null end) 金卡
,count(case when a.GOTONE_NAME='全球通白金卡' then a.user_id else null end) 白金卡
,count(case when a.GOTONE_NAME='全球通钻石卡' then a.user_id else null end) 钻石卡
,count(case when a.GOTONE_NAME='全球通卓越钻石卡' then a.user_id else null end) 卓越钻石卡
,count(case when b.IS_GOTONE=0 and a.IS_GOTONE=1 then a.user_id else null end) qqt_new--全球通客户当月新增
,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_online--拍照全球通客户在网
,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id not in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_lw--拍照全球通客户离网
,count(case when a.IS_GOTONE=1 and c.is_zw=1 then a.user_id else null end) qqtzj--全球通组家客户
,count(case when a.IS_GOTONE=1 and c.kb_user_id is not null then a.user_id else null end) qqtkd--全球通宽带客户
,count(case when a.IS_GOTONE=1 and a.group_id is not null then a.user_id else null end) qqtjt--全球通集团客户
,count(case when nvl(IMEI_LONG,0)>24 and a.IS_GOTONE=1 then a.user_id else null end) zd_online2yup--长机龄客户（2年以上）
,round(count(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.user_id else null end)/nullif(pzqqt_cnt,0)*100,2) pzqqt_gm--拍照全球通客户规模保有率
,round(sum(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.tarpu else null end)/nullif(pzqqt_amt,0)*100,2) pzqqt_jz--拍照全球通客户收入保有率
,(pzqqt_gm+pzqqt_jz)/2 pzqqt_zh--拍照全球通客户综合保有率
,round(count(case when a.IS_GOTONE=1 and e.serial_number is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ydapp_hy--中国移动APP次月活跃率
,round(count(case when a.IS_GOTONE=1 and f.is_gm=1 then a.user_id else null end)/nullif((count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end)),0)*100,2) gm_st--国漫渗透率
,round(count(case when a.IS_GOTONE=1 and g.is_zxsy=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) jc_10086_sy--10088专席使用率
,round(count(case when a.IS_GOTONE=1 and g.is_zxwh=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) jc_10086_wh--10088专席外呼率
,null dmyh_zb--低满
,round(count(case when a.IS_GOTONE=1 and h.acpt_num is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) tsuser3mon_zb--投诉用户占比
,round(count(case when a.IS_GOTONE=1 and f.is_ywtd=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ywtd_zb--业务退订用户占比
,round(count(case when a.IS_GOTONE=1 and f.is_hdjx=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) hdjx_zb--活动接续用户占比
,round(count(case when a.IS_GOTONE=1 and i.gyrhl=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) gyrh_zb--全球通客户固移融合率
,round(count(case when a.IS_GOTONE=1 and j.rxrhl=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) yxrh_zb--全球通客户有效融合率
,round(count(case when a.IS_GOTONE=1 and l.user_id is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ydkh_zb--异动客户占比
,round(count(case when a.IS_GOTONE=1 and ((a.sex_id=1 and a.age>60) or (a.sex_id=2 and a.age>55) or (a.sex_id<>1 and a.sex_id<>2 and a.age>60)) then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) old_zb--银发用户占比
,round(count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) gjmy_zb--国际用户占比
,round(count(case when a.IS_GOTONE=1 and a.is_stu=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) stu_zb--校园用户占比

,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=1000 then a.user_id else null end) 宽带1000
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=500 then a.user_id else null end) 宽带500
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=300 then a.user_id else null end) 宽带300
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=200 then a.user_id else null end) 宽带200
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=100 then a.user_id else null end) 宽带100
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)<100 and a.prod_bandwidth>0 then a.user_id else null end) 宽带100以下
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=0 then a.user_id else null end) 宽带无宽带

,count(case when a.IS_GOTONE=1 and nvl(tarpu,0)<=0 then a.user_id else null end) tarpu_fc_0
,count(case when a.IS_GOTONE=1 and tarpu>0 and tarpu<30 then a.user_id else null end) tarpu_fc_0_30
,count(case when a.IS_GOTONE=1 and tarpu>=30 and tarpu<50 then a.user_id else null end) tarpu_fc_0_50
,count(case when a.IS_GOTONE=1 and tarpu>=50 and tarpu<100 then a.user_id else null end) tarpu_fc_50_100
,count(case when a.IS_GOTONE=1 and tarpu>=100 and tarpu<150 then a.user_id else null end) tarpu_fc_100_150
,count(case when a.IS_GOTONE=1 and tarpu>=150 and tarpu<200 then a.user_id else null end) tarpu_fc_150_200
,count(case when a.IS_GOTONE=1 and tarpu>=200 and tarpu<300 then a.user_id else null end) tarpu_fc_200_300
,count(case when a.IS_GOTONE=1 and tarpu>=300 then a.user_id else null end) tarpu_fc_300

,count(case when a.IS_GOTONE=1 and nvl(dou,0)/1024=0 then a.user_id else null end) dou_fc_0
,count(case when a.IS_GOTONE=1 and dou/1024>=0 and dou/1024<1 then a.user_id else null end) dou_fc_0_1
,count(case when a.IS_GOTONE=1 and dou/1024>=1 and dou/1024<5 then a.user_id else null end) dou_fc_1_5
,count(case when a.IS_GOTONE=1 and dou/1024>=5 and dou/1024<10 then a.user_id else null end) dou_fc_5_10
,count(case when a.IS_GOTONE=1 and dou/1024>=10 and dou/1024<20 then a.user_id else null end) dou_fc_15_20
,count(case when a.IS_GOTONE=1 and dou/1024>=20 and dou/1024<30 then a.user_id else null end) dou_fc_20_30
,count(case when a.IS_GOTONE=1 and dou/1024>=30 and dou/1024<50 then a.user_id else null end) dou_fc_30_50
,count(case when a.IS_GOTONE=1 and dou/1024>=50 and dou/1024<100 then a.user_id else null end) dou_fc_50_100
,count(case when a.IS_GOTONE=1 and dou/1024>=100 and dou/1024<200 then a.user_id else null end) dou_fc_100_200
,count(case when a.IS_GOTONE=1 and dou/1024>=200 then a.user_id else null end) dou_fc_200

,count(case when a.IS_GOTONE=1 and USER_ONLINE>=0 and USER_ONLINE<1 then a.user_id else null end) online_fc_0_1--在网时长分层
,count(case when a.IS_GOTONE=1 and USER_ONLINE>1 and USER_ONLINE<5 then a.user_id else null end) online_fc_1_5
,count(case when a.IS_GOTONE=1 and USER_ONLINE>5 and USER_ONLINE<10 then a.user_id else null end) online_fc_5_10
,count(case when a.IS_GOTONE=1 and USER_ONLINE>10 and USER_ONLINE<15 then a.user_id else null end) online_fc_10_15
,count(case when a.IS_GOTONE=1 and USER_ONLINE>15 and USER_ONLINE<20 then a.user_id else null end) online_fc_15_20
,count(case when a.IS_GOTONE=1 and USER_ONLINE>20 and USER_ONLINE<30 then a.user_id else null end) online_fc_20_30
,count(case when a.IS_GOTONE=1 and USER_ONLINE>30 then a.user_id else null end) online_fc_30

,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.user_id else null end) tarpu_dwn_cnt--价值下降客户
,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_dwn_amt--价值下降客户下降总价值
,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.user_id else null end) tarpu_up_cnt--价值提升客户
,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_up_amt--价值提升客户提升总价值
,count(case when a.IS_GOTONE=1 and f.is_hyyh=1 then a.user_id else null end) hyyh_cnt--合约客户
,count(case when a.IS_GOTONE=1 and (PLAN_FEE-(ARPU-TARPU))<(PLAN_FEE-(ARPU_PRE1-TARPU_PRE1)) then a.user_id else null end) plan_dwn_cnt--套餐降档客户

,round(sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end)/nullif(pzqqt_cnt,0),2) pzqqt_tarpu--拍照全球通客户TARPU
,round(sum(case when a.IS_GOTONE_PHO=1 then dou/1024 else 0 end)/nullif(pzqqt_cnt,0),2) pzqqt_dou--拍照全球通客户DOU
,round(sum(case when a.IS_GOTONE_PHO=1 then tongyong_userd else 0 end)/nullif((sum(case when a.IS_GOTONE_PHO=1 then free_res else 0 end)),0)*100,2) pzqqt_bhd--拍照全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE_PHO=1 then OUT_CALL_DURATION_M else 0 end)/nullif(pzqqt_cnt,0),2) pzqqt_mou_zj--拍照全球通客户主叫MOU
,round(sum(case when a.IS_GOTONE=1 then tarpu else 0 end)/nullif(qqt_cnt,0),2) qqt_tarpu--当前全球通客户TARPU
,round(sum(case when a.IS_GOTONE=1 then dou/1024 else 0 end)/nullif(qqt_cnt,0),2) qqt_dou--当前全球通客户DOU
,round(sum(case when a.IS_GOTONE=1 then tongyong_userd else 0 end)/nullif((sum(case when a.IS_GOTONE=1 then free_res else 0 end)),0)*100,2) qqt_bhd--当前全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE=1 then OUT_CALL_DURATION_M else 0 end)/nullif(qqt_cnt,0),2) qqt_mou_zj--当前全球通客户主叫MOU
,count(case when a.IS_GOTONE=1 and o.is_xdr=1 then a.user_id else null end) xdr_usercnt--星动日
,count(case when a.IS_GOTONE=1 and o.user_id is not null then a.user_id else null end) qylq_usercnt--权益领取客户
,count(case when a.IS_GOTONE=1 and p.user_id is not null then a.user_id else null end) ajwlqqt_usercnt--三大行动





from
bdba.MKT_USER_PROFILE_M202506 a
left join (select user_id,IS_GOTONE from bdba.MKT_USER_PROFILE_M202505) b on a.user_id=b.user_id
left join temp_it_member_all_detail c on a.user_id=c.user_id
--left join obdw.dwv_home_cable_m202506 d on a.user_id=d.user_id
left join tangds.JZYY_CMBHPT_10002_202506 e on a.product_no=e.serial_number--(select distinct serial_number from internetdb.JZYY_CMBHPT_10002_202506)
left join ins_offer_detail_m202506 f on a.user_id=f.user_id
left join temp_10086_call_202506 g on a.product_no=g.product_no
left join (select acpt_num from (select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202504 union all
select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202505 union all
select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202506) group by 1) h on a.product_no=h.acpt_num
left join (select user_id,case when is_gyrhhy=1 or is_tfkzcy=1 then 1 else 0 end gyrhl
from OBDW.DW_HOME_BASS1_GYRHL_M202506) i on a.user_id=i.user_id
left join (select user_id,case when (eff_fuse_id =1 or kd_act_id =1) then 1 else 0 end rxrhl
from obdw.dw_home_yxrhl_m202506) j on a.user_id=j.user_id
left join (select distinct user_id from obdw.dw_nb_roamuser_gj_dm where substr(op_time,1,6)='202506')k on a.user_id=k.user_id
left join (select user_id from xuzeshuai.temp_ydkh_detail_m202506 where is_qqt=1
and is_whyk_new+is_ywzk+is_dll+is_ywjc+is_ysgw_new+doumou_sj+dou_to0+dou_dwn+is_sjtc+is_oldplan>0 and nvl(gross_score,0)<3) l on a.user_id=l.user_id
left join (select user_id,OUT_CALL_DURATION_M,nvl(user_online,0)/12 user_online from obdw.dwv_nb_product_m202506) m on a.user_id=m.user_id
left join temp_tongyong_bhd_202506 n on a.user_id=n.user_id
left join (select user_id,max(case when fld07='星动日' then 1 else 0 end) is_xdr from OBDW.DW_VGOP_QYZX_70206_202506 group by 1) o on a.user_id=o.user_id
left join temp_ajwlqqt_user_m202506 p on a.user_id=p.user_id
group by rollup(a.city_id)
)a
-- left join (select nvl(city_id,999) city_id,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt from bdba.MKT_USER_PROFILE_M202505 a group by rollup(city_id)) b on a.city_id=b.city_id

left join obdim.dim_pub_city b on a.city_id=b.city_id

union all

select 202506 op_time,2025090001 rep_no,a.city_id,c.city_name,a.county_id,b.county_name,a.county_id grid_id_1,b.county_name grid_name_1
,qqt_amt,nullif(pzqqt_amt,0),a.qqt_cnt
,普卡,银卡,金卡,白金卡,钻石卡,卓越钻石卡
,a.qqt_cnt-qqt_cnt_online-qqt_cnt_lw qqt_jz-- a.qqt_cnt-b.qqt_cnt qqt_jz--全球通客户净增
,qqt_new,qqt_cnt_online,qqt_cnt_lw,qqtzj,qqtkd,qqtjt,zd_online2yup,pzqqt_gm,pzqqt_jz,pzqqt_zh,ydapp_hy
,gm_st,jc_10086_sy,jc_10086_wh,null,tsuser3mon_zb,ywtd_zb,hdjx_zb,gyrh_zb,yxrh_zb,ydkh_zb,old_zb,gjmy_zb,stu_zb
,宽带1000,宽带500,宽带300,宽带200,宽带100,宽带100以下,宽带无宽带
,tarpu_fc_0,tarpu_fc_0_30,tarpu_fc_0_50,tarpu_fc_50_100,tarpu_fc_100_150,tarpu_fc_150_200,tarpu_fc_200_300,tarpu_fc_300
,dou_fc_0,dou_fc_0_1,dou_fc_1_5,dou_fc_5_10,dou_fc_15_20,dou_fc_20_30,dou_fc_30_50,dou_fc_50_100,dou_fc_100_200,dou_fc_200
,online_fc_0_1,online_fc_1_5,online_fc_5_10,online_fc_10_15,online_fc_15_20,online_fc_20_30,online_fc_30
,tarpu_dwn_cnt,tarpu_dwn_amt,tarpu_up_cnt,tarpu_up_amt,hyyh_cnt,plan_dwn_cnt
,pzqqt_tarpu,pzqqt_dou,pzqqt_bhd,pzqqt_mou_zj,qqt_tarpu,qqt_dou,qqt_bhd,qqt_mou_zj
,xdr_usercnt,qylq_usercnt,ajwlqqt_usercnt



from (select
a.city_id,a.county_id
,sum(case when a.IS_GOTONE=1 then tarpu else 0 end) qqt_amt--全球通客户收入
,sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end) pzqqt_amt--拍照全球通客户收入
,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt--全球通客户规模
,count(case when a.IS_GOTONE_PHO=1 then a.user_id else null end) pzqqt_cnt
,count(case when a.GOTONE_NAME='全球通普卡' then a.user_id else null end) 普卡
,count(case when a.GOTONE_NAME='全球通银卡' then a.user_id else null end) 银卡
,count(case when a.GOTONE_NAME='全球通金卡' then a.user_id else null end) 金卡
,count(case when a.GOTONE_NAME='全球通白金卡' then a.user_id else null end) 白金卡
,count(case when a.GOTONE_NAME='全球通钻石卡' then a.user_id else null end) 钻石卡
,count(case when a.GOTONE_NAME='全球通卓越钻石卡' then a.user_id else null end) 卓越钻石卡
,count(case when b.IS_GOTONE=0 and a.IS_GOTONE=1 then a.user_id else null end) qqt_new--全球通客户当月新增
,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_online--拍照全球通客户在网
,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id not in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_lw--拍照全球通客户离网
,count(case when a.IS_GOTONE=1 and c.is_zw=1 then a.user_id else null end) qqtzj--全球通组家客户
,count(case when a.IS_GOTONE=1 and c.kb_user_id is not null then a.user_id else null end) qqtkd--全球通宽带客户
,count(case when a.IS_GOTONE=1 and a.group_id is not null then a.user_id else null end) qqtjt--全球通集团客户
,count(case when nvl(IMEI_LONG,0)>24 and a.IS_GOTONE=1 then a.user_id else null end) zd_online2yup--长机龄客户（2年以上）
,round(count(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.user_id else null end)/nullif(pzqqt_cnt,0)*100,2) pzqqt_gm--拍照全球通客户规模保有率
,round(sum(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.tarpu else null end)/nullif(pzqqt_amt,0)*100,2) pzqqt_jz--拍照全球通客户收入保有率
,(pzqqt_gm+pzqqt_jz)/2 pzqqt_zh--拍照全球通客户综合保有率
,round(count(case when a.IS_GOTONE=1 and e.serial_number is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ydapp_hy--中国移动APP次月活跃率
,round(count(case when a.IS_GOTONE=1 and f.is_gm=1 then a.user_id else null end)/nullif((count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end)),0)*100,2) gm_st--国漫渗透率
,round(count(case when a.IS_GOTONE=1 and g.is_zxsy=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) jc_10086_sy--10088专席使用率
,round(count(case when a.IS_GOTONE=1 and g.is_zxwh=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) jc_10086_wh--10088专席外呼率
,null dmyh_zb--低满
,round(count(case when a.IS_GOTONE=1 and h.acpt_num is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) tsuser3mon_zb--投诉用户占比
,round(count(case when a.IS_GOTONE=1 and f.is_ywtd=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ywtd_zb--业务退订用户占比
,round(count(case when a.IS_GOTONE=1 and f.is_hdjx=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) hdjx_zb--活动接续用户占比
,round(count(case when a.IS_GOTONE=1 and i.gyrhl=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) gyrh_zb--全球通客户固移融合率
,round(count(case when a.IS_GOTONE=1 and j.rxrhl=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) yxrh_zb--全球通客户有效融合率
,round(count(case when a.IS_GOTONE=1 and l.user_id is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ydkh_zb--异动客户占比
,round(count(case when a.IS_GOTONE=1 and ((a.sex_id=1 and a.age>60) or (a.sex_id=2 and a.age>55) or (a.sex_id<>1 and a.sex_id<>2 and a.age>60)) then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) old_zb--银发用户占比
,round(count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) gjmy_zb--国际用户占比
,round(count(case when a.IS_GOTONE=1 and a.is_stu=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) stu_zb--校园用户占比

,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=1000 then a.user_id else null end) 宽带1000
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=500 then a.user_id else null end) 宽带500
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=300 then a.user_id else null end) 宽带300
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=200 then a.user_id else null end) 宽带200
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=100 then a.user_id else null end) 宽带100
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)<100 and a.prod_bandwidth>0 then a.user_id else null end) 宽带100以下
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=0 then a.user_id else null end) 宽带无宽带

,count(case when a.IS_GOTONE=1 and nvl(tarpu,0)<=0 then a.user_id else null end) tarpu_fc_0
,count(case when a.IS_GOTONE=1 and tarpu>0 and tarpu<30 then a.user_id else null end) tarpu_fc_0_30
,count(case when a.IS_GOTONE=1 and tarpu>=30 and tarpu<50 then a.user_id else null end) tarpu_fc_0_50
,count(case when a.IS_GOTONE=1 and tarpu>=50 and tarpu<100 then a.user_id else null end) tarpu_fc_50_100
,count(case when a.IS_GOTONE=1 and tarpu>=100 and tarpu<150 then a.user_id else null end) tarpu_fc_100_150
,count(case when a.IS_GOTONE=1 and tarpu>=150 and tarpu<200 then a.user_id else null end) tarpu_fc_150_200
,count(case when a.IS_GOTONE=1 and tarpu>=200 and tarpu<300 then a.user_id else null end) tarpu_fc_200_300
,count(case when a.IS_GOTONE=1 and tarpu>=300 then a.user_id else null end) tarpu_fc_300

,count(case when a.IS_GOTONE=1 and nvl(dou,0)/1024=0 then a.user_id else null end) dou_fc_0
,count(case when a.IS_GOTONE=1 and dou/1024>=0 and dou/1024<1 then a.user_id else null end) dou_fc_0_1
,count(case when a.IS_GOTONE=1 and dou/1024>=1 and dou/1024<5 then a.user_id else null end) dou_fc_1_5
,count(case when a.IS_GOTONE=1 and dou/1024>=5 and dou/1024<10 then a.user_id else null end) dou_fc_5_10
,count(case when a.IS_GOTONE=1 and dou/1024>=10 and dou/1024<20 then a.user_id else null end) dou_fc_15_20
,count(case when a.IS_GOTONE=1 and dou/1024>=20 and dou/1024<30 then a.user_id else null end) dou_fc_20_30
,count(case when a.IS_GOTONE=1 and dou/1024>=30 and dou/1024<50 then a.user_id else null end) dou_fc_30_50
,count(case when a.IS_GOTONE=1 and dou/1024>=50 and dou/1024<100 then a.user_id else null end) dou_fc_50_100
,count(case when a.IS_GOTONE=1 and dou/1024>=100 and dou/1024<200 then a.user_id else null end) dou_fc_100_200
,count(case when a.IS_GOTONE=1 and dou/1024>=200 then a.user_id else null end) dou_fc_200

,count(case when a.IS_GOTONE=1 and USER_ONLINE>=0 and USER_ONLINE<1 then a.user_id else null end) online_fc_0_1--在网时长分层
,count(case when a.IS_GOTONE=1 and USER_ONLINE>1 and USER_ONLINE<5 then a.user_id else null end) online_fc_1_5
,count(case when a.IS_GOTONE=1 and USER_ONLINE>5 and USER_ONLINE<10 then a.user_id else null end) online_fc_5_10
,count(case when a.IS_GOTONE=1 and USER_ONLINE>10 and USER_ONLINE<15 then a.user_id else null end) online_fc_10_15
,count(case when a.IS_GOTONE=1 and USER_ONLINE>15 and USER_ONLINE<20 then a.user_id else null end) online_fc_15_20
,count(case when a.IS_GOTONE=1 and USER_ONLINE>20 and USER_ONLINE<30 then a.user_id else null end) online_fc_20_30
,count(case when a.IS_GOTONE=1 and USER_ONLINE>30 then a.user_id else null end) online_fc_30

,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.user_id else null end) tarpu_dwn_cnt--价值下降客户
,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_dwn_amt--价值下降客户下降总价值
,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.user_id else null end) tarpu_up_cnt--价值提升客户
,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_up_amt--价值提升客户提升总价值
,count(case when a.IS_GOTONE=1 and f.is_hyyh=1 then a.user_id else null end) hyyh_cnt--合约客户
,count(case when a.IS_GOTONE=1 and (PLAN_FEE-(ARPU-TARPU))<(PLAN_FEE-(ARPU_PRE1-TARPU_PRE1)) then a.user_id else null end) plan_dwn_cnt--套餐降档客户

,round(sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end)/nullif(pzqqt_cnt,0),2) pzqqt_tarpu--拍照全球通客户TARPU
,round(sum(case when a.IS_GOTONE_PHO=1 then dou/1024 else 0 end)/nullif(pzqqt_cnt,0),2) pzqqt_dou--拍照全球通客户DOU
,round(sum(case when a.IS_GOTONE_PHO=1 then tongyong_userd else 0 end)/nullif((sum(case when a.IS_GOTONE_PHO=1 then free_res else 0 end)),0)*100,2) pzqqt_bhd--拍照全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE_PHO=1 then OUT_CALL_DURATION_M else 0 end)/nullif(pzqqt_cnt,0),2) pzqqt_mou_zj--拍照全球通客户主叫MOU
,round(sum(case when a.IS_GOTONE=1 then tarpu else 0 end)/nullif(qqt_cnt,0),2) qqt_tarpu--当前全球通客户TARPU
,round(sum(case when a.IS_GOTONE=1 then dou/1024 else 0 end)/nullif(qqt_cnt,0),2) qqt_dou--当前全球通客户DOU
,round(sum(case when a.IS_GOTONE=1 then tongyong_userd else 0 end)/nullif((sum(case when a.IS_GOTONE=1 then free_res else 0 end)),0)*100,2) qqt_bhd--当前全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE=1 then OUT_CALL_DURATION_M else 0 end)/nullif(qqt_cnt,0),2) qqt_mou_zj--当前全球通客户主叫MOU
,count(case when a.IS_GOTONE=1 and o.is_xdr=1 then a.user_id else null end) xdr_usercnt--星动日
,count(case when a.IS_GOTONE=1 and o.user_id is not null then a.user_id else null end) qylq_usercnt--权益领取客户
,count(case when a.IS_GOTONE=1 and p.user_id is not null then a.user_id else null end) ajwlqqt_usercnt--三大行动





from
bdba.MKT_USER_PROFILE_M202506 a
left join (select user_id,IS_GOTONE from bdba.MKT_USER_PROFILE_M202505) b on a.user_id=b.user_id
left join temp_it_member_all_detail c on a.user_id=c.user_id
--left join obdw.dwv_home_cable_m202506 d on a.user_id=d.user_id
left join tangds.JZYY_CMBHPT_10002_202506 e on a.product_no=e.serial_number--(select distinct serial_number from internetdb.JZYY_CMBHPT_10002_202506)
left join ins_offer_detail_m202506 f on a.user_id=f.user_id
left join temp_10086_call_202506 g on a.product_no=g.product_no
left join (select acpt_num from (select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202504 union all
select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202505 union all
select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202506) group by 1) h on a.product_no=h.acpt_num
left join (select user_id,case when is_gyrhhy=1 or is_tfkzcy=1 then 1 else 0 end gyrhl
from OBDW.DW_HOME_BASS1_GYRHL_M202506) i on a.user_id=i.user_id
left join (select user_id,case when (eff_fuse_id =1 or kd_act_id =1) then 1 else 0 end rxrhl
from obdw.dw_home_yxrhl_m202506) j on a.user_id=j.user_id
left join (select distinct user_id from obdw.dw_nb_roamuser_gj_dm where substr(op_time,1,6)='202506')k on a.user_id=k.user_id
left join (select user_id from xuzeshuai.temp_ydkh_detail_m202506 where is_qqt=1
and is_whyk_new+is_ywzk+is_dll+is_ywjc+is_ysgw_new+doumou_sj+dou_to0+dou_dwn+is_sjtc+is_oldplan>0 and nvl(gross_score,0)<3) l on a.user_id=l.user_id
left join (select user_id,OUT_CALL_DURATION_M,nvl(user_online,0)/12 user_online from obdw.dwv_nb_product_m202506) m on a.user_id=m.user_id
left join temp_tongyong_bhd_202506 n on a.user_id=n.user_id
left join (select user_id,max(case when fld07='星动日' then 1 else 0 end) is_xdr from OBDW.DW_VGOP_QYZX_70206_202506 group by 1) o on a.user_id=o.user_id
left join temp_ajwlqqt_user_m202506 p on a.user_id=p.user_id
group by a.city_id,a.county_id
)a
-- left join (select nvl(city_id,999) city_id,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt from bdba.MKT_USER_PROFILE_M202505 a group by rollup(city_id)) b on a.city_id=b.city_id

left join obdim.dim_pub_county b on a.city_id=b.city_id and a.county_id=b.county_id
left join obdim.dim_pub_city c on a.city_id=c.city_id

union all

select 202506 op_time,2025090001 rep_no,b.city_id,b.city_name,b.county_id,b.county_name,to_number(a.grid_id_1) grid_id_1,b.grid_name_1
,qqt_amt,nullif(pzqqt_amt,0),a.qqt_cnt
,普卡,银卡,金卡,白金卡,钻石卡,卓越钻石卡
,a.qqt_cnt-qqt_cnt_online-qqt_cnt_lw qqt_jz-- a.qqt_cnt-b.qqt_cnt qqt_jz--全球通客户净增
,qqt_new,qqt_cnt_online,qqt_cnt_lw,qqtzj,qqtkd,qqtjt,zd_online2yup,pzqqt_gm,pzqqt_jz,pzqqt_zh,ydapp_hy
,gm_st,jc_10086_sy,jc_10086_wh,null,tsuser3mon_zb,ywtd_zb,hdjx_zb,gyrh_zb,yxrh_zb,ydkh_zb,old_zb,gjmy_zb,stu_zb
,宽带1000,宽带500,宽带300,宽带200,宽带100,宽带100以下,宽带无宽带
,tarpu_fc_0,tarpu_fc_0_30,tarpu_fc_0_50,tarpu_fc_50_100,tarpu_fc_100_150,tarpu_fc_150_200,tarpu_fc_200_300,tarpu_fc_300
,dou_fc_0,dou_fc_0_1,dou_fc_1_5,dou_fc_5_10,dou_fc_15_20,dou_fc_20_30,dou_fc_30_50,dou_fc_50_100,dou_fc_100_200,dou_fc_200
,online_fc_0_1,online_fc_1_5,online_fc_5_10,online_fc_10_15,online_fc_15_20,online_fc_20_30,online_fc_30
,tarpu_dwn_cnt,tarpu_dwn_amt,tarpu_up_cnt,tarpu_up_amt,hyyh_cnt,plan_dwn_cnt
,pzqqt_tarpu,pzqqt_dou,pzqqt_bhd,pzqqt_mou_zj,qqt_tarpu,qqt_dou,qqt_bhd,qqt_mou_zj
,xdr_usercnt,qylq_usercnt,ajwlqqt_usercnt



from (select
case when a.grid_id_1 like '24%' then left(a.grid_id_1,2)||right(a.grid_id_1,3) else substr(a.grid_id_1,2,2)||right(a.grid_id_1,3) end grid_id_1
,sum(case when a.IS_GOTONE=1 then tarpu else 0 end) qqt_amt--全球通客户收入万元
,sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end) pzqqt_amt--拍照全球通客户收入万元
,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt--全球通客户规模
,count(case when a.IS_GOTONE_PHO=1 then a.user_id else null end) pzqqt_cnt
,count(case when a.GOTONE_NAME='全球通普卡' then a.user_id else null end) 普卡
,count(case when a.GOTONE_NAME='全球通银卡' then a.user_id else null end) 银卡
,count(case when a.GOTONE_NAME='全球通金卡' then a.user_id else null end) 金卡
,count(case when a.GOTONE_NAME='全球通白金卡' then a.user_id else null end) 白金卡
,count(case when a.GOTONE_NAME='全球通钻石卡' then a.user_id else null end) 钻石卡
,count(case when a.GOTONE_NAME='全球通卓越钻石卡' then a.user_id else null end) 卓越钻石卡
,count(case when b.IS_GOTONE=0 and a.IS_GOTONE=1 then a.user_id else null end) qqt_new--全球通客户当月新增
,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_online--拍照全球通客户在网
,count(case when a.IS_GOTONE_PHO=1 and a.USERSTATUS_id not in (2, 3,6, 8, 9, 16, 17, 100, 101, 102, 103,111, 112, 113,114, 115, 116, 126, 127, 128, 129, 131, 132, 133) then a.user_id else null end) qqt_cnt_lw--拍照全球通客户离网
,count(case when a.IS_GOTONE=1 and c.is_zw=1 then a.user_id else null end) qqtzj--全球通组家客户
,count(case when a.IS_GOTONE=1 and c.kb_user_id is not null then a.user_id else null end) qqtkd--全球通宽带客户
,count(case when a.IS_GOTONE=1 and a.group_id is not null then a.user_id else null end) qqtjt--全球通集团客户
,count(case when nvl(IMEI_LONG,0)>24 and a.IS_GOTONE=1 then a.user_id else null end) zd_online2yup--长机龄客户（2年以上）
,round(count(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.user_id else null end)/nullif(pzqqt_cnt,0)*100,2) pzqqt_gm--拍照全球通客户规模保有率
,round(sum(case when a.IS_GOTONE=1 and a.IS_GOTONE_PHO=1 then a.tarpu else null end)/nullif(pzqqt_amt,0)*100,2) pzqqt_jz--拍照全球通客户收入保有率
,(pzqqt_gm+pzqqt_jz)/2 pzqqt_zh--拍照全球通客户综合保有率
,round(count(case when a.IS_GOTONE=1 and e.serial_number is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ydapp_hy--中国移动APP次月活跃率
,round(count(case when a.IS_GOTONE=1 and f.is_gm=1 then a.user_id else null end)/nullif((count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end)),0)*100,2) gm_st--国漫渗透率
,round(count(case when a.IS_GOTONE=1 and g.is_zxsy=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) jc_10086_sy--10088专席使用率
,round(count(case when a.IS_GOTONE=1 and g.is_zxwh=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) jc_10086_wh--10088专席外呼率
,null dmyh_zb--低满
,round(count(case when a.IS_GOTONE=1 and h.acpt_num is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) tsuser3mon_zb--投诉用户占比
,round(count(case when a.IS_GOTONE=1 and f.is_ywtd=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ywtd_zb--业务退订用户占比
,round(count(case when a.IS_GOTONE=1 and f.is_hdjx=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) hdjx_zb--活动接续用户占比
,round(count(case when a.IS_GOTONE=1 and i.gyrhl=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) gyrh_zb--全球通客户固移融合率
,round(count(case when a.IS_GOTONE=1 and j.rxrhl=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) yxrh_zb--全球通客户有效融合率
,round(count(case when a.IS_GOTONE=1 and l.user_id is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) ydkh_zb--异动客户占比
,round(count(case when a.IS_GOTONE=1 and ((a.sex_id=1 and a.age>60) or (a.sex_id=2 and a.age>55) or (a.sex_id<>1 and a.sex_id<>2 and a.age>60)) then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) old_zb--银发用户占比
,round(count(case when a.IS_GOTONE=1 and k.user_id is not null then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) gjmy_zb--国际用户占比
,round(count(case when a.IS_GOTONE=1 and a.is_stu=1 then a.user_id else null end)/nullif(qqt_cnt,0)*100,2) stu_zb--校园用户占比

,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=1000 then a.user_id else null end) 宽带1000
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=500 then a.user_id else null end) 宽带500
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=300 then a.user_id else null end) 宽带300
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=200 then a.user_id else null end) 宽带200
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=100 then a.user_id else null end) 宽带100
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)<100 and a.prod_bandwidth>0 then a.user_id else null end) 宽带100以下
,count(case when a.IS_GOTONE=1 and nvl(a.prod_bandwidth,0)=0 then a.user_id else null end) 宽带无宽带

,count(case when a.IS_GOTONE=1 and nvl(tarpu,0)<=0 then a.user_id else null end) tarpu_fc_0
,count(case when a.IS_GOTONE=1 and tarpu>0 and tarpu<30 then a.user_id else null end) tarpu_fc_0_30
,count(case when a.IS_GOTONE=1 and tarpu>=30 and tarpu<50 then a.user_id else null end) tarpu_fc_0_50
,count(case when a.IS_GOTONE=1 and tarpu>=50 and tarpu<100 then a.user_id else null end) tarpu_fc_50_100
,count(case when a.IS_GOTONE=1 and tarpu>=100 and tarpu<150 then a.user_id else null end) tarpu_fc_100_150
,count(case when a.IS_GOTONE=1 and tarpu>=150 and tarpu<200 then a.user_id else null end) tarpu_fc_150_200
,count(case when a.IS_GOTONE=1 and tarpu>=200 and tarpu<300 then a.user_id else null end) tarpu_fc_200_300
,count(case when a.IS_GOTONE=1 and tarpu>=300 then a.user_id else null end) tarpu_fc_300

,count(case when a.IS_GOTONE=1 and nvl(dou,0)/1024=0 then a.user_id else null end) dou_fc_0
,count(case when a.IS_GOTONE=1 and dou/1024>=0 and dou/1024<1 then a.user_id else null end) dou_fc_0_1
,count(case when a.IS_GOTONE=1 and dou/1024>=1 and dou/1024<5 then a.user_id else null end) dou_fc_1_5
,count(case when a.IS_GOTONE=1 and dou/1024>=5 and dou/1024<10 then a.user_id else null end) dou_fc_5_10
,count(case when a.IS_GOTONE=1 and dou/1024>=10 and dou/1024<20 then a.user_id else null end) dou_fc_15_20
,count(case when a.IS_GOTONE=1 and dou/1024>=20 and dou/1024<30 then a.user_id else null end) dou_fc_20_30
,count(case when a.IS_GOTONE=1 and dou/1024>=30 and dou/1024<50 then a.user_id else null end) dou_fc_30_50
,count(case when a.IS_GOTONE=1 and dou/1024>=50 and dou/1024<100 then a.user_id else null end) dou_fc_50_100
,count(case when a.IS_GOTONE=1 and dou/1024>=100 and dou/1024<200 then a.user_id else null end) dou_fc_100_200
,count(case when a.IS_GOTONE=1 and dou/1024>=200 then a.user_id else null end) dou_fc_200

,count(case when a.IS_GOTONE=1 and USER_ONLINE>=0 and USER_ONLINE<1 then a.user_id else null end) online_fc_0_1--在网时长分层
,count(case when a.IS_GOTONE=1 and USER_ONLINE>1 and USER_ONLINE<5 then a.user_id else null end) online_fc_1_5
,count(case when a.IS_GOTONE=1 and USER_ONLINE>5 and USER_ONLINE<10 then a.user_id else null end) online_fc_5_10
,count(case when a.IS_GOTONE=1 and USER_ONLINE>10 and USER_ONLINE<15 then a.user_id else null end) online_fc_10_15
,count(case when a.IS_GOTONE=1 and USER_ONLINE>15 and USER_ONLINE<20 then a.user_id else null end) online_fc_15_20
,count(case when a.IS_GOTONE=1 and USER_ONLINE>20 and USER_ONLINE<30 then a.user_id else null end) online_fc_20_30
,count(case when a.IS_GOTONE=1 and USER_ONLINE>30 then a.user_id else null end) online_fc_30

,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.user_id else null end) tarpu_dwn_cnt--价值下降客户
,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu<tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_dwn_amt--价值下降客户下降总价值
,count(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.user_id else null end) tarpu_up_cnt--价值提升客户
,sum(case when a.IS_GOTONE=1 and is_cz_user=1 and tarpu>tarpu_pre1 then a.tarpu-tarpu_pre1 else null end) tarpu_up_amt--价值提升客户提升总价值
,count(case when a.IS_GOTONE=1 and f.is_hyyh=1 then a.user_id else null end) hyyh_cnt--合约客户
,count(case when a.IS_GOTONE=1 and (PLAN_FEE-(ARPU-TARPU))<(PLAN_FEE-(ARPU_PRE1-TARPU_PRE1)) then a.user_id else null end) plan_dwn_cnt--套餐降档客户

,round(sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end)/nullif(qqt_cnt,0),2) pzqqt_tarpu--拍照全球通客户TARPU
,round(sum(case when a.IS_GOTONE_PHO=1 then dou/1024 else 0 end)/nullif(qqt_cnt,0),2) pzqqt_dou--拍照全球通客户DOU
,round(sum(case when a.IS_GOTONE_PHO=1 then tongyong_userd else 0 end)/nullif((sum(case when a.IS_GOTONE_PHO=1 then free_res else 0 end)),0)*100,2) pzqqt_bhd--拍照全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE_PHO=1 then OUT_CALL_DURATION_M else 0 end)/nullif(qqt_cnt,0),2) pzqqt_mou_zj--拍照全球通客户主叫MOU
,round(sum(case when a.IS_GOTONE=1 then tarpu else 0 end)/nullif(qqt_cnt,0),2) qqt_tarpu--当前全球通客户TARPU
,round(sum(case when a.IS_GOTONE=1 then dou/1024 else 0 end)/nullif(qqt_cnt,0),2) qqt_dou--当前全球通客户DOU
,round(sum(case when a.IS_GOTONE=1 then tongyong_userd else 0 end)/nullif((sum(case when a.IS_GOTONE=1 then free_res else 0 end)),0)*100,2) qqt_bhd--当前全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE=1 then OUT_CALL_DURATION_M else 0 end)/nullif(qqt_cnt,0),2) qqt_mou_zj--当前全球通客户主叫MOU
,count(case when a.IS_GOTONE=1 and o.is_xdr=1 then a.user_id else null end) xdr_usercnt--星动日
,count(case when a.IS_GOTONE=1 and o.user_id is not null then a.user_id else null end) qylq_usercnt--权益领取客户
,count(case when a.IS_GOTONE=1 and p.user_id is not null then a.user_id else null end) ajwlqqt_usercnt--三大行动





from
bdba.MKT_USER_PROFILE_M202506 a
left join (select user_id,IS_GOTONE from bdba.MKT_USER_PROFILE_M202505) b on a.user_id=b.user_id
left join temp_it_member_all_detail c on a.user_id=c.user_id
--left join obdw.dwv_home_cable_m202506 d on a.user_id=d.user_id
left join tangds.JZYY_CMBHPT_10002_202506 e on a.product_no=e.serial_number--(select distinct serial_number from internetdb.JZYY_CMBHPT_10002_202506)
left join ins_offer_detail_m202506 f on a.user_id=f.user_id
left join temp_10086_call_202506 g on a.product_no=g.product_no
left join (select acpt_num from (select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202504 union all
select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202505 union all
select acpt_num from OBDW.DW_CUSTSVC_ALL_DTL_202506) group by 1) h on a.product_no=h.acpt_num
left join (select user_id,case when is_gyrhhy=1 or is_tfkzcy=1 then 1 else 0 end gyrhl
from OBDW.DW_HOME_BASS1_GYRHL_M202506) i on a.user_id=i.user_id
left join (select user_id,case when (eff_fuse_id =1 or kd_act_id =1) then 1 else 0 end rxrhl
from obdw.dw_home_yxrhl_m202506) j on a.user_id=j.user_id
left join (select distinct user_id from obdw.dw_nb_roamuser_gj_dm where substr(op_time,1,6)='202506')k on a.user_id=k.user_id
left join (select user_id from xuzeshuai.temp_ydkh_detail_m202506 where is_qqt=1
and is_whyk_new+is_ywzk+is_dll+is_ywjc+is_ysgw_new+doumou_sj+dou_to0+dou_dwn+is_sjtc+is_oldplan>0 and nvl(gross_score,0)<3) l on a.user_id=l.user_id
left join (select user_id,OUT_CALL_DURATION_M,nvl(user_online,0)/12 user_online from obdw.dwv_nb_product_m202506) m on a.user_id=m.user_id
left join temp_tongyong_bhd_202506 n on a.user_id=n.user_id
left join (select user_id,max(case when fld07='星动日' then 1 else 0 end) is_xdr from OBDW.DW_VGOP_QYZX_70206_202506 group by 1) o on a.user_id=o.user_id
left join temp_ajwlqqt_user_m202506 p on a.user_id=p.user_id
where a.grid_id_1 is not null
group by 1
)a
-- left join (select nvl(city_id,999) city_id,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt from bdba.MKT_USER_PROFILE_M202505 a group by rollup(city_id)) b on a.city_id=b.city_id

left join (select * from bdba.m_city_county_grid where type_c='网格') b on a.grid_id_1=b.grid_id_1
;











drop table if exists tangds.temp_tongyong_bhd_202505;--饱和度
create table tangds.temp_tongyong_bhd_202505 as
select serv_id as user_id 
,sum(free_res_used)/1024 as tongyong_userd  ---流量使用量  单位m
,sum(free_res ) /1024 as free_res ---总的资源量M
,case when sum(free_res )=0 then 0 
      else  sum(free_res_used)/sum(free_res  ) end  ty_bhd
from obods.ods_convenient_exp_m202505 a
join buff.ggprs_day_tsj_m202505 b
 on a.prod_id = b.prod_id
and a.item_id = b.item_code
where region in ('国内')
and b.dx is null 
and b.is_nigth_pkg = '否'
and b.is_time_flash = '否'
group by serv_id
;

select city_id,qqt_amt,pzqqt_amt,pzqqt_tarpu,pzqqt_dou,pzqqt_bhd,pzqqt_mou_zj,qqt_tarpu,qqt_dou,qqt_bhd,qqt_mou_zj
from
(
select
nvl(a.city_id,999) city_id
,round(sum(case when a.IS_GOTONE=1 then tarpu else 0 end)/10000,2) qqt_amt--全球通客户收入万元
,round(sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end)/10000,2) pzqqt_amt--拍照全球通客户收入万元
,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt--全球通客户规模	
,count(case when a.IS_GOTONE_PHO=1 then a.user_id else null end) pzqqt_cnt
,round(sum(case when a.IS_GOTONE_PHO=1 then tarpu else 0 end)/pzqqt_cnt,2) pzqqt_tarpu--拍照全球通客户TARPU
,round(sum(case when a.IS_GOTONE_PHO=1 then dou/1024 else 0 end)/pzqqt_cnt,2) pzqqt_dou--拍照全球通客户DOU
,round(sum(case when a.IS_GOTONE_PHO=1 then tongyong_userd else 0 end)/(sum(case when a.IS_GOTONE_PHO=1 then free_res else 0 end))*100,2) pzqqt_bhd--拍照全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE_PHO=1 then OUT_CALL_DURATION_M else 0 end)/pzqqt_cnt,2) pzqqt_mou_zj--拍照全球通客户主叫MOU
,round(sum(case when a.IS_GOTONE=1 then tarpu else 0 end)/qqt_cnt,2) qqt_tarpu--当前全球通客户TARPU
,round(sum(case when a.IS_GOTONE=1 then dou/1024 else 0 end)/qqt_cnt,2) qqt_dou--当前全球通客户DOU
,round(sum(case when a.IS_GOTONE=1 then tongyong_userd else 0 end)/(sum(case when a.IS_GOTONE=1 then free_res else 0 end))*100,2) qqt_bhd--当前全球通客户通用包月流量饱和度
,round(sum(case when a.IS_GOTONE=1 then OUT_CALL_DURATION_M else 0 end)/qqt_cnt,2) qqt_mou_zj--当前全球通客户主叫MOU



from
bdba.MKT_USER_PROFILE_M202505 a
left join (select user_id,OUT_CALL_DURATION_M,nvl(user_online,0)/12 user_online from obdw.dwv_nb_product_m202505) m on a.user_id=m.user_id
left join temp_tongyong_bhd_202505 n on a.user_id=n.user_id

group by rollup(a.city_id)) order by decode(city_id,410,420,city_id)
;





select
city_id
,qqtcz,qqttx,qqtsjsw,qqt5gzd,qqt5gdw,qqt_gprs_fee_cnt,qqt_gprs_fee_amt,qqt_yuyin_fee_cnt,qqt_yuyin_fee_amt,pzqqtxc,pzqqtsx,pzqqtqx
,cqmy_zb,qfyh_zb,jc_10086
,yxrh_cnt,zdhy_cnt,plan_up_cnt
,qqt_plan_fee_amt,plan_fee_fc_0,plan_fee_fc_0_10,plan_fee_fc_10_30,plan_fee_fc_30_50,plan_fee_fc_50_80,plan_fee_fc_80_108,plan_fee_fc_108_150,plan_fee_fc_150_200,plan_fee_fc_200_300,plan_fee_fc_300
from
(select
nvl(a.city_id,999) city_id
,count(case when a.IS_GOTONE=1 then a.user_id else null end) qqt_cnt--全球通客户规模

,count(case when a.IS_GOTONE=1 and IS_CZ_USER=1 then a.user_id else null end) qqtcz--全球通出账客户
,count(case when a.IS_GOTONE=1 and IS_TX_USER=1 then a.user_id else null end) qqttx--全球通通信客户
,count(case when a.IS_GOTONE=1 and mobile_gprs_use_mark=1 then a.user_id else null end) qqtsjsw--全球通手机上网客户
,count(case when a.IS_GOTONE=1 and is_5gzd=1 then a.user_id else null end) qqt5gzd--全球通5g终端客户
,count(case when a.IS_GOTONE=1 and is_5gzd=1 and c.user_id is not null then a.user_id else null end) qqt5gdw--全球通5g登网客户
,count(case when a.IS_GOTONE=1 and GPRS_FLOW_FEE>0 then a.user_id else null end) qqt_gprs_fee_cnt--全球通流量费超套客户
,round(sum(case when a.IS_GOTONE=1 and GPRS_FLOW_FEE>0 then GPRS_FLOW_FEE else 0 end)/qqt_gprs_fee_cnt,2) qqt_gprs_fee_amt--全球通流量费超套户均
,count(case when a.IS_GOTONE=1 and tax_on_yuyin_ct>0 then a.user_id else null end) qqt_yuyin_fee_cnt--全球通语音超套客户
,round(sum(case when a.IS_GOTONE=1 and tax_on_yuyin_ct>0 then tax_on_yuyin_ct else 0 end)/qqt_yuyin_fee_cnt,2) qqt_yuyin_fee_amt--全球通语音超套费超套户均
,count(case when a.IS_GOTONE_pho=1 and userstatus_id in (40) then a.user_id else null end) pzqqtxc--拍照全球通携出
,count(case when a.IS_GOTONE_pho=1 and userstatus_id in (4,41) then a.user_id else null end) pzqqtsx--拍照全球通申销营业销户
,count(case when a.IS_GOTONE_pho=1 and userstatus_id in (5,42,0) then a.user_id else null end) pzqqtqx--拍照全球通欠销账务销户

,round(count(case when a.IS_GOTONE=1 and IS_CM=1 then a.user_id else null end)/qqt_cnt*100,2) cqmy_zb--长漫用户占比
,round(count(case when a.IS_GOTONE=1 and owe_mark=1 then a.user_id else null end)/qqt_cnt*100,2) qfyh_zb--欠费用户占比
,round(count(case when a.IS_GOTONE=1 and g.product_no is not null then a.user_id else null end)/qqt_cnt*100,2) jc_10086--10088专席使用率

,count(case when a.IS_GOTONE=1 and j.rxrhl=1 then a.user_id else null end) yxrh_cnt --全球通客户有效融合
,count(case when a.IS_GOTONE=1 and IS_ZDHY=1 then a.user_id else null end) zdhy_cnt--终端合约用户
,count(case when a.IS_GOTONE=1 and (PLAN_FEE-(ARPU-TARPU))>(PLAN_FEE-(ARPU_PRE1-TARPU_PRE1)) then a.user_id else null end) plan_up_cnt--套餐升档客户

,round(sum(case when a.IS_GOTONE=1 then nvl(tc_fee,0) else 0 end)/qqt_cnt,2) qqt_plan_fee_amt--全球通套餐实收户均
,count(case when a.IS_GOTONE=1 and nvl(tc_fee,0)<=0 then a.user_id else null end) plan_fee_fc_0
,count(case when a.IS_GOTONE=1 and tc_fee>0 and tc_fee<10 then a.user_id else null end) plan_fee_fc_0_10
,count(case when a.IS_GOTONE=1 and tc_fee>=10 and tc_fee<30 then a.user_id else null end) plan_fee_fc_10_30
,count(case when a.IS_GOTONE=1 and tc_fee>=30 and tc_fee<50 then a.user_id else null end) plan_fee_fc_30_50
,count(case when a.IS_GOTONE=1 and tc_fee>=50 and tc_fee<80 then a.user_id else null end) plan_fee_fc_50_80
,count(case when a.IS_GOTONE=1 and tc_fee>=80 and tc_fee<108 then a.user_id else null end) plan_fee_fc_80_108
,count(case when a.IS_GOTONE=1 and tc_fee>=108 and tc_fee<150 then a.user_id else null end) plan_fee_fc_108_150
,count(case when a.IS_GOTONE=1 and tc_fee>=150 and tc_fee<200 then a.user_id else null end) plan_fee_fc_150_200
,count(case when a.IS_GOTONE=1 and tc_fee>=200 and tc_fee<300 then a.user_id else null end) plan_fee_fc_200_300
,count(case when a.IS_GOTONE=1 and tc_fee>=300 then a.user_id else null end) plan_fee_fc_300

from
(select nvl(PLAN_FEE,0)-(nvl(ARPU,0)-nvl(TARPU,0)) tc_fee,* from bdba.MKT_USER_PROFILE_M202506) a
left join (select product_no,max(case when b.out_call_counts>0 then 1 else 0 end) is_zxsy
,max(case when b.in_call_counts>0 then 1 else 0 end) is_zxwh--,count(1) cnt
from (select * from obdw.dw_call_opp_m202506) b --差异点
where (b.opposite_regular_no like '%10086' or
b.opposite_regular_no like '%10085')
and length(b.opposite_regular_no)<=9 group by 1) g on a.product_no=g.product_no
left join (select user_id,mobile_gprs_use_mark,GPRS_FLOW_FEE,owe_mark from obdw.dwv_nb_product_m202506) m on a.user_id=m.user_id
left join (select distinct a.user_id
from obdw.dw_nb_gprs_5gnet_31d_20250630 a,
           obdw.dw_nb_gprs_5gnet_pre_dm b 
   where a.user_id = b.user_id
    and substr(b.op_time,1,6)=202506
    and b.op_time <= 20250630
    and a.wlw_user_mark = 0
    and a.userstatus_id in (2, 3, 6, 8, 9, 16, 17, 100, 101, 102, 103, 111, 112, 113, 114, 115, 116, 126, 127, 128, 129, 131, 132, 133)) c on a.user_id=c.user_id
left join (select user_id,case when (eff_fuse_id =1 or kd_act_id =1) then 1 else 0 end rxrhl
from obdw.dw_home_yxrhl_m202506) j on a.user_id=j.user_id
group by rollup(a.city_id)) order by decode(city_id,410,420,city_id)
;