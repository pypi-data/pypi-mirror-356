import json
from tenacity import retry, stop_after_attempt, wait_fixed
from smartpush.base.request_base import FormRequestBase
from smartpush.base.url_enum import URL
from smartpush.export.basic.GetOssUrl import log_attempt


class FormAfter(FormRequestBase):
    def __init__(self, form_id, host, headers):
        super().__init__(form_id, host, headers)

    def callPageFormReportDetail(self, reportDetailType, start_time=None, end_time=None):
        """
        获取PageFormReportDetail数据
        :param end_time:
        :param start_time:
        :param reportDetailType:
        :return:
        """
        requestParam = {"page": 1, "pageSize": 20, "reportDetailType": reportDetailType, "formId": self.form_id}
        if start_time is not None and end_time is not None:
            requestParam["startTime"] = start_time
            requestParam["endTime"] = end_time
        result = self.request(method=URL.pageFormReportDetail.method, path=URL.pageFormReportDetail.url,
                              data=requestParam)
        persons_list = result["resultData"]["reportDetailData"]["datas"]
        return persons_list


    def callGetFormReportDetail(self):
        requestParam = {"formId": self.form_id}
        result = self.request(method=URL.getFormReportDetail.method, path=URL.getFormReportDetail.url,
                              data=requestParam)
        resultData = result["resultData"]
        return resultData

    def callGetFormPerformanceTrend(self):
        requestParam = {"formId": self.form_id}
        result = self.request(method=URL.getFormPerformanceTrend.method, path=URL.getFormPerformanceTrend.url,
                              data=requestParam)
        resultData = result["resultData"]
        return resultData

    def callEditCrowdPackage(self, _id=None, groupRules=None, groupRelation="$AND"):
        """
        更新群组条件id
        :param _id:
        :param groupRules:
        :param groupRelation:
        :return:
        """
        requestParam = {"id": _id, "crowdName": "表单查询群组-自动化", "groupRelation": groupRelation,
                        "groupRules": groupRules, "triggerStock": False}
        result = self.request(method=URL.editCrowdPackage.method, path=URL.editCrowdPackage.url, data=requestParam)
        assert result.get("code") == 1
        resultData = result["resultData"]
        assert resultData.get("status") == 2
        return resultData["id"]

    def callCrowdPersonList(self, _id, page, pageSize, filter_type, filter_value):
        requestParam = {"id": _id, "page": page, "pageSize": pageSize}
        if filter_value is not None:
            requestParam["filter"] = {filter_type: {"in": filter_value}}
        result = self.request(method=URL.crowdPersonList.method, path=URL.crowdPersonList.url, data=requestParam)
        result.raise_for_status()
        return result['resultData']

    def callGetFormList(self, formName):
        requestParam = {'page': 1, 'pageSize': 10, 'name': formName}
        result = self.request(method=URL.getFormList.method, path=URL.getFormList.url, data=requestParam)
        return result["resultData"]['datas']

    def callGetFormInfo(self):
        requestParam = {'formId': self.form_id}
        result = self.request(method=URL.getFormInfo.method, path=URL.getFormInfo.url, params=requestParam)
        return result['resultData']

    def callDeleteForm(self, merchant_id):
        requestParam = {"formId": self.form_id, "merchant_id": merchant_id}
        result = self.request(url=self.host + URL.deleteForm.url, params=requestParam)
        assert result['code']
        print(f"删除id:{self.form_id}表单成功")

    # --------        处理数据  --------------
    def collectFormDetails(self, key, start_time=None, end_time=None):
        """
        从表单收集明细中获取信息，判断是否收集成功
        :param self:
        :param key: 关键词
        :param start_time: 开始时间
        :param end_time: 结束时间
        """
        persons_list = self.callPageFormReportDetail("FORM_COLLECT", start_time, end_time)
        if persons_list:
            for person in persons_list:
                if person['email'] == key:
                    return True, person
                elif person['phone'] == key:
                    return True, person
                else:
                    return False, None

    def FormReportNumQuery(self, num_type="viewNum", assertNum=None):
        """
        表单数据数据统计
        :param assertNum:
        :param num_type:viewNum/clickNum/collectNum/orderNum
        """
        data = self.callGetFormReportDetail()
        if data is not None:
            if assertNum is None:
                var = data.get(num_type)
                return var
            else:
                return data.get(num_type) == assertNum

    def getFormAttributionSales(self, key, start_time=None, end_time=None):
        """
        判断折扣码是否能正确归因
        :param key:
        :param start_time:
        :param end_time:
        :return:
        """
        order_list = self.callPageFormReportDetail("FORM_SALES", start_time, end_time)
        if order_list:
            for order in order_list:
                if order['email'] == key:
                    return True, order
                elif order['phone'] == key:
                    return True, order
                elif order['orderId'] == key:
                    return True, order
                else:
                    return False, None

    def getFormLineChart(self, date=None, num_type="viewNum", assertNum=None):
        """
        获取表单折线图
        :param assertNum:
        :param date:
        :param num_type:viewNum/clickNum/collectNum
        """
        datas = dict(self.callGetFormPerformanceTrend())
        if datas is not None:
            for data in datas:
                if data.get(date):
                    if assertNum is not None:
                        assert data.get(num_type) == assertNum
                    else:
                        return data.get(num_type)

    def getCrowdPersonList(self, _id, page=1, pageSize=20, filter_type="email", filter_value=""):
        self.callCrowdPersonList(self, _id, page, pageSize, filter_type, filter_value)
