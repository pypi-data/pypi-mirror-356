import boto3


def fit_and_save_classification_model(df, model_obj, x_vars, y_var, expected_classes, save_path):
    """
    Fits a LightGBM object and saves the 
    1) Fitted Model 
    2) Feature Variable List
    3) Class Labels

    Inputs:
        df: pd.DataFrame: training data
        model_obj: i.e. a LightGBM object 
        x_vars: List[str] - feature variables you want to train on 
        y_var: str - groundtruth column 
        expected_classes: List[any] - All the classes that you expect to see. If the model
            doesnt train on one of this class, or trains on something unexpected, an Exception
            will be raised. 
        save_path: str - where you want to save the models
    """
    model_obj.fit(df[x_vars], df[y_var])
    for outcome in model_obj.classes_:
        if outcome not in expected_classes:
            raise Exception(f'Got unexpected class {outcome}.')
    for outcome in expected_classes:
        if outcome not in model_obj.classes_:
            classes_string = ', '.join(list(model_obj.classes_))
            raise Exception(f'Expected to get class {outcome}, but wasnt present in the data. '
                            f'Only classes: {classes_string} were found.')

    if save_path.startswith('s3://'):
        local_model_path = "/tmp/model.txt"
        model_obj.booster_.save_model(local_model_path)
        s3 = boto3.client('s3')
        bucket_name = save_path[5:].split('/')[0]
        key = '/'.join(save_path[5:].split('/')[1:])
        s3.upload_file(local_model_path, bucket_name, key)
    else:
        model_obj.booster_.save_model(f'{save_path}/model.txt')

    with open(f'{save_path}/features.txt', 'w') as f:
        f.write('\n'.join(model_obj.feature_name_))
    with open(f'{save_path}/class_labels.txt', 'w') as f:
        f.write('\n'.join([str(x) for x in model_obj.classes_]))
    print(f'Done training model, saved to folder: {save_path}.')