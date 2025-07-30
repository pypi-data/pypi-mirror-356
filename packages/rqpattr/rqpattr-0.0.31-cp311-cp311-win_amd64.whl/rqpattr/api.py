# -*- coding: utf-8 -*-
import inspect
from typing import Dict, List, Union
import pandas as pd
import rqdatac

from rqpattr.exceptions import InvalidInput
from rqpattr.const import BenchmarkType, AnalysisModel, BrinsonStandard, BarraIndustryMapping, AssetType

from rqpattr.analysis.brinson import brinson_analysis
from rqpattr.analysis.stock_factor import stock_factor_analysis, stock_factor_analysis_v2
from rqpattr.analysis.campisi import bond_campisi_analysis
from rqpattr.analysis.hedging import hedging_analysis
from rqpattr.analysis.bond_factor import bond_factor_analysis
from rqpattr.analysis.context import analysis_context

__all__ = ('performance_attribute', 'analysis_context')

analysis_funcs = {
    AnalysisModel.BOND_FACTOR: bond_factor_analysis,
    AnalysisModel.BRINSON: brinson_analysis,
    AnalysisModel.HEDGING: hedging_analysis,
    AnalysisModel.FACTOR: stock_factor_analysis,
    AnalysisModel.FACTOR_V2: stock_factor_analysis_v2,
    AnalysisModel.CAMPISI: bond_campisi_analysis,
}


def have_daily_benchmark_weight(benchmark_info: dict):
    INDEXES = [
        "000016.XSHG",
        "000300.XSHG",
        "000905.XSHG",
        "000906.XSHG",
        "000852.XSHG",
        "932000.INDX",
        "000688.XSHG",
        "000922.XSHG",
        "000510.XSHG",
    ]
    return benchmark_info["type"] == "index" and (
            benchmark_info["detail"] in INDEXES or benchmark_info["detail"].endswith("RI"))


def _model_extra_args(f):
    sig = inspect.signature(f)
    extra = []
    for i, (k, v) in enumerate(sig.parameters.items()):
        # all analysis first 3 parameters is daily_weight, daily_return, benchmark_info
        if i < 3:
            continue
        extra.append(k)
    return extra


_extra_parameters: Dict[str, List] = {k: _model_extra_args(v) for k, v in analysis_funcs.items()}


def _performance_attribute(model, daily_weight, daily_return, benchmark, kwargs):
    result = {}
    for model_key in model:
        analysis_func = analysis_funcs[model_key]
        analysis_extra_parameters = _extra_parameters[model_key]
        extra = {k: kwargs[k] for k in analysis_extra_parameters if k in kwargs}
        report = analysis_func(daily_weight, daily_return, benchmark, **extra)
        if not result:
            result.update(report)
        else:
            result['attribution'].update(report['attribution'])

    return result


def _filter_unknown_order_book_id(weighting: pd.Series) -> pd.Series:
    """ 过滤掉权重信息中不认识的 asset_type

    weighting:
        每日每个合约的权重, 其中的 index 为 ['date', 'order_book', 'asset_type'] 值为weight
        Optional: ✘
        Example:
            date        order_book_id
            2018-01-04  000001.XSHE    stock       1.0
            2018-01-05  000001.IB      bond        0.5
                        cash           cash        0.5
            2018-01-06  150008.XSHE    stock       0.5
                        TF1709         future      0.5
            Name: weight, dtype: float64
    """
    instruments_checker = {
        AssetType.STOCK: rqdatac.instruments,
        # AssetType.BOND: rqdatac.bond.instruments,   # NOTE: 下掉债券数据, 不需要这个了
        AssetType.FUND: rqdatac.fund.instruments,
        AssetType.FUTURES: rqdatac.instruments,
        AssetType.PUBLIC_FUND: rqdatac.fund.instruments,
        AssetType.OPTION: rqdatac.instruments,
        AssetType.CONVERTIBLE: rqdatac.instruments
    }

    new_index = []
    orig_index = weighting.index
    for (date, order_book_id, asset_type) in orig_index:
        if asset_type in instruments_checker:
            if instruments_checker[asset_type](order_book_id) is not None:
                new_index.append((date, order_book_id, asset_type))
        else:
            new_index.append((date, order_book_id, asset_type))
    new_index = pd.MultiIndex.from_tuples(new_index, names=orig_index.names)
    return weighting.reindex(new_index)


def inject_industry_mapping(models: list[str], kwargs: dict):
    # set industry_mapping in kwargs if user want to analysis equity/factor, equity/factor_v2
    if set(models) & {AnalysisModel.FACTOR, AnalysisModel.FACTOR_V2}:
        standard = kwargs.get("standard")
        if standard is None or standard == BrinsonStandard.SHENWAN:
            industry_mapping = BarraIndustryMapping.SW2021
        elif standard == BrinsonStandard.ZHONGXIN:
            industry_mapping = BarraIndustryMapping.CITICS2019
        else:
            raise InvalidInput(f'invalid standard: {standard}')
        kwargs["industry_mapping"] = industry_mapping


def performance_attribute(
        model: Union[str, list],
        daily_weights: pd.Series,
        daily_return: pd.Series = None,
        benchmark_info=None,
        report_save_path=None,
        **kwargs,
) -> dict:
    """start a performance attribute

    Parameters
    ----------
    model : str or list
        Optional: ✘
        Example:
             模型支持以下几种的混合:
                 "equity/brinson"            # brinson 行业归因
                 "equity/factor"             # 因子归因
                 "equity/factor_v2"          # v2版本因子归因
    daily_weights : pd.Series
        每日每个合约的权重, 其中的 index 为 ['date', 'order_book'] 值为weight
        Optional: ✘
        Example:
            date        order_book_id
            2018-01-04  000001.XSHE    1.0
            2018-01-05  000001.IB      0.5
                        cash           0.5
            2018-01-06  150008.XSHE    0.5
                        TF1709         0.5
            Name: weight, dtype: float64
    daily_return : pd.Series
                每日的总收益率, 其中 index 为 'date', 值为收益率,
        收益率的开始时间应是权重的开始时间的下一个交易日, 结束时间应是权重结束时间的下一个建议日
        Optional: ✘
        Example:
            2018-01-05    0.01
            2018-01-06    0.01
            2018-01-07    0.01
            Name: return, dtype: float64
    benchmark_info: dict
        基准
        Optional: ✔ , 无基准信息输入则以上证300作为基准
        Example:
            基准支持 4 种类型, 如下所示:
            1. {'type': 'index',  'name': '上证300', 'detail': '000300.XSHG'}
            2. {'type': 'mixed_index': 'name': '20% 上证300 + 80% 中债高信用', 'detail': {'000300.XSHG': 0.2, 'CBA01901.INDX': 0.8}}
            3. {'type': 'yield_rate': 'name': '1年期国债', 'detail': 'YIELD1Y'}
            4. {'type': 'cash', 'name': "零收益现金", 'detail': 0.0}
            注: 以上示例 name 均为可选字段.
    report_save_path: str
         将分析结果保存到excel文件的路径.
         注意: 如果 model 中传入了list, 那么只会生成 model[0]对应的分析报告.

    Other Parameters
    ----------------
    drilldown : bool
        是否穿透
        Optional: ✔ , 默认不穿透
    leverage_ratio : pd.Series or float
        杠杆率, 组合收益率当日的杠杆率
    standard : str
        行业归因标准
        model 为 "equity/brinson"时, 可选：'sws', 'citics', 'sws_second', 'citics_second'
        model 为 "equity/factor", "equity/factor_v2"时, 可选：'sws', 'citics'
    special_assets_return : pd.Series
        index 为 date, order_book_id
        value return， 其中收益率为真实组合收益率
    analysis_id: str

    Notes
    -----
    daily_weights 的 date 每一项都向后取一个交易日即为 daily_return 的日期, (如示例所示)

    Returns
    -------
    dict
    """
    # CHECK_RQSDK_PERMISSION: rqsdk__rqpattr
    
    import os as __os
    import datetime as __datetime
    
    import jwt as __jwt
    import requests as __requests
    import platform as __platform
    import uuid as __uuid
    if 'RQSDK_LICENSE' not in __os.environ and 'RQDATAC2_CONF' not in __os.environ:
        raise EnvironmentError("未检测到 licenese，请执行\"rqsdk license\"以配置您的 license")
    proxy_uri = __os.environ.get('RQSDK_PROXY')
    __rsp = __requests.get(
        'https://www.ricequant.com/api/rqlicense/rqsdk/get_permissions',
        params={
            "permission_id": "rqsdk__rqpattr" ,
            "rqdatac_uri": __os.environ.get('RQSDK_LICENSE', None) or __os.environ.get('RQDATAC2_CONF', None),
            "node": __uuid.getnode(),
            "pid": __os.getpid(),
            "python_version": __platform.python_version(),
            "system":__platform.system(),
        },
        proxies={"http": proxy_uri, "https": proxy_uri}
    )
    if __rsp.status_code != 200:
        __rsp.raise_for_status()
    if "json" in __rsp.headers['Content-Type'] and __rsp.json().get('code') is not 0:
        raise EnvironmentError(__rsp.json().get("message"))
    __rsp_payload = __jwt.decode(jwt=__rsp.content, key="-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDJPVxzOolSJ5Vc2mRNGkFB1rZl\nlxPUU4oQR1FQdZNbHdaRlmeKSOLS+6ve//3f2nbvUIMD9+q/pwnwWULtU/aYvguT\nJs6OYbE5HqzF5p3DgFoL05A+jhT1UzfafJAgbuQOalTMChi0FuvrUr+UGVyNX9YX\nj5tL4Xbu18U7qz0W4wIDAQAB\n-----END PUBLIC KEY-----\n", algorithms="RS256")
    if __rsp_payload['server_timestamp'] + 600 < __datetime.datetime.now().timestamp():
        raise RuntimeError("权限验证失败，请检查计算机时间设置")
    if not __rsp_payload.get("date_to_expire") or __rsp_payload['date_to_expire'] < 0:
        msg = "{}天".format(__rsp_payload['date_to_expire'] * -1) if __rsp_payload.get("date_to_expire") else ""
        raise PermissionError("该账号 license 已到期 {}".format(msg))
    if "rqsdk__rqpattr" not in __rsp_payload["data"]:
        raise PermissionError("当前账户没有{}权限，请联系米筐商务或技术支持".format("rqsdk__rqpattr"))
    
    if isinstance(model, str):
        models = [model]
    else:
        models = model

    daily_weights.sort_index(inplace=True)
    daily_weights = _filter_unknown_order_book_id(daily_weights)
    if daily_return is not None:
        daily_return.sort_index(inplace=True)

    if daily_return is not None:
        daily_return.name = "return"
        daily_return.index.name = 'date'

    if set(models) - set(analysis_funcs.keys()) or len(model) < 1:
        raise InvalidInput(f'invalid model: {models}')

    if not benchmark_info:
        benchmark_info = {'type': BenchmarkType.CASH, 'name': "现金", 'detail': 0.0}

    total_progress_count = 0
    for model in models:
        f = analysis_funcs[model]
        total_progress_count += analysis_context.get_analysis_count(f)

    analysis_name = ','.join(models)

    leverage_ratio = kwargs.get("leverage_ratio")
    if isinstance(leverage_ratio, pd.Series) and daily_return is not None:
        leverage_ratio.fillna(1.0, inplace=True)

    # NOTE: For `standard`, there are slightly different meaning between
    # `equity/brinson` and (`equity/factor` or `equity/factor_v2`)
    # - `equity/brinson` => standard
    # - `equity/factor` or `equity/factor_v2` => industry_mapping
    # but to make the API easy to use, we just make them same at API level
    # and inject `industry_mapping` field to kwargs if necessary
    inject_industry_mapping(models, kwargs)

    with analysis_context.do(total_progress_count, name=analysis_name, analysis_id=kwargs.get("analysis_id")):
        result = _performance_attribute(models, daily_weights, daily_return, benchmark_info, kwargs)
    result["is_benchmark_weight_daily"] = have_daily_benchmark_weight(benchmark_info)

    if report_save_path is not None:
        from rqpattr.report.excel import get_performance_attribution_excel
        dates = sorted(set(daily_weights.index.get_level_values("date")))
        exc = get_performance_attribution_excel({
            "template": models[0], "result": result,
            "benchmark": benchmark_info.get("name", benchmark_info),
            "start_date": rqdatac.get_next_trading_date(dates[0]),
            "end_date": rqdatac.get_next_trading_date(dates[-1])
        })
        exc.save(report_save_path)
    return result


def returns_decomposition(
        daily_weights: pd.Series,
        daily_return: pd.Series = None,
        benchmark_info=None,
        **kwargs
) -> dict:
    """start a returns decomposition

    Parameters
    ----------
    daily_weights : pd.Series
        每日每个合约的权重, 其中的 index 为 ['date', 'order_book'] 值为weight
        Optional: ✘
        Example:
            date        order_book_id
            2018-01-04  000001.XSHE    1.0
            2018-01-05  000001.IB      0.5
                        cash           0.5
            2018-01-06  150008.XSHE    0.5
                        TF1709         0.5
            Name: weight, dtype: float64
    daily_return : pd.Series
                每日的总收益率, 其中 index 为 'date', 值为收益率,
        收益率的开始时间应是权重的开始时间的下一个交易日, 结束时间应是权重结束时间的下一个建议日
        Optional: ✘
        Example:
            2018-01-05    0.01
            2018-01-06    0.01
            2018-01-07    0.01
            Name: return, dtype: float64
    benchmark_info: dict
        基准
        Optional: ✔ , 无基准信息输入则以上证300作为基准
        Example:
            基准支持 4 种类型, 如下所示:
            1. {'type': 'index',  'name': '上证300', 'detail': '000300.XSHG'}
            2. {'type': 'mixed_index': 'name': '20% 上证300 + 80% 中债高信用', 'detail': {'000300.XSHG': 0.2, 'CBA01901.INDX': 0.8}}
            3. {'type': 'yield_rate': 'name': '1年期国债', 'detail': 'YIELD1Y'}
            4. {'type': 'cash', 'name': "零收益现金", 'detail': 0.0}
            注: 以上示例 name 均为可选字段.

    Other Parameters
    ----------------
    leverage_ratio : pd.Series or float
        杠杆率, 组合收益率当日的杠杆率
    special_assets_return : pd.Series
        index 为 date, order_book_id
        value return， 其中收益率为真实组合收益率
    analysis_id: str

    Notes
    -----
    daily_weights 的 date 每一项都向后取一个交易日即为 daily_return 的日期, (如示例所示)

    Returns
    -------
    dict
    """
    from rqpattr.analysis import return_decomposition
    daily_weights.sort_index(inplace=True)
    daily_weights = _filter_unknown_order_book_id(daily_weights)
    if daily_return is not None:
        daily_return.sort_index(inplace=True)

    if daily_return is not None:
        daily_return.name = "return"
        daily_return.index.name = 'date'

    if not benchmark_info:
        benchmark_info = {'type': BenchmarkType.CASH, 'name': "现金", 'detail': 0.0}

    leverage_ratio = kwargs.get("leverage_ratio")
    if isinstance(leverage_ratio, pd.Series) and daily_return is not None:
        leverage_ratio.fillna(1.0, inplace=True)

    return return_decomposition.return_decomposition_analysis(daily_weights, daily_return, benchmark_info, **kwargs)
