import pytest
import math
import numpy as np
import pandas as pd
import os.path
from cm_tpm import CMImputer

class TestClass:
    def test_instance(self):
        """Test the instantiation of the CMImputer class."""
        imputer = CMImputer()
        assert imputer is not None

    def test_parameters(self):
        """Test the model parameters."""
        imputer = CMImputer(
            missing_values="",
            n_components_train=16,
            n_components_impute=8,
            latent_dim=8,
            top_k=10,
            lo=True,
            pc_type="spn",
            imputation_method="optimization",
            ordinal_features=None,
            max_depth=3,
            custom_net=None,
            hidden_layers=4,
            neurons_per_layer=128,
            activation="Tanh",
            batch_norm=True,
            dropout_rate=0.3,
            max_iter=100,
            batch_size_train=16,
            batch_size_impute=8,
            tol=1e-3,
            patience=8,
            lr=0.01,
            weight_decay=1e-3,
            use_gpu=False,
            random_state=42,
            verbose=2,
            copy=False,
            keep_empty_features=False,
        )
        assert imputer.missing_values == ""
        assert imputer.n_components_train == 16
        assert imputer.n_components_impute == 8
        assert imputer.latent_dim == 8
        assert imputer.top_k == 10
        assert imputer.lo
        assert imputer.pc_type == "spn"
        assert imputer.imputation_method == "optimization"
        assert imputer.ordinal_features is None
        assert imputer.max_depth == 3
        assert imputer.custom_net is None
        assert imputer.hidden_layers == 4
        assert imputer.neurons_per_layer == 128
        assert imputer.activation == "Tanh"
        assert imputer.batch_norm
        assert imputer.dropout_rate == 0.3
        assert imputer.max_iter == 100
        assert imputer.batch_size_train == 16
        assert imputer.batch_size_impute == 8
        assert imputer.tol == 1e-3
        assert imputer.patience == 8
        assert imputer.lr == 0.01
        assert imputer.weight_decay == 1e-3
        assert not imputer.use_gpu
        assert imputer.random_state == 42
        assert imputer.verbose == 2
        assert not imputer.copy
        assert not imputer.keep_empty_features

    def test_attributes(self):
        """Test the model attributes."""
        imputer = CMImputer(random_state=42)
        assert not imputer.is_fitted_
        assert imputer.n_features_in_ is None
        assert imputer.feature_names_in_ is None
        assert imputer.input_dimension_ is None
        assert imputer.log_likelihood_ is None
        assert imputer.training_likelihoods_ is None
        assert imputer.imputing_likelihoods_ is None
        assert imputer.min_vals_ == 0.0
        assert imputer.max_vals_ == 1.0
        assert imputer.binary_info_ is None
        assert imputer.integer_info_ is None
        assert imputer.encoding_info_ is None
        assert imputer.bin_encoding_info_ is None
        assert np.array_equal(
            imputer.random_state_.get_state()[1], 
            np.random.RandomState(42).get_state()[1]
        )

class TestSettings():
    def test_custom_settings(self):
        """Test setting custom parameters."""
        imputer = CMImputer(
            settings="custom",
            missing_values="",
            n_components_train=16,
            n_components_impute=8,
            latent_dim=8,
            top_k=10,
            lo=True,
            pc_type="spn",
            imputation_method="optimization",
            ordinal_features=None,
            max_depth=3,
            custom_net=None,
            hidden_layers=4,
            neurons_per_layer=128,
            activation="Tanh",
            batch_norm=True,
            dropout_rate=0.3,
            max_iter=100,
            batch_size_train=16,
            batch_size_impute=8,
            tol=1e-3,
            patience=8,
            lr=0.01,
            weight_decay=1e-3,
            use_gpu=False,
            random_state=42,
            verbose=2,
            copy=False,
            keep_empty_features=False,
        )
        assert imputer.missing_values == ""
        assert imputer.n_components_train == 16
        assert imputer.n_components_impute == 8
        assert imputer.latent_dim == 8
        assert imputer.top_k == 10
        assert imputer.lo
        assert imputer.pc_type == "spn"
        assert imputer.imputation_method == "optimization"
        assert imputer.ordinal_features is None
        assert imputer.max_depth == 3
        assert imputer.custom_net is None
        assert imputer.hidden_layers == 4
        assert imputer.neurons_per_layer == 128
        assert imputer.activation == "Tanh"
        assert imputer.batch_norm
        assert imputer.dropout_rate == 0.3
        assert imputer.max_iter == 100
        assert imputer.batch_size_train == 16
        assert imputer.batch_size_impute == 8
        assert imputer.tol == 1e-3
        assert imputer.patience == 8
        assert imputer.lr == 0.01
        assert imputer.weight_decay == 1e-3
        assert not imputer.use_gpu
        assert imputer.random_state == 42
        assert imputer.verbose == 2
        assert not imputer.copy
        assert not imputer.keep_empty_features

    def test_fast_settings(self):
        """Test setting fast parameters."""
        imputer = CMImputer(
            settings="fast",
            missing_values="",
        )
        assert imputer.missing_values == ""
        assert imputer.n_components_train == 128
        assert imputer.n_components_impute == 2048
        assert imputer.latent_dim == 4
        assert imputer.top_k is None
        assert imputer.lo == False
        assert imputer.pc_type == "factorized"
        assert imputer.imputation_method == "expectation"
        assert imputer.max_depth == 5
        assert imputer.custom_net is None
        assert imputer.hidden_layers == 2
        assert imputer.neurons_per_layer == 128
        assert imputer.activation == "LeakyReLU"
        assert imputer.batch_norm == False
        assert imputer.dropout_rate == 0.0
        assert imputer.max_iter == 100
        assert imputer.tol == 1e-4
        assert imputer.patience == 10
        assert imputer.lr == 0.001
        assert imputer.weight_decay == 0.01

    def test_balanced_settings(self):
        """Test setting balanced parameters."""
        imputer = CMImputer(
            settings="balanced",
        )
        assert imputer.n_components_train == 256
        assert imputer.n_components_impute == 2048
        assert imputer.latent_dim == 4
        assert imputer.top_k is None
        assert imputer.lo == False
        assert imputer.pc_type == "factorized"
        assert imputer.imputation_method == "expectation"
        assert imputer.max_depth == 5
        assert imputer.custom_net is None
        assert imputer.hidden_layers == 4
        assert imputer.neurons_per_layer == 512
        assert imputer.activation == "LeakyReLU"
        assert imputer.batch_norm == True
        assert imputer.dropout_rate == 0.1
        assert imputer.max_iter == 100
        assert imputer.tol == 1e-4
        assert imputer.patience == 10
        assert imputer.lr == 0.001
        assert imputer.weight_decay == 0.01

    def test_precise_settings(self):
        """Test setting precise parameters."""
        imputer = CMImputer(
            settings="precise",
        )
        assert imputer.n_components_train == 256
        assert imputer.n_components_impute == 1024
        assert imputer.latent_dim == 8
        assert imputer.top_k is None
        assert imputer.lo == False
        assert imputer.pc_type == "factorized"
        assert imputer.imputation_method == "optimization"
        assert imputer.max_depth == 5
        assert imputer.custom_net is None
        assert imputer.hidden_layers == 5
        assert imputer.neurons_per_layer == 1024
        assert imputer.activation == "LeakyReLU"
        assert imputer.batch_norm == True
        assert imputer.dropout_rate == 0.1
        assert imputer.max_iter == 200
        assert imputer.tol == 1e-4
        assert imputer.patience == 10
        assert imputer.lr == 0.001
        assert imputer.weight_decay == 0.01

    def test_invalid_settings(self):
        """Test setting invalid settings."""
        try:
            imputer = CMImputer(
                settings="Yellow",
            )
            assert False
        except ValueError as e:
            assert str(e) == "Unknown settings: 'Yellow'."

class TestFit():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer(n_components_train=4, random_state=0)

    def test_fitted(self):
        """Test the is_fitted_ attribute."""
        assert self.imputer.is_fitted_ == False
        self.imputer.fit(np.array([[1, 2, 3], [4, 5, 6]]))
        assert self.imputer.is_fitted_ == True

    def test_n_features_in(self):
        """Test the n_features_in_ attribute."""
        assert self.imputer.n_features_in_ is None
        self.imputer.fit(np.array([[1, 2, 3], [4, 5, 6]]))
        assert self.imputer.n_features_in_ == 3

    def test_feature_names_in(self):
        """Test the feature_names_in_ attribute."""
        assert self.imputer.feature_names_in_ is None
        self.imputer.fit(pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}))
        assert np.array_equal(self.imputer.feature_names_in_, ["A", "B"])

    def test_no_feature_names(self):
        """Test the feature_names_in_ attribute without feature names."""
        assert self.imputer.n_features_in_ is None
        self.imputer.fit(np.array([[1, 2, 3], [4, 5, 6]]))
        assert self.imputer.feature_names_in_ is None

    def test_fit_numpy(self):
        """Test fitting a NumPy array."""
        X = np.array([[1, 2, 3], [4, 5, 6]])
        imputer = self.imputer.fit(X)
        assert imputer is not None

    def test_fit_dataframe(self):
        """Test fitting a pandas DataFrame."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        imputer = self.imputer.fit(df)
        assert imputer is not None

    def test_fit_list(self):
        """Test fitting a list."""
        X = [[1, 2, 3], [4, 5, 6]]
        imputer = self.imputer.fit(X)
        assert imputer is not None

    def test_fit_file(self):
        """Test fitting data from file."""
        imputer = self.imputer.fit("tests/data/test_data.csv")
        assert imputer is not None

    def test_fit_unsupported(self):
        """Test fitting an unsupported data type."""
        try:
            self.imputer.fit(0)
            assert False
        except TypeError as e:
            assert str(e) == "Unsupported data type: int. Expected NumPy ndarray, pandas DataFrame or list."

    def test_save_fitted_model(self):
        """Test saving a model after fitting."""
        X = np.array([[1, 2, 3], [4, 5, 6]])
        imputer = self.imputer.fit(X, save_model_path="tests/saved_models/test_model_fit/")
        assert os.path.exists("tests/saved_models/test_model_fit/model.pt")
        assert os.path.exists("tests/saved_models/test_model_fit/config.json")

class TestTransform():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer(n_components_train=4, n_components_impute=8, random_state=0)

    def test_transform_no_fit(self):
        """Test transforming data without fitting the imputer."""
        try:
            self.imputer.transform(np.array([[1, 2, 3], [4, 5, 6]]))
            assert False
        except ValueError as e:
            assert str(e) == "The model has not been fitted yet. Please call the fit method first."

    def test_transform_no_missing(self):
        """Test transforming data without missing values."""
        self.imputer.missing_values = -1
        X = np.array([[1, 2, 3], [4, 5, 6]])
        imputer = self.imputer.fit(X)
        with pytest.warns(UserWarning, match="No missing values detected in input data, transformation has no effect. Did you set the correct missing value: '-1'?"):
            X_imputed = imputer.transform(X)
            assert np.array_equal(X_imputed, X)

    def test_transform_numpy(self):
        """Test the transform method on a NumPy array."""
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        imputer = self.imputer.fit(X)
        X_missing = np.array([[np.nan, 2., 3.], [4., 5., 6.]])
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, np.ndarray)
        assert X_imputed.shape == (2, 3)
        assert not np.isnan(X_imputed).any()

    def test_transform_dataframe(self):
        """Test the transform method on a pandas DataFrame."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        imputer = self.imputer.fit(df)
        df_missing = pd.DataFrame({"A": [np.nan, 2., 3.], "B": [4., 5., 6.]})
        X_imputed = imputer.transform(df_missing)
        assert isinstance(X_imputed, pd.DataFrame)
        assert X_imputed.shape == (3, 2)
        assert X_imputed.columns[0] == "A"
        assert X_imputed.columns[1] == "B"
        assert not X_imputed.isnull().values.any()

    def test_transform_list(self):
        """Test the transform method on a list."""
        X = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        imputer = self.imputer.fit(X)
        X_missing = [[np.nan, 2., 3.], [4., 5., 6.]]
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, list)
        assert len(X_imputed) == 2
        assert len(X_imputed[0]) == 3
        assert not np.isnan(X_imputed).any()

    def test_transform_file(self):
        """Test the transform method on a file."""
        if os.path.isfile("tests/data/test_data_imputed.csv"):
            os.remove("tests/data/test_data_imputed.csv")
        imputer = self.imputer.fit("tests/data/test_data.csv", sep=";", decimal=",")
        with pytest.warns(UserWarning, match="No missing values detected in input data, transformation has no effect. Did you set the correct missing value: 'nan'?"):
            X_imputed = imputer.transform("tests/data/test_data.csv", sep=';', decimal=',')
            assert isinstance(X_imputed, np.ndarray)
            assert X_imputed.shape == (10, 3)
            assert os.path.exists("tests/data/test_data_imputed.csv")

    def test_transform_save_path_from_file(self):
        """Test saving the imputed data from a file to a file."""
        try:
            import pyarrow
        except ImportError:
            pytest.skip("pyarrow is not installed, skipping test_transform_save_path_from_file.")
            
        if os.path.isfile("tests/data/test_data_save_path_file.parquet"):
            os.remove("tests/data/test_data_save_path_file.parquet")
        imputer = self.imputer.fit("tests/data/test_data.parquet")
        with pytest.warns(UserWarning, match="No missing values detected in input data, transformation has no effect. Did you set the correct missing value: 'nan'?"):
            X_imputed = imputer.transform("tests/data/test_data.parquet", save_output_path="tests/data/test_data_save_path_file.parquet")
            assert isinstance(X_imputed, np.ndarray)
            assert X_imputed.shape == (10, 3)
            assert os.path.exists("tests/data/test_data_save_path_file.parquet")

    def test_transform_save_path_from_data(self):
        """Test saving the imputed data to a file."""
        try:
            import pyarrow
        except ImportError:
            pytest.skip("pyarrow is not installed, skipping test_transform_save_path_from_data.")

        if os.path.isfile("tests/data/test_data_save_path_data.feather"):
            os.remove("tests/data/test_data_save_path_data.feather")
        X = np.array([[1, 2, 3], [4, 5, 6]])
        imputer = self.imputer.fit(X)
        with pytest.warns(UserWarning, match="No missing values detected in input data, transformation has no effect. Did you set the correct missing value: 'nan'?"):
            X_imputed = imputer.transform(X, save_output_path="tests/data/test_data_save_path_data.feather")
            assert isinstance(X_imputed, np.ndarray)
            assert X_imputed.shape == (2, 3)
            assert os.path.exists("tests/data/test_data_save_path_data.feather")

    def test_transform_non_nan(self):
        """Test the transform method with a different missing value than nan."""
        self.imputer.missing_values = -1
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        imputer = self.imputer.fit(X)
        X_missing = np.array([[-1, 2., 3.], [4., 5., 6.]])
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, np.ndarray)
        assert X_imputed.shape == (2, 3)
        assert not np.any(X_imputed == -1)

    def test_transform_string(self):
        """Test the transform method with a different missing value that is a string."""
        self.imputer.missing_values = ""
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        imputer = self.imputer.fit(X)
        X_missing = np.array([["", 2., 3.], [4., 5., 6.]])
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, np.ndarray)
        assert X_imputed.shape == (2, 3)
        assert not np.any(X_imputed == "")

    def test_transform_multiple_missing(self):
        """Test the transform method with a multiple missing values."""
        self.imputer.missing_values = [-1, ""]
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        imputer = self.imputer.fit(X)
        X_missing = np.array([["", -1, 3.], [4., 5., 6.]])
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, np.ndarray)
        assert X_imputed.shape == (2, 3)
        assert not np.any(X_imputed == "")
        assert not np.any(X_imputed == -1)

    def test_transform_seed(self):
        imputer1 = CMImputer(n_components_train=4, random_state=42)
        imputer2 = CMImputer(n_components_train=4, random_state=42)
        X = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
        imputer1.fit(X)
        imputer2.fit(X)
        X_missing = np.array([[np.nan, 2., 3.], [4., 5., 6.]])
        X_imputed1 = imputer1.transform(X_missing)
        X_imputed2 = imputer2.transform(X_missing)
        assert np.array_equal(X_imputed1, X_imputed2)

    def test_transform_binary(self):
        """Test the transform method with a binary feature."""
        X = np.array([[1, 2, 3], [0, 5, 6], [0, 3, 2]])
        imputer = self.imputer.fit(X)
        X_missing = np.array([[np.nan, 2., 3.], [1, 5., 6.]])
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, np.ndarray)
        assert X_imputed.shape == (2, 3)
        assert not np.isnan(X_imputed).any()
        assert X_imputed[0, 0] == 0 or X_imputed[0, 0] == 1

    def test_transform_non_numeric(self):
        """Test the transform method with a non-numerical feature."""
        X = np.array([["High", 2, 3], ["Medium", 5, 6], ["Low", 3, 2]])
        imputer = self.imputer.fit(X)
        X_missing = np.array([[np.nan, 2., 3.], ["Low", 5., 6.]])
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, np.ndarray)
        assert X_imputed.shape == (2, 3)
        assert X_imputed[0, 0] == "High" or X_imputed[0, 0] == "Medium" or X_imputed[0, 0] == "Low"

    def test_transform_new_value(self):
        """Test an instance where the training data adds a new value to a categorical feature."""
        X_train = np.array([[10, 0.3, "No", "Low"], [5, 0.8, "Yes", "High"], [8, 0.1, "No", "Medium"]])
        self.imputer.n_features_in_ = 4
        self.imputer.binary_info_ = np.array([False, False, True, False])
        self.imputer.encoding_info_ = (np.array([False, False, True, True]), 
                                       {2: {np.str_("No"): 0, np.str_("Yes"): 1},
                                        3: {np.str_("High"): 0, np.str_("Medium"): 1, np.str_("Low"): 2}})
        X_missing = np.array([[5, np.nan, "No", "Extremely High"], [3, 0.5, "No", np.nan], [12, 0.15, "No", "Low"]])
        with pytest.warns(UserWarning, match="New categorical value detected in column 3: 'Extremely High'. Treating this value as missing."):
            imputer = self.imputer.fit(X_train)
            X_imputed = imputer.transform(X_missing)
            assert isinstance(X_imputed, np.ndarray)
            assert X_imputed.shape == (3, 4)
            assert X_imputed[0, 3] == "Extremely High"
            assert X_imputed[1, 3] == "High" or X_imputed[1, 3] == "Medium" or X_imputed[1, 3] == "Low"

    def test_transform_optimization(self):
        """Tests the optimization imputation method"""
        self.imputer.imputation_method = "optimization"
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        imputer = self.imputer.fit(X)
        X_missing = np.array([[np.nan, 2., 3.], [4., 5., 6.]])
        X_imputed = imputer.transform(X_missing)
        assert isinstance(X_imputed, np.ndarray)
        assert X_imputed.shape == (2, 3)
        assert not np.isnan(X_imputed).any()

class TestTransformFromFile():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        imputer = CMImputer(n_components_train=4, n_components_impute=8)
        imputer.fit(X, save_model_path="tests/saved_models/test_model_transform/")

    def test_transform_from_file(self):
        """Test transform function from a model loaded from a file."""
        X_missing = np.array([[1., 2., np.nan], [4., 5., 6.], [7., 8., 9.]])
        X_imputed = CMImputer.transform_from_file(X_missing, load_model_path="tests/saved_models/test_model_transform/")
        assert X_imputed.shape[0] == 3
        assert X_imputed.shape[1] == 3
        assert not np.isnan(X_imputed).any()

    def test_transform_from_file_none(self):
        """Test transform function from a model loaded from no file."""
        X_missing = np.array([[1., 2., np.nan], [4., 5., 6.], [7., 8., 9.]])
        try:
            X_imputed = CMImputer.transform_from_file(X_missing, load_model_path=None)
            assert False
        except ValueError as e:
            assert str(e) == "No model path provided. Either pass a valid `load_model_path`, or create an instance of CMImputer and call `.transform()`."

class TestFitTransform():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer(n_components_train=4, n_components_impute=8)

    def test_fit_transform(self):
        """Test the fit transform function."""
        X_missing = np.array([[1., 2., np.nan], [4., 5., 6.], [7., 8., 9.]])
        X_imputed = self.imputer.fit_transform(X_missing)
        assert X_imputed.shape[0] == 3
        assert X_imputed.shape[1] == 3
        assert not np.isnan(X_imputed).any()

    def test_fit_transform_cpu(self):
        """Test the fit transform function on cpu."""
        self.imputer.use_gpu = False
        X_missing = np.array([[1., 2., np.nan], [4., 5., 6.], [7., 8., 9.]])
        X_imputed = self.imputer.fit_transform(X_missing)
        assert X_imputed.shape[0] == 3
        assert X_imputed.shape[1] == 3
        assert not np.isnan(X_imputed).any()

class TestSaveModel():
    def test_save_model_not_fitted(self):
        """Test saving a model that is not fitted."""
        imputer = CMImputer()
        try:
            imputer.save_model("tests/saved_models/test_model_save/")
            assert False
        except ValueError as e:
            assert str(e) == "The model has not been fitted yet. Please call the fit method first."
    
    def test_save_model(self):
        """Test saving a model that is not fitted."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        imputer = CMImputer(n_components_train=4, n_components_impute=8)
        imputer.fit(X)
        imputer.save_model("tests/saved_models/test_model_save/")
        assert os.path.exists("tests/saved_models/test_model_save/model.pt")
        assert os.path.exists("tests/saved_models/test_model_save/config.json")

class TestLoadModel():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        imputer = CMImputer(n_components_train=4, 
                            n_components_impute=8,
                            latent_dim=8,
                            batch_size_train=512,)
        imputer.fit(X, save_model_path="tests/saved_models/test_model_load/")

    def test_load_model_invalid_location(self):
        """Test loading from a file location where no model files are stored."""
        try:
            imputer = CMImputer.load_model("some/path/")
            assert False
        except FileNotFoundError as e:
            assert str(e) == "No model files found at: 'some/path/'."

    def test_load_model(self):
        """Test loading a model from a file."""
        imputer = CMImputer.load_model("tests/saved_models/test_model_load/")
        assert isinstance(imputer, CMImputer)
        assert imputer.n_components_train == 4
        assert imputer.n_components_impute == 8
        assert imputer.latent_dim == 8
        assert imputer.batch_size_train == 512

        assert imputer.is_fitted_
        assert imputer.n_features_in_ is not None
        assert imputer.input_dimension_ is not None
        assert imputer.training_likelihoods_ is not None
        assert imputer.min_vals_ is not None 
        assert imputer.max_vals_ is not None
        assert imputer.binary_info_ is not None
        assert imputer.integer_info_ is not None
        assert imputer.encoding_info_ is not None
        assert imputer.bin_encoding_info_ is not None

class TestGetFeatureNames():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer()

    def test_model_not_fitted(self):
        """Test the function on a model that is not fitted."""
        try:
            names = self.imputer.get_feature_names_out()
            assert False
        except ValueError as e:
            assert str(e) == "The model has not been fitted yet. Please call the fit method first."

    def test_input_unequal_names(self):
        """Test inputting feature names unequal to the detected feature names."""
        data = {
            'column_1': [1, 2, 3],
            'column_2': [4, 5, 6],
        }
        X = pd.DataFrame(data)
        self.imputer.fit(X)
        try:
            names = self.imputer.get_feature_names_out(input_features=["wrong_name", "also_wrong"])
            assert False
        except ValueError as e:
            assert str(e) == "input_features is not equal to feature_names_in_."

    def test_wrong_input_length(self):
        """Test inputting an invalid amount of feature names."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        self.imputer.fit(X)
        try:
            names = self.imputer.get_feature_names_out(input_features=["column_1", "column_2"])
            assert False
        except ValueError as e:
            assert str(e) == "Expected 3 input features, got 2."

    def test_no_n_features_in(self):
        """Test an instance where n_features_in is not set."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        self.imputer.fit(X)
        self.imputer.n_features_in_ = None
        try:
            names = self.imputer.get_feature_names_out()
            assert False
        except ValueError as e:
            assert str(e) == "Unable to generate feature names without n_features_in."

    def test_no_input(self):
        """Test with no input and with detected names."""
        data = {
            'column_1': [1, 2, 3],
            'column_2': [4, 5, 6],
        }
        X = pd.DataFrame(data)
        self.imputer.fit(X)
        names = self.imputer.get_feature_names_out()
        assert np.array_equal(names, np.array(["column_1", "column_2"]))

    def test_input_and_names(self):
        """Test with input and with detected names."""
        data = {
            'column_1': [1, 2, 3],
            'column_2': [4, 5, 6],
        }
        X = pd.DataFrame(data)
        self.imputer.fit(X)
        names = self.imputer.get_feature_names_out(input_features=["column_1", "column_2"])
        assert np.array_equal(names, np.array(["column_1", "column_2"]))

    def test_input_no_names(self):
        """Test with input but without detected names."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        self.imputer.fit(X)
        names = self.imputer.get_feature_names_out(input_features=["column_1", "column_2", "column_3"])
        assert np.array_equal(names, np.array(["column_1", "column_2", "column_3"]))

    def test_generate(self):
        """Test the generating names option when there is no input and no detected names."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        self.imputer.fit(X)
        names = self.imputer.get_feature_names_out()
        assert np.array_equal(names, np.array(["x0", "x1", "x2"]))

class TestParams():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer(
            missing_values="",
            n_components_train=16,
            n_components_impute=8,
            latent_dim=8,
            top_k=10,
            lo=True,
            pc_type="spn",
            imputation_method="optimization",
            ordinal_features=None,
            max_depth=3,
            custom_net=None,
            hidden_layers=4,
            neurons_per_layer=128,
            activation="Tanh",
            batch_norm=True,
            dropout_rate=0.3,
            max_iter=100,
            batch_size_train=16,
            batch_size_impute=8,
            tol=1e-3,
            patience=8,
            lr=0.01,
            weight_decay=1e-3,
            use_gpu=False,
            random_state=42,
            verbose=2,
            copy=False,
            keep_empty_features=False,
            )

    def test_get_params(self):
        """Test getting parameters."""
        params = self.imputer.get_params()
        assert params["missing_values"] == ""
        assert params["n_components_train"] == 16
        assert params["n_components_impute"] == 8
        assert params["latent_dim"] == 8
        assert params["top_k"] == 10
        assert params["lo"] == True
        assert params["pc_type"] == "spn"
        assert params["imputation_method"] == "optimization"
        assert params["ordinal_features"] is None
        assert params["max_depth"] == 3
        assert params["custom_net"] is None
        assert params["hidden_layers"] == 4
        assert params["neurons_per_layer"] == 128
        assert params["activation"] == "Tanh"
        assert params["batch_norm"] == True
        assert params["dropout_rate"] == 0.3
        assert params["max_iter"] == 100
        assert params["batch_size_train"] == 16
        assert params["batch_size_impute"] == 8
        assert params["tol"] == 1e-3
        assert params["patience"] == 8
        assert params["lr"] == 0.01
        assert params["weight_decay"] == 1e-3
        assert params["use_gpu"] == False
        assert params["random_state"] == 42
        assert params["verbose"] == 2
        assert params["copy"] == False
        assert params["keep_empty_features"] == False

    def test_set_params(self):
        """Test setting parameters."""
        self.imputer.set_params(
            missing_values=np.nan, 
            n_components_train=8,
            n_components_impute=4,
            latent_dim=4,
            top_k=None,
            lo=False,
            pc_type="clt",
            imputation_method="expectation",
            ordinal_features={0: {"Low": 0, "Medium": 1, "High": 2}},
            max_depth=5,
            hidden_layers=2,
            neurons_per_layer=256,
            activation="Sigmoid",
            batch_norm=False,
            dropout_rate=0.5,
            max_iter=200,
            batch_size_train=64,
            batch_size_impute=32,
            tol=1e-4,
            patience=5,
            lr=0.001,
            weight_decay=1e-6,
            use_gpu=True,
            random_state=43,
            verbose=1,
            copy=True,
            keep_empty_features=True,
            )
        assert np.isnan(self.imputer.missing_values)
        assert self.imputer.n_components_train == 8
        assert self.imputer.n_components_impute == 4
        assert self.imputer.latent_dim == 4
        assert self.imputer.top_k is None
        assert self.imputer.lo == False
        assert self.imputer.pc_type == "clt"
        assert self.imputer.imputation_method == "expectation"
        assert self.imputer.ordinal_features == {0: {"Low": 0, "Medium": 1, "High": 2}}
        assert self.imputer.max_depth == 5
        assert self.imputer.hidden_layers == 2
        assert self.imputer.neurons_per_layer == 256
        assert self.imputer.activation == "Sigmoid"
        assert self.imputer.batch_norm == False
        assert self.imputer.dropout_rate == 0.5
        assert self.imputer.max_iter == 200
        assert self.imputer.batch_size_train == 64
        assert self.imputer.batch_size_impute == 32
        assert self.imputer.tol == 1e-4
        assert self.imputer.patience == 5
        assert self.imputer.lr == 0.001
        assert self.imputer.weight_decay == 1e-6
        assert self.imputer.use_gpu == True
        assert self.imputer.random_state == 43
        assert self.imputer.verbose == 1
        assert self.imputer.copy == True
        assert self.imputer.keep_empty_features == True

class TestEvaluate():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer(random_state=42)

    def test_model_not_fitter(self):
        """Test the evaluate function on a model that is not fitted."""
        X = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        try:
            self.imputer.evaluate(X)
            assert False
        except ValueError as e:
            assert str(e) == "The model has not been fitted yet. Please call the fit method first."
    
    def test_evaluate_train_data(self):
        """Test the evaluate function on the train data."""
        X_train = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        self.imputer.fit(X_train)
        log_likelihood = self.imputer.evaluate(X_train)
        assert isinstance(log_likelihood, float)

    def test_evaluate_test_data(self):
        """Test the evaluate function on test data."""
        X_train = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        self.imputer.fit(X_train)
        X_test = np.array([
            [9, 8, 7],
            [3, 2, 1],
        ])
        log_likelihood = self.imputer.evaluate(X_test)
        assert isinstance(log_likelihood, float)

    def test_evaluate_results(self):
        """Test the results of the evaluate function."""
        X_train = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ])
        self.imputer.fit(X_train)
        X_test = np.array([     # Data very different than training data, likelihood should be lower
            [0.1, 100, 0.5],
            [17, 0.5, 152],
        ])
        log_likelihood_train = self.imputer.evaluate(X_train)
        log_likelihood_test = self.imputer.evaluate(X_test)
        assert isinstance(log_likelihood_train, float)
        assert isinstance(log_likelihood_test, float)
        assert log_likelihood_train > log_likelihood_test

class TestApplySettings():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer()

    def test_invalid_settings(self):
        """Test setting an invalid setting option."""
        setting = "invalid_setting"
        try:
            self.imputer._apply_preset_settings(setting)
            assert False
        except ValueError as e:
            assert str(e) == "Unknown settings: 'invalid_setting'."

    def test_apply_fast(self):
        """Test applying the fast setting"""
        setting = "fast"
        self.imputer._apply_preset_settings(setting)
        assert self.imputer.n_components_train == 128
        assert self.imputer.n_components_impute == 2048
        assert self.imputer.latent_dim == 4
        assert self.imputer.top_k is None
        assert self.imputer.lo == False
        assert self.imputer.pc_type == "factorized"
        assert self.imputer.imputation_method == "expectation"
        assert self.imputer.max_depth == 5
        assert self.imputer.custom_net is None
        assert self.imputer.hidden_layers == 2
        assert self.imputer.neurons_per_layer == 128
        assert self.imputer.activation == "LeakyReLU"
        assert self.imputer.batch_norm == False
        assert self.imputer.dropout_rate == 0.0
        assert self.imputer.max_iter == 100
        assert self.imputer.tol == 1e-4
        assert self.imputer.patience == 10
        assert self.imputer.lr == 0.001
        assert self.imputer.weight_decay == 0.01

    def test_apply_balanced(self):
        """Test applying the balanced setting"""
        setting = "balanced"
        self.imputer._apply_preset_settings(setting)
        assert self.imputer.n_components_train == 256
        assert self.imputer.n_components_impute == 2048
        assert self.imputer.latent_dim == 4
        assert self.imputer.top_k is None
        assert self.imputer.lo == False
        assert self.imputer.pc_type == "factorized"
        assert self.imputer.imputation_method == "expectation"
        assert self.imputer.max_depth == 5
        assert self.imputer.custom_net is None
        assert self.imputer.hidden_layers == 4
        assert self.imputer.neurons_per_layer == 512
        assert self.imputer.activation == "LeakyReLU"
        assert self.imputer.batch_norm == True
        assert self.imputer.dropout_rate == 0.1
        assert self.imputer.max_iter == 100
        assert self.imputer.tol == 1e-4
        assert self.imputer.patience == 10
        assert self.imputer.lr == 0.001
        assert self.imputer.weight_decay == 0.01

    def test_apply_precise(self):
        """Test applying the precise setting"""
        setting = "precise"
        self.imputer._apply_preset_settings(setting)
        assert self.imputer.n_components_train == 256
        assert self.imputer.n_components_impute == 1024
        assert self.imputer.latent_dim == 8
        assert self.imputer.top_k is None
        assert self.imputer.lo == False
        assert self.imputer.pc_type == "factorized"
        assert self.imputer.imputation_method == "optimization"
        assert self.imputer.max_depth == 5
        assert self.imputer.custom_net is None
        assert self.imputer.hidden_layers == 5
        assert self.imputer.neurons_per_layer == 1024
        assert self.imputer.activation == "LeakyReLU"
        assert self.imputer.batch_norm == True
        assert self.imputer.dropout_rate == 0.1
        assert self.imputer.max_iter == 200
        assert self.imputer.tol == 1e-4
        assert self.imputer.patience == 10
        assert self.imputer.lr == 0.001
        assert self.imputer.weight_decay == 0.01

class TestConsistency():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer()

    def test_consistent(self):
        """Test an instance where the training and input data are consistent."""
        X_train = np.array([[10, 0.3, "No", "Low"], [5, 0.8, "Yes", "High"], [8, 0.1, "No", "Medium"]])
        self.imputer.n_features_in_ = 4
        self.imputer.binary_info_ = np.array([False, False, True, False])
        self.imputer.encoding_info_ = (np.array([False, False, True, True]), 
                                       {2: {np.str_("No"): 0, np.str_("Yes"): 1},
                                        3: {np.str_("High"): 0, np.str_("Medium"): 1, np.str_("Low"): 2}})
        X_missing = np.array([[5, np.nan, "No", "High"], [3, 0.5, "No", np.nan], [12, 0.15, "No", "Low"]])
        X, mask, info = self.imputer._check_consistency(X_missing)
        assert X.shape == X_missing.shape
        assert self.imputer.encoding_info_ == (mask, info)

    def test_inconsistent_features(self):
        """Test an instance where the training and input data have a different amount of features."""
        X_train = np.array([[10, 0.3, "No", "Low"], [5, 0.8, "Yes", "High"], [8, 0.1, "No", "Medium"]])
        self.imputer.n_features_in_ = 4
        self.imputer.binary_info_ = np.array([False, False, True, False])
        self.imputer.encoding_info_ = (np.array([False, False, True, True]), 
                                       {2: {np.str_("No"): 0, np.str_("Yes"): 1},
                                        3: {np.str_("High"): 0, np.str_("Medium"): 1, np.str_("Low"): 2}})
        X_missing = np.array([[5, np.nan, "No"], [3, 0.5, "No"], [12, 0.15, "No"]])
        try:
            X, mask, info = self.imputer._check_consistency(X_missing)
            assert False
        except ValueError as e:
            assert str(e) == "Mismatch in number of features. Expected 4, got 3."

    def test_inconsistent_cat_to_num(self):
        """Test an instance where the training and input data have a different features (categorical to numerical)."""
        X_train = np.array([[10, 0.3, "No", "Low"], [5, 0.8, "Yes", "High"], [8, 0.1, "No", "Medium"]])
        self.imputer.n_features_in_ = 4
        self.imputer.binary_info_ = np.array([False, False, True, False])
        self.imputer.encoding_info_ = (np.array([False, False, True, True]), 
                                       {2: {np.str_("No"): 0, np.str_("Yes"): 1},
                                        3: {np.str_("High"): 0, np.str_("Medium"): 1, np.str_("Low"): 2}})
        X_missing = np.array([[5, np.nan, 0, "High"], [3, 0.5, 1, np.nan], [12, 0.15, 0, "Low"]])
        try:
            X, mask, info = self.imputer._check_consistency(X_missing)
            assert False
        except ValueError as e:
            assert str(e) == "Feature 2 was categorical during training but numeric in new data."

    def test_inconsistent_num_to_cat(self):
        """Test an instance where the training and input data have a different features (numerical to categorical)."""
        X_train = np.array([[10, 0.3, "No", "Low"], [5, 0.8, "Yes", "High"], [8, 0.1, "No", "Medium"]])
        self.imputer.n_features_in_ = 4
        self.imputer.binary_info_ = np.array([False, False, True, False])
        self.imputer.encoding_info_ = (np.array([False, False, True, True]), 
                                       {2: {np.str_("No"): 0, np.str_("Yes"): 1},
                                        3: {np.str_("High"): 0, np.str_("Medium"): 1, np.str_("Low"): 2}})
        X_missing = np.array([["Yes", np.nan, "No", "High"], ["No", 0.5, "No", np.nan], ["Maybe", 0.15, "No", "Low"]])
        try:
            X, mask, info = self.imputer._check_consistency(X_missing)
            assert False
        except ValueError as e:
            assert str(e) == "Feature 0 was numeric during training but categorical in new data."

    def test_update_encoding(self):
        """Test an instance where the training data adds a new value to a categorical feature."""
        X_train = np.array([[10, 0.3, "No", "Low"], [5, 0.8, "Yes", "High"], [8, 0.1, "No", "Medium"]])
        self.imputer.n_features_in_ = 4
        self.imputer.binary_info_ = np.array([False, False, True, False])
        self.imputer.encoding_info_ = (np.array([False, False, True, True]), 
                                       {2: {np.str_("No"): 0, np.str_("Yes"): 1},
                                        3: {np.str_("High"): 0, np.str_("Medium"): 1, np.str_("Low"): 2}})
        X_missing = np.array([[5, np.nan, "No", "Extremely High"], [3, 0.5, "No", np.nan], [12, 0.15, "No", "Low"]])
        with pytest.warns(UserWarning, match="New categorical value detected in column 3: 'Extremely High'. Treating this value as missing."):
            X, mask, info = self.imputer._check_consistency(X_missing)
            assert X.shape == X_missing.shape
            assert np.array_equal(mask, np.array([False, False, True, True]))
            assert info == {2: {np.str_("No"): 0, np.str_("Yes"): 1},
                            3: {np.str_("High"): 0, np.str_("Medium"): 1, np.str_("Low"): 2}}
            assert np.isnan(X[0, 3])

class TestPreprocess():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer()

    def test_preprocess_ints(self):
        """Test preprocessing an array with integers."""
        X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert isinstance(X_preprocessed, np.ndarray)

    def test_preprocess_nan(self):
        """Test preprocessing an array with a missing value."""
        X = np.array([[1., 2., np.nan], [4., 5., 6.], [7., 8., 9.]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert X.shape == X_preprocessed.shape
        assert np.isnan(X_preprocessed[0, 2])

    def test_preprocess_non_nan(self):
        """Test preprocessing an array with a different missing value than NaN."""
        self.imputer.missing_values = -1
        X = np.array([[1., 2., -1], [4., 5., 6.], [7., 8., 9.]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert X.shape == X_preprocessed.shape
        assert np.isnan(X_preprocessed[0, 2])

    def test_preprocess_remove_nan_features(self):
        """Test preprocessing removes NaN features."""
        X = np.array([[1., 2., np.nan], [4., 5., np.nan], [7., 8., np.nan]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert X_preprocessed.shape[0] == 3
        assert X_preprocessed.shape[1] == 2
        assert not np.isnan(X_preprocessed).any()

    def test_preprocess_remove_missing_features(self):
        """Test preprocessing removes other missing features."""
        self.imputer.missing_values = -10
        X = np.array([[1., 2., -10], [4., 5., -10], [7., 8., -10]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert X_preprocessed.shape[0] == 3
        assert X_preprocessed.shape[1] == 2
        assert not np.isnan(X_preprocessed).any()
        assert not np.any(X_preprocessed == -10)

    def test_preprocess_fill_nan_features(self):
        """Test preprocessing fills NaN features."""
        self.imputer.keep_empty_features = True
        X = np.array([[1., 2., np.nan], [4., 5., np.nan], [7., 8., np.nan]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert X_preprocessed[0, 2] == 0
        assert X_preprocessed[1, 2] == 0 
        assert X_preprocessed[2, 2] == 0 

    def test_preprocess_fill_missing_features(self):
        """Test preprocessing fills other missing features."""
        self.imputer.missing_values = -1
        self.imputer.keep_empty_features = True
        X = np.array([[1., 2., -1], [4., 5., -1], [7., 8., -1]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert X_preprocessed[0, 2] == 0
        assert X_preprocessed[1, 2] == 0 
        assert X_preprocessed[2, 2] == 0 

    def test_preprocess_min_max_values(self):
        """Test updating the min and max values while preprocessing."""
        X = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
        X_preprocessed, _, _, _ = self.imputer._preprocess_data(X, train=True)
        assert np.array_equal(self.imputer.min_vals_, np.array([1., 2., 3.]))
        assert np.array_equal(self.imputer.max_vals_, np.array([7., 8., 9.]))
        assert np.array_equal(X_preprocessed, np.array([[0., 0., 0.], [0.5, 0.5, 0.5], [1., 1., 1.]]))

    def test_preprocess_binary_info(self):
        """Test if the binary info is set correctly during preprocessing."""
        X = np.array([[0, 2., 3.], [1, 5., 6.], [0, 8., 9.]])
        X_preprocessed, binary_mask, _, _ = self.imputer._preprocess_data(X, train=True)
        assert np.array_equal(binary_mask, np.array([True, False, False]))
        assert X_preprocessed[0, 0] == 0
        assert X_preprocessed[1, 0] == 1
        assert X_preprocessed[2, 0] == 0

    def test_preprocess_binary_string(self):
        """Test if binary values are converted to 0/1."""
        X = np.array([["Yes", 2., 3.], ["No", 5., 6.], ["Yes", 8., 9.]])
        X_preprocessed, binary_mask, _, _ = self.imputer._preprocess_data(X, train=True)
        assert np.array_equal(binary_mask, np.array([True, False, False]))
        assert X_preprocessed[0, 0] == 1
        assert X_preprocessed[1, 0] == 0
        assert X_preprocessed[2, 0] == 1

    def test_preprocess_binary_float(self):
        """Test if binary floats are converted to 0/1."""
        X = np.array([[0.5, 2., 3.], [-0.5, 5., 6.], [0.5, 8., 9.]])
        X_preprocessed, binary_mask, _, _ = self.imputer._preprocess_data(X, train=True)
        assert np.array_equal(binary_mask, np.array([True, False, False]))
        assert X_preprocessed[0, 0] == 1
        assert X_preprocessed[1, 0] == 0
        assert X_preprocessed[2, 0] == 1

    def test_preprocess_integer_info(self):
        """Test if the binary info is set correctly during preprocessing."""
        X = np.array([[0, 2., 3.], [1, 5., 6.], [0, 8., 9.]])
        X_preprocessed, _, integer_info, _ = self.imputer._preprocess_data(X, train=True)
        assert np.array_equal(integer_info, np.array([True, True, True]))

    def test_preprocess_non_numerical(self):
        """Test if non numerical feature values are converted to integers."""
        X = np.array([["Yes", "Medium", 3.], ["No", "High", 6.], ["Maybe", "Low", 9.]])
        X_preprocessed, binary_mask, integer_mask, (encoding_mask, _) = self.imputer._preprocess_data(X, train=True)
        #assert np.array_equal(binary_mask, np.array([False, False, False]))
        assert np.array_equal(integer_mask, np.array([False, False, True]))
        assert np.array_equal(encoding_mask, np.array([True, True, False]))

class TestImpute():
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for the test class."""
        self.imputer = CMImputer()
        self.imputer.fit(np.array([[1, 2, 3], [4, 5, 6]]))

    def test_no_missing(self):
        """Test imputation when there are no missing values."""
        X_no_missing = np.array([[1, 2, 3]])
        with pytest.warns(UserWarning, match="No missing values detected in input data, transformation has no effect. Did you set the correct missing value: 'nan'?"):
            X_imputed = self.imputer._impute(X_no_missing)
            assert np.array_equal(X_no_missing, X_imputed)

    def test_expectation_impute(self):
        """Test the expectation imputation method."""
        X_missing = np.array([[1, 2, np.nan]])
        X_imputed = self.imputer._impute(X_missing)
        assert not np.isnan(X_imputed).any()
    
    def test_optimization_impute(self):
        """Test the optimization imputation method."""
        self.imputer.imputation_method = "optimization"
        X_missing = np.array([[1, 2, np.nan]])
        X_imputed = self.imputer._impute(X_missing)
        assert not np.isnan(X_imputed).any()
