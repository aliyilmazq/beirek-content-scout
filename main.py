#!/usr/bin/env python3
"""
BEIREK Content Scout
====================

Automatic news scanning and content generation CLI application.

Usage:
    python main.py

Features:
- 65+ RSS source scanning
- NewsData.io API integration
- Claude AI filtering and framing
- User approval flow for filtered articles
- 3-format content generation (Article, LinkedIn, Twitter)
- Folder-based storage (no database)

Workflow:
1. TARA: Scan RSS feeds + NewsData API
2. BIRLESTIR: Deduplicate by URL
3. ANALIZ: Claude relevance scoring + BEIREK area assignment
4. FILTRELE: Score >= 7 articles
5. ONAYLA: User approval (E/H/S/T)
6. KAYDET: Save to girdiler/ and raporlar/ folders
7. RAPOR: Summary statistics
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

# Initialize logging first
from modules.logger import setup_logging, get_logger
setup_logging()
logger = get_logger(__name__)

from modules.scanner import NewsScanner
from modules.filter import ArticleFilter
from modules.generator import ContentGenerator
from modules.framer import ContentFramer
from modules import storage
from modules.storage import init_database, get_storage
from modules.ui import TerminalUI
from modules.config_manager import check_claude_cli, ensure_paths_exist
from modules.claude_session import get_session, start_session, stop_session


class ContentScout:
    """
    Main application class for BEIREK Content Scout.
    """

    def __init__(self):
        """Initialize application and all modules."""
        # Ensure required paths exist
        ensure_paths_exist()

        # Initialize folder storage
        init_database()

        # Get storage instance
        self.storage = get_storage()

        # Check Claude CLI availability
        self.cli_status = check_claude_cli()
        self.cli_available = self.cli_status.get('available', False)

        if not self.cli_available:
            logger.warning(f"Claude CLI not available: {self.cli_status.get('error', 'Unknown error')}")
        else:
            logger.info(f"Claude CLI available: {self.cli_status.get('version', 'unknown')}")

        # Initialize Claude session if available
        if self.cli_available:
            self.session = get_session()
            start_session()

        # Initialize modules
        self.scanner = NewsScanner()
        self.ui = TerminalUI()
        self.ui.cli_available = self.cli_available

        # Only initialize CLI-dependent modules if CLI is available
        self.filter = None
        self.generator = None
        self.framer = None

        if self.cli_available:
            try:
                self.filter = ArticleFilter()
                self.generator = ContentGenerator()
                self.framer = ContentFramer()
            except Exception as e:
                logger.error(f"Error initializing CLI-dependent modules: {e}")
                self.cli_available = False
                self.ui.cli_available = False

    def run(self):
        """Main application loop."""
        self.ui.clear()
        self.ui.show_banner()

        # Show CLI status warning if not available
        if not self.cli_available:
            self.ui.show_warning("Claude CLI bulunamadi! Bazi ozellikler devre disi.")
            self.ui.pause()
            return

        # AUTO-START: Run scan, filter, and approval flow automatically
        try:
            self.run_auto_flow()
        except KeyboardInterrupt:
            self.cleanup()
            self.ui.show_info("\nCikiliyor...")
            sys.exit(0)
        except Exception as e:
            self.ui.show_error(str(e))
            logger.error(f"Error in auto flow: {e}", exc_info=True)

        # After auto flow, show menu for additional actions
        while True:
            try:
                choice = self.ui.show_main_menu(self.cli_available)

                if choice == '1':
                    self.run_scan_and_filter_flow()
                elif choice == '2':
                    if self._check_cli_required():
                        self.run_approval_flow()
                elif choice == '3':
                    if self._check_cli_required():
                        self.run_content_generation_flow()
                elif choice == '4':
                    if self._check_cli_required():
                        self.run_concept_flow()
                elif choice == '5':
                    if self._check_cli_required():
                        self.run_request_flow()
                elif choice == '6':
                    self.show_workflow_status()
                elif choice == '7':
                    self.show_statistics()
                elif choice == '8':
                    self.show_settings()
                elif choice == '0':
                    self.cleanup()
                    self.ui.show_success("Gule gule!")
                    sys.exit(0)

                self.ui.pause()
                self.ui.clear()

            except KeyboardInterrupt:
                self.cleanup()
                self.ui.show_info("\nCikiliyor...")
                sys.exit(0)
            except Exception as e:
                self.ui.show_error(str(e))
                logger.error(f"Error in main loop: {e}", exc_info=True)
                self.ui.pause()

    def run_auto_flow(self):
        """
        Automatic startup flow:
        1. Scan all sources (RSS + NewsData)
        2. Filter with Claude
        3. Show approval screen
        """
        self.ui.show_info("Otomatik akis baslatiliyor...")
        logger.info("Starting automatic flow")

        # Step 1: Scan and Filter
        self.run_scan_and_filter_flow()

        # Step 2: If there are pending approvals, show approval screen
        pending = self.storage.get_pending_approvals()
        if pending:
            self.ui.clear()
            self.ui.show_banner()
            self.run_approval_flow()

            # Step 3: If there are approved articles, ask about content generation
            approved = self.storage.get_approved_articles()
            if approved:
                self.ui.clear()
                if self.ui.confirm(f"{len(approved)} onaylanmis makale var. Icerik uretilsin mi?"):
                    self.run_content_generation_flow()
        else:
            self.ui.show_info("Onay bekleyen makale yok.")

        self.ui.pause()
        self.ui.clear()

    def cleanup(self):
        """Cleanup resources on exit."""
        if self.cli_available:
            stop_session()

    def _check_cli_required(self) -> bool:
        """Check if CLI is available, show error if not."""
        if not self.cli_available:
            self.ui.show_error("Bu ozellik icin Claude CLI gereklidir!")
            self.ui.show_info("Kurulum: https://claude.ai/cli")
            return False
        return True

    def run_scan_and_filter_flow(self):
        """
        Run scan and filter flow.

        1. Load sources to storage if needed
        2. Scan all RSS sources + NewsData API
        3. Filter articles with Claude (if CLI available)
        4. Add filtered articles to pending approvals
        """
        if self.cli_available:
            self.ui.show_info("Tara ve Filtrele akisi baslatiliyor...")
        else:
            self.ui.show_info("Tarama akisi baslatiliyor (filtreleme devre disi)...")
        logger.info("Starting scan and filter flow")

        # Check if sources are loaded
        if storage.get_source_count() == 0:
            self.ui.show_info("Kaynaklar yukleniyor...")
            count = self.scanner.load_sources_to_db()
            self.ui.show_success(f"{count} kaynak yuklendi")

        # Scan
        with self.ui.show_scan_progress(100) as progress:
            task = progress.add_task("Taraniyor...", total=100)

            def update_progress(current, total, source_name):
                progress.update(task, completed=int(current/total*100),
                              description=f"Taraniyor: {source_name[:30]}")

            result = self.scanner.scan_all_sources(progress_callback=update_progress)

        self.ui.show_success(f"Tarama tamamlandi: {result['new_articles']} yeni makale bulundu")

        # If CLI not available, show scan-only summary and return
        if not self.cli_available:
            self.ui.show_warning("Claude CLI olmadan filtreleme yapilamaz.")
            self.ui.show_summary({
                'Taranan Kaynak': result.get('sources_scanned', 0),
                'Yeni Makale': result['new_articles'],
                'Hatalar': len(result.get('errors', []))
            })
            return

        # Filter with Claude
        relevant = []
        scanned_articles = result.get('articles', [])
        if scanned_articles:
            self.ui.show_info(f"{len(scanned_articles)} makale filtreleniyor...")

            with self.ui.show_scan_progress(100) as progress:
                task = progress.add_task("Filtreleniyor...", total=100)

                def filter_progress(current, total):
                    progress.update(task, completed=int(current/total*100))

                relevant = self.filter.filter_articles(
                    articles=scanned_articles,
                    progress_callback=filter_progress
                )

            self.ui.show_success(f"{len(relevant)} ilgili makale bulundu")

            # Add filtered articles to pending approvals
            if relevant:
                self.ui.show_info("Onay kuyruğuna ekleniyor...")
                for r in relevant:
                    self.storage.add_pending_approval(r['article'], r)

                self.ui.show_success(f"{len(relevant)} makale onay bekliyor")

        # Show summary
        self.ui.show_summary({
            'Taranan Kaynak': result.get('sources_scanned', 0),
            'Yeni Makale': result['new_articles'],
            'Ilgili Makale': len(relevant),
            'Hatalar': len(result.get('errors', []))
        })

    def run_approval_flow(self):
        """
        Run user approval flow.

        1. Get pending approvals
        2. Show each article with details
        3. Allow user to approve/reject/skip
        4. Update storage accordingly
        """
        self.ui.show_info("Onay akisi baslatiliyor...")
        logger.info("Starting approval flow")

        # Get pending approvals
        pending = self.storage.get_pending_approvals()

        if not pending:
            self.ui.show_info("Onay bekleyen makale yok. Once tarama yapin.")
            return

        self.ui.show_info(f"{len(pending)} makale onay bekliyor")

        # Show approval flow
        decisions = self.ui.show_approval_flow(pending)

        # Process decisions
        approved_count = 0
        rejected_count = 0

        for approval_id in decisions.get('approved', []):
            if self.storage.approve_article(str(approval_id)):
                approved_count += 1

        for approval_id in decisions.get('rejected', []):
            if self.storage.reject_article(str(approval_id)):
                rejected_count += 1

        # Show summary
        self.ui.show_summary({
            'Onaylanan': approved_count,
            'Reddedilen': rejected_count,
            'Atlanan': len(decisions.get('skipped', []))
        })

    def run_content_generation_flow(self):
        """
        Run content generation flow.

        1. Get approved articles
        2. Generate content for each (makale, linkedin, twitter)
        3. Save to folder structure
        """
        self.ui.show_info("Icerik uretim akisi baslatiliyor...")
        logger.info("Starting content generation flow")

        # Get approved articles
        approved = self.storage.get_approved_articles()

        if not approved:
            self.ui.show_info("Icerik uretilecek onaylanmis makale yok.")
            return

        self.ui.show_info(f"{len(approved)} onaylanmis makale bulundu")

        # Ask for confirmation
        if not self.ui.confirm(f"{len(approved)} makale icin icerik uretilsin mi?"):
            return

        # Generate content for each approved article
        success_count = 0
        for approval in approved:
            title = approval.get('article', {}).get('title', 'Untitled')
            self.ui.show_info(f"Uretiliyor: {title[:50]}...")

            try:
                folder_path = self.generator.generate_for_approved_article(approval)
                self.ui.show_success(f"Kaydedildi: {folder_path.split('/')[-1]}")
                success_count += 1

            except Exception as e:
                self.ui.show_error(f"Uretim hatasi: {e}")

        self.ui.show_summary({
            'Toplam': len(approved),
            'Basarili': success_count,
            'Basarisiz': len(approved) - success_count
        })

    def run_concept_flow(self):
        """Run daily concept flow (placeholder for now)."""
        self.ui.show_info("Gunluk kavram akisi henuz uygulanmadi.")
        self.ui.show_info("Bu ozellik ileriki surumde eklenecek.")

    def run_request_flow(self):
        """Run request pool flow (placeholder for now)."""
        self.ui.show_info("Istek havuzu akisi henuz uygulanmadi.")
        self.ui.show_info("Bu ozellik ileriki surumde eklenecek.")

    def show_workflow_status(self):
        """Display current workflow status."""
        stats = storage.get_proposal_stats()
        self.ui.show_workflow_status(stats)

    def show_statistics(self):
        """Display application statistics."""
        stats = storage.get_stats()
        self.ui.show_statistics(stats)

    def show_settings(self):
        """Display and manage settings."""
        self.ui.show_info("Ayarlar menusu")

        settings_panel = """
[bold cyan]Mevcut Ayarlar[/bold cyan]

[1] Kaynak yonetimi
[2] Filtreleme ayarlari
[3] Icerik ayarlari
[4] Klasor yapisini goster
[5] Geri
"""
        self.ui.console.print(settings_panel)

        choice = self.ui.console.input("\n[bold]Seciminiz:[/bold] ")

        if choice == '4':
            # Show folder structure
            self.ui.show_info(f"Icerik klasoru: {self.storage.content_path}")
            self.ui.show_info(f"Veri klasoru: {self.storage.data_path}")
            self.ui.show_info(f"Girdi klasoru: {self.storage.inputs_folder}")
            self.ui.show_info(f"Rapor klasoru: {self.storage.reports_folder}")


def main():
    """Application entry point."""
    logger.info("BEIREK Content Scout starting...")

    try:
        app = ContentScout()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
