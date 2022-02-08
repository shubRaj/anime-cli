from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import webbrowser
from utils.anime import getSources, search, getEpisode, getAnimeInfo
console = Console()
def main():
    query = Prompt.ask("Search Anime")
    with console.status(f"[bold green]Searching for {query}...") as status:
        if True:
            searchResults = search(query)
            console.print(f"{len(searchResults)} results found")
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("SN", style="bold cyan")
    table.add_column("Anime", style="blue")
    for i, searchResult in enumerate(searchResults, start=1):
        table.add_row(str(i), searchResult.title)
    console.print(table)
    selectedAnime = Prompt.ask(f"Select Anime[1-{len(searchResults)}]")
    selectedAnime = int(selectedAnime)
    if not (selectedAnime in range(1, len(searchResults)+1)):
        raise Exception("Invalid Input")
    anime = searchResults[selectedAnime-1]
    animeInfo = getAnimeInfo(anime.url)
    selectedEpisode = Prompt.ask(f"Select Episode[1-{animeInfo.episodes}]")
    selectedEpisode = int(selectedEpisode)
    if not (selectedEpisode in range(1, int(animeInfo.episodes)+1)):
        raise Exception("Invalid Input")
    episode = getEpisode(animeInfo.animeID, selectedEpisode)
    sources = getSources(episode.url).get("source")
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("SN", style="bold cyan")
    table.add_column("Quality", style="blue")
    for i, source in enumerate(sources, start=1):
        table.add_row(str(i), source.get("label").split()[0])
    console.print(table)
    selectedQuality = Prompt.ask(f"Select Quality[1-{len(sources)}]")
    selectedQuality = int(selectedQuality)
    if not (selectedQuality in range(1,len(sources)+1)):
        raise Exception("Invalid Input")
    webbrowser.open(f'{sources[selectedQuality-1].get("file")}')
if __name__ == "__main__":
    main()
