#!/usr/bin/env python3
"""
Sprint Report Scheduler
Automatically runs AI efficiency reports every 2 weeks (bi-weekly sprint cycle).
"""

import os
import sys
import time
import schedule
import logging
from datetime import datetime, timedelta
from generate_sprint_report import main as generate_report


class SprintReportScheduler:
    """Scheduler for automatic sprint report generation."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        # Sprint start date - September 22, 2025 (first scheduled report)
        self.sprint_start_date = datetime(2025, 9, 22)
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
    
    def is_sprint_report_day(self, date=None):
        """Check if the given date (or today) is a bi-weekly sprint report day."""
        if date is None:
            date = datetime.now()
        
        # Calculate the number of days since the sprint start date
        days_since_start = (date.date() - self.sprint_start_date.date()).days
        
        # Check if it's exactly on a bi-weekly boundary (every 14 days)
        return days_since_start >= 0 and days_since_start % 14 == 0
    
    def get_next_sprint_report_date(self):
        """Get the next scheduled sprint report date."""
        today = datetime.now().date()
        
        # If we haven't reached the first sprint date yet
        if today < self.sprint_start_date.date():
            return self.sprint_start_date.date()
        
        # Calculate how many sprints have passed
        days_since_start = (today - self.sprint_start_date.date()).days
        sprints_passed = (days_since_start // 14) + 1
        
        # Calculate the next sprint date
        next_sprint_date = self.sprint_start_date.date() + timedelta(days=sprints_passed * 14)
        
        return next_sprint_date
    
    def get_current_sprint_number(self):
        """Get the current sprint number based on the schedule."""
        today = datetime.now().date()
        
        # If we haven't reached the first sprint date yet, we're still in Sprint 19
        if today < self.sprint_start_date.date():
            return 19
        
        # Calculate how many sprints have passed since Sprint 20 (Sept 22)
        days_since_start = (today - self.sprint_start_date.date()).days
        sprints_passed = days_since_start // 14
        
        return 20 + sprints_passed
    
    def generate_report_job(self):
        """Job function to generate the sprint report."""
        try:
            self.logger.info("Starting scheduled sprint report generation...")
            
            # Check if today is actually a sprint report day
            if not self.is_sprint_report_day():
                current_sprint = self.get_current_sprint_number()
                next_date = self.get_next_sprint_report_date()
                self.logger.info(f"Today is not a sprint report day. Current: Sprint {current_sprint}, Next report: {next_date}")
                return
            
            # Generate the report using our sprint report generator
            filepath = generate_report()
            
            if filepath:
                current_sprint = self.get_current_sprint_number()
                self.logger.info(f"Scheduled report generated successfully for Sprint {current_sprint}: {filepath}")
                
                # Optionally send notifications here
                self.send_notification(filepath, current_sprint)
            else:
                self.logger.warning("No report generated - no data found")
                
        except Exception as e:
            self.logger.error(f"Error in scheduled report generation: {e}")
    
    def send_notification(self, filepath: str, sprint_number: int):
        """Send notification about report generation (placeholder for future implementation)."""
        self.logger.info(f"Sprint {sprint_number} report ready for review: {filepath}")
        # TODO: Implement email notifications or Slack notifications
    
    def run_scheduler(self):
        """Run the scheduler continuously."""
        # Schedule the job for every Monday at 9:00 AM
        schedule.every().monday.at("09:00").do(self.generate_report_job)
        
        next_date = self.get_next_sprint_report_date()
        current_sprint = self.get_current_sprint_number()
        
        self.logger.info("Sprint report scheduler started. Will run every Monday at 9:00 AM.")
        self.logger.info(f"Reports will be generated bi-weekly (every 2 weeks).")
        self.logger.info(f"Current Sprint: {current_sprint}")
        self.logger.info(f"Next scheduled report: {next_date}")
        
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
    
    parser = argparse.ArgumentParser(description='Bi-weekly Sprint Report Scheduler')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--test', '-t', action='store_true', 
                        help='Test mode: generate report immediately')
    parser.add_argument('--check-schedule', action='store_true',
                        help='Check current sprint and next report date')
    parser.add_argument('--next-dates', action='store_true',
                        help='Show next 5 scheduled report dates')
    
    args = parser.parse_args()
    
    scheduler = SprintReportScheduler(args.config)
    
    if args.check_schedule:
        today = datetime.now().strftime('%Y-%m-%d')
        is_report_day = scheduler.is_sprint_report_day()
        current_sprint = scheduler.get_current_sprint_number()
        next_date = scheduler.get_next_sprint_report_date()
        
        print(f"Today ({today}) is {'a' if is_report_day else 'NOT a'} sprint report day.")
        print(f"Current Sprint: {current_sprint}")
        print(f"Next scheduled report: {next_date}")
        return
    
    if args.next_dates:
        print("Next 5 scheduled report dates:")
        current_date = scheduler.get_next_sprint_report_date()
        sprint_num = scheduler.get_current_sprint_number()
        
        # If today is a report day, start from next sprint
        if scheduler.is_sprint_report_day():
            sprint_num += 1
            current_date = current_date + timedelta(days=14)
        
        for i in range(5):
            print(f"  Sprint {sprint_num + i}: {current_date + timedelta(days=i*14)} (Monday)")
        return
    
    if args.test:
        print("Running in test mode - generating report immediately...")
        scheduler.generate_report_job()
    else:
        scheduler.run_scheduler()


if __name__ == '__main__':
    main()
