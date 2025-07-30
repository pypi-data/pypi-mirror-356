import polars as pl
import muse_config as s
TEST_LOCATE = s.APP_LOCATE + '/data/'
# DATA_SOURCE = 'parquet'
DATA_SOURCE = 'xlsx'

BASIC_COLS = ['资产代码', '资产名称', '资产标签', '产品代码', '产品简称', '产品标签', '主体代码', '主体名称', '主体标签', '日期']
# 暂时写死，方便单元测试。TODO 转义到指标列表源数据管理
PORT_TAG_COLS = ['采用摊余成本法进行核算的现金管理类理财产品', '固定收益类产品', '混合类产品', '面向非机构投资者发行的产品', '开放式公募产品', '定开周期小于90天的产品', '权益类产品', '现金管理类产品', '封闭式公募产品',
                 '商品及金融衍生品类产品', '私募产品', '公募产品', '定开周期小于90天的公募产品', '定开周期大于等于90天的公募产品', '每日开放公募产品', '每日开放产品', '封闭式产品']

PORT_ZB_COLS = ['平均剩余存续期限', '杠杆率（穿透后）', '当日净资产', '杠杆率', '连续5个交易日累计赎回比例', '当日至1个工作日之内是否有开放日', '上一日净资产', '是否允许单一投资者投资份额超50%', '前10大投资者比例',
                '日期', '是否面向单一投资者发行', '每万份收益', '连续3个交易日累计赎回份额', '开放类型', '连续5个交易日累计赎回份额', '当日累计单位净值', '当日赎回份额', '当日申购份额', '当日总资产',
                '3个工作日后是否开放日', '当日份额', '当日至7个工作日之内是否有开放日', '产品代码', '当日至4个工作日之内是否有开放日', '产品经理', '当日至10个工作日之内是否有开放日', '产品简称', '当日赎回金额',
                '当日单位净值', '当日估值偏离度(%)', '当日总资产（穿透后）', '当日申购金额', '平均剩余期限', '是否巨额赎回', '连续3个交易日累计赎回比', '复权单位净值', '开放频率', '七日年化收益率']

HLD_TAG_COLS = ['定期存款（不可提前支取）', '债券（不包含国债和政策性金融债、同业存单）', '定期存款（可提前支取，支取剩余期限≤7个工作日）', '债权类资产', 'AA级及其它同业存单', '信贷资产及其受（收）益权',
                '同业存单（PCLASS）', '逆回购', '资产端和正回购', '资产管理产品（PCLASS）', '债券买入返售（剩余期限>10个交易日）', '不良资产', '可交换债券', '现金', '高流动性资产', '债券（发行人债务违约）',
                '信用等级在AA+以下的资产支持证券', '债券（不包含同业存单和资产支持证券）', '以定期存款利率为基准利率的浮动利率债券', '定期存款（不可提前支取，剩余期限>10个交易日）', '公募基金（除货币基金、可赎回日>10个交易日）',
                '债券（除发行人债务违约）', '正回购', '商品及金融衍生品类资产', '资产支持证券（剩余期限≤5个交易日）', '债券（除发行人债务违约，剩余期限≤5个交易日）', '需折算基金资产', '定期存款（可提前支取，支取剩余期限≤5个交易日）',
                '定期存款（PCLASS）', '主体外部评级在AA+以下的债券', '债券买入返售（剩余期限≤7个工作日）', '同业存单（剩余期限≤5个交易日）', '中央银行票据（PCLASS）', '资产管理产品（可赎回日>10个交易日）',
                '同业存单（剩余期限≤7个工作日）', '现金及活期存款', '债券买入返售（剩余期限≤5个交易日）', '股票（除停牌、流通受限、非公开发行）', '定期存款（不可提前支取，剩余期限≤5个交易日）', '债券（除发行人债务违约，剩余期限≤7个工作日）',
                '单一资产', '权益类资产', '资产支持证券（PCLASS）', '定期存款（可提前支取，支取剩余期限>10个交易日）', '不良资产受（收）益权', '未上市企业股权及其受（收）益权', '质押式回购', '定期存款（可提前支取）', '信贷资产',
                '非标准化债权（PCLASS）', '可转换债券', '信用债（PCLASS）', '活期存款', '政策性金融债券（剩余期限≤365天）', '股票（PCLASS）', '测试标签-01', '国债（PCLASS）', '中央银行票据（剩余期限≤365天）', '非上市企业股权',
                '政策性金融债券（PCLASS）', '定期存款（不可提前支取，剩余期限≤7个工作日）', '私募证券投资基金', '股票（停牌）+股票（非公开发行）', '货币基金', '买断式回购', '不良资产支持证券', '债券（包含同业存单和资产支持证券）',
                '国债（剩余期限≤365天）']


HLD_ZB_COLS = ['最近一个季度净资产', '数量', 'IS_OPEN_DATE', '资产代码', '主体代码', '资产负债标识', '商品及金融衍生品类比例', '穿透类型', '支取剩余期限', '持仓面值',  '币种',  '剩余期限（年）', '债权类资产比例',
               '距最近可赎回日交易日天数', '是否停牌', '基金流通份额', '净价成本', '是否违约主体', '是否不良', '权益类资产比例', '剩余期限（天）', '证券外部评级', '会计分类', '产品到期日', '净价市值', '面值',
               '估值增值', '是否受（收）益权', '是否公开发行', '资管计划代码', '主体外部评级', '上一日持仓市值', '主体名称', 'PCLASS三级分类', '关联代码', '剩余交易日', '利息', '剩余存续期限（天）',
               '是否可提前支取', '全价市值', '金融机构类别（三级）', '剩余工作日', '基金总份额', '股票发行性质', '资产到期日', '资产名称', '下一开放起始日']

def get_all_unique_fields(cols: list) -> list:
    """返回 cols 和 basic_cols 的并集（去重后的所有字段）

    Args:
        cols: 额外字段列表
        basic_cols: 基础字段列表

    Returns:
        去重后的所有字段列表（顺序不保证）
    """
    return list(set(cols) | set(BASIC_COLS))

# 根据产品代码或者资产代码过滤
def filter_ports_sec(pdf: pl.dataframe, port_ids: list=[], sec_ids: list=[]):
    if (port_ids is not None) and (len(port_ids) > 0) and ('查询所有组合' not in port_ids):
        pdf = pdf.filter(pl.col("产品代码").is_in(port_ids))
    if sec_ids is not None and len(sec_ids) > 0:
        pdf = pdf.filter(pl.col("资产代码").is_in(sec_ids))
    return pdf

def filter_ports(pdf: pl.dataframe, port_ids: list=[]):
    if (port_ids is not None) and (len(port_ids) > 0) and ('查询所有组合' not in port_ids):
        pdf = pdf.filter(pl.col("产品代码").is_in(port_ids))
    return pdf

def filter_hld_data(df: pl.dataframe, penetrate: str):
    ctlx = []
    if penetrate is None:
        ctlx = ['00', '01', '02']
    elif penetrate == '不穿透':
        ctlx = ['00', '01', '02']
    elif penetrate == '全穿透':
        ctlx = ['00', '11', '12']
    elif penetrate == '自主管理穿透':
        ctlx = ['00', '11', '02']
    elif penetrate == '委外投资穿透':
        ctlx = ['00', '01', '12']
    df = df.filter(pl.col("穿透类型").is_in(ctlx))
    return df

def convert_decimal_to_float(df: pl.DataFrame) -> pl.DataFrame:
    exprs = []
    for col_name, dtype in df.schema.items():
        if str(dtype).startswith("Decimal"):
            exprs.append(pl.col(col_name).cast(pl.Float64).alias(col_name))
        # 其他类型（如 Struct/List）可在此扩展
    return df.with_columns(exprs) if exprs else df

def get_data(run_method: str, data_subject: str, sec_ids: list=[], port_ids: list=[],
             tags: list=[], inds: list=[], start_date = None, end_date = None, penetrate=None):
    # run_method: 批处理 / 历史试算 / 日间实时 / 日间试算 / 测试
    if penetrate:
        penetrate = '全穿透'
    else:
        penetrate = '不穿透'
    pdf = None
    if data_subject == '持仓指标':
        file_path = s.APP_LOCATE + '/muse/data/test_hld.parquet'
        pdf = pl.read_parquet(file_path)
        pdf = filter_ports_sec(pdf=pdf, port_ids=port_ids, sec_ids=sec_ids)
        pdf = filter_hld_data(pdf, penetrate)
    if data_subject == '主体指标':
        file_path = s.APP_LOCATE + '/muse/data/test_hld.parquet'
        pdf = pl.read_parquet(file_path)
        pdf = filter_ports_sec(pdf=pdf, sec_ids=sec_ids)
    elif data_subject == '产品指标':
        file_path = s.APP_LOCATE + '/muse/data/test_port.parquet'
        pdf = pl.read_parquet(file_path)
        pdf = filter_ports_sec(pdf=pdf, port_ids=port_ids)
    elif data_subject == '交易指标':
        file_path = s.APP_LOCATE + '/muse/data/test_trade.parquet'
        pdf = pl.read_parquet(file_path)
        pdf = filter_ports_sec(pdf=pdf, port_ids=port_ids, sec_ids=sec_ids)

    merged_cols = tags + inds
    if len(merged_cols)>0:
        all_cols = get_all_unique_fields(merged_cols)
        existing_cols = [c for c in all_cols if c in pdf.columns]
        pdf = pdf.select(existing_cols)
    return pdf

if __name__ == '__main__':
    # prd = get_data('批处理', "产品指标", end_date='2022-04-30')
    # print(hld)
    # hld = get_data('批处理', "持仓指标", end_date='2022-04-30')
    # print(hld)
    trd = get_data('单元测试', "产品指标", end_date='2022-04-30')
    print(trd)


