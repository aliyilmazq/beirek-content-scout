"""
BEIREK Content Scout - UI Module
================================

Terminal user interface using Rich library.

Features:
- Beautiful menus and tables
- Progress bars
- Article selection
- Statistics display
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.markdown import Markdown
from rich.text import Text
from rich import box
from typing import List, Dict, Optional


class TerminalUI:
    """
    Terminal user interface for BEIREK Content Scout.
    """

    def __init__(self):
        self.console = Console()
        self.cli_available = True  # Will be set by main.py

    def show_banner(self):
        """Display application banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    ██████╗ ███████╗██╗██████╗ ███████╗██╗  ██╗               ║
║    ██╔══██╗██╔════╝██║██╔══██╗██╔════╝██║ ██╔╝               ║
║    ██████╔╝█████╗  ██║██████╔╝█████╗  █████╔╝                ║
║    ██╔══██╗██╔══╝  ██║██╔══██╗██╔══╝  ██╔═██╗                ║
║    ██████╔╝███████╗██║██║  ██║███████╗██║  ██╗               ║
║    ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝               ║
║                                                               ║
║              C O N T E N T   S C O U T   v1.0                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold blue")

    def show_main_menu(self, cli_available: bool = None) -> str:
        """
        Display main menu and get selection.

        Args:
            cli_available: Whether Claude CLI is available (uses self.cli_available if None)

        Returns:
            Selected menu option
        """
        if cli_available is None:
            cli_available = self.cli_available

        # Define menu items with CLI dependency flags
        if cli_available:
            menu_content = """
[bold cyan]Ana Menu[/bold cyan]

  [1] Tara ve Cercevele
  [2] Onerileri Gozden Gecir (Kabul/Red)
  [3] Klasor Olustur (Kabul Edilenler)
  [4] Icerik Uret (Hazir Olanlar)
  [5] Gunluk Kavram
  [6] Istek Havuzu
  [7] Is Akisi Durumu
  [8] Istatistikler
  [9] Ayarlar
  [0] Cikis
"""
            valid_choices = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        else:
            menu_content = """
[bold cyan]Ana Menu[/bold cyan]

  [1] Tara (sadece tarama) [dim][CLI YOK - filtreleme devre disi][/dim]
  [dim][2] Onerileri Gozden Gecir [CLI YOK][/dim]
  [dim][3] Klasor Olustur [CLI YOK][/dim]
  [dim][4] Icerik Uret [CLI YOK][/dim]
  [dim][5] Gunluk Kavram [CLI YOK][/dim]
  [dim][6] Istek Havuzu [CLI YOK][/dim]
  [7] Is Akisi Durumu
  [8] Istatistikler
  [9] Ayarlar
  [0] Cikis

[bold yellow]Uyari:[/bold yellow] Claude CLI bulunamadi!
   Filtreleme ve icerik uretimi icin Claude CLI gereklidir.
   Kurulum: https://claude.ai/cli
"""
            valid_choices = ['0', '1', '7', '8', '9']

        menu = Panel(
            menu_content,
            title="BEIREK Content Scout",
            border_style="blue" if cli_available else "yellow",
            box=box.DOUBLE
        )

        self.console.print(menu)
        choice = Prompt.ask("\n[bold]Seciminiz[/bold]", choices=valid_choices)

        return choice

    def show_scan_progress(self, total_sources: int):
        """
        Show scanning progress.

        Returns:
            Progress context manager
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            console=self.console
        )

    def show_article_table(self, articles: List[Dict], show_selection: bool = True) -> List[int]:
        """
        Display articles in a table and get selection.

        Args:
            articles: List of article dicts
            show_selection: Whether to show selection prompt

        Returns:
            List of selected article IDs
        """
        if not articles:
            self.console.print("[yellow]Gösterilecek makale yok.[/yellow]")
            return []

        table = Table(
            title="Filtrelenmiş Makaleler",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("#", style="dim", width=4)
        table.add_column("Başlık", width=50)
        table.add_column("Skor", justify="center", width=6)
        table.add_column("Kaynak", width=20)
        table.add_column("BEIREK Alanı", width=15)

        for i, article in enumerate(articles, 1):
            score = article.get('relevance_score', 0)
            score_style = "green" if score >= 8 else "yellow" if score >= 6 else "red"

            table.add_row(
                str(i),
                article.get('title', '')[:48] + ('...' if len(article.get('title', '')) > 48 else ''),
                f"[{score_style}]{score:.0f}/10[/{score_style}]",
                article.get('source_name', 'N/A')[:18],
                article.get('beirek_area', '')[:13]
            )

        self.console.print(table)

        if not show_selection:
            return []

        # Get selection
        self.console.print("\n[dim]Seçim için numara girin (örn: 1,3,5 veya 'all' hepsi için, 'q' iptal)[/dim]")
        selection = Prompt.ask("[bold]Seçiminiz[/bold]")

        if selection.lower() == 'q':
            return []
        elif selection.lower() == 'all':
            return [a.get('id') for a in articles if a.get('id')]
        else:
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                return [articles[i-1].get('id') for i in indices if 0 < i <= len(articles)]
            except (ValueError, IndexError):
                self.console.print("[red]Geçersiz seçim![/red]")
                return []

    def show_article_detail(self, article: Dict):
        """Display article details in a panel."""
        content = f"""
[bold]Başlık:[/bold] {article.get('title', 'N/A')}

[bold]Kaynak:[/bold] {article.get('source_name', 'N/A')}
[bold]URL:[/bold] {article.get('url', 'N/A')}

[bold]Relevance Skor:[/bold] {article.get('relevance_score', 0):.1f}/10
[bold]BEIREK Alanı:[/bold] {article.get('beirek_area', 'N/A')}

[bold]Özet:[/bold]
{article.get('summary', 'Özet yok.')[:500]}
"""

        panel = Panel(
            content,
            title=f"Makale #{article.get('id', '?')}",
            border_style="cyan"
        )
        self.console.print(panel)

    def show_generation_options(self) -> List[str]:
        """
        Show format selection for generation.

        Returns:
            List of selected formats
        """
        self.console.print("\n[bold cyan]Hangi formatlar üretilsin?[/bold cyan]\n")
        self.console.print("  [1] 📝 Sadece Makale")
        self.console.print("  [2] 💼 Sadece LinkedIn")
        self.console.print("  [3] 🐦 Sadece Twitter")
        self.console.print("  [4] 📝💼🐦 Hepsi [dim](Önerilen)[/dim]")

        choice = Prompt.ask("\n[bold]Seçiminiz[/bold]", choices=['1', '2', '3', '4'], default='4')

        format_map = {
            '1': ['article'],
            '2': ['linkedin'],
            '3': ['twitter'],
            '4': ['article', 'linkedin', 'twitter']
        }

        return format_map.get(choice, ['article', 'linkedin', 'twitter'])

    def show_generation_progress(self, article_title: str, current_format: str = None):
        """Show content generation progress."""
        status = {
            'article': '[ ]',
            'linkedin': '[ ]',
            'twitter': '[ ]'
        }

        if current_format:
            for fmt in ['article', 'linkedin', 'twitter']:
                if fmt == current_format:
                    status[fmt] = '[◐]'
                    break
                status[fmt] = '[✓]'

        self.console.print(f"\n[bold]Üretiliyor:[/bold] {article_title[:50]}...")
        self.console.print(f"  {status['article']} Makale")
        self.console.print(f"  {status['linkedin']} LinkedIn")
        self.console.print(f"  {status['twitter']} Twitter")

    def show_summary(self, stats: Dict):
        """Display operation summary."""
        content = ""

        for key, value in stats.items():
            if isinstance(value, dict):
                continue
            label = key.replace('_', ' ').title()
            content += f"[bold]{label}:[/bold] {value}\n"

        panel = Panel(
            content,
            title="İşlem Özeti",
            border_style="green",
            box=box.ROUNDED
        )
        self.console.print(panel)

    def show_statistics(self, stats: Dict):
        """Display application statistics."""
        table = Table(
            title="İstatistikler",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("Metrik", style="bold")
        table.add_column("Değer", justify="right")

        stat_labels = {
            'total_sources': 'Toplam Kaynak',
            'total_articles': 'Toplam Makale',
            'relevant_articles': 'Ilgili Makale',
            'processed_articles': 'Islenmis Makale',
            'pending_articles': 'Bekleyen Makale',
            'pending_proposals': 'Bekleyen Oneri',
            'accepted_proposals': 'Kabul Edilen Oneri',
            'ready_for_generation': 'Uretim Icin Hazir',
            'total_content': 'Uretilen Icerik',
            'today_content': 'Bugunku Icerik',
            'total_concepts': 'Kullanilan Kavram',
            'pending_requests': 'Bekleyen Istek',
            'today_scans': 'Bugunku Tarama'
        }

        for key, label in stat_labels.items():
            value = stats.get(key, 0)
            table.add_row(label, str(value))

        self.console.print(table)

    def show_concept_info(self, concept: Dict):
        """Display daily concept information."""
        content = f"""
[bold cyan]Günün Kavramı[/bold cyan]

[bold]İngilizce:[/bold] {concept.get('concept_en', 'N/A')}
[bold]Türkçe:[/bold] {concept.get('concept_tr', 'N/A')}

[bold]BEIREK Alanı:[/bold] {concept.get('beirek_area', 'N/A')}
[bold]Seçim Nedeni:[/bold] {concept.get('selection_reason', 'N/A')}
"""

        panel = Panel(
            content,
            title="Günlük Kavram",
            border_style="magenta"
        )
        self.console.print(panel)

    def show_request_list(self, requests: List[Dict]):
        """Display request pool list."""
        if not requests:
            self.console.print("[yellow]Bekleyen istek yok.[/yellow]")
            return

        table = Table(
            title="İstek Havuzu",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("#", style="dim", width=4)
        table.add_column("Klasör Adı", width=35)
        table.add_column("Konu", width=30)
        table.add_column("Brief", justify="center", width=8)
        table.add_column("Durum", width=12)

        for i, req in enumerate(requests, 1):
            brief_status = "✓" if req.get('has_brief') else "✗"
            topic = req.get('brief_content', {}).get('topic', '-')[:28]

            status_style = "green" if req['status'] == 'completed' else "yellow"

            table.add_row(
                str(i),
                req['folder_name'][:33],
                topic,
                brief_status,
                f"[{status_style}]{req['status']}[/{status_style}]"
            )

        self.console.print(table)

    def show_glossary_stats(self, stats: Dict):
        """Display glossary statistics."""
        content = f"""
[bold]Toplam Terim:[/bold] {stats.get('total', 0):,}
[bold]Kullanilan:[/bold] {stats.get('used', 0):,}
[bold]Kalan:[/bold] {stats.get('remaining', 0):,}
"""

        panel = Panel(
            content,
            title="Sozluk Durumu",
            border_style="cyan"
        )
        self.console.print(panel)

    def show_proposal_list(self, proposals: List[Dict]) -> Dict:
        """
        Display proposals and get accept/reject decisions.

        Args:
            proposals: List of proposal dicts

        Returns:
            Dict with 'accepted' and 'rejected' lists of proposal IDs
        """
        if not proposals:
            self.console.print("[yellow]Gosterilecek oneri yok.[/yellow]")
            return {'accepted': [], 'rejected': []}

        # Build the display
        header = Panel(
            f"[bold cyan]Icerik Onerileri ({len(proposals)} adet)[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        )
        self.console.print(header)

        # Display each proposal
        for i, proposal in enumerate(proposals, 1):
            score = proposal.get('confidence_score')
            if score is None:
                score_display = "N/A"
                score_style = "dim"
            else:
                score = float(score)
                score_display = f"{score * 10:.1f}"
                score_style = "green" if score >= 0.8 else "yellow" if score >= 0.6 else "red"

            # Get BEIREK area display
            area = proposal.get('beirek_area', '')
            subarea = proposal.get('beirek_subarea', '')
            area_display = f"{area}.{subarea}" if subarea else area

            proposal_panel = Panel(
                f"""[bold]{i}. [{area_display}] {proposal.get('suggested_title', 'Baslik Yok')[:55]}[/bold]
   > {proposal.get('content_angle', '')[:60]}
   Skor: [{score_style}]{score_display}[/{score_style}] | Kaynak: {proposal.get('source_name', 'N/A')[:25]}""",
                border_style="dim",
                box=box.ROUNDED
            )
            self.console.print(proposal_panel)

        # Show commands
        self.console.print("\n[dim]Komutlar:[/dim]")
        self.console.print("  [cyan]a1,2,3[/cyan] - 1, 2, 3 numarali onerileri kabul et")
        self.console.print("  [cyan]r4,5[/cyan]   - 4, 5 numarali onerileri reddet")
        self.console.print("  [cyan]a*[/cyan]     - Tum onerileri kabul et")
        self.console.print("  [cyan]d3[/cyan]     - 3 numarali onerinin detayini goster")
        self.console.print("  [cyan]q[/cyan]      - Cikis")

        # Get user input
        result = {'accepted': [], 'rejected': []}

        while True:
            cmd = Prompt.ask("\n[bold]Komut[/bold]")
            cmd = cmd.strip().lower()

            if cmd == 'q':
                break
            elif cmd == 'a*':
                result['accepted'] = [p.get('id') for p in proposals if p.get('id')]
                self.console.print(f"[green]Tum oneriler kabul edildi ({len(result['accepted'])} adet)[/green]")
                break
            elif cmd.startswith('d'):
                # Detail view
                try:
                    idx = int(cmd[1:])
                    if 0 < idx <= len(proposals):
                        self.show_proposal_detail(proposals[idx - 1])
                    else:
                        self.console.print("[red]Gecersiz numara![/red]")
                except ValueError:
                    self.console.print("[red]Gecersiz komut![/red]")
            elif cmd.startswith('a'):
                # Accept
                try:
                    indices = [int(x.strip()) for x in cmd[1:].split(',')]
                    for idx in indices:
                        if 0 < idx <= len(proposals):
                            pid = proposals[idx - 1].get('id')
                            if pid and pid not in result['accepted']:
                                result['accepted'].append(pid)
                                self.console.print(f"[green]#{idx} kabul edildi[/green]")
                        else:
                            self.console.print(f"[red]Gecersiz numara: {idx}[/red]")
                except ValueError:
                    self.console.print("[red]Gecersiz komut![/red]")
            elif cmd.startswith('r'):
                # Reject
                try:
                    indices = [int(x.strip()) for x in cmd[1:].split(',')]
                    for idx in indices:
                        if 0 < idx <= len(proposals):
                            pid = proposals[idx - 1].get('id')
                            if pid and pid not in result['rejected']:
                                result['rejected'].append(pid)
                                self.console.print(f"[yellow]#{idx} reddedildi[/yellow]")
                        else:
                            self.console.print(f"[red]Gecersiz numara: {idx}[/red]")
                except ValueError:
                    self.console.print("[red]Gecersiz komut![/red]")
            else:
                self.console.print("[red]Gecersiz komut! (a, r, d, veya q kullanin)[/red]")

            # Check if all proposals have been processed
            processed = len(result['accepted']) + len(result['rejected'])
            if processed == len(proposals):
                break

        return result

    def show_proposal_detail(self, proposal: Dict):
        """Display detailed proposal information."""
        import json

        key_points = proposal.get('key_talking_points', '[]')
        if isinstance(key_points, str):
            try:
                key_points = json.loads(key_points)
            except (json.JSONDecodeError, TypeError, ValueError):
                key_points = []

        points_text = "\n".join([f"  - {p}" for p in key_points]) if key_points else "  (Yok)"

        content = f"""
[bold cyan]Onerilen Baslik:[/bold cyan]
{proposal.get('suggested_title', 'N/A')}

[bold cyan]Bakis Acisi:[/bold cyan]
{proposal.get('content_angle', 'N/A')}

[bold cyan]Kisa Aciklama:[/bold cyan]
{proposal.get('brief_description', 'N/A')}

[bold cyan]Hedef Kitle:[/bold cyan]
{proposal.get('target_audience', 'N/A')}

[bold cyan]Ana Konusma Noktalari:[/bold cyan]
{points_text}

[bold cyan]BEIREK Alani:[/bold cyan] {proposal.get('beirek_area', 'N/A')}.{proposal.get('beirek_subarea', '')}
[bold cyan]Guven Skoru:[/bold cyan] {(proposal.get('confidence_score', 0) or 0) * 10:.1f}/10

[bold cyan]Kaynak Makale:[/bold cyan]
{proposal.get('article_title', 'N/A')}
Kaynak: {proposal.get('source_name', 'N/A')}
"""

        panel = Panel(
            content,
            title=f"Oneri Detayi #{proposal.get('proposal_number', proposal.get('id', '?'))}",
            border_style="cyan"
        )
        self.console.print(panel)

    def show_outline_list(self, proposals: List[Dict]) -> List[int]:
        """
        Display proposals ready for content generation.

        Args:
            proposals: List of proposal dicts with outline_created status

        Returns:
            List of selected proposal IDs
        """
        if not proposals:
            self.console.print("[yellow]Uretim icin hazir icerik yok.[/yellow]")
            return []

        table = Table(
            title="Icerik Uretimi Icin Hazir",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("#", style="dim", width=4)
        table.add_column("Baslik", width=45)
        table.add_column("BEIREK", width=8)
        table.add_column("Klasor", width=30)

        for i, proposal in enumerate(proposals, 1):
            folder = proposal.get('folder_path', '')
            if folder:
                folder = folder.split('/')[-1][:28]

            table.add_row(
                str(i),
                proposal.get('suggested_title', '')[:43],
                f"{proposal.get('beirek_area', '')}.{proposal.get('beirek_subarea', '')}",
                folder
            )

        self.console.print(table)

        # Get selection
        self.console.print("\n[dim]Secim icin numara girin (orn: 1,3,5 veya 'all' hepsi icin, 'q' iptal)[/dim]")
        selection = Prompt.ask("[bold]Seciminiz[/bold]")

        if selection.lower() == 'q':
            return []
        elif selection.lower() == 'all':
            return [p.get('id') for p in proposals if p.get('id')]
        else:
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                return [proposals[i-1].get('id') for i in indices if 0 < i <= len(proposals)]
            except (ValueError, IndexError):
                self.console.print("[red]Gecersiz secim![/red]")
                return []

    def show_workflow_status(self, stats: Dict):
        """Display workflow status panel."""
        content = f"""
[bold cyan]Is Akisi Durumu[/bold cyan]

[bold]Oneriler:[/bold]
  Bekleyen:        {stats.get('suggested', 0)}
  Kabul Edilen:    {stats.get('accepted', 0)}
  Reddedilen:      {stats.get('rejected', 0)}

[bold]Uretim:[/bold]
  Outline Hazir:   {stats.get('outline_created', 0)}
  Icerik Uretildi: {stats.get('content_generated', 0)}

[bold]Bugun:[/bold]
  Toplam Oneri:    {stats.get('today_total', 0)}
"""

        panel = Panel(
            content,
            title="BEIREK Content Scout - Durum",
            border_style="green",
            box=box.DOUBLE
        )
        self.console.print(panel)

    def confirm(self, message: str) -> bool:
        """Get user confirmation."""
        return Confirm.ask(message)

    def show_error(self, message: str):
        """Display error message."""
        self.console.print(f"[bold red]Hata:[/bold red] {message}")

    def show_success(self, message: str):
        """Display success message."""
        self.console.print(f"[bold green]✓[/bold green] {message}")

    def show_warning(self, message: str):
        """Display warning message."""
        self.console.print(f"[bold yellow]Uyarı:[/bold yellow] {message}")

    def show_info(self, message: str):
        """Display info message."""
        self.console.print(f"[bold blue]ℹ[/bold blue] {message}")

    def pause(self):
        """Pause and wait for user input."""
        self.console.input("\n[dim]Devam etmek için Enter'a basın...[/dim]")

    def clear(self):
        """Clear the console."""
        self.console.clear()


if __name__ == "__main__":
    ui = TerminalUI()
    ui.show_banner()
    ui.show_main_menu()
