from neural_network_model import __version__ as _version
from neural_network_model.predict import (make_single_prediction)


def test_make_prediction_on_sample(charlock_dir):
    # Given
    filename = '1.png'
    # For testing the code, we only use a small sample which produces a
    # poor model, so we cannot guarantee what prediction it will make for the
    # test image. Therefore, allow any prediction from those available in
    # the small sample of data.
    allowable_classifications = ['Black-grass', 'Charlock', 'Fat Hen']

    # When
    results = make_single_prediction(image_directory=charlock_dir,
                                     image_name=filename)

    # Then
    assert results['predictions'] is not None
    assert results['readable_predictions'][0] in allowable_classifications
    assert results['version'] == _version
