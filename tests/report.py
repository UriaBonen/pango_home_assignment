import statistics

class ReportGenerator:
    def __init__(self, data):
        self.data = data

    def generate_html(self, filename="weather_report.html"):
        discrepancies = [abs(entry['temperature_web'] - entry['temperature_api']) for entry in self.data]
        mean_discrepancy = round(statistics.mean(discrepancies), 2)
        max_discrepancy = round(max(discrepancies), 2)
        min_discrepancy = round(min(discrepancies), 2)

        rows = ""
        for entry in self.data:
            discrepancy = abs(entry['temperature_web'] - entry['temperature_api'])
            rows += f"""
            <tr>
                <td>{entry['city']}</td>
                <td>{entry['temperature_web']:.2f}</td>
                <td>{entry['feels_like_web']:.2f}</td>
                <td>{entry['temperature_api']:.2f}</td>
                <td>{entry['feels_like_api']:.2f}</td>
                <td>{entry['avg_temperature']:.2f}</td>
                <td>{discrepancy:.2f}</td>
            </tr>
            """

        html = f"""
        <html>
        <head>
            <title>Weather Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>City Weather Comparison Report</h1>
            <table>
                <thead>
                    <tr>
                        <th>City</th>
                        <th>Temp (Web)</th>
                        <th>Feels Like (Web)</th>
                        <th>Temp (API)</th>
                        <th>Feels Like (API)</th>
                        <th>Avg Temp</th>
                        <th>Discrepancy</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            <h2>Summary Statistics</h2>
            <ul>
                <li><strong>Mean Discrepancy:</strong> {mean_discrepancy}</li>
                <li><strong>Max Discrepancy:</strong> {max_discrepancy}</li>
                <li><strong>Min Discrepancy:</strong> {min_discrepancy}</li>
            </ul>
        </body>
        </html>
        """

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Report generated: {filename}")
