from numpy import float64
from pandas.tseries.offsets import DateOffset
from typing import List, Union

class Installments:
    def __init__(self,
        loantype: str,
        installment_amount: int,
    ):
        self.loantype = loantype
        self.installment_amount = installment_amount
        

class Ln001:
    def __init__(self,
        decision_date: any,
        instalments: List[Installments],
        non_installments: List
    ) -> None:
        self.decision_date = decision_date
        self.non_installments = non_installments

    def calc(self):
        # do something

class PCBException(Exception):

class XmlError:
    def __init__(self,
        error_code,
        error_message,
        error_descripion
    ):
        self.error_code = error_code
        self.error_message = error_message
        self.error_description = error_descripion

    def raize(self) -> PCBException:
        raise 


class XmlObject:
    def __init__(self,
        customer,
        installments,
        non_installments,
    ):
        self.customer = customer
        self.installments = installments
        self.non_installment = non_installments


class XmlSource:
    def __init__(self,
        content: str
    ):
        self.content = content

    def convert(self) -> Union[XmlObject, PCBException]:
        # travel xml 
        # if error code -> return PCBException
        # else 
        return XmlObject()



def calculate_ln001(xml_df):  #xml_df: pcb_final
    # num_CIs_paid: so_tctd_da_tra_xong_no_ngan_han_trong_24_thang 
    xml_df['date_calc'] = xml_df['decision_date'] - DateOffset(months=24)
    loan = ['Vay_Thong_Thuong', 'Vay_Thau_Chi']
    df_new = xml_df.loc[(xml_df['loai_khoan_vay'].map(lambda x: x in loan)) \
        & (xml_df['giai_doan_hdv'].map(lambda x: x in ["TM", "TA"])) \
        & (xml_df.ngay_ket_thuc <= xml_df.date_calc) \
        & (xml_df.tenor_khoan_vay == 'ngan_han')][['id_no', 'ma_tctd']]
    df_new = df_new.groupby(['id_no'], as_index=False).count().rename(columns={'ma_tctd':'num_CIs_paid'})
    return df_new

xml_object 
ln001 = Ln001(xml_object.decision_date, xml_object.installments, xml_object.non_installments)
value_ln001 = ln001.calc()


class FeatureBuilder:
    def __init__(self, feature_name, fields: List[str]) -> None:
        pass

    def build() -> object:
        for key, value in xml_objects:
            setattr("decision_date", value)


ln001 = FeatureBuilder(
        "Ln001",
        ["decision_date", "installments", "non_installments"]
    ).build()
ln001 = Ln001(
    xml_object.decision_date,
)
ln002 = FeatureBuilder() 


class FeatureValue:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class FeaturesManage()
    {"Ln001", []}
    ["Ln001", [""]]

    .build() -> [FeatureObject]
    for obj in FeatureObject:
        obj.calc()

class ProcessXml():
    def __init__(self) -> None:
        pass

    def process(self):
        # 1 call pcb
        # 2 convert to object and handling error
        # 3 init feature object
        # 4 calc on appropriate object
        # 5 drool class accept value from step 4 then make request to and receive response then convert to object then store.

## R-code
# pcb_final %>%
#   filter.(loai_khoan_vay %in% loan) %>%
#   filter.(giai_doan_hdv %in% c("TM", "TA")) %>%
#   filter.(ngay_ket_thuc <= decision_date - dmonths(24)) %>%
#   filter.(tenor_khoan_vay == "ngan_han") %>%
#   select.(id_no,  ma_tctd) %>% 
#   summarise.(so_tctd_da_tra_xong_no_ngan_han_trong_24_thang = n_distinct.(ma_tctd), .by = id_no) %>%
#   right_join.(data_loan) %>% distinct.()  -> data_loan