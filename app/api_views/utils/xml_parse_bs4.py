from typing import List, Union
from bs4 import BeautifulSoup
from pathlib import Path
from pandas import DataFrame
from pandas.tseries.offsets import DateOffset
from itertools import chain
from enum import Enum
import logging
import numpy as np
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore")


class MTs:
    def __init__(self,
        MessageResponse: str,
    ) -> None:
        self.MessageResponse = MessageResponse

    @classmethod
    def from_xml(cls, bs):
        return cls(
            MessageResponse=bs.find("MessageResponse").get_attribute_list('MTs')[0][:10]
        )


class CBSubjectCode:
    def __init__(self,
        CBSubjectCode: str
    ) -> None:
        self.CBSubjectCode = CBSubjectCode

    @classmethod
    def from_xml(cls, bs):
        return cls(
            CBSubjectCode=bs.find("CBSubjectCode").text
        )


class IDCard:
    def __init__(self,
        id_card: str
    ) -> None:
        self.id_card = id_card

    @classmethod
    def from_xml(cls, bs):
        return cls(
            id_card=bs.find("IDCard").text
        )


class ScoreRaw:
    def __init__(self,
        score_raw: Union[str, int]
    ) -> None:
        self.score_raw = score_raw

    @classmethod
    def from_xml(cls, bs):
        try:
            score_raw = bs.find("ScoreRaw").text
        except Exception:
            score_raw = bs.find("ScoreRaw")
        return cls(
            score_raw
        )


class GrantedContract:
    def __init__(self,
        CBContractCode: str,
        EncryptedFICode: str,
        ContractPhase: str,
        StartingDate: str,
        EndDateOfContract: str,
        TotalAmount: str
    ) -> None:
        self.CBContractCode = CBContractCode  # ma_hdv_tai_pcb
        self.EncryptedFICode = EncryptedFICode  # ma_tctd
        self.ContractPhase = ContractPhase  # giai_doan_hdv
        self.StartingDate = StartingDate  # ngay_bat_dau
        self.EndDateOfContract = EndDateOfContract
        self.TotalAmount = TotalAmount

    @classmethod
    def from_xml(cls, bs):
        try:
            TotalAmount = bs.find("TotalAmount").text
        except Exception:
            TotalAmount = bs.find("TotalAmount")
        return cls(
            CBContractCode=bs.find('CBContractCode').text,        # ma_hdv_tai_pcb
            EncryptedFICode=bs.find('EncryptedFICode').text,      # ma_tctd
            ContractPhase=bs.find('ContractPhase').text,          # giai_doan_hdv
            StartingDate=bs.find('StartingDate').text,            # ngay_bat_dau
            EndDateOfContract=bs.find('EndDateOfContract').text,  # ngay_ket_thuc
            TotalAmount=TotalAmount                               # so_tien_vay
        )


class GrantedContracts(GrantedContract):
    @classmethod
    def from_xml(cls, bs_tags) -> List[GrantedContract]:
        return [GrantedContract.from_xml(bs_tag) for bs_tag in bs_tags]


class NotGrantedContract:
    def __init__(self,
        CBContractCode: str,
        EncryptedFICode: str,
        ContractPhase: str,
        StartingDate: str,  # RequestDateOfTheContract
        TotalAmount: str
    ) -> None:
        self.CBContractCode = CBContractCode
        self.EncryptedFICode = EncryptedFICode
        self.ContractPhase = ContractPhase
        self.StartingDate = StartingDate
        self.TotalAmount = TotalAmount

    @classmethod
    def from_xml(cls, bs):
        try:
            TotalAmount = bs.find("TotalAmount").text
        except Exception:
            TotalAmount = bs.find("TotalAmount")
        return cls(
            CBContractCode=bs.find('CBContractCode').text,
            EncryptedFICode=bs.find('EncryptedFICode').text,
            ContractPhase=bs.find('ContractPhase').text,
            StartingDate=bs.find('RequestDateOfTheContract').text,
            TotalAmount=TotalAmount
        )


class NotGrantedContracts(NotGrantedContract):
    @classmethod
    def from_xml(cls, bs_tags) -> List[NotGrantedContract]:
        return [NotGrantedContract.from_xml(bs_tag) for bs_tag in bs_tags]


class Instalments:
    def __init__(self,
        grantedContract: GrantedContracts,
        notGrantedContract: NotGrantedContracts,
    ) -> None:
        self.grantedContract = grantedContract
        self.notGrantedContract = notGrantedContract

    @classmethod
    def from_xml(cls, grantedContract: GrantedContracts, notGrantedContract: NotGrantedContracts):
        return cls(
            grantedContract=grantedContract,
            notGrantedContract=notGrantedContract,
        )


class NonInstalments:
    def __init__(self,
        grantedContract: GrantedContracts,
        notGrantedContract: NotGrantedContracts,
    ) -> None:
        self.grantedContract = grantedContract
        self.notGrantedContract = notGrantedContract

    @classmethod
    def from_xml(cls,
        grantedContract: GrantedContracts,
        notGrantedContract: NotGrantedContracts
    ):
        return cls(
            grantedContract=grantedContract,
            notGrantedContract=notGrantedContract,
        )


class Cards:
    def __init__(self,
        grantedContract: GrantedContracts,
        notGrantedContract: NotGrantedContracts,
    ):
        self.grantedContract = grantedContract
        self.notGrantedContract = notGrantedContract

    @classmethod
    def from_xml(cls, grantedContract: GrantedContracts, notGrantedContract: NotGrantedContracts):
        return cls(
            grantedContract=grantedContract,
            notGrantedContract=notGrantedContract,
        )


class Contract:
    def __init__(
        self,
        instalments: Instalments,
        nonInstalments: NonInstalments,
        cards: Cards
    ) -> None:
        self.instalments = instalments
        self.nonInstalments = nonInstalments
        self.cards = cards

    @classmethod
    def from_xml(cls, instalments: Instalments, nonInstalments: NonInstalments, cards: Cards):
        return cls(
            instalments=instalments,
            nonInstalments=nonInstalments,
            cards=cards
        )


class PCBData:
    def __init__(self,
        MTs: MTs,
        CBSubjectCode: CBSubjectCode,
        IDCard: IDCard,
        ScoreRaw: ScoreRaw,
        Contract: Contract,
    ) -> None:
        self.MTs = MTs
        self.CBSubjectCode = CBSubjectCode
        self.IDCard = IDCard
        self.ScoreRaw = ScoreRaw
        self.Contract = Contract


class LoanType(Enum):
    Instalment = "installment"
    NonInstallment = "non_installments"
    Card = "cards"


class Contracts:
    def __init__(self,
        granted: GrantedContracts,  # List[GrantedContracts]
        not_granted: NotGrantedContracts,  # List[NotGrantedContracts]
        loantype: LoanType
    ):
        self.granted = granted
        self.not_granted = not_granted
        self.loantype = loantype


class DFHandler:
    loan = ['Instalment', 'NonInstallment']
    hasloan = ['LV', 'TM', 'TA']
    notloan = ['RQ', 'RN', 'RF']
    loancompleted = ['TM', 'TA']

    def __init__(self, df_xml: DataFrame, df_f1: DataFrame) -> DataFrame():
        self.df_xml = df_xml
        self.df_f1 = df_f1

    def calc_all(self):
        ln_all = pd.concat([self.calc_ln001(), self.calc_ln002(), self.calc_ln003(), self.calc_ln004(), self.calc_ln005(), self.calc_ln006()], axis=1)
        for col in ln_all.columns:
            if col != "IDCard":
                ln_all[col] = ln_all[col].fillna(0)
        ln_all = ln_all.dropna(axis=1, how='all')
        # drop dupplicated col
        ln_all = ln_all.loc[:, ~ln_all.columns.duplicated()].copy()
        ln_all = ln_all.dropna()
        ln_all.reset_index(inplace=True, drop=True)
        ln_all['pcb_score'] = self.df_xml['ScoreRaw'].values[0]
        ascore_input_all = pd.concat([ln_all, self.df_f1], axis=1)
        # print(ascore_input_all.columns)
        return ascore_input_all

    def calc_ln001(self):
        # num_CIs_paid: so_tctd_da_tra_xong_no_ngan_han_trong_24_thang
        xml_df = self.preprocess()
        if not (xml_df.empty):
            xml_df['date_calc'] = xml_df['decision_date'] - DateOffset(months=24)
            df_new = xml_df.loc[(xml_df['LoanType']
                .map(lambda x: x in ['Instalment', 'NonInstallment'])) & (xml_df['ContractPhase']
                .map(lambda x: x in ["TM", "TA"])) & (xml_df.EndDateOfContract <= xml_df.date_calc) & (xml_df.loan_tenor == 'short_term')][['IDCard', 'EncryptedFICode']]
            df_new = df_new.groupby(['IDCard'], as_index=False).count().rename(columns={'EncryptedFICode': 'num_CIs_paid'})
        else:
            df_new = self.df_xml
        # print(df_new)
        return df_new

    def calc_ln002(self):
        # num_CIs_approved = sl_tctd_moi_phat_sinh_trung_han_trong_vong_6_thang
        xml_df = self.preprocess()
        if not (xml_df.empty):
            xml_df['date_calc'] = xml_df['decision_date'] - DateOffset(months=6)
            df_new = xml_df.loc[(xml_df['LoanType']
            .map(lambda x: x in self.loan)) & (xml_df['ContractPhase']
            .map(lambda x: x in self.hasloan)) & (xml_df.StartingDate >= xml_df.date_calc) & (xml_df.loan_tenor == 'medium_term')][['IDCard', 'EncryptedFICode']]
            df_new.drop_duplicates(inplace=True).reset_index(drop=True, inplace=True)
            df_new = df_new.groupby(['IDCard'], as_index=False).count().rename(columns={'EncryptedFICode': 'num_CIs_approved'})
        else:
            df_new = self.df_xml
        return df_new

    def calc_ln003(self):
        xml_df = self.preprocess()
        if not (xml_df.empty):
            # df1
            df1 = xml_df.loc[(xml_df['LoanType'].map(lambda x: x in self.loan)) & (xml_df.ContractPhase == "LV")][['IDCard', 'CBContractCode']]
            df1 = df1.groupby(['IDCard'], as_index=False).count().rename(columns={'CBContractCode': 'contract_living'})  # tong_so_hdv_dang_living
            # df2
            df2 = xml_df.loc[(xml_df['LoanType'].map(lambda x: x in self.loan)) & (xml_df['ContractPhase'].map(lambda x: x in self.hasloan))][['IDCard', 'CBContractCode']]
            df2 = df2.groupby(['IDCard'], as_index=False).count().rename(columns={'CBContractCode': 'contract_loaned'})  # tong_so_hdv_duoc_cho_vay
            # df1 merge df2
            df_new = pd.merge(df1, df2, on='IDCard')
            # ratio_living_contract = tong_so_hdv_dang_living_tren_tong_so_hdv
            df_new['ratio_living_contract'] = df_new['contract_living'] / df_new['contract_loaned']
            df_new = df_new[['IDCard', 'ratio_living_contract']]
        else:
            df_new = self.df_xml
        return df_new

    def calc_ln004(self):
        # total_contracts_approved : tong_so_hdv_thong_thuong_duoc_cho_vay
        xml_df = self.preprocess()
        if not (xml_df.empty):
            df_new = xml_df.loc[(xml_df.LoanType == self.loan[0]) & (xml_df['ContractPhase'].map(lambda x: x in self.hasloan))][['IDCard', 'CBContractCode']]
            df_new = df_new.groupby(['IDCard'], as_index=False).count().rename(columns={'CBContractCode': 'total_contracts_approved'})
        else:
            df_new = self.df_xml
        return df_new

    def calc_ln005(self):
        # total_contracts_rejected = tong_so_hdv_thong_thuong_bi_reject
        xml_df = self.preprocess()
        if not (xml_df.empty):
            df_new = xml_df.loc[(xml_df.LoanType == self.loan[0]) & (xml_df.ContractPhase == "RF")][['IDCard', 'CBContractCode']]
            df_new = df_new.groupby(['IDCard'], as_index=False).count().rename(columns={'CBContractCode': 'total_contracts_rejected'})
        else:
            df_new = self.df_xml
        return df_new

    def calc_ln006(self):
        # total_requires = so_lan_tra_cuu_trong_vong_6_thang
        xml_df = self.preprocess()
        if not (xml_df.empty):
            xml_df['date_calc'] = xml_df['decision_date'] - DateOffset(months=6)
            df_new = xml_df.loc[(xml_df.StartingDate >= xml_df.date_calc)][['IDCard', 'EncryptedFICode', 'StartingDate', 'CBContractCode']]
            df_new = df_new.groupby(['IDCard', 'EncryptedFICode', 'StartingDate'], as_index=False).count().rename(columns={'CBContractCode': 'total_requires'})
            # df_new['total_requires'] = 0 if df_new['total_requires']
            df_new = df_new['total_requires']
        else:
            df_new = self.df_xml
        return df_new

    # create dataframe for calculate input parammeters of Ascore model
    def preprocess(self):
        xml_df = self.df_xml
        try:
            # convert to datetime
            xml_df['StartingDate'] = pd.to_datetime(xml_df['StartingDate'], format='%d%m%Y')
            xml_df['EndDateOfContract'] = pd.to_datetime(xml_df['EndDateOfContract'], format='%d%m%Y')
            xml_df['MTs'] = pd.to_datetime(xml_df['MTs'], format='%Y-%m-%d')

            # calc diff dates => "thoi_han_vay" ("loan_period")
            xml_df['loan_period'] = (xml_df['EndDateOfContract'] - xml_df['StartingDate']) / np.timedelta64(1, 'D')

            # Create loan_tenor ('tenor_khoan_vay')
            xml_df[['loan_tenor']] = ""
            for i, val in enumerate(xml_df['loan_period']):
                if (val <= 360) and (xml_df['ContractPhase'][i] in self.hasloan):
                    xml_df['loan_tenor'][i] = "short_term"
                elif (val <= 1800) and (xml_df['ContractPhase'][i] in self.hasloan):
                    xml_df['loan_tenor'][i] = "medium_term"
                elif (val > 1800) and (xml_df['ContractPhase'][i] in self.hasloan):
                    xml_df['loan_tenor'][i] = 'long_term'
                else:
                    xml_df['loan_tenor'][i] = "not_loan"

            # Create fake decision date for testing
            # dec_date = "2022-12-25"
            # xml_df['decision_date'] = dec_date
            # xml_df['decision_date'] = pd.to_datetime(xml_df['decision_date'])  # , format='%d%m%Y'
            dec_date = self.df_f1
            xml_df['decision_date'] = dec_date['DECISION_DATE'].values[0]
            xml_df['decision_date'] = pd.to_datetime(xml_df['decision_date'])

        except Exception as e:
            logging.getLogger(str(e))
            raise e

        return xml_df


class AScoreData:
    def __init__(self,
        Loantype: LoanType,
        MTs: MTs,
        CBSubjectCode: CBSubjectCode,
        IDCard: IDCard,
        ScoreRaw: ScoreRaw,
    ) -> None:
        self.Loantype = Loantype
        self.MTs = MTs
        self.CBSubjectCode = CBSubjectCode
        self.IDCard = IDCard
        self.ScoreRaw = ScoreRaw

    def todataframe(xmlfilepath, dbfilepath) -> DFHandler:
        ascore_data = XmlContent.XmlSource(xmlfilepath).read()
        ascore_data = ascore_data.__dict__
        df_xml = pd.DataFrame()
        for k, val in ascore_data.items():
            df = pd.DataFrame()
            contract_all = []
            if k=="Loantype":
                for i in val.__iter__():
                    loantype = {}
                    contract = i.granted + i.not_granted
                    contracts = []
                    for ct in contract:
                        loantype["LoanType"] = i.loantype.name
                        contracts.append({**loantype, **ct.__dict__})
                    contract_all.append(contracts)
                contract_all = list(chain.from_iterable(contract_all))
                df = DataFrame.from_dict(contract_all, orient='columns')
                df_xml = pd.concat([df_xml, df], axis=1)
            else:
                df_xml[k] = val

        # inputs get from F1 database
        df_f1 = F1Input(dbfilepath, xmlfilepath).input_from_db()
        # print(df_f1)
        return DFHandler(df_xml=df_xml, df_f1=df_f1)


class F1Input:
    def __init__(self, dbfilepath, xmlfilepath) -> None:
        self.dbfilepath = dbfilepath
        self.xmlfilepath = xmlfilepath
    # inputs get from F1 database
    def input_from_db(self) -> DataFrame:
        f1_data = pd.read_csv(self.dbfilepath, index_col=False)
        # get App name from xml file
        app = re.search('FICO_(.*).xml', self.xmlfilepath)
        try:
            # find info of App in F1 db
            df_f1=f1_data.loc[f1_data.APPLICATION_NUMBER==app.group(1)]
            df_f1 = df_f1.reset_index(drop=True)
        except Exception as e:
            logging.getLogger("error %s: Not found App name in F1" %(str(e)))
            df_f1 = DataFrame()
            raise e
            
        return df_f1


class XmlContent:
    def __init__(self, content: str):
        self.content = content

    @classmethod
    def XmlSource(cls, filename: str):
        filepath = f"{filename}"
        xml_data = ""
        with open(filepath, 'r') as xml_file:
            xml_data = xml_file.read()
        return cls(content=xml_data)

    def read(self):
        try:
            ascore = self.parse(self.content)
        except Exception as e:
            logging.error("Error: %s" % str(e))
            raise e
        return ascore

    def parse(self, xml_data: str) -> Union[AScoreData, None]:
        bs = BeautifulSoup(xml_data, 'xml')
        contract = Contract.from_xml(Instalments, NonInstalments, Cards)
        installments = Contracts(
            contract
                .instalments
                .from_xml(GrantedContracts, NotGrantedContracts)
                .grantedContract.from_xml(bs.find("Instalments").find_all('GrantedContract')),
            contract
                .instalments
                .from_xml(GrantedContracts, NotGrantedContracts)
                .notGrantedContract
                .from_xml(bs.find("Instalments")
                .find_all('NotGrantedContract')),
            LoanType.Instalment
        )
        noninstalments = Contracts(
            contract
                .nonInstalments
                .from_xml(GrantedContracts, NotGrantedContracts)
                .grantedContract
                .from_xml(bs.find("NonInstalments")
                .find_all('GrantedContract')),
            contract
                .nonInstalments
                .from_xml(GrantedContracts, NotGrantedContracts)
                .notGrantedContract
                .from_xml(bs.find("NonInstalments")
                .find_all('NotGrantedContract')),
            LoanType.NonInstallment
        )
        cards = Contracts(
            contract
                .cards
                .from_xml(GrantedContracts, NotGrantedContracts)
                .grantedContract
                .from_xml(bs.find("Cards")
                .find_all('GrantedContract')),
            contract
                .cards
                .from_xml(GrantedContracts, NotGrantedContracts)
                .notGrantedContract
                .from_xml(bs.find("Cards")
                .find_all('NotGrantedContract')),
            LoanType.Card
        )
        return AScoreData(
            Loantype=(installments, noninstalments, cards),
            MTs=MTs.from_xml(bs).MessageResponse,
            CBSubjectCode=CBSubjectCode.from_xml(bs).CBSubjectCode,
            IDCard=IDCard.from_xml(bs).id_card,
            ScoreRaw=ScoreRaw.from_xml(bs).score_raw
        )


if __name__ == "__main__":
    XmlFolder = str(Path(__file__).parent / "xml/1_patch")
    dbfilepath = str(Path(__file__).parent / "xml/f1_data/f1_ascore_input.csv")
    filename = 'FICO_APPL00939435.xml'
    # XmlFolder = str(Path(__file__).parent / "xml/")
    # filename = '000186042261.xml'
    xmlfilepath = f"{XmlFolder}/{filename}"
    ascore_data = XmlContent.XmlSource(xmlfilepath).read()
    df = AScoreData.todataframe(xmlfilepath, dbfilepath)
    print(df.calc_all().T.to_dict())