#!/usr/bin/env python3
"""
Sprint Report Scheduler
Automatically runs AI efficiency reports every second Monday (sprint start days).
"""

import os
import sys
import time
import schedule
import logging
from datetime import datetime, timedelta
from ai_efficiency_reporter import AIEfficiencyReporter


class SprintReportScheduler:
    """Scheduler for automatic sprint report generation."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self.setup_logging()
        
    def setup_logging(self):
        """Set up logging for the scheduler."""
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'scheduler.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def is_second_monday(self, date=None):
        """Check if the given date (or today) is the second Monday of the month."""
        if date is None:
            date = datetime.now()
        
        # Find the first day of the month
        first_day = date.replace(day=1)
        
        # Find the first Monday of the month
        days_until_monday = (7 - first_day.weekday()) % 7
        first_monday = first_day + timedelta(days=days_until_monday)
        
        # The second Monday is 7 days later
        second_monday = first_monday + timedelta(days=7)
        
        return date.date() == second_monday.date()
    
    def generate_report_job(self):
        """Job function to generate the sprint report."""
        try:
            self.logger.info("Starting scheduled sprint report generation...")
            
            # Check if today is actually the second Monday
            if not self.is_second_monday():
                self.logger.info("Today is not the second Monday. Skipping report generation.")
                return
            
            reporter = AIEfficiencyReporter(self.config_path)
            filepath = reporter.generate_report()
            
            if filepath:
                self.logger.info(f"Scheduled report generated successfully: {filepath}")
                
                # Optionally send notifications here
                self.send_notification(filepath)
            else:
                self.logger.warning("No report generated - no data found")
                
        except Exception as e:
            self.logger.error(f"Error in scheduled report generation: {e}")
    
    def send_notification(self, filepath: str):
        """Send notification about report generation (placeholder for future implementation)."""
        self.logger.info(f"Report ready for review: {filepath}")
        # TODO: Implement email notifications or Slack notifications
    
    def run_scheduler(self):
        """Run the scheduler continuously."""
        # Schedule the job for every Monday at 9:00 AM
        schedule.every().monday.at("09:00").do(self.generate_report_job)
        
        self.logger.info("Sprint report scheduler started. Will run every Monday at 9:00 AM.")
        self.logger.info("Reports will only be generated on the second Monday of each month.")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                self.logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying


def main():
    """Main entry point for the scheduler."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sprint Report Scheduler')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--test', '-t', action='store_true', 
                        help='Test mode: generate report immediately')
    parser.add_argument('--check-date', action='store_true',
                        help='Check if today is the second Monday')
    
    args = parser.parse_args()
    
    scheduler = SprintReportScheduler(args.config)
    
    if args.check_date:
        is_second_monday = scheduler.is_second_monday()
        print(f"Today ({datetime.now().strftime('%Y-%m-%d')}) is {'the' if is_second_monday else 'NOT the'} second Monday of the month.")
        return
    
    if args.test:
        print("Running in test mode - generating report immediately...")
        scheduler.generate_report_job()
    else:
        scheduler.run_scheduler()


if __name__ == '__main__':
    main()
