import polars as pl
import pandas as pd
import numpy as np
import muse.data_interface as di
import random
from datetime import timedelta, datetime
import muse_config as s
DATE = '2024-11-30'
DDATE = datetime.strptime(DATE, '%Y-%m-%d')


# 生成产品信息
def gen_port_info():
    # 生成产品信息
    port = pl.read_excel(di.TEST_LOCATE + '产品信息.xlsx')
    port_tags = list(port.select('产品标签').unique().to_series())
    ports = list()
    for i in range(0, 10000):
        p = dict()
        p['产品代码'] = 'P' + str(i)
        p['产品简称'] = '产品' + str(i)
        p['产品标签'] = random.sample(port_tags, 1)[0]
        ports.append(p)
    port_info = pl.DataFrame(ports)
    port_info.write_parquet(di.TEST_LOCATE + '产品信息.parquet')


# 生成主体信息
def gen_issuer_info():
    issuer = pl.read_excel(di.TEST_LOCATE + '主体信息.xlsx')
    tags = list(issuer.select('主体标签').unique().to_series())
    issuers = list()
    for i in range(0, 300):
        p = dict()
        p['主体代码'] = 'ISSUER' + str(i)
        p['主体标签'] = random.sample(tags, 1)[0]
        p['主体名称'] = '主体' + str(i)
        issuers.append(p)
    issuer_info = pl.DataFrame(issuers)
    issuer_info.write_parquet(di.TEST_LOCATE + '主体信息.parquet')
    print(issuer_info)


# 生成资产信息
def gen_sec_info():
    sec_info = pl.read_excel(di.TEST_LOCATE + '资产信息.xlsx')
    sec_tags = list(sec_info.select('资产标签').unique().to_series())
    issuer = pl.read_parquet(di.TEST_LOCATE + '主体信息.parquet')
    issuer_ids = list(issuer.select('主体代码').unique().to_series())
    secs = list()
    for i in range(0, 1000):
        s = dict()
        s['资产代码'] = 'SEC' + str(i)
        s['资产简称'] = '资产' + str(i)
        s['主体代码'] = random.sample(issuer_ids, 1)[0]
        s['资产标签'] = random.sample(sec_tags, 1)[0]
        secs.append(s)
    sec_info = pl.DataFrame(secs)
    sec_info.write_parquet(di.TEST_LOCATE + '资产信息.parquet')
    print(sec_info)


# 生成持仓指标
def gen_hld_ind():
    hlds = list()
    port = pl.read_parquet(di.TEST_LOCATE + '产品信息.parquet')
    port_ids = list(port.select('产品代码').unique().to_series())
    sec = pl.read_parquet(di.TEST_LOCATE + '资产信息.parquet')
    sec_ids = list(sec.select('资产代码').unique().to_series())

    for port_id in port_ids:
        selected_sec_ids = random.sample(sec_ids, len(sec_ids) - 200)
        for s_id in selected_sec_ids:
            row = dict()
            row['产品代码'] = port_id
            row['资产代码'] = s_id
            row['日期'] = DATE
            row['估值方法'] = random.sample(['摊余成本法', '市价法', '市价法', '市价法', '市价法', '市价法', '市价法'], 1)[0]
            row['持仓市值'] = random.randint(100000, 1000000)
            hlds.append(row)
    hld_df = pl.DataFrame(hlds)
    hld_df.write_parquet(di.TEST_LOCATE + '持仓指标.parquet')
    print(hld_df)


# 生成产品指标
def gen_port_ind():
    hld_df = pd.read_parquet(di.TEST_LOCATE + '持仓指标.parquet')
    sec_df = pd.read_parquet(di.TEST_LOCATE + '资产信息.parquet')
    hld_df = hld_df.merge(sec_df, on='资产代码', how='left')
    port_df = hld_df.groupby(['产品代码', '日期'], as_index=False).agg(总资产=('持仓市值', 'sum'))
    zhg_df = hld_df[hld_df.资产标签 == '债券正回购'].groupby(['产品代码', '日期'], as_index=False).agg(正回购市值=('持仓市值', 'sum'))
    port_df = port_df.merge(zhg_df, on=['产品代码', '日期'], how='left')
    port_df['净资产'] = port_df.总资产 - port_df.正回购市值
    port_df['杠杆率'] = np.round(port_df.总资产 / port_df.净资产, 4)
    port_df['前一日净资产'] = np.round(port_df.净资产 * 0.99, 2)
    port_df['上月末净资产'] = np.round(port_df.净资产 * 0.9, 2)
    port_df['产品开放期'] = np.random.randint(1, 120, size=(10000, 1))
    port_df['产品剩余期限'] = np.random.randint(360, 720, size=(10000, 1))
    port_df['产品剩余存续期'] = np.random.randint(0, 60, size=(10000, 1)) / 100
    port_df['下一开放日'] = port_df.apply(lambda r: (timedelta(days=r['产品开放期']) + DDATE).strftime('%Y-%m-%d'), axis=1)
    port_df['产品到期日'] = port_df.apply(lambda r: (timedelta(days=r['产品剩余存续期']) + DDATE).strftime('%Y-%m-%d'),axis=1)
    port_df['总份额'] = np.round(port_df.净资产 / 1000000, 0) * 1000000
    port_df['单位净值'] = np.round(port_df.净资产 / port_df.总份额, 3)
    port_df['前10名投资者份额占比'] = np.random.randint(40, 80, size=(10000, 1))
    port_df['前10名投资者的持有份额'] = port_df.前10名投资者份额占比 / 100 * port_df.总份额
    port_df['最大单一投资者份额占比'] = np.random.randint(5, 30, size=(10000, 1))
    port_df['最大单一投资者持有份额'] = port_df.最大单一投资者份额占比 / 100 * port_df.总份额
    port_df['个人投资者占比'] = np.random.randint(0, 60, size=(10000, 1)) / 100
    port_df['机构投资者占比'] = 1 - port_df.个人投资者占比
    port_df.to_parquet(di.TEST_LOCATE + '产品指标.parquet')
    print(port_df.iloc[0])


# 生成资产指标和主体指标
def gen_sec_ind():
    sec_df = pd.read_parquet(di.TEST_LOCATE + '资产信息.parquet')
    secs = sec_df[['资产代码', '主体代码']].drop_duplicates()
    issuer_df = pd.read_parquet(di.TEST_LOCATE + '主体信息.parquet')
    issuer_df = issuer_df[['主体代码', '主体名称']]
    issuer_df = issuer_df.rename(columns={'主体名称': '主体'})
    issuer_df = issuer_df.drop_duplicates()
    secs = secs.merge(issuer_df, on='主体代码', how='left')
    secs['发行人'] = secs.主体
    secs['债权人'] = secs.主体
    secs['实际信用承担方'] = secs.主体
    secs['原始权益人'] = secs.主体
    secs['剩余期限'] = np.random.randint(1, 720, size=(len(secs), 1))
    secs['存续期限'] = secs.剩余期限 + 100
    secs['资产到期日'] = secs.apply(lambda r: (timedelta(days=r['剩余期限']) + DDATE).strftime('%Y-%m-%d'), axis=1)
    secs['资产起始日'] = secs.apply(
        lambda r: (datetime.strptime(r['资产到期日'], '%Y-%m-%d') - timedelta(days=r['存续期限'])).strftime('%Y-%m-%d'),axis=1)
    hld_df = pd.read_parquet(di.TEST_LOCATE + '持仓指标.parquet')
    hld_vals = hld_df.groupby(['资产代码'], as_index=False).agg(发行市值=('持仓市值', 'sum'))
    hld_vals['发行市值'] = hld_vals.发行市值 * 5
    secs = secs.merge(hld_vals, on='资产代码', how='left')
    secs['可流通市值'] = secs['发行市值']
    secs['久期'] = np.random.randint(1, 10, size=(len(secs), 1))
    secs['日期'] = DATE
    # 生成主体数据
    issuer_df['上一季度末净资产'] = np.random.randint(20000000, 30000000, size=(len(issuer_df), 1))
    issuer_df = issuer_df[['主体代码', '上一季度末净资产']]
    issuer_df['日期'] = DATE

    secs.to_parquet(di.TEST_LOCATE + '资产指标.parquet')
    issuer_df.to_parquet(di.TEST_LOCATE + '主体指标.parquet')
    print(secs)
    print(issuer_df)


def gen_yields():
    key_points = [0.1, 0.3, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]
    points = len(key_points)
    date_range = pd.date_range(start='2024-01-01', end='2024-12-01', freq='B')
    days = len(date_range)

    # 生成利率债市场行情信息
    data = np.random.randint(10, 300, [days, points])
    data = np.round(data / 10000, 4)
    df = pd.DataFrame(data=data, index=date_range, columns=key_points)
    df.index.name = '日期'
    df.to_excel(di.TEST_LOCATE + '国债收益率曲线.xlsx')

    # 生成信用债
    data1 = np.random.randint(10, 400, [days, points])
    data1 = np.round(data1 / 10000, 4)
    df1 = pd.DataFrame(data=data1, index=date_range, columns=key_points)
    df1.index.name = '日期'
    df1.to_excel(di.TEST_LOCATE + '信用债收益率曲线.xlsx')
    return 0


def gen_index():
    date_range = pd.date_range(start='2024-01-01', end='2024-12-01', freq='B')
    days = len(date_range)
    data = np.random.randint(-300, 300, [days, 1])
    data = np.round(data / 1000, 4)
    df = pd.DataFrame(data=data, index=date_range, columns=['PCT_CHANGE'])
    df.index.name = '日期'
    df.to_excel(di.TEST_LOCATE + '沪深300指数.xlsx')
    return 0


def gen_hld_ind2():
    hld_df = pd.read_excel(s.APP_LOCATE + '/muse/data/持仓指标.xlsx')
    hlds = hld_df[hld_df.产品代码.isin(['P01', 'P02'])]
    hlds = hlds.drop(columns=['估值方法'])
    hlds = hlds.rename(columns={'产品代码': 'PORT_ID', '资产代码': 'SEC_ID', '日期': 'VALID_DATE', '持仓市值': 'FULL_MV'})
    tags = np.random.choice(['利率债', '信用债', '股票'], len(hlds))
    hlds['AST_TAG'] = tags
    hlds['REMAIN_DAYS'] = np.nan
    hlds['MOD_DURATION'] = np.nan
    hlds['CONVEXITY'] = np.nan
    hlds['BETA'] = np.nan

    stock_len = len(hlds[hlds.AST_TAG == '股票'])
    bond_len = len(hlds) - stock_len
    hlds.loc[hlds.AST_TAG == '股票', ['BETA']] = np.random.randint(50, 200, [stock_len, 1]) / 100
    hlds.loc[hlds.AST_TAG != '股票', ['MOD_DURATION']] = np.random.randint(1, 300, [bond_len, 1]) / 100 + 1
    hlds.loc[hlds.AST_TAG != '股票', ['CONVEXITY']] = np.random.randint(100, 500, [bond_len, 1]) / 10 + 1
    hlds.loc[hlds.AST_TAG != '股票', ['REMAIN_DAYS']] = np.random.randint(1, 300, [bond_len, 1]) / 100 + 1
    hlds['NET_ASSET'] = hlds.groupby(['PORT_ID'])['FULL_MV'].transform('sum') + 10000000
    hlds.to_excel(di.TEST_LOCATE + '持仓数据.xlsx', index=False)
    return 0


if __name__ == '__main__':
    # gen_port_info()
    # gen_issuer_info()
    # gen_sec_info()
    # gen_hld_ind()
    # gen_port_ind()
    # gen_sec_ind()
    print(gen_yields())
    gen_hld_ind2()
    gen_index()