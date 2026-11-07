<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img src="assets/banner-light.svg" width="100%" alt="Gabriel Antoniette. Python, LLM agents, API">
  </picture>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=500&size=21&pause=1200&color=4A7DBF&center=true&vCenter=true&width=620&height=40&lines=Data+engineer+moving+into+AI+engineering;Postgrad+in+Software+Engineering+with+Applied+AI;Everything+I+learn+gets+shipped+in+public" alt="Data engineer moving into AI engineering. Postgrad in Software Engineering with Applied AI. Everything I learn gets shipped in public.">
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/gabriel-antoniette/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Gabriel Antoniette on LinkedIn">
  </a>
  <a href="mailto:gabrantoniette@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email Gabriel Antoniette">
  </a>
  <img src="https://img.shields.io/badge/Based%20in-Brazil-FFDF00?style=for-the-badge&labelColor=009C3B" alt="Based in Brazil">
  <img src="https://img.shields.io/badge/Open_to-AI_Engineering_roles-4A7DBF?style=for-the-badge" alt="Open to AI engineering roles">
</p>

---

### About

Short version: I spent three years making sure data was right before anyone made a decision with it. Now I'm doing the same thing one layer up, for models.

My current job is called Data Quality Analyst. What I actually do is find where a model gets things wrong: which field it misreads, which entities it misclassifies, how much of that would reach production if nobody checked. Around 20,000 transaction batches a week.

I don't have professional experience as an AI engineer yet. What I do have is three years of production data work, plus the systems I'm building on my own time to close the gap: RAG, multi-agent orchestration, API development.

Everything I build ends up here, working.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Gabriel:
    now: str = "Data Quality Analyst, model evaluation in practice"
    heading: str = "AI Engineering"
    stack: tuple[str, ...] = ("Python", "FastAPI", "PostgreSQL", "Docker", "LLM agents")
    background: tuple[str, ...] = ("3 years as Data Analyst and Engineer", "Data Transformation", "Reports", "BI")
    education: tuple[str, ...] = (
        "Technologist Degree (2-year undergraduate): Data Science, FIAP",
        "Postgraduate, in progress: Software Engineering with Applied AI, UNIPDS",
    )
    languages: tuple[str, ...] = ("Portuguese (native)", "English (full professional proficiency)")

    def open_to(self) -> list[str]:
        return ["AI engineering roles"]
```

---

### Stack

<!-- stack:start -->
**AI and Python**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Agno-1F3864?style=flat-square&logo=python&logoColor=white" alt="Agno">
  <img src="https://img.shields.io/badge/Anthropic_API-D97757?style=flat-square&logo=anthropic&logoColor=white" alt="Anthropic API">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest">
</p>

**Backend and data**

<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLModel-7E56C2?style=flat-square&logo=python&logoColor=white" alt="SQLModel">
  <img src="https://img.shields.io/badge/Alembic-6BA81E?style=flat-square&logo=python&logoColor=white" alt="Alembic">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/Fastify-000000?style=flat-square&logo=fastify&logoColor=white" alt="Fastify">
  <img src="https://img.shields.io/badge/Neo4j-4581C3?style=flat-square&logo=neo4j&logoColor=white" alt="Neo4j">
</p>

**Infrastructure**

<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" alt="Grafana">
</p>

**Frontend, when the project needs one**

<p>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/CSS-663399?style=flat-square&logo=css&logoColor=white" alt="CSS">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5">
</p>

**From the data years**

<p>
  <img src="https://img.shields.io/badge/Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white" alt="Databricks">
  <img src="https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" alt="Microsoft Azure">
  <img src="https://img.shields.io/badge/PySpark-E25A1C?style=flat-square&logo=apachespark&logoColor=white" alt="PySpark">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black" alt="Power BI">
</p>

**Recently picked up**

<p>
  <img src="https://img.shields.io/badge/OpenRouter-94A3B8?style=flat-square&logo=openrouter&logoColor=white" alt="OpenRouter">
</p>
<!-- stack:end -->

---

### What I'm building

<!-- projects:start -->
#### [LLMs-APIs-integrations](https://github.com/gabrantoniette/LLMs-APIs-integrations)

<p>
  <a href="https://github.com/gabrantoniette/LLMs-APIs-integrations">
    <img src="https://img.shields.io/badge/Repository-LLMs--APIs--integrations-1F3864?style=flat-square&logo=github&logoColor=white" alt="LLMs-APIs-integrations repository">
  </a>
  <img src="https://img.shields.io/github/last-commit/gabrantoniette/LLMs-APIs-integrations?style=flat-square&color=4A7DBF" alt="Date of the last commit">
</p>

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/generated/languages/LLMs-APIs-integrations-dark.svg">
    <img src="assets/generated/languages/LLMs-APIs-integrations-light.svg" alt="Languages in LLMs-APIs-integrations, by share of code">
  </picture>
</p>

Fastify gateway that routes LLM chat requests through OpenRouter with model fallback and price/latency/throughput sorting

<p>
  <code>Fastify</code> <code>Node.js</code> <code>OpenRouter</code> <code>TypeScript</code>
</p>

<br>

#### [rag-implementation](https://github.com/gabrantoniette/rag-implementation)

<p>
  <a href="https://github.com/gabrantoniette/rag-implementation">
    <img src="https://img.shields.io/badge/Repository-rag--implementation-1F3864?style=flat-square&logo=github&logoColor=white" alt="rag-implementation repository">
  </a>
  <img src="https://img.shields.io/github/last-commit/gabrantoniette/rag-implementation?style=flat-square&color=4A7DBF" alt="Date of the last commit">
</p>

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/generated/languages/rag-implementation-dark.svg">
    <img src="assets/generated/languages/rag-implementation-light.svg" alt="Languages in rag-implementation, by share of code">
  </picture>
</p>

Zero-cost, reusable GraphRAG in TypeScript: Neo4j vector + graph retrieval, free OpenRouter models, and locally verified citations with an evidence gate.

<p>
  <code>Grafana</code> <code>Neo4j</code> <code>OpenRouter</code> <code>TensorFlow</code> <code>TypeScript</code>
</p>

<br>

#### [ai-web](https://github.com/gabrantoniette/ai-web)

<p>
  <a href="https://github.com/gabrantoniette/ai-web">
    <img src="https://img.shields.io/badge/Repository-ai--web-1F3864?style=flat-square&logo=github&logoColor=white" alt="ai-web repository">
  </a>
  <img src="https://img.shields.io/github/last-commit/gabrantoniette/ai-web?style=flat-square&color=4A7DBF" alt="Date of the last commit">
</p>

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/generated/languages/ai-web-dark.svg">
    <img src="assets/generated/languages/ai-web-light.svg" alt="Languages in ai-web, by share of code">
  </picture>
</p>

On-device AI demos running 100% in the browser with Chrome's Built-in AI APIs (Gemini Nano): Prompt API, Translator and Language Detector.

<p>
  <code>JavaScript</code>
</p>
<!-- projects:end -->

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
    <source media="(prefers-color-scheme: dark)" srcset="assets/generated/languages-by-repo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/generated/languages-by-repo-light.svg">
    <img height="165" src="assets/generated/languages-by-repo-light.svg" alt="The three most used languages across my public repositories, each repository weighted equally">
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
    <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=gabrantoniette&theme=github_dark">
    <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=gabrantoniette&theme=default">
    <img width="100%" src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=gabrantoniette&theme=default" alt="Profile summary for gabrantoniette: commits, stars and contributions">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/generated/languages-by-commit-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/generated/languages-by-commit-light.svg">
    <img height="165" src="assets/generated/languages-by-commit-light.svg" alt="The three most used languages across my public repositories, weighted by my commits to each">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=gabrantoniette&theme=github_dark">
    <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=gabrantoniette&theme=default">
    <img height="165" src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=gabrantoniette&theme=default" alt="Time of day when most commits happen">
  </picture>
</p>

<p align="center">
  <sub>Some of my work lives in private repositories, so these charts tell part of the story, not all of it.</sub>
</p>

---

### Let's talk

If you hire for applied AI, or you build in this space and want to argue about something on this page, the inbox is open.

<p>
  <a href="https://www.linkedin.com/in/gabriel-antoniette/">
    <img src="https://img.shields.io/badge/Message%20on%20LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Message Gabriel on LinkedIn">
  </a>
  <a href="mailto:gabrantoniette@gmail.com">
    <img src="https://img.shields.io/badge/Send%20an%20email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Send Gabriel an email">
  </a>
</p>

<sub>The language charts and the project language bars are drawn by this repository from my public repositories. The other stats cards are served by third-party open source projects. To host your own, see <a href="docs/self-host-stats.md">docs/self-host-stats.md</a>.</sub>
