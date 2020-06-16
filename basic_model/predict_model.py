def predict_cover_type(data):
    import pickle
    filename = r"basic_model/svm_model.pkl"
    svm_model = pickle.load(open(filename, 'rb'))
    res = svm_model.predict(data)
    return res