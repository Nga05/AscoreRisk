

def calculate_ln005(xml_df):
    # total_contracts_rejected = tong_so_hdv_thong_thuong_bi_reject
    df_new = xml_df.loc[(xml_df.loai_khoan_vay == "Vay_Thong_Thuong") \
        & (xml_df.giai_doan_hdv == "RF")][['id_no', 'ma_hdv_tai_pcb']]
    df_new = df_new.group_by(['id_no'], as_index=False).count().rename({'ma_hdv_tai_pcb': 'total_contracts_rejected'})
    return df_new



# Rcoding: 
# pcb_final %>%
#   filter.(loai_khoan_vay %in% "Vay_Thong_Thuong") %>%
#   filter.(giai_doan_hdv %in% "RF") %>%
#   select.(id_no,  ma_hdv_tai_pcb) %>% 
#   distinct.() %>%
#   summarise.(tong_so_hdv_thong_thuong_bi_reject = n_distinct.(ma_hdv_tai_pcb), .by = id_no) %>%
#   right_join.(data_loan) %>% distinct.()  -> data_loan
