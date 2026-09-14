from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "migration"
CONFIG = json.loads((MIG / "repositorios.json").read_text(encoding="utf-8"))
OUT = MIG / "generated"

PAGES_WORKFLOW = """name: Publicar GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v4
        with:
          path: .
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
"""


def build_manifest(repo):
    item = dict(repo["item"])
    item["url"] = repo["target_url"]
    return {"brand": "Te Equipamos", "items": [item]}


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    created = []
    for repo in CONFIG["repositories"]:
        source = ROOT / repo["source_path"]
        if not source.exists():
            raise SystemExit(f"Falta la fuente: {source}")

        dest = OUT / repo["name"]
        (dest / ".github" / "workflows").mkdir(parents=True)
        shutil.copy2(source, dest / "index.html")
        (dest / ".nojekyll").write_text("", encoding="utf-8")
        (dest / ".github" / "workflows" / "pages.yml").write_text(PAGES_WORKFLOW, encoding="utf-8")

        if repo.get("hub"):
            (dest / "te-equipamos.json").write_text(
                json.dumps(build_manifest(repo), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        title = repo.get("title") or repo.get("item", {}).get("title") or repo["name"]
        readme = (
            f"# {title}\n\n"
            f"Proyecto independiente de Te Equipamos.\n\n"
            f"Página prevista: {repo['target_url']}\n"
        )
        (dest / "README.md").write_text(readme, encoding="utf-8")
        created.append(repo["name"])

    print(f"Paquetes preparados: {len(created)}")
    for name in created:
        print(f" - {name}")


if __name__ == "__main__":
    main()
