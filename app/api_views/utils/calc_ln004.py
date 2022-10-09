

def calculate_ln004(xml_df, co_khoan_vay):
    # total_contracts_approved : tong_so_hdv_thong_thuong_duoc_cho_vay
    df_new = xml_df.loc[(xml_df.loai_khoan_vay == "Vay_Thong_Thuong") \
        & (xml_df['giai_doan_hdv'].map(lambda x: x in co_khoan_vay))][['id_no', 'ma_hdv_tai_pcb']]
    df_new = df_new.group_by(['id_no'], as_index=False).count().rename({'ma_hdv_tai_pcb': 'total_contracts_approved'})
    return df_new


# Rcoding: 
# pcb_final %>%
#   filter.(loai_khoan_vay %in% "Vay_Thong_Thuong") %>%
#   filter.(giai_doan_hdv %in% co_khoan_vay) %>%
#   select.(id_no,  ma_hdv_tai_pcb) %>% 
#   distinct.() %>%
#   summarise.(tong_so_hdv_thong_thuong_duoc_cho_vay = n_distinct.(ma_hdv_tai_pcb), .by = id_no) %>%
#   right_join.(data_loan) %>% distinct.()  -> data_loan

