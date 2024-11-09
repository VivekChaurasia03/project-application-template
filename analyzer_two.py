from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import DataLoader
from model import Issue
import config

class AnalyzerTwo:
    """
    Implements Temporal Analysis of Issue Lifecycles to analyze and visualize
    issue duration and seasonal trends.
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Optional label filter to analyze specific labels, retrieved from config
        self.label_filter = config.get_parameter('label')

    def run(self):
        """
        Runs the lifecycle analysis by calculating issue durations and generating visualizations.
        """
        issues: List[Issue] = DataLoader().get_issues()
        
        # Calculate lifecycle durations
        self.calculate_issue_durations(issues)
        
        # Visualize the lifecycle data
        self.issue_lifecycle_visualization(issues)
        self.seasonal_trends_analysis(issues)
        self.bottleneck_analysis(issues)

    def calculate_issue_durations(self, issues: List[Issue]):
        """
        Calculates the time duration each issue stayed open (in days).
        """
        for issue in issues:
            if issue.created_date and issue.updated_date:
                issue.duration_days = (issue.updated_date - issue.created_date).days

    def issue_lifecycle_visualization(self, issues: List[Issue]):
        """
        Creates a bar chart showing the average time-to-close for each label.
        """
        # Filter issues if a specific label is provided
        if self.label_filter:
            issues = [issue for issue in issues if self.label_filter in issue.labels]

        # Calculate average duration per label
        label_durations = {}
        for issue in issues:
            for label in issue.labels:
                if label not in label_durations:
                    label_durations[label] = []
                label_durations[label].append(issue.duration_days)

        avg_label_durations = {label: sum(durations) / len(durations) for label, durations in label_durations.items()}

        # Plotting
        labels, avg_durations = zip(*avg_label_durations.items())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, avg_durations, color='skyblue')
        plt.xlabel('Labels')
        plt.ylabel('Average Time-to-Close (days)')
        plt.title('Average Time-to-Close by Label')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def seasonal_trends_analysis(self, issues: List[Issue]):
        """
        Analyzes and plots monthly trends in issue creation and closure.
        """
        data = {
            'created_month': [issue.created_date.strftime('%Y-%m') for issue in issues if issue.created_date],
            'closed_month': [issue.updated_date.strftime('%Y-%m') for issue in issues if issue.updated_date]
        }

        df = pd.DataFrame(data)

        # Count issues created and closed per month
        created_counts = df['created_month'].value_counts().sort_index()
        closed_counts = df['closed_month'].value_counts().sort_index()

        # Plotting
        plt.figure(figsize=(12, 6))
        created_counts.plot(label='Issues Created', marker='o', color='b')
        closed_counts.plot(label='Issues Closed', marker='o', color='r')
        plt.xlabel('Month')
        plt.ylabel('Number of Issues')
        plt.title('Monthly Trends of Issues Created and Closed')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def bottleneck_analysis(self, issues: List[Issue]):
        """
        Identifies bottleneck issues and displays the counts by label.
        """
        avg_duration = sum(issue.duration_days for issue in issues if hasattr(issue, 'duration_days')) / len(issues)
        
        bottleneck_issues = [issue for issue in issues if issue.duration_days > avg_duration]
        
        bottleneck_counts = {}
        for issue in bottleneck_issues:
            for label in issue.labels:
                if label not in bottleneck_counts:
                    bottleneck_counts[label] = 0
                bottleneck_counts[label] += 1

        # Plotting
        labels, counts = zip(*sorted(bottleneck_counts.items(), key=lambda x: x[1], reverse=True))
        plt.figure(figsize=(10, 6))
        plt.bar(labels, counts, color='salmon')
        plt.xlabel('Labels')
        plt.ylabel('Count of Bottleneck Issues')
        plt.title('Bottleneck Issues by Label')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    AnalyzerTwo().run()
