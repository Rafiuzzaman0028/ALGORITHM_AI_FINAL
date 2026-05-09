class ReportBuilder:

    def build_report(self, title, content):

        report = f"# {title}\n\n"
        report += content

        return report