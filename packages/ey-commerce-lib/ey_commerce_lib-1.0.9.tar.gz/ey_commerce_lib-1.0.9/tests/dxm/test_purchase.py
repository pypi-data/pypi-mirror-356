import pytest

from ey_commerce_lib.four_seller.main import FourSellerClient
from ey_commerce_lib.four_seller.schemas.query.order import FourSellerOrderQueryModel


async def login_success(user_token: str):
    print(f'user_token: {user_token}')
    pass


@pytest.mark.asyncio
async def test_auto_login_4seller():
    # user_token = await auto_login_4seller(user_name="sky@eeyoung.com", password="ey010203@@")
    # print(user_token)
    async with FourSellerClient(
            user_name="xxxxx",
            password="xxxxxx",
            login_success_call_back=login_success,
            user_token="xxxxxx") as four_seller_client:
        await four_seller_client.list_history_order(FourSellerOrderQueryModel())
