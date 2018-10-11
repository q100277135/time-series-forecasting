# configs for the model training
class model_training_configs:
    INFO_FREQ = 1

# configs for the model testing
class model_testing_configs:
    RNN_FORECASTS_DIRECTORY = 'results/rnn_forecasts/'
    SNAIVE_FORECASTS_DIRECTORY = 'results/snaive_forecasts/'

# configs for hyperparameter tuning(bayesian optimization/SMAC3)
class hyperparameter_tuning_configs:
    BAYESIAN_INIT_POINTS = 2
    BAYESIAN_NUM_ITER = 30
    SMAC_RUNCOUNT_LIMIT = 30

class training_data_configs:
    SHUFFLE_BUFFER_SIZE = 10000