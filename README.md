# Scribe

**Scribe** est un outil en ligne de commande qui transforme un enregistrement audio
(réunion, cours, note vocale) en un compte rendu écrit et structuré.

Le fonctionnement tient en trois temps :

1. L'utilisateur fournit un fichier audio.
2. Un modèle de transcription (Speech-to-Text) convertit l'audio en texte brut.
3. Un LLM reformule ce texte en compte rendu propre : titre, résumé, points clés,
   décisions et actions.

Les deux modèles sont appelés via l'API serverless de [Groq](https://console.groq.com).
Aucun modèle n'est entraîné : Scribe intègre des briques intelligentes existantes.

---

## Prérequis

- [pyenv](https://github.com/pyenv/pyenv) (gestion de la version de Python)
- [Poetry](https://python-poetry.org/) (gestion des dépendances)
- Une clé API Groq (gratuite sur [console.groq.com](https://console.groq.com))

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/TchappiR/scribe.git
cd scribe

# 2. Installer les dépendances (Poetry crée le virtualenv et lit poetry.lock)
poetry install

# 3. Configurer la clé API
cp .env.example .env
# puis éditer .env et renseigner GROQ_API_KEY=gsk_...
```

## Utilisation

```bash
poetry run python -m source.cli samples/demo.m4a
```

Le compte rendu s'affiche à l'écran et est enregistré dans un fichier Markdown daté,
dans le dossier `output/`.

---

## Structure du projet

```
scribe/
├── source/              # code source (package Python)
│   ├── config.py        # clé API + noms des modèles, centralisés
│   ├── transcription.py # audio -> texte (STT Groq)
│   ├── summary.py       # texte -> compte rendu structuré (LLM Groq)
│   └── cli.py           # point d'entrée en ligne de commande
├── prompts/             # prompts système (éditables sans toucher au code)
│   └── summary.txt
├── samples/             # fichiers audio d'exemple
├── output/              # comptes rendus générés (ignoré par Git)
├── pyproject.toml       # dépendances déclarées
├── poetry.lock          # versions verrouillées (installation reproductible)
└── .env.example         # variables d'environnement attendues
```

## Choix techniques

**Gestion des dépendances — Poetry plutôt que `requirements.txt`.**
Poetry sépare les dépendances déclarées (`pyproject.toml`) des versions exactes
verrouillées (`poetry.lock`). Le `lock` garantit qu'une réinstallation produit un
environnement identique au bit près, ce qu'un `requirements.txt` sans versions figées
ne garantit pas.

**Modèles (Q2).** Vérifier les identifiants à jour sur
[console.groq.com/docs/models](https://console.groq.com/docs/models).

- STT : `whisper-large-v3-turbo` — très rapide et peu coûteux, précision suffisante
  pour transcrire une réunion.
- LLM : `llama-3.3-70b-versatile` — bon compromis qualité / vitesse / coût pour
  reformuler un texte en compte rendu structuré.

Les noms de modèles sont définis à un **seul endroit** (`source/config.py`).

---

## Workflow Git

Le projet suit un workflow inspiré de GitHub Flow, avec une branche d'intégration :

- `main` : version stable et démontrable. Jamais de commit direct ; ne reçoit que des
  merges depuis `dev` via pull request, aux jalons, avec un tag de version.
- `dev` : branche d'intégration, état courant du travail.
- `feature/…` : une branche par fonctionnalité, créée depuis `dev`, intégrée par pull
  request relue, puis supprimée.

---

## Questions de réflexion

**Q1 — Pourquoi le `.gitignore` doit-il exister avant d'écrire du code manipulant des
secrets ?**
Parce que Git conserve tout l'historique. Une clé committée une seule fois reste
récupérable dans les commits passés, même après suppression du fichier. Le `.gitignore`
doit donc empêcher le suivi du `.env` *avant* que ce fichier existe : on ferme la porte
avant de faire entrer le secret.

**Q2 — Quels modèles STT et LLM propose Groq, et lesquels choisir ?**
Voir la section « Choix techniques » : `whisper-large-v3-turbo` (STT) et
`llama-3.3-70b-versatile` (LLM), retenus pour leur équilibre qualité / vitesse / coût.

**Q3 — Que renvoie l'API de transcription en plus du texte ?**
Avec `response_format="verbose_json"`, l'API renvoie aussi la langue détectée, la durée,
et des segments horodatés. Ces horodatages permettraient une évolution future de Scribe :
naviguer dans l'audio, sous-titrer, ou citer le passage source d'un point clé.

**Q4 — Quelle température pour la génération du compte rendu ?**
Une température basse (~0.2). On veut un résumé fidèle et déterministe, pas de la
créativité : le LLM ne doit pas broder ni inventer de décisions absentes de l'audio.

**Q5 — Le prompt système est envoyé à chaque requête : quel lien avec les tokens en
cache ?**
Le prompt système est identique d'un appel à l'autre. Les providers mettent en cache
ce préfixe commun : les requêtes suivantes réutilisent les tokens déjà traités, ce qui
réduit la latence et le coût par rapport à un recalcul complet à chaque fois.