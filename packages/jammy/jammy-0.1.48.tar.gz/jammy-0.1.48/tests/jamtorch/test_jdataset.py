from jamtorch.jdatasets import Points2Dataset


def test_toy_dataset():
    dataset = Points2Dataset("swissroll", 1000, 0.0)
    for i in range(10):
        print(dataset[i])


# pytest -s tests/jamtorch/test_jdataset.py
