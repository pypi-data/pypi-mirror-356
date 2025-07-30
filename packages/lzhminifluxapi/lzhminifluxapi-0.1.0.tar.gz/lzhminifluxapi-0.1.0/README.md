# miniflux api

获取`MiniFlux`数据库中对应`site_url`的订阅源中已有的`link`的列表

## 示例
```python
import asyncio

async def main():
    connection_string='postgres://user:password@localhost/database'
    links = {'https://jandan.net/t/5932788', 'https://jandan.net/t/5930642', 'https://jandan.net/t/5929636'}
    try:
        e_links = await pg_get_exist_links_by_site_url(
            site_url="https://jandan.net/top#tab=7days",
            links = links,
            connection_string = connection_string
        )
        print(e_links)

asyncio.run(main())
```
