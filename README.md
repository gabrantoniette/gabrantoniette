<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
    <img src="assets/banner-light.svg" width="100%" alt="Gabriel Antoniette — Python Developer, Data Engineer, Analytics">
  </picture>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/gabriel-antoniette/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn de Gabriel Antoniette">
  </a>
  <a href="mailto:gabrantoniette@gmail.com">
    <img src="https://img.shields.io/badge/E--mail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Enviar e-mail para Gabriel Antoniette">
  </a>
  <img src="https://img.shields.io/badge/Brasil-UTC%E2%88%923-1F3864?style=for-the-badge" alt="Baseado no Brasil, fuso UTC menos 3">
</p>

---

### Sobre

Trabalho com **Análise e Engenharia de Dados**, com foco em qualidade de dados e BI. Gosto de resolver o problema inteiro: da modelagem e da ingestão até a API que entrega o dado e a tela onde alguém decide algo com ele.

Hoje construo projetos próprios levando essa mesma disciplina — dado validado, API previsível, documentação honesta — para ferramentas do dia a dia. Se você chegou aqui por causa de um deles, fico feliz em conversar.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Gabriel:
    roles: tuple[str, ...] = ("Python Developer", "Data Engineer", "Analytics")
    stack: tuple[str, ...] = ("Python", "SQL", "FastAPI", "Power BI", "Azure", "Databricks")
    education: str = "B.Sc. Data Science — FIAP"
    languages: tuple[str, ...] = ("Português", "English")

    def currently(self) -> str:
        return "construindo e documentando projetos full-stack de dados"

    def open_to(self) -> list[str]:
        return ["colaborações em open source", "conversas sobre dados, APIs e Python"]
```

---

### Como eu trabalho

- **Validação na borda.** Contratos com Pydantic/SQLModel antes de gravar — BI não deveria herdar sujeira de ingestão.
- **Uma camada HTTP só.** Dashboard web e menu de terminal consomem a mesma API; regra de negócio não se duplica.
- **Acessibilidade não é enfeite.** Cor nunca é o único indicador de estado.
- **Documentação que explica decisão.** Um bom README conta *por que*, não só *como instalar*.

---

### Stack

**Linguagens e dados**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/DAX-F2C811?style=flat-square" alt="DAX">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
</p>

**Back-end e APIs**

<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLModel-7E56C2?style=flat-square&logo=python&logoColor=white" alt="SQLModel">
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic">
</p>

**Front-end**

<p>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
</p>

**Cloud e BI**

<p>
  <img src="https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" alt="Microsoft Azure">
  <img src="https://img.shields.io/badge/Databricks-FF3621?style=flat-square&logo=databricks&logoColor=white" alt="Databricks">
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white" alt="Google Cloud">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black" alt="Power BI">
</p>

**Ferramentas**

<p>
  <img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub">
</p>

---

### Projeto em destaque

#### [Halcyon Goods](https://github.com/gabrantoniette/halcyon-goods-product-control) — controle de estoque

<!-- pin:start -->
<p>
  <a href="https://github.com/gabrantoniette/halcyon-goods-product-control">
    <img src="https://img.shields.io/badge/Reposit%C3%B3rio-halcyon--goods--product--control-1F3864?style=flat-square&logo=github&logoColor=white" alt="Repositório halcyon-goods-product-control">
  </a>
  <img src="https://img.shields.io/github/languages/top/gabrantoniette/halcyon-goods-product-control?style=flat-square&color=4A7DBF" alt="Linguagem principal do projeto">
  <img src="https://img.shields.io/github/last-commit/gabrantoniette/halcyon-goods-product-control?style=flat-square&color=4A7DBF" alt="Data do último commit">
</p>
<!-- pin:end -->

Sistema interno de estoque (back-office, sem carrinho ou checkout). Uma API em FastAPI + SQLModel/SQLite serve **dois** clientes — um dashboard web e um menu de terminal — que compartilham a mesma camada HTTP, então nenhuma regra de negócio vive em dois lugares.

<details>
<summary><b>Decisões que valem o clique</b></summary>

<br>

- **Paginação server-side** desde o começo: a tela não decide o que o banco já sabe filtrar.
- **Filtros por status de estoque** derivados no domínio, não no front — o terminal recebe a mesma verdade que o navegador.
- **Temas claro e escuro** com contraste checado, e status sempre com rótulo além da cor.
- **Camada HTTP única**, testável isolada dos dois clientes.

</details>

<p>
  <code>Python</code> <code>FastAPI</code> <code>SQLModel</code> <code>SQLite</code> <code>Pydantic</code> <code>Vanilla JS</code>
</p>

---

### GitHub em números

<!-- cards:start -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=gabrantoniette&theme=github_dark">
    <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=gabrantoniette&theme=default">
    <img height="165" src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=gabrantoniette&theme=default" alt="Resumo de estatísticas do GitHub de gabrantoniette">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=gabrantoniette&theme=github_dark">
    <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=gabrantoniette&theme=default">
    <img height="165" src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=gabrantoniette&theme=default" alt="Linguagens mais usadas por repositório">
  </picture>
</p>
<!-- cards:end -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=gabrantoniette&hide_border=true&background=0D111700&border=30363D&stroke=30363D&ring=4A7DBF&fire=4A7DBF&currStreakLabel=4A7DBF&sideLabels=8B949E&dates=6E7681&currStreakNum=E6EDF3&sideNums=E6EDF3">
    <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com/?user=gabrantoniette&hide_border=true&background=FFFFFF00&border=D0D7DE&stroke=D0D7DE&ring=1F3864&fire=1F3864&currStreakLabel=1F3864&sideLabels=5A6674&dates=8B949E&currStreakNum=12233F&sideNums=12233F">
    <img src="https://streak-stats.demolab.com/?user=gabrantoniette&hide_border=true&background=FFFFFF00&border=D0D7DE&stroke=D0D7DE&ring=1F3864&fire=1F3864&currStreakLabel=1F3864&sideLabels=5A6674&dates=8B949E&currStreakNum=12233F&sideNums=12233F" alt="Sequência de contribuições de gabrantoniette">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=gabrantoniette&bg_color=0D1117&color=E6EDF3&title_color=4A7DBF&line=4A7DBF&point=E6EDF3&area=true&area_color=1F3864&hide_border=true&custom_title=Atividade%20de%20contribui%C3%A7%C3%B5es">
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=gabrantoniette&bg_color=FFFFFF&color=12233F&title_color=1F3864&line=1F3864&point=12233F&area=true&area_color=4A7DBF&hide_border=true&custom_title=Atividade%20de%20contribui%C3%A7%C3%B5es">
    <img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=gabrantoniette&bg_color=FFFFFF&color=12233F&title_color=1F3864&line=1F3864&point=12233F&area=true&area_color=4A7DBF&hide_border=true&custom_title=Atividade%20de%20contribui%C3%A7%C3%B5es" alt="Gráfico de atividade de contribuições dos últimos meses">
  </picture>
</p>

---

### Vamos conversar

Se você trabalha com dados, Python ou APIs — ou só quer trocar uma ideia sobre algum projeto daqui — a caixa de entrada está aberta.

<p>
  <a href="https://www.linkedin.com/in/gabriel-antoniette/">
    <img src="https://img.shields.io/badge/Chamar%20no%20LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Chamar Gabriel no LinkedIn">
  </a>
  <a href="mailto:gabrantoniette@gmail.com">
    <img src="https://img.shields.io/badge/Mandar%20um%20e--mail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Mandar um e-mail para Gabriel">
  </a>
</p>

<sub>Os cartões de estatísticas são servidos por projetos open source de terceiros. Para hospedar os seus, veja <a href="docs/self-host-stats.md">docs/self-host-stats.md</a>.</sub>
