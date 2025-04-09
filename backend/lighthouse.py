# Tencent Lighthouse API wrapper

from typing_extensions import Literal
from fastapi import APIRouter, HTTPException,Depends
from model import KVStore
from cache import get_global_kv, MemStorage
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models
from pydantic import BaseModel
from api import verify_token
light_house_router = APIRouter(prefix="/instance", tags=['lighthouse'], dependencies=[Depends(verify_token)])

async def get_tencent_tuples()-> tuple:
    """
    Get tencent instances from KVStore
    """
    tencent_secret_id = await KVStore.filter(key="tencent_secret_id").first()
    tencent_secret_key = await KVStore.filter(key="tencent_secret_key").first()
    if tencent_secret_id and tencent_secret_key:
        return (tencent_secret_id.value, tencent_secret_key.value)
    else:
        raise HTTPException(status_code=404, detail="Tencent credentials not found")

TENCENT_REGIONS = {
    "ap-singapore": "新加坡",
    "ap-guangzhou": "广州",
    "ap-shanghai": "上海",
    "ap-beijing": "北京",
    "ap-chengdu": "成都",
    "ap-seoul": "首尔",
    "eu-frankfurt": "法兰克福",
    "na-siliconvalley": "硅谷",
    "ap-bangkok": "曼谷",
    "ap-tokyo": "东京"
}


@light_house_router.get("/info/all")
async def get_all_lighthouses(refresh:bool=False, cache:MemStorage=Depends(get_global_kv)):
    if not refresh:
        cached_info = cache.get_value("all_instances")
        if cached_info:
            return cached_info
    SecretId, SecretKey = await get_tencent_tuples()
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        all_instances = []
        for region in TENCENT_REGIONS.keys():
            client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
            req = models.DescribeInstancesRequest()
            req.from_json_string(json.dumps({}))

            resp = client.DescribeInstances(req)
            all_instances.extend(resp.InstanceSet)
        cache.set_value("all_instances", all_instances)
        return all_instances
    except TencentCloudSDKException as err:
        raise HTTPException(status_code=400, detail=str(err))

@light_house_router.get("/firewallRules")
async def api_get_lighthouset_firewall_rules(instance_id: str, region: str):
    try:
        SecretId, SecretKey = await get_tencent_tuples()
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
        req = models.DescribeFirewallRulesRequest()
        params = {
            "InstanceId": instance_id
        }
        req.from_json_string(json.dumps(params))
        resp = client.DescribeFirewallRules(req)
        return resp.FirewallRuleSet

    except TencentCloudSDKException as err:
        raise HTTPException(status_code=400, detail=str(err))

class FirewallRule(BaseModel):
    Protocol: Literal["TCP", "UDP", "ICMP", "ALL", "ICMPv6"]
    Port: str
    CidrBlock: str
    Ipv6CidrBlock: str
    Action: Literal["ACCEPT", "DROP"]
    FirewallRuleDescription: str

@light_house_router.delete("/firewallRules")
async def delete_lighthouse_instance(rule: FirewallRule, instance_id: str, region: str):
    try:
        SecretId, SecretKey = await get_tencent_tuples()
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
        req = models.DeleteFirewallRulesRequest()
        params = {
            "InstanceId": instance_id,
            "FirewallRules": [
                {
                    "Protocol": rule.Protocol,
                    "Port": rule.Port,
                    "CidrBlock": rule.CidrBlock,
                    "Ipv6CidrBlock": rule.Ipv6CidrBlock,
                    "Action": rule.Action,
                }
            ]
        }
        req.from_json_string(json.dumps(params))

        resp = client.DeleteFirewallRules(req)
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        raise HTTPException(status_code=400, detail=str(err))
    
@light_house_router.post("/firewallRules")
async def add_lighthouse_instance(rule: FirewallRule, instance_id: str, region: str):
    try:
        SecretId, SecretKey = await get_tencent_tuples()
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
        req = models.CreateFirewallRulesRequest()
        params = {
            "InstanceId": instance_id,
            "FirewallRules": [
                {
                    "Protocol": rule.Protocol,
                    "Port": rule.Port,
                    "CidrBlock": rule.CidrBlock,
                    "Ipv6CidrBlock": rule.Ipv6CidrBlock,
                    "Action": rule.Action,
                    "FirewallRuleDescription": rule.FirewallRuleDescription
                }
            ]
        }
        req.from_json_string(json.dumps(params))
        resp = client.CreateFirewallRules(req)
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        raise HTTPException(status_code=400, detail=str(err))