<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img src="assets/banner-light.svg" width="100%" alt="Gabriel Antoniette — Python Developer, Data Engineer, Analytics">
  </picture>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/gabriel-antoniette/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Gabriel Antoniette on LinkedIn">
  </a>
  <a href="mailto:gabrantoniette@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email Gabriel Antoniette">
  </a>
  <img src="https://img.shields.io/badge/Brazil-UTC%E2%88%923-1F3864?style=for-the-badge" alt="Based in Brazil">
</p>

---

### About

I work in **data analysis and data engineering**, focused on data quality and BI. I like owning the whole problem: from modeling and ingestion, through the report that serves the data, to the screen where someone actually decides something with it.

These days I build my own projects carrying that same discipline: developing systems into everyday tools. If one of them brought you here, I'd be glad to here that!

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Gabriel:
    roles: tuple[str, ...] = ("Python Developer", "Data Engineer", "Analytics")
    stack: tuple[str, ...] = ("Python", "SQL", "FastAPI", "Power BI", "Azure", "Databricks")
    education: str = "B.Sc. Data Science — FIAP"
    languages: tuple[str, ...] = ("Portuguese", "English")

    def currently(self) -> str:
        return "building and documenting full-stack data projects"

    def open_to(self) -> list[str]:
        return ["companies collaboration", "systems developments"]
```


### Stack

**Languages and data**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/DAX-F2C811?style=flat-square" alt="DAX">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
</p>

**Backend and APIs**

<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLModel-7E56C2?style=flat-square&logo=python&logoColor=white" alt="SQLModel">
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic">
</p>

**Frontend**

<p>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
</p>

**Cloud and BI**

<p>
  <img src="https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" alt="Microsoft Azure">
  <img src="https://img.shields.io/badge/Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white" alt="Databricks">
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white" alt="Google Cloud">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black" alt="Power BI">
</p>

**Tools**

<p>
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub">
</p>

---

### Featured project

#### [Halcyon Goods](https://github.com/gabrantoniette/halcyon-goods-product-control) — inventory control

<!-- pin:start -->
<p>
  <a href="https://github.com/gabrantoniette/halcyon-goods-product-control">
    <img src="https://img.shields.io/badge/Repository-halcyon--goods--product--control-1F3864?style=flat-square&logo=github&logoColor=white" alt="halcyon-goods-product-control repository">
  </a>
  <img src="https://img.shields.io/github/languages/top/gabrantoniette/halcyon-goods-product-control?style=flat-square&color=4A7DBF" alt="Primary language of the project">
  <img src="https://img.shields.io/github/last-commit/gabrantoniette/halcyon-goods-product-control?style=flat-square&color=4A7DBF" alt="Date of the last commit">
</p>
<!-- pin:end -->

An internal inventory system (back-office — no cart, no checkout). A FastAPI + SQLModel/SQLite API serves **two** clients — a web dashboard and a terminal menu — sharing the same HTTP layer, so no business rule lives in two places.

<details>
<summary><b>Decisions worth the click</b></summary>

<br>

- **Server-side pagination** from day one: the screen doesn't decide what the database already knows how to filter.
- **Stock status filters** derived in the domain, not in the frontend — the terminal gets the same truth as the browser.
- **Light and dark themes** with checked contrast, and status always carries a label beyond color.
- **A single HTTP layer**, testable in isolation from both clients.

</details>

<p>
  <code>Python</code> <code>FastAPI</code> <code>SQLModel</code> <code>SQLite</code> <code>Pydantic</code> <code>Vanilla JS</code>
</p>

---

### GitHub at a glance

<!-- cards:start -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=gabrantoniette&theme=github_dark">
    <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=gabrantoniette&theme=default">
    <img height="165" src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=gabrantoniette&theme=default" alt="GitHub stats summary for gabrantoniette">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=gabrantoniette&theme=github_dark">
    <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=gabrantoniette&theme=default">
    <img height="165" src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=gabrantoniette&theme=default" alt="Most used languages by repository">
  </picture>
</p>
<!-- cards:end -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=gabrantoniette&hide_border=true&background=0D111700&border=30363D&stroke=30363D&ring=4A7DBF&fire=4A7DBF&currStreakLabel=4A7DBF&sideLabels=8B949E&dates=6E7681&currStreakNum=E6EDF3&sideNums=E6EDF3">
    <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com/?user=gabrantoniette&hide_border=true&background=FFFFFF00&border=D0D7DE&stroke=D0D7DE&ring=1F3864&fire=1F3864&currStreakLabel=1F3864&sideLabels=5A6674&dates=8B949E&currStreakNum=12233F&sideNums=12233F">
    <img src="https://streak-stats.demolab.com/?user=gabrantoniette&hide_border=true&background=FFFFFF00&border=D0D7DE&stroke=D0D7DE&ring=1F3864&fire=1F3864&currStreakLabel=1F3864&sideLabels=5A6674&dates=8B949E&currStreakNum=12233F&sideNums=12233F" alt="Contribution streak for gabrantoniette">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=gabrantoniette&bg_color=0D1117&color=E6EDF3&title_color=4A7DBF&line=4A7DBF&point=E6EDF3&area=true&area_color=1F3864&hide_border=true&custom_title=Contribution%20activity">
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=gabrantoniette&bg_color=FFFFFF&color=12233F&title_color=1F3864&line=1F3864&point=12233F&area=true&area_color=4A7DBF&hide_border=true&custom_title=Contribution%20activity">
    <img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=gabrantoniette&bg_color=FFFFFF&color=12233F&title_color=1F3864&line=1F3864&point=12233F&area=true&area_color=4A7DBF&hide_border=true&custom_title=Contribution%20activity" alt="Contribution activity graph over the last months">
  </picture>
</p>

---

### Let's talk

If you work with data, Python or APIs — or just want to trade ideas about one of the projects here — the inbox is open.

<p>
  <a href="https://www.linkedin.com/in/gabriel-antoniette/">
    <img src="https://img.shields.io/badge/Message%20on%20LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Message Gabriel on LinkedIn">
  </a>
  <a href="mailto:gabrantoniette@gmail.com">
    <img src="https://img.shields.io/badge/Send%20an%20email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Send Gabriel an email">
  </a>
</p>

<sub>Stats cards are served by third-party open source projects. To host your own, see <a href="docs/self-host-stats.md">docs/self-host-stats.md</a>.</sub>
