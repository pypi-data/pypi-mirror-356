import asyncpg

async def pg_get_exist_links_by_site_url(site_url, links:list, connection_string) -> list:
    conn = await asyncpg.connect(connection_string)
    try:
        rows = await conn.fetch("""
            SELECT e.url
            FROM entries e
            JOIN feeds f ON e.feed_id = f.id
            WHERE f.site_url = $1 AND e.url = ANY($2)
        """, site_url, links)
        return [row['url'] for row in rows]
    finally:
        await conn.close()

if __name__ == "__main__":
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
        except Exception as e:
            print(e)

    asyncio.run(main())
