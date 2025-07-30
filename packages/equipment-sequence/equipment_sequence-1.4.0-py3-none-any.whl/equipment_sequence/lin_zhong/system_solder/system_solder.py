"""
    半桥请求进站
        PC -> MES: {"bridge_request": "bridge_code"}
        MES -> PC: 1: 可做, 2: 不可做
    焊接盘进站
        PC -> MES: {"carrier_in": "carrier_code"}
        MES -> PC: OK
    带有产品和半桥的焊接托盘出站
        PC -> MES:
            {
                "carrier_out": {
                    "carrier_code": "carrier_code_value",
                    "product_codes": ["code1", "code2"],
                    "bridge_codes: ["bridge_code1", "bridge_code2", "bridge_code3", "bridge_code4", "bridge_code5", "bridge_code6"]
                }
            }
        MES -> PC: OK


    控制状态改变
        PC -> MES: {"control_state_change": "当前控制状态的值"}
        MES -> PC: OK
    运行状态改变
        PC -> MES: {"machine_state_change": "当前运行状态的值"}
        MES -> PC: OK
    切换配方
        MES -> PC: {"pp_select": "recipe_name_value"}
        PC -> MES: {"pp_select_result": 1}, 1: 切换成功, 2: 切换失败
    询问当前配方
        MES -> PC: current_recipe_name
        PC -> MES: {"current_recipe_name": "recipe_name_value"}
    出现报警
        PC -> MES: {"occur_alarm": {"alarm_id": 100,"alarm_text":"this is alarm content"}}
        MES -> PC: OK
    报警消除
        PC -> MES: {"clean_alarm": {"alarm_id": 100,"alarm_text":"this is alarm content"}}
        MES -> PC: OK
"""
from inovance_tag.tag_communication import TagCommunication
from passive_equipment.handler_passive import HandlerPassive
from socket_cyg.socket_server_asyncio import CygSocketServerAsyncio

from equipment_sequence.lin_zhong.system_solder import table_models


class SystemSolder(HandlerPassive):

    def __init__(self):
        control_dict = {
            "uploading_tag": TagCommunication("127.0.0.1"),
            "place_solder_sheet": CygSocketServerAsyncio("127.0.0.1", 1830),
            "cutting_tag": TagCommunication("127.0.0.2")
        }
        super().__init__(__file__, control_dict, open_flag=False)

    def _on_rcmd_LotStartReply(self, **kwargs):
        """eap监控到 1006 new_circulate 事件后下发的 LotStartReply.

        Args:
            **kwargs:
        """

    def _on_rcmd_keyCarrierReply(self, **kwargs):
        """eap监控到 2003 solder_carrier_in_request_uploading 回复回流焊托盘是否可以进站.

        Args:
            **kwargs:
        """
        circulate_name = kwargs.get("Circulate_No", "")
        self.set_dv_value_with_name("circulate_name", circulate_name)

        code = int(kwargs.get("CODE", 2))
        self.set_dv_value_with_name("is_allow_solder_carrier_in_uploading", code)
        if code == 1:  # 允许进站
            self.set_time_dv_value({"dv_name": "solder_carrier_in_time_uploading"})
        self.set_dv_value_with_name("is_eap_reply_carrier_in_uploading", True)

    def _on_rcmd_START(self, **kwargs):
        """eap监控到 1011 product_in_request 回复基板产品是否可以做.

        Args:
            **kwargs:
        """
        code = int(kwargs.get("CODE", 2))
        self.set_dv_value_with_name("is_allow_product_in_uploading", code)
        self.set_dv_value_with_name("is_eap_reply_product_in_uploading", True)

    def _on_rcmd_BridgeInReply(self, **kwargs):
        """eap监控到 1012 bridge_in_request 回复半桥产品是否可以做.

        Args:
            **kwargs:
        """
        code = int(kwargs.get("CODE", 2))
        self.set_dv_value_with_name("is_allow_bridge_in", code)
        circulate_name = kwargs.get("Circulate_No", "")
        self.set_dv_value_with_name("circulate_name", circulate_name)
        self.set_dv_value_with_name("is_eap_reply_bridge_in", True)

    def new_circulate(self, circulate_name: str) -> str:
        """在设备上开工单.

        Args:
            circulate_name: 流转单号.

        Returns:
            str: 返回 OK.
        """
        self.set_dv_value_with_name("circulate_name", circulate_name)
        self.send_s6f11("new_circulate")
        return "OK"

    def new_solder_sheet_info(self, solder_sheet_info: dict) -> str:
        """上传新的焊片料号信息.

        Args:
            solder_sheet_info: 焊片料号信息.

        Returns:
            str: 返回 OK.
        """
        solder_material_name = solder_sheet_info.get("solder_material_name", "")
        solder_lot_name = solder_sheet_info.get("solder_lot_name", "")
        self.set_dv_value_with_name("solder_material_name", solder_material_name)
        self.set_dv_value_with_name("solder_lot_name", solder_lot_name)
        return "OK"

    def bridge_request(self, bridge_code: str) -> str:
        """请求二桥是否可做.

        Args:
            bridge_code: 二桥码.

        Returns:
            str: 返回半桥是否可做, 1: 可做, 2: 不可做.
        """
        self.set_dv_value_with_name("bridge_code", bridge_code)
        self.send_s6f11("bridge_in_request")

        self.wait_eap_reply(self.config["socket_signal_info"]["bridge_request"])

        is_allow_bridge_in = self.get_dv_value_with_name("is_allow_bridge_in")
        return str(is_allow_bridge_in)

    def occur_alarm(self, alarm_info: dict) -> str:
        """放半桥设备出现报警.

        Args:
            alarm_info: 报警信息.
            {"alarm_id": 100,"alarm_text":"this is alarm content"}

        Returns:
            str: 返回 OK.
        """
        alarm_id = alarm_info.get("alarm_id", 0)
        alarm_text = alarm_info.get("alarm_text", "not define")
        self.set_clear_alarm_socket(128, alarm_id, alarm_text)
        return "OK"

    def clean_alarm(self, alarm_info: dict) -> str:
        """放半桥设备报警消除.

        Args:
            alarm_info: 报警信息.
            {"alarm_id": 100,"alarm_text":"this is alarm content"}

        Returns:
            str: 返回 OK.
        """
        alarm_id = alarm_info.get("alarm_id", 0)
        alarm_text = alarm_info.get("alarm_text", "not define")
        self.set_clear_alarm_socket(0, alarm_id, alarm_text)
        return "OK"

    def carrier_in(self, carrier_code: str) -> str:
        """焊接托盘进放半桥设备.

        Args:
            carrier_code: 二桥码.

        Returns:
            str: 返回 OK.
        """
        self.set_dv_value_with_name("solder_carrier_code_in_bridge", carrier_code)
        self.set_time_dv_value({"dv_name": "solder_carrier_in_time_bridge"})
        return "OK"

    def carrier_out(self, carrier_info: dict) -> str:
        """焊接托盘出放半桥设备.

        Args:
            carrier_info: 焊接托盘里面的基板产品和半桥信息.
            {
                "carrier_code": "carrier_code_value",
                "product_codes": ["code1", "code2"],
                "bridge_codes: ["bridge_code1", "bridge_code2", "bridge_code3", "bridge_code4", "bridge_code5", "bridge_code6"]
            }

        Returns:
            str: 返回 OK.
        """
        solder_carrier_code_out_bridge = carrier_info.get("carrier_code", "")
        self.set_dv_value_with_name("solder_carrier_code_out_bridge", solder_carrier_code_out_bridge)

        product_code_list_bridge = carrier_info.get("product_codes", [])
        self.set_dv_value_with_name("product_code_list_bridge", product_code_list_bridge)

        bridge_list = carrier_info.get("bridge_codes", [])
        self.set_dv_value_with_name("bridge_list", bridge_list)

        self.set_time_dv_value({"dv_name": "solder_carrier_out_time_bridge"})

        self.save_data_to_database_solder_carrier_out_bridge()
        return "OK"

    def set_dv_from_database_solder_carrier_in_cutting(self, call_back: dict):
        """下料机焊接托盘进站时从数据库获取数据设置 dv.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        table_model_class_name = call_back["table_model_class_name"]
        table_model_class = getattr(table_models, table_model_class_name)
        filter_dict = {
            "solder_carrier_code": self.get_dv_value_with_name("solder_carrier_code_in_cutting")
        }
        data_list = self.mysql.query_data(table_model_class, filter_dict)
        product_code_set, bridge_list = set(), []
        for data in data_list:
            product_code_set.add(data["product_code"])
            bridge_list.append(data["bridge_code"])
        product_code_list = list(product_code_set)
        product_state_list = [1 for _ in range(len(product_code_list))]

        circulate_name = data_list[0]["circulate_name"]
        self.set_dv_value_with_name("circulate_name", circulate_name)
        self.config_instance.update_config_dv_value("circulate_name", circulate_name)

        self.set_dv_value_with_name("product_code_list_cutting_write", product_code_list)
        self.set_dv_value_with_name("bridge_code_list_cutting_write", bridge_list)
        self.set_dv_value_with_name("product_state_list_cutting_write", product_state_list)

    def set_dv_from_database_key_carrier_out_cutting(self, call_back: dict):
        """下料机键合托盘出站时从数据库获取数据设置 dv.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        table_model_class_name = call_back["table_model_class_name"]
        table_model_class = getattr(table_models, table_model_class_name)
        filter_dict = {
            "key_carrier_code": self.get_dv_value_with_name("key_carrier_code_out_cutting")
        }
        data_list = self.mysql.query_data(table_model_class, filter_dict)
        product_code_set, bridge_list = set(), []
        for data in data_list:
            product_code_set.add(data["product_code"])
            bridge_list.append(data["bridge_code"])
        product_code_list = list(product_code_set)

        self.set_dv_value_with_name("product_code_list_cutting", product_code_list)
        self.set_dv_value_with_name("bridge_code_list_cutting", bridge_list)

    # 焊接托盘出站
    def save_data_to_database_solder_carrier_out_uploading(self, call_back: dict):
        """保存焊接托盘从上料机出站数据.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        table_model_class_name = call_back["table_model_class"]
        table_model_class = getattr(table_models, table_model_class_name)

        product_code_list_uploading = self.get_dv_value_with_name("product_code_list_uploading")
        solder_jig_code_list = self.get_dv_value_with_name("solder_jig_code_list")

        add_data_list = []
        for index, product_code in enumerate(product_code_list_uploading):
            add_data_list.append({
                "product_code": product_code,
                "solder_carrier_code": self.get_dv_value_with_name("solder_carrier_in_time_uploading"),
                "solder_carrier_in_time": self.get_dv_value_with_name("solder_carrier_in_time_uploading"),
                "solder_carrier_out_time": self.get_dv_value_with_name("solder_carrier_out_time_uploading"),
                "solder_jig_code": solder_jig_code_list[index],
                "lot_name": self.get_sv_value_with_name("lot_name"),
                "circulate_name": self.get_dv_value_with_name("circulate_name"),
            })

        self.mysql.add_data(table_model_class, add_data_list)

    def save_data_to_database_solder_carrier_out_bridge(self):
        """保存焊接托盘从放半桥设备出站数据."""
        bridge_list = self.get_dv_value_with_name("bridge_list")
        product_code_list_bridge = self.get_dv_value_with_name("product_code_list_bridge")
        solder_carrier_code_out_bridge = self.get_dv_value_with_name("solder_carrier_code_out_bridge")
        add_data = []
        for index, bridge_code in enumerate(bridge_list):
            add_data.append({
                "bridge_code": bridge_code,
                "product_code": product_code_list_bridge[0] if index > 2 else product_code_list_bridge[1],
                "solder_carrier_code": solder_carrier_code_out_bridge,
                "solder_carrier_in_time": self.get_dv_value_with_name("solder_carrier_in_time_bridge"),
                "solder_carrier_out_time": self.get_dv_value_with_name("solder_carrier_out_time_bridge"),
                "lot_name": self.get_dv_value_with_name("current_lot_name"),
                "circulate_name": self.get_dv_value_with_name("circulate_name"),
            })
        self.mysql.add_data(table_models.Bridge, add_data)

    def save_data_to_database_solder_carrier_out_cutting(self, call_back: dict):
        """焊接托盘从下料设备出站保存进出站时间.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        table_model_class_name = call_back["table_model_class"]
        table_model_class = getattr(table_models, table_model_class_name)

        solder_carrier_out_time_cutting = self.get_dv_value_with_name("solder_carrier_out_time_cutting")
        solder_carrier_in_time_cutting = self.get_dv_value_with_name("solder_carrier_in_time_cutting")

        add_data_list = [{
            "solder_carrier_code": self.get_dv_value_with_name("solder_carrier_out_cutting"),
            "solder_carrier_in_time": solder_carrier_in_time_cutting,
            "solder_carrier_out_time": solder_carrier_out_time_cutting,
            "lot_name": self.get_sv_value_with_name("current_lot_name"),
            "circulate_name": self.get_dv_value_with_name("circulate_name"),
        }]

        self.mysql.add_data(table_model_class, add_data_list)

    # ------------------
    def save_data_to_database_product_in_key_carrier(self, call_back: dict):
        """保存下料机产品放入键合托盘数据.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        table_model_class_name = call_back["table_model_class"]
        table_model_class = getattr(table_models, table_model_class_name)

        key_carrier_code_product_in_key = self.get_dv_value_with_name("key_carrier_code_product_in_key")
        product_code_product_in_key = self.get_dv_value_with_name("product_code_product_in_key")
        bridge_code_list_product_in_key = self.get_dv_value_with_name("bridge_code_list_product_in_key")

        add_data_list = []
        for index, bridge_code in enumerate(bridge_code_list_product_in_key):
            add_data_list.append({
                "circulate_name": self.get_dv_value_with_name("circulate_name"),
                "bridge_code": bridge_code,
                "product_code": product_code_product_in_key,
                "key_carrier_code": key_carrier_code_product_in_key
            })

        self.mysql.add_data(table_model_class, add_data_list)

    def save_data_to_database_records(self, call_back: dict):
        """焊接托盘从下料设备出站保存此焊接托盘的生命周期.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        table_model_class_name = call_back["table_model_class"]
        table_model_class = getattr(table_models, table_model_class_name)

        solder_carrier_out_cutting = self.get_dv_value_with_name("solder_carrier_out_cutting")
        filter_dict = {
            "solder_carrier_code": solder_carrier_out_cutting
        }
        data_list = self.mysql.query_data_join(table_models.Bridge, table_models.Uploading, "product_code", filter_dict)
        data_list_cutting = self.mysql.query_data(table_models.Cutting, filter_dict)
        solder_carrier_in_time_cutting = data_list_cutting[0]["solder_carrier_in_time_cutting"]
        solder_carrier_out_time_cutting = data_list_cutting[0]["solder_carrier_out_time_cutting"]

        real_data_list = []
        for data in data_list:
            data.pop("id")
            data.pop("created_at")
            data.pop("updated_at")
            data.update({
                "solder_carrier_in_time_cutting": solder_carrier_in_time_cutting,
                "solder_carrier_out_time_cutting": solder_carrier_out_time_cutting
            })
            real_data_list.append(data)
        self.mysql.add_data(table_model_class, real_data_list)

    def delete_database_data_solder_carrier_out_cutting(self, call_back: dict):
        """焊接托盘出站删除此焊接托盘的所有信息.

        Args:
            call_back: 要执行的 call_back 信息.
        """
        carrier_code = self.get_dv_value_with_name("solder_carrier_code_out_cutting")
        self.mysql.delete_data(table_models.Uploading, {"solder_carrier_code": carrier_code})
        self.mysql.delete_data(table_models.Bridge, {"solder_carrier_code": carrier_code})
        self.mysql.delete_data(table_models.Cutting, {"solder_carrier_code": carrier_code})