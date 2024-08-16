import os
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from app.services.image_service import get_image_description
from app.utils.helpers import encode_image
from app.utils.logger import report_logger


def generate_report():
    data = []
    test_data_path = "test-data"
    os.makedirs("report", exist_ok=True)

    report_logger.info("Starting report generation")
    
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
                        "Original Response": "YES",
                        "OpenAI Response": ai_response
                    })

                    print(f"Generated report for {image_name} in {category}")
                    report_logger.info(f"Processed {image_name}. AI Response: {ai_response}")

                except Exception as e:
                    report_logger.error(f"Error processing {image_name}: {str(e)}")
    
    report_logger.info("Generating Excel report")
    df = pd.DataFrame(data)
    df.to_csv(os.path.join("report", "report.csv"), index=False)
    
    report_logger.info("Generating ML evaluation report")
    y_true = [1 if resp == "YES" else 0 for resp in df["Original Response"]]
    y_pred = [1 if resp == "YES" else 0 for resp in df["OpenAI Response"]]
    
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)
    
    with open(os.path.join("report", "ml_report.txt"), "w") as f:
        f.write(f"Precision: {precision}\n")
        f.write(f"Recall: {recall}\n")
        f.write(f"F1 Score: {f1}\n")
        f.write(f"Confusion Matrix:\n{cm}\n")
    
    report_logger.info(f"Precision: {precision}\nRecall: {recall}\nF1 Score: {f1}\nConfusion Matrix:\n{cm}")
    report_logger.info("Report generation completed")
    report_logger.info("+-------------------------------------------------+\n\n\n")