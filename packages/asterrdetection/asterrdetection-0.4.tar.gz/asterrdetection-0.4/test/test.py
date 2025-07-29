from ast_error_detection import visualize_plain_ast_from_code, visualize_custom_ast_from_code
from ast_error_detection.error_diagnosis import get_typology_based_code_error, get_primary_code_errors

import pandas as pd
import json
import random
from collections import defaultdict


def load_data():
    """Load CSV and JSON data"""
    try:
        # Load CSV file
        df = pd.read_csv('test/submissions.csv')

        # Load JSON file
        with open('test/exercises.json', 'r', encoding='utf-8') as f:
            exercises = json.load(f)

        return df, exercises
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None


def filter_submissions_by_exercise(df):
    """Group submissions by exercise ID and select up to 20 per exercise"""
    filtered_rows = []

    # Group by exercise ID (assuming there's an 'id_exercice' column in the CSV)
    grouped = df.groupby('id_exercice')

    for exercise_id, group in grouped:
        # Select up to 20 random submissions for each exercise
        selected = group.sample(n=min(20, len(group)), random_state=42)
        filtered_rows.append(selected)

    # Concatenate all filtered submissions
    filtered_df = pd.concat(filtered_rows, ignore_index=True)

    # Sort by exercise ID to group submissions by exercise
    filtered_df = filtered_df.sort_values('id_exercice')

    return filtered_df


def display_analysis(submission, exercise, errors):
    """Display the analysis for one submission"""
    print("=" * 80)
    print(f"EXERCISE: {exercise['exerciseTitle']} (ID: {exercise['exerciseId']})")
    print(f"SERIES: {exercise['series']}")
    print(f"TYPE: {exercise['exerciseType']}")
    print("-" * 80)

    print("SUBMITTED CODE:")
    print(submission['code'])
    print("-" * 40)

    print("CORRECT CODE(S):")
    for i, correct_code in enumerate(exercise['correctCodes'], 1):
        print(f"Solution {i}:")
        print(correct_code)
        print()
    print("-" * 40)

    print("TYPOLOGICAL ERRORS:")
    if errors:
        print(errors)

    print("=" * 80)


def main():
    print("Loading data...")
    df, exercises = load_data()

    if df is None or exercises is None:
        print("Failed to load data. Please check your files.")
        return

    print(f"Loaded {len(df)} submissions and {len(exercises)} exercises.")

    # Create exercise lookup dictionary using exerciseId
    exercise_map = {ex['exerciseId']: ex for ex in exercises}

    # Filter submissions to get up to 20 per exercise
    filtered_df = filter_submissions_by_exercise(df)

    if filtered_df.empty:
        print("No submissions found.")
        return

    print(f"Filtered to {len(filtered_df)} submissions.")
    print("Starting analysis... Press Enter to continue to next submission, 'q' to quit.")

    total_analyzed = 0
    current_exercise_id = None
    exercise_count = 0
    skipped_exercises = set()

    # Process each submission
    for idx, submission in filtered_df.iterrows():
        exercise_id = submission['id_exercice']

        # Skip if this exercise was already skipped
        if exercise_id in skipped_exercises:
            continue

        # Check if we're starting a new exercise
        if current_exercise_id != exercise_id:
            current_exercise_id = exercise_id
            exercise_count = 0
            print(f"\n--- Starting new exercise: ID {exercise_id} ---")
            user_input = input("Press Enter to continue, 's' to skip this exercise, or 'q' to quit: ").strip().lower()
            if user_input == 'q':
                print(f"Analysis stopped. Analyzed {total_analyzed} submissions total.")
                return
            elif user_input == 's':
                skipped_exercises.add(exercise_id)
                print(f"Exercise {exercise_id} skipped.")
                continue

        exercise_count += 1

        # Find the corresponding exercise from JSON
        if exercise_id not in exercise_map:
            print(f"Warning: Exercise ID {exercise_id} not found in exercises.json")
            continue

        exercise = exercise_map[exercise_id]

        print(f"\n[Exercise {exercise_id} - Submission {exercise_count}] Analyzing...")

        # Get typological errors
        try:
            errors = get_typology_based_code_error(submission['code'], exercise['correctCodes'])
        except (SyntaxError, TypeError):
            errors = "Syntax Error"  # or [] or any default fallback

        # Display analysis
        display_analysis(submission, exercise, errors)

        total_analyzed += 1

        # Wait for user input
        user_input = input("\nPress Enter to continue, 'q' to quit: ").strip().lower()
        if user_input == 'q':
            print(f"Analysis stopped. Analyzed {total_analyzed} submissions total.")
            return

    print(f"\nAnalysis complete! Analyzed {total_analyzed} submissions total.")


if __name__ == "__main__":
    main()
