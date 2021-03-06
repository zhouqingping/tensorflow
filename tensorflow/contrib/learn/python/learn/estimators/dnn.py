# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Deep Neural Network estimators."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.contrib import layers
from tensorflow.contrib.learn.python.learn.estimators import _sklearn
from tensorflow.contrib.learn.python.learn.estimators import dnn_linear_combined
from tensorflow.contrib.learn.python.learn.estimators.base import DeprecatedMixin
from tensorflow.python.ops import nn


class DNNClassifier(dnn_linear_combined.DNNLinearCombinedClassifier):
  """A classifier for TensorFlow DNN models.

    Example:
      ```
      installed_app_id = sparse_column_with_hash_bucket("installed_id", 1e6)
      impression_app_id = sparse_column_with_hash_bucket("impression_id", 1e6)

      installed_emb = embedding_column(installed_app_id, dimension=16,
                                       combiner="sum")
      impression_emb = embedding_column(impression_app_id, dimension=16,
                                        combiner="sum")

      estimator = DNNClassifier(
          feature_columns=[installed_emb, impression_emb],
          hidden_units=[1024, 512, 256])

      # Input builders
      def input_fn_train: # returns x, Y
        pass
      estimator.fit(input_fn=input_fn_train)

      def input_fn_eval: # returns x, Y
        pass
      estimator.evaluate(input_fn=input_fn_eval)
      estimator.predict(x=x)
      ```

    Input of `fit` and `evaluate` should have following features,
      otherwise there will be a `KeyError`:
        if `weight_column_name` is not `None`, a feature with
          `key=weight_column_name` whose value is a `Tensor`.
        for each `column` in `feature_columns`:
        - if `column` is a `SparseColumn`, a feature with `key=column.name`
          whose `value` is a `SparseTensor`.
        - if `column` is a `RealValuedColumn, a feature with `key=column.name`
          whose `value` is a `Tensor`.
        - if `feauture_columns` is None, then `input` must contains only real
          valued `Tensor`.

  Parameters:
    hidden_units: List of hidden units per layer. All layers are fully
      connected. Ex. [64, 32] means first layer has 64 nodes and second one has
      32.
    feature_columns: An iterable containing all the feature columns used by the
      model. All items in the set should be instances of classes derived from
      `FeatureColumn`.
    model_dir: Directory to save model parameters, graph and etc.
    n_classes: number of target classes. Default is binary classification.
      It must be greater than 1.
    weight_column_name: A string defining feature column name representing
      weights. It is used to down weight or boost examples during training. It
      will be multiplied by the loss of the example.
    optimizer: An instance of `tf.Optimizer` used to train the model. If `None`,
      will use an Adagrad optimizer.
    activation_fn: Activation function applied to each layer. If `None`, will
      use `tf.nn.relu`.
    dropout: When not None, the probability we will drop out a given coordinate.
    gradient_clip_norm: A float > 0. If provided, gradients are clipped
      to their global norm with this clipping ratio. See tf.clip_by_global_norm
      for more details.
    config: RunConfig object to configure the runtime settings.
  """

  def __init__(self,
               hidden_units,
               feature_columns=None,
               model_dir=None,
               n_classes=2,
               weight_column_name=None,
               optimizer=None,
               activation_fn=nn.relu,
               dropout=None,
               gradient_clip_norm=None,
               config=None):
    super(DNNClassifier, self).__init__(model_dir=model_dir,
                                        n_classes=n_classes,
                                        weight_column_name=weight_column_name,
                                        dnn_feature_columns=feature_columns,
                                        dnn_optimizer=optimizer,
                                        dnn_hidden_units=hidden_units,
                                        dnn_activation_fn=activation_fn,
                                        dnn_dropout=dropout,
                                        gradient_clip_norm=gradient_clip_norm,
                                        config=config)

  def _get_train_ops(self, features, targets):
    """See base class."""
    if self._dnn_feature_columns is None:
      self._dnn_feature_columns = layers.infer_real_valued_columns(features)
    return super(DNNClassifier, self)._get_train_ops(features, targets)

  @property
  def weights_(self):
    return self.dnn_weights_

  @property
  def bias_(self):
    return self.dnn_bias_


class DNNRegressor(dnn_linear_combined.DNNLinearCombinedRegressor):
  """A regressor for TensorFlow DNN models.

    Example:
      ```
      installed_app_id = sparse_column_with_hash_bucket("installed_id", 1e6)
      impression_app_id = sparse_column_with_hash_bucket("impression_id", 1e6)

      installed_emb = embedding_column(installed_app_id, dimension=16,
                                       combiner="sum")
      impression_emb = embedding_column(impression_app_id, dimension=16,
                                        combiner="sum")

      estimator = DNNRegressor(
          feature_columns=[installed_emb, impression_emb],
          hidden_units=[1024, 512, 256])

      # Input builders
      def input_fn_train: # returns x, Y
        pass
      estimator.fit(input_fn=input_fn_train)

      def input_fn_eval: # returns x, Y
        pass
      estimator.evaluate(input_fn=input_fn_eval)
      estimator.predict(x=x)
      ```

    Input of `fit` and `evaluate` should have following features,
      otherwise there will be a `KeyError`:
        if `weight_column_name` is not `None`, a feature with
          `key=weight_column_name` whose value is a `Tensor`.
        for each `column` in `feature_columns`:
        - if `column` is a `SparseColumn`, a feature with `key=column.name`
          whose `value` is a `SparseTensor`.
        - if `column` is a `RealValuedColumn, a feature with `key=column.name`
          whose `value` is a `Tensor`.
        - if `feauture_columns` is None, then `input` must contains only real
          valued `Tensor`.



  Parameters:
    hidden_units: List of hidden units per layer. All layers are fully
      connected. Ex. [64, 32] means first layer has 64 nodes and second one has
      32.
    feature_columns: An iterable containing all the feature columns used by the
      model. All items in the set should be instances of classes derived from
      `FeatureColumn`.
    model_dir: Directory to save model parameters, graph and etc.
    weight_column_name: A string defining feature column name representing
      weights. It is used to down weight or boost examples during training. It
      will be multiplied by the loss of the example.
    optimizer: An instance of `tf.Optimizer` used to train the model. If `None`,
      will use an Adagrad optimizer.
    activation_fn: Activation function applied to each layer. If `None`, will
      use `tf.nn.relu`.
    dropout: When not None, the probability we will drop out a given coordinate.
    gradient_clip_norm: A float > 0. If provided, gradients are clipped
      to their global norm with this clipping ratio. See tf.clip_by_global_norm
      for more details.
    config: RunConfig object to configure the runtime settings.
  """

  def __init__(self,
               hidden_units,
               feature_columns=None,
               model_dir=None,
               weight_column_name=None,
               optimizer=None,
               activation_fn=nn.relu,
               dropout=None,
               gradient_clip_norm=None,
               config=None):
    super(DNNRegressor, self).__init__(
        model_dir=model_dir,
        weight_column_name=weight_column_name,
        dnn_feature_columns=feature_columns,
        dnn_optimizer=optimizer,
        dnn_hidden_units=hidden_units,
        dnn_activation_fn=activation_fn,
        dnn_dropout=dropout,
        gradient_clip_norm=gradient_clip_norm,
        config=config)

  def _get_train_ops(self, features, targets):
    """See base class."""
    if self._dnn_feature_columns is None:
      self._dnn_feature_columns = layers.infer_real_valued_columns(features)
    return super(DNNRegressor, self)._get_train_ops(features, targets)

  @property
  def weights_(self):
    return self.dnn_weights_

  @property
  def bias_(self):
    return self.dnn_bias_


# TensorFlowDNNClassifier and TensorFlowDNNRegressor are deprecated.
class TensorFlowDNNClassifier(DeprecatedMixin, DNNClassifier,
                              _sklearn.ClassifierMixin):
  pass


class TensorFlowDNNRegressor(DeprecatedMixin, DNNRegressor,
                             _sklearn.RegressorMixin):
  pass
