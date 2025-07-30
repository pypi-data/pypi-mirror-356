import pytest

from ey_commerce_lib.kogan.main import KoganClient
from ey_commerce_lib.kogan.schemas.query.product import KoganProductQuery


@pytest.mark.asyncio
async def test_client():
    async with KoganClient(
        seller_id="xxxxx",
        seller_token="xxxxxx"
    ) as client:
        await client.products(KoganProductQuery(search="Spider School Bags Kids Superhero Spider-Man Backpack Gift Set (Color:A)"))
