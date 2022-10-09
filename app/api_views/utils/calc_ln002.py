from pandas.tseries.offsets import DateOffset


def calculate_ln002(xml_df, co_khoan_vay):
    # num_CIs_approved = sl_tctd_moi_phat_sinh_trung_han_trong_vong_6_thang
    xml_df['date_calc'] = xml_df['decision_date'] - DateOffset(months=6)
    loan = ['Vay_Thong_Thuong', 'Vay_Thau_Chi']
    df_new = xml_df.loc[(xml_df['loai_khoan_vay'].map(lambda x: x in loan)) \
        & (xml_df['giai_doan_hdv'].map(lambda x: x in co_khoan_vay)) \
        & (xml_df.ngay_bat_dau >= xml_df.date_calc) \
        & (xml_df.tenor_khoan_vay == 'trung_han')][['id_no', 'ma_tctd']]
    df_new = df_new.group_by(['id_no'], as_index=False).count().rename({'ma_tctd': 'num_CIs_approved'})
    return df_new


# Rcoding: 
# pcb_final %>%
#   filter.(loai_khoan_vay %in% loan) %>%
#   filter.(giai_doan_hdv %in% co_khoan_vay) %>%
#   filter.(ngay_bat_dau >= decision_date - dmonths(6)) %>%
#   filter.(tenor_khoan_vay == "trung_han") %>%
#   select.(id_no,  ma_tctd) %>% 
#   summarise.(sl_tctd_moi_phat_sinh_trung_han_trong_vong_6_thang = n_distinct.(ma_tctd), .by = id_no) %>%
#   right_join.(data_loan) %>% distinct.()  -> data_loan
