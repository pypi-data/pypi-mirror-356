# 指标提取引擎
# 根据金融对象.指标的方法提取金融对象的数值类指标
# 同一类金融对象需要一次性提取避免性能的额外开销
import logging
import polars as pl

def indicator_handle(base, prop):
    if isinstance(base, pl.DataFrame) and prop not in base.columns:
        logging.error(f'调用点运算失败：{prop} 不在 {base}中')
        return prop, pl.DataFrame()
    return prop, base
