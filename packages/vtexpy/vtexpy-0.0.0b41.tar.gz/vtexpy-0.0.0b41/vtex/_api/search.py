from typing import Any, Union

from .._dto import VTEXDataResponse
from .base import BaseAPI


class SearchAPI(BaseAPI):
    """
    Client for the Search API.
    https://developers.vtex.com/docs/api-reference/search-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def search_sku_offers(
        self,
        product_id: Union[int, str],
        sku_id: Union[int, str],
        **kwargs: Any,
    ) -> VTEXDataResponse[Any]:
        return self._request(
            method="GET",
            endpoint=(
                f"/api/catalog_system/pub/products/offers/{product_id}/sku/{sku_id}"
            ),
            environment=self.ENVIRONMENT,
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[Any],
        )
