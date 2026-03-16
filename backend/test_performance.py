#!/usr/bin/env python3
import asyncio
import uuid
import httpx
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"


async def register_user(client: httpx.AsyncClient, username: str, email: str, password: str) -> None:
    r = await client.post(
        f"{API_BASE_URL}/api/auth/register",
        json={"username": username, "email": email, "password": password}
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"register failed: {r.status_code} {r.text}")


async def login_user(client: httpx.AsyncClient, email: str, password: str) -> str:
    r = await client.post(
        f"{API_BASE_URL}/api/auth/login",
        json={"email": email, "password": password}
    )
    if r.status_code != 200:
        raise RuntimeError(f"login failed: {r.status_code} {r.text}")
    return r.json()["access_token"]


async def run_smoke() -> None:
    async with httpx.AsyncClient(timeout=60.0) as client:
        suffix = uuid.uuid4().hex[:8]
        admin_username = f"admin_{suffix}"
        admin_email = f"admin_{suffix}@example.com"
        password = "test123456"

        await register_user(client, admin_username, admin_email, password)
        token = await login_user(client, admin_email, password)
        headers = {"Authorization": f"Bearer {token}"}

        r = await client.post(f"{API_BASE_URL}/api/families/", json={"name": f"家庭_{suffix}"}, headers=headers)
        if r.status_code != 201:
            raise RuntimeError(f"create family failed: {r.status_code} {r.text}")
        family_id = r.json()["id"]

        invited_emails = []
        for i in range(1, 6):
            u = f"m{i}_{suffix}"
            e = f"m{i}_{suffix}@example.com"
            await register_user(client, u, e, password)
            invited_emails.append(e)

        for e in invited_emails[:4]:
            r = await client.post(f"{API_BASE_URL}/api/families/{family_id}/invite", json={"email": e}, headers=headers)
            if r.status_code != 200:
                raise RuntimeError(f"invite member failed: {r.status_code} {r.text}")

        r = await client.post(f"{API_BASE_URL}/api/families/{family_id}/invite", json={"email": invited_emails[4]}, headers=headers)
        if r.status_code == 200:
            raise RuntimeError("invite limit should fail but succeeded")

        now = datetime.now()
        for amt in (60.0, 70.0):
            r = await client.post(
                f"{API_BASE_URL}/api/transactions/",
                json={
                    "date": now.isoformat(),
                    "time": now.strftime("%H:%M"),
                    "amount": amt,
                    "category": "餐饮美食",
                    "item": "测试",
                    "merchant": "测试商家",
                    "notes": ""
                },
                headers=headers
            )
            if r.status_code != 201:
                raise RuntimeError(f"create tx failed: {r.status_code} {r.text}")

        r = await client.post(
            f"{API_BASE_URL}/api/budgets/",
            json={
                "family_id": family_id,
                "category": "餐饮美食",
                "amount": 100.0,
                "period": "monthly",
                "year": now.year,
                "month": now.month
            },
            headers=headers
        )
        if r.status_code != 201:
            raise RuntimeError(f"create budget failed: {r.status_code} {r.text}")

        r = await client.get(
            f"{API_BASE_URL}/api/budgets/status?family_id={family_id}&year={now.year}&month={now.month}",
            headers=headers
        )
        if r.status_code != 200:
            raise RuntimeError(f"budget status failed: {r.status_code} {r.text}")

        r = await client.get(
            f"{API_BASE_URL}/api/budgets/alerts?family_id={family_id}&year={now.year}&month={now.month}",
            headers=headers
        )
        if r.status_code != 200:
            raise RuntimeError(f"budget alerts failed: {r.status_code} {r.text}")

        r = await client.get(f"{API_BASE_URL}/api/stats/periods?family_id={family_id}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"stats periods failed: {r.status_code} {r.text}")

        r = await client.get(f"{API_BASE_URL}/api/stats/forecast?family_id={family_id}&period=month", headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"stats forecast failed: {r.status_code} {r.text}")

        r = await client.get(f"{API_BASE_URL}/api/version/export-csv?family_id={family_id}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"export csv failed: {r.status_code} {r.text}")

        r = await client.get(f"{API_BASE_URL}/api/version/export-excel?family_id={family_id}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"export excel failed: {r.status_code} {r.text}")

        r = await client.get(f"{API_BASE_URL}/api/version/export-pdf?family_id={family_id}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError(f"export pdf failed: {r.status_code} {r.text}")

        r = await client.post(
            f"{API_BASE_URL}/api/transactions/",
            json={
                "date": now.isoformat(),
                "time": now.strftime("%H:%M"),
                "amount": 12.34,
                "category": "交通出行",
                "item": "删除测试",
                "merchant": "",
                "notes": ""
            },
            headers=headers
        )
        if r.status_code != 201:
            raise RuntimeError(f"create tx for delete failed: {r.status_code} {r.text}")
        tx_id = r.json()["id"]

        sync_from = (datetime.utcnow() - timedelta(minutes=1)).isoformat()
        r = await client.delete(f"{API_BASE_URL}/api/transactions/{tx_id}", headers=headers)
        if r.status_code not in (200, 204):
            raise RuntimeError(f"delete tx failed: {r.status_code} {r.text}")

        r = await client.get(
            f"{API_BASE_URL}/api/transactions/?include_deleted=true&updated_since={sync_from}",
            headers=headers
        )
        if r.status_code != 200:
            raise RuntimeError(f"sync list failed: {r.status_code} {r.text}")
        found = [t for t in r.json() if t["id"] == tx_id]
        if not found or not found[0].get("deleted_at"):
            raise RuntimeError("deleted tombstone not returned in sync response")

        print("OK")


if __name__ == "__main__":
    asyncio.run(run_smoke())
