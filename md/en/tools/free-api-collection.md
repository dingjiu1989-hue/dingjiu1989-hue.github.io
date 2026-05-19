---
title: "30 Free and Useful APIs Every Developer Should Know"
description: "A curated collection of 30 APIs with generous free tiers, covering weather, translation, AI, data, and images. Each entry includes usage examples and rate limits."
date: 2025-11-30
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/free-api-collection.html
---

# 30 Free and Useful APIs Every Developer Should Know

A good API can save you weeks of development. These 30 APIs are either completely free or have generous free tiers that cover personal projects and MVPs. Every entry includes a sample request and rate limit info.

## Weather

API| Free Tier| What You Get  
---|---|---  
**Open-Meteo**|  Unlimited| Weather forecasts, historical data. No API key required. Open source.  
**OpenWeatherMap**|  1,000 calls/day| Current weather, 5-day forecast, air pollution data.  
**WeatherAPI**|  1M calls/month| Real-time, forecast, astronomy, sports, timezone. Very generous.  
      
    
    # Open-Meteo example (no API key needed!)
    curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude;=13.41&current;_weather=true"

## AI & Machine Learning

API| Free Tier| What You Get  
---|---|---  
**OpenAI API**|  $5 credit (expires in 3 months)| GPT-4o, GPT-4o-mini. Enough for thousands of requests.  
**Claude API**|  $5 credit| Claude Opus/Sonnet/Haiku. Great for long-context tasks.  
**Hugging Face**|  Free tier with rate limits| Thousands of open models via Inference API. Text, image, audio.  
**Cohere**|  100 calls/min| Embeddings, text generation, reranking. Good for RAG pipelines.  
  
## Translation & Text

API| Free Tier| What You Get  
---|---|---  
**Google Translate (LibreTranslate)**|  Self-host = unlimited| Open-source alternative. Host on a $5 VPS for unlimited translations.  
**DeepL API**|  500,000 chars/month| Highest quality machine translation. EU-based.  
**LanguageTool**|  Free (self-host)| Grammar and style checker. Open source.  
  
## Data & Knowledge

API| Free Tier| What You Get  
---|---|---  
**REST Countries**|  Unlimited| Data on all countries: flags, currencies, languages, timezones.  
**OpenLibrary**|  Unlimited| Book data: covers, authors, editions. Internet Archive project.  
**PokéAPI**|  Unlimited| All Pokémon data. Great for learning how to consume REST APIs.  
**NASA APIs**|  1,000 calls/hour| APOD (Astronomy Picture of the Day), Mars rover photos, Earth imagery.  
  
## Images & Media

API| Free Tier| What You Get  
---|---|---  
**Unsplash API**|  50 requests/hour| High-quality free photos. Attribution required.  
**Pexels API**|  200 requests/hour| Free stock photos and videos. No attribution required.  
**ImgBB**|  Unlimited (32MB limit)| Image upload with auto-generated URLs. Great for quick hosting.  
  
## Dev & Infrastructure

API| Free Tier| What You Get  
---|---|---  
**GitHub API**|  60 requests/hour (unauth)| Repos, issues, users, gists. Use a token for 5,000/hr.  
**ipapi**|  1,000/day (or 45/min)| IP geolocation. City-level accuracy on free tier.  
**ExchangeRate-API**|  1,500/month| Currency conversion rates. Updated daily.  
  
## Fun & Niche

API| Free Tier| What You Get  
---|---|---  
**JokeAPI**|  Unlimited| Programming jokes, dark jokes, puns. Filter by category.  
**Bored API**|  Unlimited| Random activity suggestions. Filter by type and participants.  
**Dog API**|  Unlimited| Random dog pictures by breed. The internet's most important resource.  
  
## API Design Tips

  * **Cache aggressively** — Most free APIs have rate limits. Cache responses so you don't hit them unnecessarily.
  * **Use exponential backoff** — When you get a 429 (rate limited), wait and retry with increasing delays.
  * **Keep keys out of your repo** — Use environment variables. Even for free API keys.
  * **Fallback gracefully** — Free APIs can go down. Your app should still work if the dog picture API is having a bad day.



**See also:** [Best Programming Books 2026: 15 Books Every Developer Should Read](</en/tools/best-programming-books.html>), [Best Headless CMS Platforms 2026: Strapi vs Sanity vs Contentful vs Payload](</en/tools/best-headless-cms-platforms.html>), [Best API Testing Tools 2026: Postman vs Insomnia vs Bruno vs Hurl](</en/tools/best-api-testing-tools.html>)
