import boto3
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME


def upload_to_s3(bucket_name, filename):
    """Method to upload files to s3 bucket"""
    s3 = boto3.client(
        "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )
    bucket_resource = s3
    bucket_resource.upload_file(Bucket=BUCKET_NAME, Filename=filename, Key=filename)


def main():
    # Load Dataset
    iris = load_iris()
    data, labels = iris.data, iris.target
    # 70%/30% split
    training_data, test_data, training_labels, test_labels = train_test_split(
        data, labels, test_size=0.30
    )
    # Logistics Regression Model
    model = LogisticRegression(multi_class="multinomial", max_iter=200)
    # Train Model
    model.fit(training_data, training_labels)
    # Score Model
    accuracy = model.score(test_data, test_labels)
    # Print Accuracy
    print("Accuracy: {:.2f}".format(accuracy))

    # save the model
    pickle.dump(model, open("model.pkl", "wb"))
    # upload model
    upload_to_s3(BUCKET_NAME, "model.pkl")


if __name__ == '__main__':
    main()
