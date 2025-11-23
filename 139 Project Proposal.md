Seasons of Sound: How Audio Features and Artist Traits Relate to Popularity Across the Year  
Alan Huang  
Anya Mostek  
Berke Altiparmak  
Justin Jiao  
**Motivation**  
Some songs feel like July: fast, bright, high-energy. Others feel like January: quieter, acoustic, reflective. We want to move past vibes and test, with data, whether the strength and direction of associations between track/artist traits and popularity actually change across the year. The goal isn’t a leaderboard predictor but rather a clear inference: which features matter, by how much, and when.

**Variables** and **Data Source**:

* Target (daily, on-chart only)  
  * global\_streams: daily global Spotify streams on days a track appears in the Top-200 (from Kworb track pages: [https://kworb.net/spotify/country/global\_daily\_totals.html](https://kworb.net/spotify/country/global_daily_totals.html)).  
    * We will either have to web-scrape the Kworb data or use this dataset from Kaggle (even though it’s up to 2022): [https://www.kaggle.com/datasets/jfreyberg/spotify-chart-data](https://www.kaggle.com/datasets/jfreyberg/spotify-chart-data)   
* Predictors  
  * Track-level features (Spotify Web API: [https://developer.spotify.com/documentation/web-api](https://developer.spotify.com/documentation/web-api))  
    * Audio: danceability, energy, valence, tempo, loudness, acousticness, instrumentalness, liveness, speechiness, duration\_ms, key, mode, time\_signature.  
    * Metadata: release\_date, explicit.  
  * Artist-level metadata (Spotify Web API)  
    * artist\_popularity, followers, genres (collapsed to coarse buckets, e.g., pop/hip-hop/EDM/rock/latin/etc.).

We will be joining the Kworb data with Spotify Web API on Spotify track ID (Kworb pages are track-ID keyed). We are also using a multi-year window (2014–2025) to capture repeated seasonal cycles.

**Tests**:

**Nested F-test / overall model test.**  
To test whether the model provides explanatory power beyond a constant mean, we will do an overall F-test for the regression:

* H0​: β1​ \= β2​ \= … \= βp​= 0 (no audio/artist features help explain popularity)  
* HA: At least one βj  ≠ 0  (1+ features significantly predict popularity)

**Individual feature tests (t-tests on coefficients).**  
To identify which characteristics are most influential overall, for each predictor (e.g., energy, valence, acousticness), we will test:

* H₀: βj \= 0 (feature has no effect on popularity).  
* HA: βj ≠ 0 (feature significantly affects popularity).

**Seasonal interaction tests.**  
To test whether effects differ across the year, we will add month or season indicators and their interactions with major audio features (e.g., energy × season, valence × season).

* H₀: Interaction \= 0 (effect of each feature is constant across months).  
* HA: Interaction ≠ 0 (feature-popularity relationships vary seasonally).

**Model diagnostics and robustness checks.** We will inspect residual plots, check for multicollinearity, and consider transformations (e.g., log) if needed. If nonlinearity appears, we may compare linear vs. polynomial fits or try standardized coefficients for interpretability.

**Challenges**: 

1. Spotify API doesn’t provide data from the past, hence we resorted to third party data providers to extract this information.   
2. Spotify API provides information about features, but we need to find a way to combine those information with corresponding date and streaming counts from another dataset.  
3. Since the date column contains exact release dates, we need to aggregate by time periods to better analyze trends over time in the future.  
   1. Pandas’ merge\_asof function should come in handy here.

[​​https://developer.spotify.com/documentation/web-api/reference/get-audio-features](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)  
[https://community.spotify.com/t5/Content-Questions/Artist-popularity/td-p/4415259](https://community.spotify.com/t5/Content-Questions/Artist-popularity/td-p/4415259)  
[https://kworb.net/spotify/country/global\_daily\_totals.html](https://kworb.net/spotify/country/global_daily_totals.html)  
[https://www.kaggle.com/datasets/jfreyberg/spotify-chart-data](https://www.kaggle.com/datasets/jfreyberg/spotify-chart-data)