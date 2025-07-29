use sqlx::AnyPool;
use dashmap::DashMap;
use std::sync::OnceLock;
use std::time::Instant;

static DB_CACHE: OnceLock<DashMap<String, AnyPool>> = OnceLock::new();

pub async fn get_or_create_pool(db_url: &str, use_cache: bool) -> Result<AnyPool, sqlx::Error> {
    let cache = DB_CACHE.get_or_init(DashMap::new);

    if use_cache {
        if let Some(pool) = cache.get(db_url) {
            return Ok(pool.clone());
        }
    }

    let start = Instant::now();
    let pool = AnyPool::connect(db_url).await?;
    if use_cache {
        cache.insert(db_url.to_string(), pool.clone());
    }

    let elapsed = start.elapsed();
    if elapsed.as_millis() > 500 {
        println!("[SLOW] Creating new DB connection took {:?}", elapsed);
    }

    Ok(pool)
}
