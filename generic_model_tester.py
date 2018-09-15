import csv
import tensorflow as tf
import numpy as np
import random

# import the different model types

# stacking model
from rnn_architectures.stacking_model.moving_window.stacking_model_tester import StackingModelTester

# seq2seq model with decoder
from rnn_architectures.seq2seq_model.with_decoder.non_moving_window.seq2seq_model_tester import Seq2SeqModelTester as Seq2SeqModelTesterWithNonMovingWindow
from rnn_architectures.seq2seq_model.with_decoder.moving_window.window_per_step.seq2seq_model_tester import Seq2SeqModelTester as Seq2SeqModelTesterWithMovingWindow
from rnn_architectures.seq2seq_model.with_decoder.moving_window.one_input_per_step.seq2seq_model_tester import Seq2SeqModelTester as Seq2SeqModelTesterWithMovingWindowOneInputPerStep

# seq2seq model with dense layer
from rnn_architectures.seq2seq_model.with_dense_layer.non_moving_window.seq2seq_model_tester import Seq2SeqModelTesterWithDenseLayer

# attention model
from rnn_architectures.attention_model.bahdanau_attention.without_seasonality.non_moving_window.attention_model_tester import AttentionModelTester as AttentionModelTesterWithNonMovingWindow
from rnn_architectures.attention_model.bahdanau_attention.without_seasonality.moving_window.attention_model_tester import AttentionModelTester as AttentionModelTesterWithMovingWindow

# import the cocob optimizer
from external_packages import cocob_optimizer
from utility_scripts.invoke_r_final_evaluation import invoke_r_script

from configs.global_configs import model_testing_configs

LSTM_USE_PEEPHOLES = True
BIAS = False

learning_rate = 0.0

# function to create the optimizer
def adagrad_optimizer_fn(total_loss):
    return tf.train.AdagradOptimizer(learning_rate=learning_rate).minimize(total_loss)

def adam_optimizer_fn(total_loss):
    return tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(total_loss)

def cocob_optimizer_fn(total_loss):
    return cocob_optimizer.COCOB().minimize(loss=total_loss)

def testing(args, config_dictionary):

    # argument_parser = argparse.ArgumentParser("Test different forecasting models on different datasets")
    # argument_parser.add_argument('--binary_train_file', required=True, help='The tfrecords file for train dataset')
    # argument_parser.add_argument('--binary_test_file', required=True, help='The tfrecords file for test dataset')
    # argument_parser.add_argument('--input_size', required=True, help='The input size of the dataset')
    # argument_parser.add_argument('--forecast_horizon', required=True, help='The forecast horizon of the dataset')
    # argument_parser.add_argument('--optimizer', required = True, help = 'The type of the optimizer(cocob/adam/adagrad...)')
    # argument_parser.add_argument('--hyperparameter_tuning', required=True,
    #                              help='The method for hyperparameter tuning(bayesian/smac)')
    # argument_parser.add_argument('--model_type', required=True, help='The type of the model(stacking/non_moving_window/attention)')
    #
    # # parse the user arguments
    # args = argument_parser.parse_args()

    # to make the random number choices reproducible
    np.random.seed(1)
    random.seed(1)

    global learning_rate

    dataset_name = args.dataset_name
    contain_zero_values = args.contain_zero_values
    binary_train_file_path_test_mode = args.binary_train_file_test_mode
    binary_test_file_path_test_mode = args.binary_test_file_test_mode
    txt_test_file_path = args.txt_test_file
    actual_results_file_path = args.actual_results_file
    if(args.input_size):
        input_size = int(args.input_size)
    else:
        input_size = 0
    output_size = int(args.forecast_horizon)
    optimizer = args.optimizer
    hyperparameter_tuning = args.hyperparameter_tuning
    model_type = args.model_type
    input_format = args.input_format

    print("Model Testing Started for {}_{}_{}_{}_{}".format(dataset_name, model_type, input_format, hyperparameter_tuning, optimizer))

    # select the optimizer
    if optimizer == "cocob":
        optimizer_fn = cocob_optimizer_fn
    elif optimizer == "adagrad":
        optimizer_fn = adagrad_optimizer_fn
    elif optimizer == "adam":
        optimizer_fn = adam_optimizer_fn

    # select the model type
    if model_type == "stacking":
        model_tester = StackingModelTester(
            use_bias=BIAS,
            use_peepholes=LSTM_USE_PEEPHOLES,
            input_size=input_size,
            output_size=output_size,
            binary_train_file_path=binary_train_file_path_test_mode,
            binary_test_file_path=binary_test_file_path_test_mode
        )
    elif model_type == "seq2seq":
        if input_format == "non_moving_window":
            model_tester = Seq2SeqModelTesterWithNonMovingWindow(
                use_bias=BIAS,
                use_peepholes=LSTM_USE_PEEPHOLES,
                output_size=output_size,
                binary_train_file_path=binary_train_file_path_test_mode,
                binary_test_file_path=binary_test_file_path_test_mode
            )
        elif input_format == "moving_window":
            model_tester = Seq2SeqModelTesterWithMovingWindow(
                use_bias=BIAS,
                use_peepholes=LSTM_USE_PEEPHOLES,
                input_size=input_size,
                output_size=output_size,
                binary_train_file_path=binary_train_file_path_test_mode,
                binary_test_file_path=binary_test_file_path_test_mode
            )
        elif input_format == "moving_window_one_input_per_step":
            model_tester = Seq2SeqModelTesterWithMovingWindowOneInputPerStep(
                use_bias=BIAS,
                use_peepholes=LSTM_USE_PEEPHOLES,
                input_size=input_size,
                output_size=output_size,
                binary_train_file_path=binary_train_file_path_test_mode,
                binary_test_file_path=binary_test_file_path_test_mode
            )

    elif model_type == "seq2seqwithdenselayer":
        model_tester = Seq2SeqModelTesterWithDenseLayer(
            use_bias=BIAS,
            use_peepholes=LSTM_USE_PEEPHOLES,
            output_size=output_size,
            binary_train_file_path=binary_train_file_path_test_mode,
            binary_test_file_path=binary_test_file_path_test_mode
        )
    elif model_type == "attention":
        if input_format == "non_moving_window":
            model_tester = AttentionModelTesterWithNonMovingWindow(
                use_bias=BIAS,
                use_peepholes=LSTM_USE_PEEPHOLES,
                output_size=output_size,
                binary_train_file_path=binary_train_file_path_test_mode,
                binary_test_file_path=binary_test_file_path_test_mode
            )
        elif input_format == "moving_window":
            model_tester = AttentionModelTesterWithMovingWindow(
                use_bias=BIAS,
                use_peepholes=LSTM_USE_PEEPHOLES,
                input_size=input_size,
                output_size=output_size,
                binary_train_file_path=binary_train_file_path_test_mode,
                binary_test_file_path=binary_test_file_path_test_mode
            )

    if 'learning_rate' in config_dictionary:
        learning_rate = config_dictionary['learning_rate']
    num_hidden_layers = config_dictionary['num_hidden_layers']
    max_num_epochs = config_dictionary['max_num_epochs']
    max_epoch_size = config_dictionary['max_epoch_size']
    lstm_cell_dimension = config_dictionary['lstm_cell_dimension']
    l2_regularization = config_dictionary['l2_regularization']
    minibatch_size = config_dictionary['minibatch_size']
    gaussian_noise_stdev = config_dictionary['gaussian_noise_stdev']

    list_of_forecasts = model_tester.test_model(num_hidden_layers = int(round(num_hidden_layers)),
                                      lstm_cell_dimension = int(round(lstm_cell_dimension)),
                                      minibatch_size = int(round(minibatch_size)),
                                      max_epoch_size = int(round(max_epoch_size)),
                                      max_num_epochs = int(round(max_num_epochs)),
                                      l2_regularization = l2_regularization,
                                      gaussian_noise_stdev = gaussian_noise_stdev,
                                      optimizer_fn = optimizer_fn)

    # write the forecasting results to a file
    forecast_file_path = model_testing_configs.FORECASTS_DIRECTORY + dataset_name + '_' + model_type + '_' + input_format + '_' + hyperparameter_tuning + '_' + optimizer + '.txt'

    with open(forecast_file_path, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(list_of_forecasts)

    # invoke the final evaluation R script
    error_file_name = dataset_name + '_' + model_type + '_' + input_format + '_' + hyperparameter_tuning + '_' + optimizer + '.txt'

    if(input_format == "moving_window"):
        invoke_r_script((forecast_file_path, error_file_name, txt_test_file_path, actual_results_file_path, str(input_size), str(output_size), contain_zero_values), True)
    else:
        invoke_r_script((forecast_file_path, error_file_name, txt_test_file_path, actual_results_file_path, str(output_size), contain_zero_values), False)




