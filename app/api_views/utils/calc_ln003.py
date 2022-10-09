import pandas as pd


def calculate_ln003(xml_df, co_khoan_vay):
    loan = ['Vay_Thong_Thuong', 'Vay_Thau_Chi']
    df1 = xml_df.loc[(xml_df['loai_khoan_vay'].map(lambda x: x in loan)) \
        & (xml_df.giai_doan_hdv == "LV")][['id_no', 'ma_hdv_tai_pcb']]
    df1 = df1.group_by(['id_no'], as_index=False).count().rename({'ma_hdv_tai_pcb': 'tong_so_hdv_dang_living'})
    
    df2 = xml_df.loc[(xml_df['loai_khoan_vay'].map(lambda x: x in loan)) \
        & (xml_df['giai_doan_hdv'].map(lambda x: x in co_khoan_vay))][['id_no', 'ma_hdv_tai_pcb']]
    df2 = df2.groupby(['id_no'], as_index=False).count().rename({'ma_hdv_tai_pcb': 'tong_so_hdv_duoc_cho_vay'})

    df_new = pd.merge(df1, df2, on='id_no')
    # ratio_living_contract = tong_so_hdv_dang_living_tren_tong_so_hdv
    df_new['tong_so_hdv_dang_living_tren_tong_so_hdv'] = df_new['tong_so_hdv_dang_living']/df_new['tong_so_hdv_duoc_cho_vay']
    return df_new[['id_no', 'tong_so_hdv_dang_living_tren_tong_so_hdv']]

    

# pcb_final %>%
#   filter.(loai_khoan_vay %in% loan) %>%
#   filter.(giai_doan_hdv %in% "LV") %>%
#   select.(id_no,  ma_hdv_tai_pcb) %>% 
#   distinct.() %>%
#   summarise.(tong_so_hdv_dang_living = n_distinct.(ma_hdv_tai_pcb), .by = id_no) %>%
#   right_join.(data_loan) %>% distinct.()  -> data_loan

# pcb_final %>%
#   filter.(loai_khoan_vay %in% loan) %>%
#   filter.(giai_doan_hdv %in% co_khoan_vay) %>%
#   select.(id_no,  ma_hdv_tai_pcb) %>% 
#   distinct.() %>%
#   summarise.(tong_so_hdv_duoc_cho_vay = n_distinct.(ma_hdv_tai_pcb), .by = id_no) %>%
#   right_join.(data_loan) %>% distinct.()  -> data_loan

# data_loan %>% 
#   mutate.(tong_so_hdv_dang_living_tren_tong_so_hdv = tong_so_hdv_dang_living/tong_so_hdv_duoc_cho_vay) %>%
#   select.(-c(tong_so_hdv_dang_living, tong_so_hdv_duoc_cho_vay)) -> data_loan
# mutate(tên_cột_mới, điều kiện hoặc ct tạo cột)