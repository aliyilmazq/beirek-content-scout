#!/usr/bin/env python3
"""
BEIREK Content Scout
====================

Automatic news scanning and content generation CLI application.

Usage:
    python main.py

Features:
- 300+ source RSS/Web scanning
- Claude AI filtering
- 3-format content generation (Article, LinkedIn, Twitter)
- Daily concept from 7000+ term glossary
- Request pool for manual topics
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
from modules.storage import init_database
from modules.concept_manager import ConceptManager
from modules.request_manager import RequestManager
from modules.ui import TerminalUI
from modules.config_manager import check_claude_cli, ensure_paths_exist


class ContentScout:
    """
    Main application class for BEIREK Content Scout.
    """

    def __init__(self):
        """Initialize application and all modules."""
        # Ensure required paths exist
        ensure_paths_exist()

        # Initialize database
        init_database()

        # Check Claude CLI availability
        self.cli_status = check_claude_cli()
        self.cli_available = self.cli_status.get('available', False)

        if not self.cli_available:
            logger.warning(f"Claude CLI not available: {self.cli_status.get('error', 'Unknown error')}")
        else:
            logger.info(f"Claude CLI available: {self.cli_status.get('version', 'unknown')}")

        # Initialize modules
        self.scanner = NewsScanner()
        self.ui = TerminalUI()
        self.ui.cli_available = self.cli_available

        # Only initialize CLI-dependent modules if CLI is available
        self.filter = None
        self.generator = None
        self.framer = None
        self.concept_manager = None
        self.request_manager = None

        if self.cli_available:
            try:
                self.filter = ArticleFilter()
                self.generator = ContentGenerator()
                self.framer = ContentFramer()
                self.concept_manager = ConceptManager()
                self.request_manager = RequestManager()
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

        while True:
            try:
                choice = self.ui.show_main_menu(self.cli_available)

                if choice == '1':
                    self.run_scan_and_frame_flow()
                elif choice == '2':
                    if self._check_cli_required():
                        self.run_proposal_review_flow()
                elif choice == '3':
                    if self._check_cli_required():
                        self.run_outline_creation_flow()
                elif choice == '4':
                    if self._check_cli_required():
                        self.run_individual_generation_flow()
                elif choice == '5':
                    if self._check_cli_required():
                        self.run_concept_flow()
                elif choice == '6':
                    if self._check_cli_required():
                        self.run_request_flow()
                elif choice == '7':
                    self.show_workflow_status()
                elif choice == '8':
                    self.show_statistics()
                elif choice == '9':
                    self.show_settings()
                elif choice == '0':
                    self.ui.show_success("Gule gule!")
                    sys.exit(0)

                self.ui.pause()
                self.ui.clear()

            except KeyboardInterrupt:
                self.ui.show_info("\nCikiliyor...")
                sys.exit(0)
            except Exception as e:
                self.ui.show_error(str(e))
                logger.error(f"Error in main loop: {e}", exc_info=True)
                self.ui.pause()

    def _check_cli_required(self) -> bool:
        """Check if CLI is available, show error if not."""
        if not self.cli_available:
            self.ui.show_error("Bu ozellik icin Claude CLI gereklidir!")
            self.ui.show_info("Kurulum: https://claude.ai/cli")
            return False
        return True

    def run_scan_and_frame_flow(self):
        """
        Run scan and frame flow (Step 1-2).

        1. Load sources to DB if needed
        2. Scan all sources
        3. Filter articles with Claude (if CLI available)
        4. Frame relevant articles into content proposals (if CLI available)
        """
        if self.cli_available:
            self.ui.show_info("Tara ve Cercevele akisi baslatiliyor...")
        else:
            self.ui.show_info("Tarama akisi baslatiliyor (filtreleme devre disi)...")
        logger.info("Starting scan and frame flow")

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
            self.ui.show_warning("Claude CLI olmadan filtreleme ve cerceveleme yapilamaz.")
            self.ui.show_summary({
                'Taranan Kaynak': result.get('sources_scanned', 0),
                'Yeni Makale': result['new_articles'],
                'Hatalar': len(result.get('errors', []))
            })
            return

        # Filter
        relevant_articles = []
        if result['new_articles'] > 0:
            self.ui.show_info("Makaleler filtreleniyor...")

            with self.ui.show_scan_progress(100) as progress:
                task = progress.add_task("Filtreleniyor...", total=100)

                def filter_progress(current, total):
                    progress.update(task, completed=int(current/total*100))

                relevant = self.filter.filter_articles(progress_callback=filter_progress)

            self.ui.show_success(f"{len(relevant)} ilgili makale bulundu")
            relevant_articles = [r['article'] for r in relevant]

        # Frame relevant articles
        if relevant_articles:
            self.ui.show_info(f"{len(relevant_articles)} makale cerceveleniyor...")

            with self.ui.show_scan_progress(len(relevant_articles)) as progress:
                task = progress.add_task("Cerceveleniyor...", total=len(relevant_articles))

                def frame_progress(current, total):
                    progress.update(task, completed=current)

                proposals = self.framer.frame_articles(relevant_articles, progress_callback=frame_progress)

            self.ui.show_success(f"{len(proposals)} icerik onerisi olusturuldu")

            # Show summary
            self.ui.show_summary({
                'Taranan Kaynak': result.get('sources_scanned', 0),
                'Yeni Makale': result['new_articles'],
                'Ilgili Makale': len(relevant_articles),
                'Olusturulan Oneri': len(proposals)
            })
        else:
            self.ui.show_info("Cercevelenecek makale yok.")
            self.ui.show_summary(result)

    def run_proposal_review_flow(self):
        """
        Run proposal review flow (Step 3).

        1. Get pending proposals
        2. Display them to user
        3. Accept/reject based on user decisions
        """
        self.ui.show_info("Onerileri gozden gecirme akisi baslatiliyor...")
        logger.info("Starting proposal review flow")

        # Get suggested proposals
        proposals = storage.get_proposals_by_status('suggested')

        if not proposals:
            self.ui.show_info("Bekleyen oneri yok. Once tarama ve cerceveleme yapin.")
            return

        self.ui.show_info(f"{len(proposals)} bekleyen oneri bulundu")

        # Show proposals and get decisions
        decisions = self.ui.show_proposal_list(proposals)

        # Process decisions
        accepted_count = 0
        rejected_count = 0

        for proposal_id in decisions.get('accepted', []):
            storage.accept_proposal(proposal_id)
            accepted_count += 1

        for proposal_id in decisions.get('rejected', []):
            storage.reject_proposal(proposal_id)
            rejected_count += 1

        # Show summary
        self.ui.show_summary({
            'Kabul Edilen': accepted_count,
            'Reddedilen': rejected_count,
            'Islenmemis': len(proposals) - accepted_count - rejected_count
        })

    def run_outline_creation_flow(self):
        """
        Run outline creation flow (Step 4).

        1. Get accepted proposals
        2. Create folder structure for each
        3. Generate _outline.md, _proposal.json, _source.json
        """
        self.ui.show_info("Klasor olusturma akisi baslatiliyor...")
        logger.info("Starting outline creation flow")

        # Get accepted proposals
        proposals = storage.get_proposals_for_outline()

        if not proposals:
            self.ui.show_info("Klasor olusturulacak oneri yok. Once onerileri kabul edin.")
            return

        self.ui.show_info(f"{len(proposals)} kabul edilmis oneri bulundu")

        # Ask for confirmation
        if not self.ui.confirm(f"{len(proposals)} oneri icin klasor olusturulsun mu?"):
            return

        # Create outlines
        created_paths = []

        with self.ui.show_scan_progress(len(proposals)) as progress:
            task = progress.add_task("Klasorler olusturuluyor...", total=len(proposals))

            def outline_progress(current, total):
                progress.update(task, completed=current)

            created_paths = self.framer.create_outlines_for_accepted(progress_callback=outline_progress)

        self.ui.show_success(f"{len(created_paths)} klasor olusturuldu")

        # Show created paths
        for path in created_paths[:5]:  # Show first 5
            self.ui.show_info(f"  -> {path.split('/')[-1]}")

        if len(created_paths) > 5:
            self.ui.show_info(f"  ... ve {len(created_paths) - 5} daha")

    def run_individual_generation_flow(self):
        """
        Run individual content generation flow (Step 5).

        1. Get proposals with outlines
        2. Let user select which to generate
        3. Generate content for selected proposals
        """
        self.ui.show_info("Icerik uretim akisi baslatiliyor...")
        logger.info("Starting content generation flow")

        # Get proposals ready for generation
        proposals = storage.get_proposals_for_generation()

        if not proposals:
            self.ui.show_info("Uretim icin hazir oneri yok. Once klasor olusturun.")
            return

        self.ui.show_info(f"{len(proposals)} oneri uretim icin hazir")

        # Let user select
        selected_ids = self.ui.show_outline_list(proposals)

        if not selected_ids:
            self.ui.show_info("Hicbir oneri secilmedi.")
            return

        # Get format selection
        formats = self.ui.show_generation_options()
        self.ui.show_info(f"Secilen formatlar: {', '.join(formats)}")

        # Generate content for each selected proposal
        success_count = 0
        for proposal_id in selected_ids:
            proposal = storage.get_proposal_by_id(proposal_id)
            if not proposal:
                continue

            self.ui.show_info(f"\nUretiliyor: {proposal['suggested_title'][:50]}...")

            try:
                # Get source content
                article_content = proposal.get('article_content') or proposal.get('article_summary') or ''

                if not article_content:
                    # Try to fetch from URL
                    article_url = proposal.get('article_url')
                    if article_url:
                        source_content = self.scanner.extract_article_content(article_url)
                        article_content = source_content.get('content', '')

                if not article_content:
                    self.ui.show_warning(f"Icerik cekilemedi: {proposal['suggested_title'][:30]}")
                    continue

                # Generate content using proposal's angle, talking points, and description
                content = self.generator.generate_from_proposal(
                    proposal=proposal,
                    source_content=article_content
                )

                # Save to the proposal's folder
                folder_path = proposal.get('folder_path')
                if folder_path:
                    # Use save_proposal_content for proper formatting
                    self.generator.save_proposal_content(content, proposal)

                    # Update proposal status
                    storage.update_proposal_status(proposal_id, 'content_generated')
                    success_count += 1

                    # Get folder name safely
                    folder_name = folder_path.rstrip('/').split('/')[-1] if folder_path else 'unknown'
                    self.ui.show_success(f"Kaydedildi: {folder_name}")

            except Exception as e:
                self.ui.show_error(f"Uretim hatasi: {e}")

        self.ui.show_summary({
            'Secilen': len(selected_ids),
            'Basarili': success_count,
            'Basarisiz': len(selected_ids) - success_count
        })

    def show_workflow_status(self):
        """Display current workflow status."""
        stats = storage.get_proposal_stats()
        self.ui.show_workflow_status(stats)

    def run_concept_flow(self):
        """
        Run daily concept flow.

        1. Check if concept already selected today
        2. Select concept from glossary
        3. Generate content in 3 formats
        4. Save to daily-concepts folder
        """
        self.ui.show_info("Günlük kavram akışı başlatılıyor...")

        # Check glossary
        stats = self.concept_manager.get_glossary_status()
        self.ui.show_glossary_stats(stats)

        if stats['total'] == 0:
            self.ui.show_warning("Sözlük boş! Önce sözlük import edilmeli.")
            if self.ui.confirm("Varsayılan sözlükten import edilsin mi?"):
                try:
                    count = self.concept_manager.import_glossary()
                    self.ui.show_success(f"{count} terim import edildi")
                except Exception as e:
                    self.ui.show_error(f"Import başarısız: {e}")
                    return

        # Run concept flow
        try:
            result = self.concept_manager.run_daily_concept_flow()
            self.ui.show_concept_info(result['concept'])
            self.ui.show_success(f"İçerik oluşturuldu: {result['content_path']}")

            # Show word counts
            self.ui.show_summary({
                'Makale': f"{result['word_counts']['article']} kelime",
                'LinkedIn': f"{result['word_counts']['linkedin']} kelime",
                'Twitter': f"{result['word_counts']['twitter']} kelime"
            })

        except Exception as e:
            self.ui.show_error(f"Kavram akışı hatası: {e}")

    def run_request_flow(self):
        """
        Run request pool flow.

        1. Scan request pool folder
        2. Show pending requests
        3. Process selected requests
        """
        self.ui.show_info("İstek havuzu taranıyor...")

        requests = self.request_manager.scan_request_pool()
        pending = [r for r in requests if r['status'] == 'pending']

        if not pending:
            self.ui.show_info("Bekleyen istek yok.")
            return

        self.ui.show_request_list(pending)

        if self.ui.confirm(f"\n{len(pending)} bekleyen istek var. Hepsi işlensin mi?"):
            with self.ui.show_scan_progress(len(pending)) as progress:
                task = progress.add_task("İşleniyor...", total=len(pending))

                result = self.request_manager.process_all_pending()

                progress.update(task, completed=len(pending))

            self.ui.show_summary({
                'İşlenen': result['processed'],
                'Başarılı': result['success'],
                'Başarısız': result['failed']
            })

    def show_statistics(self):
        """Display application statistics."""
        stats = storage.get_stats()
        self.ui.show_statistics(stats)

        # Also show glossary stats
        try:
            glossary_stats = self.concept_manager.get_glossary_status()
            self.ui.show_glossary_stats(glossary_stats)
        except Exception:
            pass  # Glossary stats are optional, don't fail if unavailable

    def show_settings(self):
        """Display and manage settings."""
        self.ui.show_info("Ayarlar menüsü")

        settings_panel = """
[bold cyan]Mevcut Ayarlar[/bold cyan]

[1] Kaynak yönetimi
[2] Filtreleme ayarları
[3] İçerik ayarları
[4] Sözlük import
[5] Geri
"""
        self.ui.console.print(settings_panel)

        choice = self.ui.console.input("\n[bold]Seçiminiz:[/bold] ")

        if choice == '4':
            # Glossary import
            self.ui.show_info("Sözlük import ediliyor...")
            try:
                count = self.concept_manager.import_glossary()
                self.ui.show_success(f"{count} terim import edildi")
            except Exception as e:
                self.ui.show_error(f"Import hatası: {e}")


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
