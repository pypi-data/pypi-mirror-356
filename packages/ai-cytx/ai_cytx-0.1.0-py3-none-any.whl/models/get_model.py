from typing import Optional, List
from pydantic import BaseModel


class IntegerDecimal(BaseModel):
    """com.cytx.plan.bean.dto.base.IntegerDecimal

    IntegerDecimal
    """
    key: Optional[int] = None
    value: Optional[float] = None


class AgedTrendDTO(BaseModel):
    """增长趋势调整对象

    AgedTrendDTO
    """
    """调整明细,k=年龄,v=调整后金额"""
    adj_item_list: Optional[List[IntegerDecimal]] = None
    """调整后的金额列表"""
    after_adj_amt_arr: Optional[List[float]] = None
    """调整后的增长率列表"""
    after_adj_rt_arr: Optional[List[float]] = None
    """年龄列表"""
    age_arr: Optional[List[int]] = None
    """使用趋势类型(0=预测前或调整前,1=预测后或调整后)"""
    apply_type: Optional[int] = None
    """调整前的金额列表"""
    before_adj_amt_arr: Optional[List[float]] = None
    """调整前的增长率列表"""
    before_adj_rt_arr: Optional[List[float]] = None
    """复利收益率"""
    rt_amt_arr: Optional[List[float]] = None
    """收益率"""
    rt_amt_arr_growth_rate: Optional[List[float]] = None
    """根据预测算法的收益率"""
    rt_amt_arr_prediction: Optional[List[float]] = None
    """根据预测算法的收益率"""
    rt_amt_arr_prediction_growth_rate: Optional[List[float]] = None


class HouseAssetsList(BaseModel):
    """tbl_tp_plan_res_house"""
    """商贷金额|每月还款金额"""
    balance_commercial: Optional[float] = None
    """房价成长率"""
    growth_rate: Optional[float] = None
    """id"""
    id: Optional[int] = None
    """现金流成长率"""
    income_growth_rate: Optional[float] = None
    """是否贷款中，0-否，1-是"""
    is_loaning: Optional[int] = None
    """拥有者；0.本人，1.配偶"""
    owner_type: Optional[int] = None
    """现值"""
    present_value: Optional[float] = None
    """剩余还贷期限，单位月"""
    remain_repay_term: Optional[int] = None
    """每年房租收入,默认0"""
    rental_income: Optional[float] = None
    """租房波动率"""
    rent_vibration_rate: Optional[float] = None
    """标题"""
    title: Optional[str] = None
    """增长趋势调整对象"""
    trend_dto: Optional[AgedTrendDTO] = None
    """房产类型：0.投资性,1.自主性"""
    use_type: Optional[int] = None
    """房价波动率"""
    vibration_rate: Optional[float] = None


class AssetsList(BaseModel):
    """金额价值"""
    amount: Optional[float] = None
    """资产分类-标签"""
    category: Optional[int] = None
    """描述"""
    desp: Optional[str] = None
    """结束年"""
    end_age: Optional[int] = None
    """增长率、收益率"""
    growth_rate: Optional[float] = None
    """是否必要支出(1=是,0=否)"""
    has_must: Optional[int] = None
    house_assets_list: Optional[List[HouseAssetsList]] = None
    """id"""
    id: Optional[int] = None
    """【财务】                     <br/>
    收入 - itemName: 1          <br/>
    财务 - 支出 - itemName: 4    <br/>
    <br/>
    【资产】                     <br/>
    现金类资产 - itemName: 8     <br/>
    权益类资产 - itemName: 9     <br/>
    固收类资产 - itemName: 11    <br/>
    房产 - itemName: 14         <br/>
    其他资产 - itemName: 12       <br/>
    首年社保养老金 - itemName: 17    <br/>
    <br/>
    【保险】                      <br/>
    保费支出 -  itemName: 19      <br/>
    保险分红或年金收入 -  itemName: 20  <br/>
    """
    item_name: Optional[int] = None
    """拥有者；0.本人，1.配偶"""
    owner_type: Optional[int] = None
    """资产：社保养老金/个人养老金/公积金/企业年金 - 每月缴费基数（元/月）"""
    payment_base: Optional[float] = None
    """资产：社保养老金/个人养老金/公积金/企业年金 - 缴费比例（0.03代表3%）"""
    payment_ratio: Optional[float] = None
    """资产：社保养老金-已缴费年限（含视同缴费）"""
    pension_years: Optional[int] = None
    """开始年"""
    start_age: Optional[int] = None
    """增长趋势调整对象"""
    trend_dto: Optional[AgedTrendDTO] = None
    """收益增长趋势json"""
    trend_json: Optional[str] = None
    """波动率"""
    vibration_rate: Optional[float] = None


class MapString(BaseModel):
    """二级资产列表

    MapString
    """
    the_0: Optional[str] = None


class AssetsTypeAmountList(BaseModel):
    """入参、出参模型"""
    """资产列表"""
    assets_list: Optional[List[AssetsList]] = None
    """二级资产列表"""
    type_list: Optional[MapString] = None
    """资产类型：1-现金类资产，2-固收类资产，3-权益类资产，4-其他资产，5-房产类资产，46-个人养老金，47-个人养老金，48-企业年金，17-社保养老账户"""
    type: Optional[int] = None
    """资产类型名称"""
    typeName: Optional[str] = None


class FinanceInfoList(BaseModel):
    """养老规划财务信息"""
    """金额"""
    amount: Optional[float] = None
    """描述"""
    desp: Optional[str] = None
    """结束年"""
    end_age: Optional[int] = None
    """增长率、收益率"""
    growth_rate: Optional[float] = None
    """是否必要支出(1-是,0=否)"""
    has_must: Optional[int] = None
    """
    项目：1.工作收入,2.经营净收入,3.利息收入,4.家庭生活支出,5.现金，6.活期存款，7.定期存款，8.货币基金，9.股票，10.其他股票投资资产，11.债券，12.其他固定收益类资产，13.企业股权，14.房产，15.退休后期望支出，16.非工作收入，17.首年社保养老金，18.养老专属账户
    """
    item_name: Optional[int] = None
    """拥有者；0.本人，1.配偶"""
    owner_type: Optional[int] = None
    """开始年"""
    start_age: Optional[int] = None


class AgedPlanSaveParam(BaseModel):
    """基本信息

    AgedPlanSaveParam
    """
    """退休后投资回报率"""
    after_retire_rate: Optional[float] = None
    """退休前投资回报率"""
    before_retire_rate: Optional[float] = None
    """出生年月"""
    birth_date: Optional[str] = None
    """孩子数量"""
    child_num: Optional[int] = None
    """已缴费年限"""
    contribution_years: Optional[int] = None
    """年龄"""
    current_age: Optional[int] = None
    """学历-枚举[EduLevelEnum]"""
    edu_level: Optional[int] = None
    """本人首年养老金（当年年龄 > 退休年龄时显示）"""
    first_pension_amt: Optional[float] = None
    """当年收入"""
    income_amount: Optional[float] = None
    """工作所属行业-枚举[IndustryEnum]"""
    industry_type: Optional[int] = None
    """是否考虑配偶:0-不考虑、1-考虑"""
    is_spouse: Optional[int] = None
    """预期寿命"""
    life_expectancy: Optional[int] = None
    """社保所在地名称"""
    location_social_security: Optional[str] = None
    """社保所地在code"""
    location_social_security_code: Optional[str] = None
    """婚姻状况"""
    marital_status: Optional[int] = None
    """配偶出生年月"""
    mate_birth_date: Optional[str] = None
    """配偶孩子数量"""
    mate_child_num: Optional[int] = None
    """配偶 - 社保已缴费年限"""
    mate_contribution_years: Optional[int] = None
    """配偶年龄"""
    mate_current_age: Optional[int] = None
    """配偶学历-枚举[EduLevelEnum]"""
    mate_edu_level: Optional[int] = None
    """配偶首年养老金（当年年龄 > 退休年龄时显示）"""
    mate_first_pension_amt: Optional[float] = None
    """配偶工作所属行业-枚举[IndustryEnum]"""
    mate_industry_type: Optional[int] = None
    """配偶预期寿命"""
    mate_life_expectancy: Optional[int] = None
    """配偶 - 社保所在地名称"""
    mate_location_social_security: Optional[str] = None
    """配偶 - 社保所在地Code"""
    mate_location_social_security_code: Optional[str] = None
    """配偶婚姻状况"""
    mate_marital_status: Optional[int] = None
    """配偶 - 社保养老金累计金额"""
    mate_pension_acc_amt: Optional[float] = None
    """配偶领取退休金年龄"""
    mate_retire_age: Optional[int] = None
    """配偶性别0女1男"""
    mate_sex: Optional[int] = None
    """配偶是否缴纳社保0否1是"""
    mate_social_security_type: Optional[int] = None
    """配偶意向养老城市code"""
    mate_target_city_code: Optional[str] = None
    """配偶意向养老城市名称"""
    mate_target_city_name: Optional[str] = None
    """配偶工作时长"""
    mate_work_hour: Optional[int] = None
    """养老账户累计"""
    pension_acc_amt: Optional[float] = None
    """养老金增长率"""
    pension_growth_rate: Optional[float] = None
    """退休金账户投资回报率"""
    pension_return_rate: Optional[float] = None
    """规划名称"""
    plan_name: Optional[str] = None
    """领取退休金年龄"""
    retire_age: Optional[int] = None
    """退休后风险属性:1-保守型,2-稳健型,3-平衡型,4-积极型,5-进取型"""
    retire_risk_level: Optional[int] = None
    """风险属性:1-保守型,2-稳健型,3-平衡型,4-积极型,5-进取型"""
    risk_level: Optional[int] = None
    """本人性别：0-女、1-男"""
    sex: Optional[int] = None
    """是否缴纳社保0否1是"""
    social_security_type: Optional[int] = None
    """社平工资增长率"""
    social_wage_growth_rate: Optional[float] = None
    """目标城市"""
    target_city_code: Optional[str] = None
    """意向养老城市名称"""
    target_city_name: Optional[str] = None
    """预测趋势模型-枚举[TrendTypeEnum]"""
    trend_type: Optional[int] = None
    """每周工作时长"""
    work_hour: Optional[int] = None
    """通货膨胀率"""
    inflation_rate: Optional[float] = None
    """养老金账户累计金额"""
    pension_social_amount: Optional[float] = None
    """初始资产"""
    initial_assets: Optional[float] = None
    """投资回报率"""
    invest_return_rate: Optional[float] = None
    """可接受亏损程度"""
    accept_loss: Optional[float] = None
    """养老金推动增长率"""
    pension_push_growth_rate: Optional[float] = None
    """养老前后支出比例"""
    aged_before_after_cost_ratio: Optional[float] = None
    """退休前非工作收入占比"""
    aged_before_retire_income_rate: Optional[float] = None
    """退休后生活支出"""
    retire_live: Optional[float] = None
    """每月缴费基数"""
    fee_month: Optional[float] = None
    """首年养老金金额"""
    pension_income_month: Optional[float] = None
    """是否已领取养老金"""
    pensionable: Optional[int] = None
    """扩展参数JSON字符串"""
    json_param: Optional[str] = None
    """社会平均工资"""
    avg_social_wage: Optional[float] = None
    """社保缴费比例"""
    pension_contribution_ratio: Optional[float] = None
    """养老生活开始年"""
    aged_live_start: Optional[int] = None
    """社区服务开始年"""
    aged_community_start: Optional[int] = None
    """保姆服务开始年"""
    aged_babysitter_start: Optional[int] = None
    """护理服务开始年"""
    aged_nurse_start: Optional[int] = None
    """医疗支出开始年"""
    aged_medical_start: Optional[int] = None
    """存储时间戳"""
    storage_time: Optional[str] = None


class NationalRegionVersionDTO(BaseModel):
    """com.cytx.plan.bean.dto.pub.NationalRegionVersionDTO

    NationalRegionVersionDTO
    """
    """code"""
    code: Optional[str] = None
    """名称"""
    name: Optional[str] = None
    """父类code"""
    parent_code: Optional[str] = None
    """版本日期"""
    version: Optional[str] = None


class NationalRegion(BaseModel):
    """省市列表

    NationalRegion
    """
    """子级列表"""
    list: Optional[List[NationalRegionVersionDTO]] = None
    """父级列表"""
    parent_list: Optional[List[NationalRegionVersionDTO]] = None
    """版本时间"""
    version: Optional[str] = None


class Data(BaseModel):
    """查询结果"""
    assets_type_amount_list: Optional[List[AssetsTypeAmountList]] = None
    """财务信息"""
    finance_info_list: Optional[List[FinanceInfoList]] = None
    plan_id: Optional[str] = None
    """基本信息"""
    plan_info: Optional[AgedPlanSaveParam] = None
    """省市列表"""
    region: Optional[NationalRegion] = None


class GetModel(BaseModel):
    """0-失败、1-正常、-1-验证失败"""
    code: Optional[str] = None
    """查询结果"""
    data: Optional[Data] = None
    """信息提示"""
    message: Optional[str] = None