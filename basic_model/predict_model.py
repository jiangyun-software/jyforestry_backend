def predict_cover_type(data):
    import pickle
    filename = r"jyforestry_server/basic_model/svm_model.pkl"
    svm_model = pickle.load(open(filename, 'rb'))
    res = svm_model.predict(data)[0]
    return res