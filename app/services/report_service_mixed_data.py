import os
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from app.services.image_service import get_image_description
from app.utils.helpers import encode_image
from app.utils.logger import report_logger
import matplotlib.pyplot as plt
import seaborn as sns


def generate_report_for_mixed_data():
    data = []
    test_data_path = "test-data-v2"
    os.makedirs("report-v2", exist_ok=True)

    report_logger.info("Starting report generation for mixed data")
    
    for category in os.listdir(test_data_path):
        category_path = os.path.join(test_data_path, category)
        if os.path.isdir(category_path):
            report_logger.info(f"Processing category: {category}")
            for image_name in os.listdir(category_path):
                image_path = os.path.join(category_path, image_name)
                report_logger.info(f"Processing image: {image_name}")

                try:
                    with open(image_path, "rb") as image_file:
                        base64_image = encode_image(image_file.read())
                    
                    response = get_image_description(category, base64_image)
                    if "yes" in response.lower():
                        ai_response = "YES"
                    else:
                        ai_response = "NO"
                    
                    data.append({
                        "Image Name": image_name,
                        "Category Name": category,
                        "OpenAI Response": ai_response
                    })

                    print(f"Generated report for {image_name} in {category}")
                    report_logger.info(f"Processed {image_name}. AI Response: {ai_response}")

                except Exception as e:
                    report_logger.error(f"Error processing {image_name}: {str(e)}")
    
    report_logger.info("Generating Excel report")
    df = pd.DataFrame(data)
    df.to_csv(os.path.join("report-v2", "report.csv"), index=False)
    
    report_logger.info("Report generation completed")
    report_logger.info("+-------------------------------------------------+\n\n\n")



def create_bar_chart(data, title, filename):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(data.keys()), y=list(data.values()))
    plt.title(title)
    plt.ylim(0, 1)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"report-v2/{filename}.png")
    plt.close()



def create_confusion_matrix_heatmap(cm, title, filename):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['NO', 'YES'], yticklabels=['NO', 'YES'])
    plt.title(title)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(f"report-v2/{filename}.png")
    plt.close()




def perform_sanity_checks(df):
    issues = []
    if df.isnull().values.any():
        issues.append("Data contains null values")
    if not set(df["OpenAI Response"].unique()) <= {"YES", "NO"}:
        issues.append("OpenAI Response column contains values other than YES/NO")
    if not set(df["Original Response"].unique()) <= {"YES", "NO"}:
        issues.append("Original Response column contains values other than YES/NO")
    return issues


def calculate_metrics(y_true, y_pred):
    precision = precision_score(y_true, y_pred, pos_label="YES")
    recall = recall_score(y_true, y_pred, pos_label="YES")
    f1 = f1_score(y_true, y_pred, pos_label="YES")
    cm = confusion_matrix(y_true, y_pred, labels=["YES", "NO"])
    return precision, recall, f1, cm


def get_report():
    # Read the CSV file
    df = pd.read_csv("report-v2/report.csv")
    # Perform sanity checks
    issues = perform_sanity_checks(df)
    if issues:
        return {"error": "Data sanity check failed", "issues": issues}
    
    # Calculate overall metrics
    precision, recall, f1, cm = calculate_metrics(df["Original Response"], df["OpenAI Response"])

    # Create visualizations for overall metrics
    create_bar_chart(
        {"Precision": precision, "Recall": recall, "F1 Score": f1},
        "Overall Metrics",
        "overall_metrics"
    )
    create_confusion_matrix_heatmap(cm, "Overall Confusion Matrix", "overall_confusion_matrix")

    # Calculate metrics per category
    categories = df["Category Name"].unique()
    category_metrics = {}
    for category in categories:
        cat_df = df[df["Category Name"] == category]
        cat_precision, cat_recall, cat_f1, cat_cm = calculate_metrics(
            cat_df["Original Response"], cat_df["OpenAI Response"]
        )
        category_metrics[category] = {
            "precision": cat_precision,
            "recall": cat_recall,
            "f1_score": cat_f1,
            "confusion_matrix": cat_cm.tolist()
        }

        # Create visualizations for each category
        create_bar_chart(
            {"Precision": cat_precision, "Recall": cat_recall, "F1 Score": cat_f1},
            f"Metrics for {category}",
            f"category_metrics_{category.replace(' ', '_').lower()}"
        )
        create_confusion_matrix_heatmap(
            cat_cm,
            f"Confusion Matrix for {category}",
            f"category_confusion_matrix_{category.replace(' ', '_').lower()}"
        )

    # Prepare the report
    report = {
        "overall_metrics": {
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "confusion_matrix": cm.tolist()
        },
        "category_metrics": category_metrics,
        "total_images": len(df),
        "categories": categories.tolist(),
        "sanity_check": "Passed" if not issues else "Failed",
        "sanity_check_issues": issues
    }

    # Save the report to a text file in user-friendly format
    with open("report-v2/report.txt", "w") as f:
        f.write("Overall Metrics\n")
        f.write(f"Precision: {precision}\n")
        f.write(f"Recall: {recall}\n")
        f.write(f"F1 Score: {f1}\n")
        f.write(f"Confusion Matrix:\n{cm}\n\n")

        f.write("Category-wise Metrics\n")
        for category, metrics in category_metrics.items():
            f.write(f"Category: {category}\n")
            f.write(f"Precision: {metrics['precision']}\n")
            f.write(f"Recall: {metrics['recall']}\n")
            f.write(f"F1 Score: {metrics['f1_score']}\n")
            f.write(f"Confusion Matrix:\n{metrics['confusion_matrix']}\n\n")
            f.write(f"(See category_metrics_{category.replace(' ', '_').lower()}.png and "
                    f"category_confusion_matrix_{category.replace(' ', '_').lower()}.png "
                    f"for visualizations)\n\n")

        f.write("Sanity Check\n")
        if issues:
            f.write("Data sanity check failed. Issues:\n")
            for issue in issues:
                f.write(f"- {issue}\n")
        else:
            f.write("Data sanity check passed\n")

    return report