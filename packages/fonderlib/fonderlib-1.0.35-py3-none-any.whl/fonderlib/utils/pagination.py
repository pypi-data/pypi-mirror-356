def paginated_request(
    make_request_fn,
    api_url: str,
    customer_id: str,
    resource_key: str,
    options: dict = None,
    default_limit: int = 50,
    default_page: int = 0,
):
    all_items = []
    page = default_page
    limit = default_limit

    base_params = {"customer-id": customer_id}
    if options:
        params = {**base_params, **options}
    else:
        params = base_params

    while True:
        params["limit"] = limit
        params["page"] = page

        response = make_request_fn(api_url, params, {})
        items = response.get(resource_key, [])
        general_data = response.get("general_data", {})
        total_rows = general_data.get("total_rows", len(items))

        all_items.extend(items)

        if (page + 1) * limit >= total_rows:
            break
        page += 1

    return {
        resource_key: all_items,
        "general_data": {
            "limit": limit,
            "page": 0,
            "total_rows": len(all_items),
        },
    }
