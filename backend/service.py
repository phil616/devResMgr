from fastapi import APIRouter, HTTPException
from model import KVStore
import requests
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException
service_router = APIRouter(prefix="/domain", tags=['domain'])

async def get_cf_api_key() -> str:
    cf_api = await KVStore.filter(key="cloudflare_api").first()
    if not cf_api:
        raise HTTPException(status_code=404, detail="Cloudflare API not configured.")
    return cf_api.value
async def get_sld() -> str:
    sld = await KVStore.filter(key="sld").first()
    if not sld:
        raise HTTPException(status_code=404, detail="Second-level domain not configured.")
    return sld.value


class DomainRecord(BaseModel):
    id: str
    name: str
    type: str
    content: str
    proxied: bool

@service_router.get("/update_kvstore")
async def update_kvstore(key: str, value: str):
    kv = await KVStore.filter(key=key).first()
    if not kv:
        kv = KVStore(key=key, value=value)
    else:
        kv.value = value
    await kv.save()
    return {"key": kv.key, "value": kv.value}

# Cloudflare API Baseurl
BASE_URL = "https://api.cloudflare.com/client/v4"


async def cf_get_zone_id(domain_name: str, token: str) -> str:
    """
    Get Cloudflare Zone ID by domain name.
    """
    url = f"{BASE_URL}/zones"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    zones = response.json().get("result", [])
    for zone in zones:
        if zone["name"] == domain_name:
            return zone["id"]

    raise HTTPException(status_code=404, detail=f"Domain {domain_name} not found in your Cloudflare account.")

async def get_domains(domain_name: str, token: str, zone_id: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    per_page = 100
    page = 1
    all_records = []
    while True:
        params = {"page": page, "per_page": per_page}
        url = f"{BASE_URL}/zones/{zone_id}/dns_records"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json().get("result", [])
        if not result:
            break
        all_records.extend(result)
        page += 1
    return [DomainRecord(**record) for record in all_records]


@service_router.get("/domains")
async def api_get_domain_records():
    cf_api = await get_cf_api_key()
    sld = await get_sld()
    zone_id = await cf_get_zone_id(sld, cf_api)
    results = await get_domains(sld, cf_api, zone_id)
    return results


@service_router.post("/deleteDomainRecordByCfID")
async def api_update_domain_record(cf_id:str):
    """Delete a domain record by Cloudflare ID"""
    cf_api = await get_cf_api_key()
    sld = await get_sld()
    zone_id = await cf_get_zone_id(sld, cf_api)
    headers = {
        "Authorization": f"Bearer {cf_api}",
        "Content-Type": "application/json",
    }
    url = f"{BASE_URL}/zones/{zone_id}/dns_records/{cf_id}"
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return {"message": "success"}

@service_router.post("/createDomainRecord")
async def api_create_domain_record(prefix:str, a_record:str):
    """Create a new domain record"""
    cf_api = await get_cf_api_key()
    sld = await get_sld()
    zone_id = await cf_get_zone_id(sld, cf_api)
    headers = {
        "Authorization": f"Bearer {cf_api}",
        "Content-Type": "application/json",
    }
    data = {
        "type": "A",
        "name": prefix + "." + sld,
        "content": a_record,
        "ttl": 1,  # Auto TTL
        "proxied": False,  # Whether to proxy the record through Cloudflare
    }
    url = f"{BASE_URL}/zones/{zone_id}/dns_records"
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()


@service_router.post("/setSLD")
async def api_set_second_level_domain(domain_name:str):
    """Set the second-level domain for the Cloudflare account"""
    sld = await KVStore.filter(key="sld").first()
    if not sld:
        sld = KVStore(key="sld", value=domain_name)
    else:
        sld.value = domain_name
    await sld.save()
    return {"message": "success"}