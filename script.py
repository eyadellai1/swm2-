from selenium import webdriver
import json
import csv
import time


def extract_performance_data():
    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/Software_metric")

    # Allow the page to load and performance metrics to be collected
    time.sleep(5)

    # Get performance data from the browser
    performance_data = driver.execute_script("return window.performance.getEntries();")

    # Save performance data to JSON file
    with open('performance_data.json', 'w') as json_file:
        json.dump(performance_data, json_file, indent=4)

    # Parse performance data for CSV
    parsed_data = [{"name": entry["name"], "duration": entry["duration"]} for entry in performance_data]

    # Save parsed performance data to CSV
    with open('performance_data.csv', 'w', newline='') as csv_file:
        fieldnames = ['name', 'duration']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_data)

    driver.quit()
    return parsed_data


def run_performance_test(iterations=10):
    all_durations = []

    for _ in range(iterations):
        print(f"Run {_ + 1}/{iterations}")
        data = extract_performance_data()
        durations = [entry['duration'] for entry in data]
        all_durations.append(durations)
        time.sleep(1)

    # Calculate average durations
    average_durations = [sum(x) / len(x) for x in zip(*all_durations)]

    # Save average performance data to CSV
    with open('average_performance.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['name', 'average_duration'])
        for name, avg_duration in zip([entry['name'] for entry in data], average_durations):
            writer.writerow([name, avg_duration])


if __name__ == "__main__":
    run_performance_test()
