import csv
import matplotlib.pyplot as plt
import os

def analyze_survey():
    input_file = "Alternative CPA Pathways Survey_December 31, 2025_09.45.csv"
    output_report = "awareness_analysis_report.md"
    output_chart = "awareness_impact_chart.png"

    # Mapping for Q52 responses based on actual data values
    # "Greatly decreased" (1) -> "Significantly decreased desire"
    # "Somewhat decreased" (2) -> "Decreased desire"
    # "No change in desire" (3) -> "No change in desire"
    # "Somewhat increased" (4) -> "Increased desire"
    # "Greatly increased" (5) -> "Significantly increased desire"

    q52_mapping = {
        "Significantly decreased desire": 1,
        "Decreased desire": 2,
        "No change in desire": 3,
        "Increased desire": 4,
        "Significantly increased desire": 5
    }

    scores_aware = []
    scores_unaware = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        # Skip the first two rows (descriptive text and metadata)
        # Row 1: Descriptive text
        next(reader)
        # Row 2: Metadata (ImportId)
        next(reader)

        count_processed = 0
        count_skipped = 0

        for row in reader:
            # Note: The prompt referred to Q31 for awareness, but the description
            # "Were you aware of the alternative pathway to CPA licensure before taking the survey?"
            # corresponds to column Q53 in the file. Q31 is about awareness before *graduate program*.
            # Q52 is about impact on desire to pursue graduate degree.
            # Using Q53 as the Awareness variable as it matches the prompt description and has data with Q52.
            awareness = row.get('Q53', '').strip()
            impact = row.get('Q52', '').strip()

            # Filter out empty or N/A
            if not awareness or awareness == "N/A" or not impact or impact == "N/A":
                count_skipped += 1
                continue

            # Ensure valid response for Q52 (impact)
            if impact not in q52_mapping:
                # If the response is not in mapping, skip it
                count_skipped += 1
                continue

            score = q52_mapping[impact]

            if awareness == "Yes":
                scores_aware.append(score)
                count_processed += 1
            elif awareness == "No":
                scores_unaware.append(score)
                count_processed += 1
            else:
                # Handle unexpected values in awareness if any
                count_skipped += 1
                continue

    # Calculate averages
    avg_aware = sum(scores_aware) / len(scores_aware) if scores_aware else 0
    avg_unaware = sum(scores_unaware) / len(scores_unaware) if scores_unaware else 0

    print(f"Processed {count_processed} rows.")
    print(f"Skipped {count_skipped} rows.")
    print(f"Average Impact Score (Aware - Yes): {avg_aware:.2f} (n={len(scores_aware)})")
    print(f"Average Impact Score (Unaware - No): {avg_unaware:.2f} (n={len(scores_unaware)})")

    # Generate Visualization
    groups = ['Aware (Yes)', 'Unaware (No)']
    averages = [avg_aware, avg_unaware]

    plt.figure(figsize=(8, 6))
    plt.bar(groups, averages, color=['skyblue', 'lightcoral'])
    plt.title('Average Impact on Desire to Pursue Graduate Degree by Awareness')
    plt.ylabel('Average Impact Score (1-5)')
    plt.ylim(0, 5.5)  # Scale up to 5.5 to show 5 clearly
    for i, v in enumerate(averages):
        plt.text(i, v + 0.1, f"{v:.2f}", ha='center', va='bottom')

    plt.savefig(output_chart)
    print(f"Chart saved as {output_chart}")

    # Generate Report
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write("# Awareness Analysis Report\n\n")
        f.write("## Does early awareness of the alternative pathway correlate with a decreased desire to pursue a graduate degree?\n\n")
        f.write("### Methodology\n\n")
        f.write("We analyzed the survey responses focusing on two questions:\n")
        f.write("- **Awareness**: \"Were you aware of the alternative pathway to CPA licensure before taking the survey?\" (Column Q53 in the dataset, referred to as Q31 in the task description).\n")
        f.write("- **Impact**: \"How has the availability of (or knowledge about) the alternative pathway to CPA licensure impacted your desire to pursue a graduate degree?\" (Column Q52).\n\n")
        f.write("The responses to the impact question (Q52) were mapped to a numerical scale:\n")
        f.write("- Significantly decreased desire = 1\n")
        f.write("- Decreased desire = 2\n")
        f.write("- No change in desire = 3\n")
        f.write("- Increased desire = 4\n")
        f.write("- Significantly increased desire = 5\n\n")
        f.write("### Results\n\n")
        f.write("| Group (Awareness) | Average Impact Score | Sample Size |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write(f"| Yes (Aware) | {avg_aware:.2f} | {len(scores_aware)} |\n")
        f.write(f"| No (Unaware) | {avg_unaware:.2f} | {len(scores_unaware)} |\n\n")

        f.write("### Visualization\n\n")
        f.write(f"![Average Impact Score by Awareness Group]({output_chart})\n\n")

        f.write("### Summary\n\n")
        if avg_aware < avg_unaware:
            diff = avg_unaware - avg_aware
            f.write(f"Those who were **aware** of the alternative pathway had a **lower** average desire score ({avg_aware:.2f}) compared to those who were unaware ({avg_unaware:.2f}). This suggests a potential correlation between early awareness and a decreased desire to pursue a graduate degree.\n")
        elif avg_aware > avg_unaware:
            diff = avg_aware - avg_unaware
            f.write(f"Those who were **aware** of the alternative pathway had a **higher** average desire score ({avg_aware:.2f}) compared to those who were unaware ({avg_unaware:.2f}). This suggests early awareness might not correlate with a decreased desire.\n")
        else:
            f.write(f"Both groups had the same average desire score ({avg_aware:.2f}). There appears to be no significant difference based on awareness.\n")

if __name__ == "__main__":
    analyze_survey()
