# Product Requirement Document (PRD)

## Product: MovieSearchHub
- Requested by: Andy Le
- Creation Date: 03/22/2025
- Written by: ChatGPT

---

## 1. Product Objectives

Create a website capable of:
- Searching movies by various criteria such as: movie title, actors, directors, or movie content.
- Displaying detailed movie information, including: description, genre, release date, cast, director, poster, trailer, user reviews, ratings from various sources (IMDb, Rotten Tomatoes, etc.).
- Automatically collecting (crawling) data from the internet to provide free movie watching links (if available) from public websites that don't require paid subscriptions.

---

## 2. Key Features

### 2.1 Movie Search

**Functionality:**
Users can enter keywords into the search box, and the system will return a list of matching movies.

**Supported Search Criteria:**
- Movie title (e.g., "Inception")
- Actor name (e.g., "Leonardo DiCaprio")
- Director name (e.g., "Christopher Nolan")
- Content/description (e.g., "dream within a dream")

**Suggested Technology:**
Elasticsearch or an advanced search engine for full-text search capabilities, supporting fuzzy search.

---

### 2.2 Displaying Detailed Movie Information

**Functionality:**
The movie detail page will display:
- Movie title
- Poster image
- Trailer (YouTube API)
- Brief description
- Genre
- Release date
- Main cast & director
- Aggregate reviews from major sites (IMDb, Rotten Tomatoes, Metacritic)
- User reviews (if available)
- Average rating

**Data Sources:**
- The Movie Database (TMDB) API
- OMDb API
- IMDb (if feasible via API or through crawling)

---

### 2.3 Automatic Search for Free Movie Links

**Functionality:**
- Automatically crawl data from public movie websites (no paid account required), for example: phimmoi, phim14, moviesub, etc.
- Analyze search results from Google, Bing, etc. based on movie titles.
- Return available links to watch movies, possibly with a "consider the safety of the website" warning.

**Suggested Technology:**
- Use Python with Scrapy or Selenium for crawling.
- Apply content filters (regex, AI models) to identify correct movie links.
- Potentially use Google Custom Search API to get search results from the web.

**Legal Considerations:**
Providing free movie links requires careful legal verification. The website should have a clear disclaimer: only displaying public links from third parties, not storing any movie content.

---

## 3. User Roles

| Role | Description |
|------|-------------|
| Visitor | Can search for movies, view detailed information, click on movie links. |
| Administrator | Moderate crawled data, remove invalid links, manage content. |

---

## 4. Non-functional Requirements
- **Performance**: Fast search response under 1 second.
- **Security**: Do not store any movie content to avoid legal risks.
- **Scalability**: Support expandable crawling over time (adding new websites).
- **UX/UI**: Modern interface, easy to use on mobile and desktop.

---

## 5. Suggested Technologies

| Component | Technology |
|-----------|------------|
| Frontend | ReactJS / Next.js, TailwindCSS |
| Backend | Node.js or Python (FastAPI) |
| Database | PostgreSQL / MongoDB |
| Search Engine | Elasticsearch |
| Crawler | Scrapy, BeautifulSoup, Selenium |
| API Data Sources | TMDB API, OMDb API, Google Custom Search API |
| Hosting | Vercel (frontend), Render / Heroku / AWS (backend + crawler) |

---

## 6. MVP (Minimum Viable Product)
- Search for movies by title.
- Display movie information from TMDB API.
- Crawl and display free movie links from 1-2 websites.

---

## 7. Risks & Solutions

| Risk | Proposed Solution |
|------|-------------------|
| Incorrect data crawling, wrong or fake links | Add moderation system, link evaluation |
| Legal issues when displaying movie links | Display disclaimer, don't store movie content |
| API request limitations | Use caching / purchase paid plans if needed |
| Crawling being blocked (anti-bot) | Use proxies, fake headers, random delays |

---

## 8. KPIs / Success Metrics
- Number of weekly user visits
- Search → movie detail click-through rate
- Click rate on movie links
- Number of movies with successful viewing links (coverage)