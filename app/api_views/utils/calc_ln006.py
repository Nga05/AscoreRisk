from pandas.tseries.offsets import DateOffset



def calculate_ln006(xml_df):
    # total_requires = so_lan_tra_cuu_trong_vong_6_thang
    xml_df['date_calc'] = xml_df['decision_date'] - DateOffset(months=6)
    df_new = xml_df.loc[(xml_df.ngay_bat_dau >= xml_df.date_calc)][['id_no', 'ma_tctd', 'ngay_bat_dau', 'ma_hdv_tai_pcb']]
    df_new = df_new.group_by(['id_no', 'ma_tctd', 'ngay_bat_dau'], as_index=False).count().rename({'ma_hdv_tai_pcb': 'total_requires'})
    return df_new


# Rcoding: 
# pcb_final %>% 
#   filter.(ngay_bat_dau >= decision_date - dmonths(6)) %>%
#   select.(id_no,  ma_tctd, ngay_bat_dau, ma_hdv_tai_pcb) %>%
#   distinct.() %>%
#   summarise.(so_lan_tra_cuu_trong_vong_6_thang = n_distinct.(ma_hdv_tai_pcb), 
#              .by = c(id_no,  ma_tctd, ngay_bat_dau)) %>%
#   summarise.(so_lan_tra_cuu_trong_vong_6_thang = n(), .by = id_no) %>%
#   right_join.(data_loan) %>% distinct.()  -> data_loan