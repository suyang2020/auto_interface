import os
import re
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print(sys.path)
from requests import Session
from httprunner import make

import debugtalk
from utils import tools
from utils import logger

class SwaggerParser(object):
    def __init__(self, swagger_url, module_name):
        self.swagger_url = swagger_url
        self.module_name = module_name
        # self.project_name = project_name
        api_url = self.swagger_url + self.module_name + "/v2/api-docs"
        res = Session().request('get', api_url).json()
        self.data_path = res.get('paths')  # 获取swagger Json 格式下 paths节点 接口的 path
        self.definitions = res.get('definitions')  # 获取swagger定义的元数据, param参数
        self.host = res.get("host")
        self.basepath = res.get("basePath")

    def _make_data(self, type):
        """
        根据数据类型生成不同的测试数据
        :param type: 数据类型
        :return:
        """
        if type == "string":
            return ""
        elif type == "int" or type == "integer":
            return 0
        elif type == "boolean":
            return True
        elif type == "array":
            return []
        elif type == "file":
            return ""

    def _prepare_config(self, name="testcase description"):
        """ prepare config block.
        """
        return {"name": name, "variables": {}, "verify": False}

    def _prepare_get_requests(self, teststep_dict, get_requests):
        """
        准备get请求所需要的header和参数
        :param teststep_dict: 将header和params写入此字典变量
        :param get_requests: 从此数据中解析都有哪些参数
        :return:
        """
        parameters = get_requests["parameters"]

        # headers = debugtalk.set_headers(self.project_name)

        params = {}

        for p in parameters:
            if p["in"] == "header" and p["name"] != "token":
                if "type" in p.keys():
                    teststep_dict["request"]["headers"][p["name"]] = self._make_data(p["type"])
            elif p["in"] == "query":

                if "type" in p.keys():
                    params[p["name"]] = self._make_data(p["type"])
                    teststep_dict["request"]["params"] = params

        # teststep_dict["request"]["headers"] = headers

    def _find_definitions(self, datas, schema):
        """
        从definitions解析post请求想要的参数，并返回一个字典数据
        :param datas:字典变量，保存解析过的参数
        :param schema:definitions中用到的键
        :return:
        """
        if schema == "JSON":
            return {}
        dto = self.definitions[schema]
        if "type" in dto.keys() and dto["type"] == "object":
            for dto_key, dto_value in dto["properties"].items():
                if "$ref" in dto_value.keys():
                    child_dto_outside = dto_value["$ref"].split("/")[-1]
                    datas[dto_key] = {}
                    datas[dto_key] = self._find_definitions(datas[dto_key], child_dto_outside)

                if "type" in dto_value.keys() and dto_value["type"] == "array" and "items" in dto_value.keys():
                    if "$ref" in dto_value["items"].keys():
                        child_dto = dto_value["items"]["$ref"].split("/")[-1]
                        datas[dto_key] = []
                        dto_stmp = {}
                        datas[dto_key].append(self._find_definitions(dto_stmp, child_dto))
                    elif dto_value["type"] == "array":
                        datas[dto_key] = self._make_data(dto_value["type"])
                    else:
                        datas[dto_key] = self._make_data(dto_value["items"]["type"])
                elif "type" in dto_value.keys() :
                    datas[dto_key] = self._make_data(dto_value["type"])
        return datas

    def _prepare_post_requests(self, teststep_dict, post_requests):
        """
        解析post方法所需要的参数，有些可以直接解析到，有些事通过_find_definitions到下面定义的字典中找到
        :param teststep_dict: 保存解析过的参数的字典
        :param post_requests: 从这个参数中解析
        :return:
        """
        parameters = post_requests["parameters"]

        # headers = debugtalk.set_headers(self.project_name)
        datas = {}
        params = {}
        files = {}

        for param in parameters:
            if param["in"] == "header" and param["name"] != "token":
                if "type" in param.keys():
                    teststep_dict["request"]["headers"][param["name"]] = self._make_data(param["type"])
            elif param["in"] == "body":
                if "schema" in param.keys():
                    try:
                        schemas = param.get("schema").get("$ref")
                        schema = schemas.split("/")[-1]
                    except AttributeError:
                        schemas = param.get("schema").get("items")
                        schemas = schemas["$ref"]
                        schema = schemas.split("/")[-1]

                    self._find_definitions(datas, schema)
                elif "type" in param.keys() and "format" in param.keys():
                    datas[param["name"]] = self._make_data(param["type"])

                if "type" in param.get("schema").keys() and param["schema"]["type"] == "array":
                    array_datas = []
                    array_datas.append(datas)
                    teststep_dict["request"]["json"] = array_datas
                else:
                    teststep_dict["request"]["json"] = datas
            elif param["in"] == "query":
                if "type" in param.keys():
                    params[param["name"]] = self._make_data(param["type"])
                    teststep_dict["request"]["params"] = params
            elif param["in"] == "formData":
                if "type" in param.keys() and param["type"] == "file":
                    files[param["name"]] = self._make_data(param["type"])
                    teststep_dict["request"]["files"] = files

        # teststep_dict["request"]["headers"] = headers

    def _prepare_teststeps(self, url_path, step):
        """ make teststep list.
            teststeps list are parsed from HAR log entries list.
        """
        description = ""
        teststep_dict = {"name": "", "request": {}, "validate": []}
        teststeps = []
        test_url = "https://" + self.host + self.basepath

        teststep_dict["name"] = str(url_path)
        teststep_dict["request"]["url"] = test_url + teststep_dict["name"]
        headers = {
            "user-agent": "auto_interface_test",
            "Content-Type": "application/json;charset=utf-8",
            "Cookie": '${get_cookies()}',
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "token": '${get_token()}'
        }
        # headers = debugtalk.set_headers(self.project_name)
        teststep_dict["request"]["headers"] = headers

        for k_,v_ in step.items():
            description = v_["summary"]
            k_ = k_.upper()
            if k_ == 'GET':
                teststep_dict["request"]["method"] = "GET"
                self._prepare_get_requests(teststep_dict, v_)
            elif k_ == "POST":
                teststep_dict["request"]["method"] = "POST"
                self._prepare_post_requests(teststep_dict, v_)

        validate = [{"eq": ["status_code", 200]}, {"eq": ["body.code", "0"]}]
        teststep_dict["validate"].extend(validate)

        teststeps.append(teststep_dict)
        return teststeps,description

    def _make_testcase(self):
        """ Extract info from HAR file and prepare for testcase
        """
        logger.log.info("Extract info from swagger url and prepare for testcase.")
        project_dir = self._make_project_dir()
        # testcases = []
        for url_path, step in self.data_path.items():
            # 创建yaml文件
            pa_res = re.split(r'[/]+', url_path)  # 获取path路径, 切片保存保存为: ['api', 'v1', 'five-elements']
            if "{" in pa_res[-1]:
                pa_res.pop()
            api, *file = pa_res[1:]
            if file:  # 如果file存在就进行转换
                file = '_'.join(["".join(x[:1].upper() + x[1:]) for x in file]) # 把 file 首字母转换为大写, 进行拼接
            else:
                file = api

            # 添加文件后缀
            file += '.yml'  # 文件后缀加上 .yml
            # 比如路径是：/api/im-web/file/upload，那这里创建的就是在im-web下创建test_file文件夹
            dirs = os.path.join(project_dir, f"test_{api}")  # 使用项目名称+ api 在项目目录下创建 api文件夹
            dirs = tools.ensure_path_sep(dirs)
            if not os.path.exists(dirs):  # 判断项目的 api 是否存在，不存在就创建
                os.mkdir(dirs)

            # 切换工作目录路径
            os.chdir(dirs)  # 方法用于改变当前工作目录到指定的路径
            yaml_file_dir = os.path.join(dirs, file) # yaml文件路径
            if not os.path.exists(yaml_file_dir):
                # 生成测试用例
                datas = self._prepare_teststeps(url_path, step)
                teststeps = datas[0]
                config = self._prepare_config(datas[1])
                testcase = {"config": config, "teststeps": teststeps}
                # 用例转成yaml
                tools.dump_yaml(testcase, yaml_file_dir)

    def _make_project_dir(self):
        workspace = os.path.join(os.path.join(debugtalk.RootDir,"testcases")) # 获取当前文件路径
        # case_space = workspace.split()
        project_ = os.path.join(workspace, self.module_name)  # 获取当前文件目录路径+项目名称，进行拼接 如 C:\Users\Administrator\Desktop\demo\five
        # 创建项目文件
        project_ = make.ensure_file_abs_path_valid(project_)
        project_ = tools.ensure_path_sep(project_)
        if not os.path.exists(project_):  # 如果项目文件不存在就创建文件
            os.makedirs(project_)
        return project_

    def gen_testcase(self):
        logger.log.info(f"Start to generate testcase from {self.module_name}")

        self._make_testcase()


if __name__ == '__main__':
    # args_list = sys.argv
    # system_name = args_list[1]
    # project_name = args_list[2]
    # swagger_url_pre = 'https://api-gateway.medbanks-test.com/api/'
    # SwaggerParser(swagger_url_pre, system_name, project_name).gen_testcase()

    swagger_url_pre = 'https://api-gateway.medbanks-test.com/api/'  # "swagger 对应服务接口地址"
    SwaggerParser(swagger_url_pre, "im-web").gen_testcase()