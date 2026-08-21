# Hospedar seus próprios cartões de estatísticas

## Por que

Os cartões deste README dependem de instâncias públicas e gratuitas mantidas por terceiros. Elas caem. Em agosto de 2026 aconteceram duas quedas ao mesmo tempo:

| Serviço | O que aconteceu |
| --- | --- |
| `github-readme-stats.vercel.app` | Responde `503 DEPLOYMENT_PAUSED` — a instância pública oficial foi pausada na Vercel. |
| `github-readme-streak-stats.herokuapp.com` | Sem resposta — a Heroku encerrou os dynos gratuitos e o projeto mudou de host (hoje é `streak-stats.demolab.com`). |

Enquanto isso, o README usa `github-profile-summary-cards`, `streak-stats.demolab.com` e `github-readme-activity-graph`, que estão no ar. Todos continuam sendo instâncias compartilhadas de terceiros — o mesmo risco, só que adiado.

Rodando a sua própria instância do [github-readme-stats](https://github.com/anuraghazra/github-readme-stats), o único jeito de ela cair é você derrubar. De quebra, você recupera três cartões melhores que os substitutos atuais: o card de stats oficial, o de top languages e o *pin* de repositório.

## Passo a passo

Leva ~10 minutos e é tudo gratuito.

### 1. Faça o fork

```bash
gh repo fork anuraghazra/github-readme-stats --clone=false
```

(Ou pelo botão **Fork** em github.com/anuraghazra/github-readme-stats.)

### 2. Gere um token do GitHub

Em **Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)**:

- **Note:** `readme-stats`
- **Expiration:** sem expiração, ou anote na agenda para renovar
- **Scopes:** **nenhum**. Não marque nada — o token só precisa ler dados públicos, e um token sem escopo é o mais seguro que existe. Marque `repo` apenas se quiser contar commits de repositórios privados.

Copie o token. Ele só aparece uma vez.

### 3. Suba na Vercel

1. Entre em [vercel.com](https://vercel.com) com a conta do GitHub.
2. **Add New → Project → Import** o seu fork `github-readme-stats`.
3. Antes de clicar em Deploy, abra **Environment Variables** e adicione:
   - **Name:** `PAT_1`
   - **Value:** o token do passo 2
4. **Deploy**.

Ao final você tem um domínio parecido com `https://github-readme-stats-seunome.vercel.app`.

> O nome da variável é `PAT_1` mesmo, com underline e o número. Sem ela o cartão renderiza um SVG escrito *"Maximum retries exceeded"* em vez das estatísticas — é assim que dá para saber que o token não chegou.

### 4. Aponte o README para a sua instância

```bash
python scripts/use-self-hosted-stats.py github-readme-stats-seunome.vercel.app
```

O script troca os blocos entre `<!-- cards:start -->` / `<!-- cards:end -->` e `<!-- pin:start -->` / `<!-- pin:end -->` pelos cartões da sua instância, já com as cores da identidade do perfil (`#1F3864` / `#4A7DBF`) e com `<picture>` para tema claro e escuro. Ele salva `README.bak.md` antes de mexer.

Confira o resultado e commite:

```bash
git diff README.md
git add README.md && git commit -m "stats: aponta cartoes para instancia propria"
```

### 5. Verifique

```bash
python scripts/check-readme-links.py
```

Percorre todas as imagens do README e falha se alguma responder fora de 200 ou devolver um SVG de erro. Vale rodar de vez em quando — é exatamente esse check que teria pego as duas quedas acima no dia em que aconteceram.

## Voltar atrás

`README.bak.md` guarda a versão anterior. Para desfazer sem o backup, `git checkout README.md`.

## Manutenção

- **Token expirado** derruba os cartões da mesma forma que um serviço fora do ar. Se você escolheu expiração, coloque um lembrete.
- **O fork não precisa ser atualizado** para os cartões funcionarem. Sincronize com o upstream só se quiser temas ou parâmetros novos.
- A Vercel hiberna projetos gratuitos sem tráfego; a primeira requisição depois de um tempo parado pode demorar alguns segundos. Isso é lentidão, não queda.
