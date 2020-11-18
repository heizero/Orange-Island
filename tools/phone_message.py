from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入 SMS 模块的client models
from tencentcloud.sms.v20190711 import sms_client, models

# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile



def send_message(phone_number,random_code):
    '''
    传参为[],
    :param phone_number:
    :return:
    '''


    SecretId = 'AKIDlFTO42L8F56sMZJAYfU8WfcCYnlalrhI'
    SecretKey = 'YvBOzJkYse9SgcIgfLkrhTzKPq77rM2S'
    area = "ap-guangzhou"
    sdkappid = '1400431734'
    sign = '达到理想不太易公众号'
    TemplateID = '737059'


    try:
        # 腾讯云"secretId", "secretKey"
        cred = credential.Credential(SecretId, SecretKey)


        httpProfile = HttpProfile()
        httpProfile.reqMethod = "POST"  # POST 请求（默认为 POST 请求）
        httpProfile.reqTimeout = 30    # 请求超时时间，单位为秒（默认60秒）
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名（默认就近接入）
        client = sms_client.SmsClient(cred, area)
        req = models.SendSmsRequest()
        # 短信应用 ID: 在 [短信控制台] 添加应用后生成的实际 SDKAppID，例如1400006666
        req.SmsSdkAppid = sdkappid
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，可登录 [短信控制台] 查看签名信息
        req.Sign = sign
        # 例如+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        req.PhoneNumberSet = ['+86'+phone_number]
        # 模板 ID: 必须填写已审核通过的模板 ID，可登录 [短信控制台] 查看模板 ID
        req.TemplateID = TemplateID
        # 模板参数: 若无模板参数，则设置为空
        req.TemplateParamSet = [random_code]


        # 通过 client 对象调用 SendSms 方法发起请求。注意请求方法名与请求对象是对应的
        resp = client.SendSms(req)

        # 输出 JSON 格式的字符串回包
        print(resp.to_json_string(indent=2))

    except TencentCloudSDKException as err:
        print(err)