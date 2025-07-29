# actix/activations_tf.py

import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras import activations as keras_standard_activations
from tensorflow.keras import constraints

# --- Helper Functions for TF Activations ---

def tf_lambertw_principal(z, iterations=8):
    """
    Computes the principal branch of the Lambert W function using Newton's method.
    W(z) such that W(z) * exp(W(z)) = z.
    Assumes z >= 0, for which W_0(z) >= 0.
    """
    w = tf.where(z < 1.0, z, tf.math.log(z + 1e-38))
    w = tf.maximum(w, 0.0)
    for _ in range(iterations):
        ew = tf.math.exp(w)
        w_ew_minus_z = w * ew - z
        denominator = ew * (w + 1.0) + 1e-20
        delta_w = w_ew_minus_z / denominator
        w = w - delta_w
        w = tf.maximum(w, 0.0)
    return w

def tf_ellipj_cn(u, m, num_terms=4):
    """
    Computes the Jacobi elliptic function cn(u,m) using a series expansion.
    cn(u,m) = 1 - u^2/2! + u^4/4! (1+4m) - u^6/6! (1+44m+16m^2) + ...
    """
    u_sq = tf.square(u)
    cn_val = tf.ones_like(u)
    if num_terms > 1:
        term1_val = -u_sq / 2.0
        cn_val = cn_val + term1_val
    if num_terms > 2:
        u_4 = u_sq * u_sq
        term2_val = (u_4 / 24.0) * (1.0 + 4.0 * m)
        cn_val = cn_val + term2_val
    if num_terms > 3:
        u_6 = u_4 * u_sq
        term3_val = -(u_6 / 720.0) * (1.0 + 44.0 * m + 16.0 * tf.square(m))
        cn_val = cn_val + term3_val
    cn_val = tf.clip_by_value(cn_val, -1.0, 1.0)
    return cn_val

# --- Custom Constraint for EllipticGaussianActivation ---
class ClipConstraint(constraints.Constraint):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, w):
        return tf.clip_by_value(w, self.min_value, self.max_value)

    def get_config(self):
        return {'min_value': self.min_value, 'max_value': self.max_value}

# --- Parametric Activation Functions (Keras Layers) ---

class OptimA(Layer):
    """
    OptimA: An 'Optimal Activation' function with trainable parameters.
    f(x) = alpha * tanh(beta * x) + gamma * softplus(delta * x) * sigmoid(lambda_ * x)
    """
    def __init__(self, **kwargs):
        super(OptimA, self).__init__(**kwargs)

    def build(self, input_shape):
        """Defines the trainable weights (parameters) of the activation function."""
        self.alpha = self.add_weight(name='alpha', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.gamma = self.add_weight(name='gamma', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.lambda_ = self.add_weight(name='lambda_param', shape=(), initializer='ones', trainable=True) # Renamed from lambda
        super(OptimA, self).build(input_shape)

    def call(self, x):
        """Defines the forward pass of the activation function."""
        term1 = self.alpha * tf.math.tanh(self.beta * x)
        term2 = self.gamma * tf.math.softplus(self.delta * x) * tf.math.sigmoid(self.lambda_ * x)
        return term1 + term2

    def get_config(self):
        """Ensures the layer can be saved and loaded."""
        config = super(OptimA, self).get_config()
        return config

class ParametricPolyTanh(Layer):
    """f(x) = alpha * tanh(beta * x^2 + gamma_ppt * x + delta_ppt)"""
    def __init__(self, **kwargs):
        super(ParametricPolyTanh, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_ppt = self.add_weight(name='alpha_ppt', shape=(), initializer='ones', trainable=True)
        self.beta_ppt = self.add_weight(name='beta_ppt', shape=(), initializer='ones', trainable=True)
        self.gamma_ppt = self.add_weight(name='gamma_ppt', shape=(), initializer='zeros', trainable=True)
        self.delta_ppt = self.add_weight(name='delta_ppt', shape=(), initializer='zeros', trainable=True)
        super(ParametricPolyTanh, self).build(input_shape)
    def call(self, x):
        return self.alpha_ppt * tf.math.tanh(self.beta_ppt * tf.square(x) + self.gamma_ppt * x + self.delta_ppt)
    def get_config(self): return super(ParametricPolyTanh, self).get_config()

class AdaptiveRationalSoftsign(Layer):
    """f(x) = (alpha * x) / (1 + |beta * x|^gamma)"""
    def __init__(self, **kwargs):
        super(AdaptiveRationalSoftsign, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_ars = self.add_weight(name='alpha_ars', shape=(), initializer='ones', trainable=True)
        self.beta_ars = self.add_weight(name='beta_ars', shape=(), initializer='ones', trainable=True)
        self.gamma_ars = self.add_weight(name='gamma_ars', shape=(), initializer=tf.keras.initializers.Constant(2.0), trainable=True)
        super(AdaptiveRationalSoftsign, self).build(input_shape)
    def call(self, x):
        return (self.alpha_ars * x) / (tf.constant(1.0, dtype=x.dtype) + tf.math.pow(tf.abs(self.beta_ars * x), self.gamma_ars))
    def get_config(self): return super(AdaptiveRationalSoftsign, self).get_config()

class OptimXTemporal(Layer):
    """f(x) = alpha * tanh(beta * x) + gamma * sigmoid(delta * x)"""
    def __init__(self, **kwargs):
        super(OptimXTemporal, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_oxt = self.add_weight(name='alpha_oxt', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.beta_oxt = self.add_weight(name='beta_oxt', shape=(), initializer='ones', trainable=True)
        self.gamma_oxt = self.add_weight(name='gamma_oxt', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.delta_oxt = self.add_weight(name='delta_oxt', shape=(), initializer='ones', trainable=True)
        super(OptimXTemporal, self).build(input_shape)
    def call(self, x):
        return self.alpha_oxt * tf.math.tanh(self.beta_oxt * x) + self.gamma_oxt * tf.math.sigmoid(self.delta_oxt * x)
    def get_config(self): return super(OptimXTemporal, self).get_config()

class ParametricGaussianActivation(Layer):
    """f(x) = alpha * x * exp(-beta * x^2)"""
    def __init__(self, **kwargs):
        super(ParametricGaussianActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_pga = self.add_weight(name='alpha_pga', shape=(), initializer='ones', trainable=True)
        self.beta_pga = self.add_weight(name='beta_pga', shape=(), initializer='ones', trainable=True)
        super(ParametricGaussianActivation, self).build(input_shape)
    def call(self, x):
        return self.alpha_pga * x * tf.math.exp(-self.beta_pga * tf.square(x))
    def get_config(self): return super(ParametricGaussianActivation, self).get_config()

class LearnableFourierActivation(Layer):
    """f(x) = alpha * sin(beta * x + gamma_shift) + delta * cos(lambda_param * x + phi)"""
    def __init__(self, **kwargs):
        super(LearnableFourierActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_lfa = self.add_weight(name='alpha_lfa', shape=(), initializer='ones', trainable=True)
        self.beta_lfa = self.add_weight(name='beta_lfa', shape=(), initializer='ones', trainable=True)
        self.gamma_shift_lfa = self.add_weight(name='gamma_shift_lfa', shape=(), initializer='zeros', trainable=True)
        self.delta_lfa = self.add_weight(name='delta_lfa', shape=(), initializer='ones', trainable=True)
        self.lambda_param_lfa = self.add_weight(name='lambda_param_lfa', shape=(), initializer='ones', trainable=True)
        self.phi_lfa = self.add_weight(name='phi_lfa', shape=(), initializer='zeros', trainable=True)
        super(LearnableFourierActivation, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha_lfa * tf.math.sin(self.beta_lfa * x + self.gamma_shift_lfa)
        term2 = self.delta_lfa * tf.math.cos(self.lambda_param_lfa * x + self.phi_lfa)
        return term1 + term2
    def get_config(self): return super(LearnableFourierActivation, self).get_config()

class A_ELuC(Layer):
    """f(x) = alpha * ELU(beta * x) + gamma * x * sigmoid(delta * x)"""
    def __init__(self, **kwargs):
        super(A_ELuC, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_aeluc = self.add_weight(name='alpha_aeluc', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.beta_aeluc = self.add_weight(name='beta_aeluc', shape=(), initializer='ones', trainable=True)
        self.gamma_aeluc = self.add_weight(name='gamma_aeluc', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.delta_aeluc = self.add_weight(name='delta_aeluc', shape=(), initializer='ones', trainable=True)
        super(A_ELuC, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha_aeluc * keras_standard_activations.elu(self.beta_aeluc * x)
        term2 = self.gamma_aeluc * x * tf.math.sigmoid(self.delta_aeluc * x)
        return term1 + term2
    def get_config(self): return super(A_ELuC, self).get_config()

class ParametricSmoothStep(Layer):
    """f(x) = alpha * sigmoid(beta_slope*(x - gamma_shift)) - alpha * sigmoid(delta_slope*(x + mu_shift))"""
    def __init__(self, **kwargs):
        super(ParametricSmoothStep, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_pss = self.add_weight(name='alpha_pss', shape=(), initializer='ones', trainable=True)
        self.beta_slope_pss = self.add_weight(name='beta_slope_pss', shape=(), initializer='ones', trainable=True)
        self.gamma_shift_pss = self.add_weight(name='gamma_shift_pss', shape=(), initializer='zeros', trainable=True)
        self.delta_slope_pss = self.add_weight(name='delta_slope_pss', shape=(), initializer='ones', trainable=True)
        self.mu_shift_pss = self.add_weight(name='mu_shift_pss', shape=(), initializer='zeros', trainable=True)
        super(ParametricSmoothStep, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha_pss * tf.math.sigmoid(self.beta_slope_pss * (x - self.gamma_shift_pss))
        term2 = self.alpha_pss * tf.math.sigmoid(self.delta_slope_pss * (x + self.mu_shift_pss))
        return term1 - term2
    def get_config(self): return super(ParametricSmoothStep, self).get_config()

class AdaptiveBiHyperbolic(Layer):
    """f(x) = alpha * tanh(beta * x) + (1-alpha) * tanh^3(gamma_param * x)"""
    def __init__(self, **kwargs):
        super(AdaptiveBiHyperbolic, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_abh = self.add_weight(name='alpha_abh', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.beta_abh = self.add_weight(name='beta_abh', shape=(), initializer='ones', trainable=True)
        self.gamma_param_abh = self.add_weight(name='gamma_param_abh', shape=(), initializer='ones', trainable=True)
        super(AdaptiveBiHyperbolic, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha_abh * tf.math.tanh(self.beta_abh * x)
        term2 = (tf.constant(1.0, dtype=x.dtype) - self.alpha_abh) * tf.math.pow(tf.math.tanh(self.gamma_param_abh * x), 3)
        return term1 + term2
    def get_config(self): return super(AdaptiveBiHyperbolic, self).get_config()

class ParametricLogish(Layer):
    """f(x) = alpha * x * sigmoid(beta * x)"""
    def __init__(self, **kwargs):
        super(ParametricLogish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_pl = self.add_weight(name='alpha_pl', shape=(), initializer='ones', trainable=True)
        self.beta_pl = self.add_weight(name='beta_pl', shape=(), initializer='ones', trainable=True)
        super(ParametricLogish, self).build(input_shape)
    def call(self, x):
        return self.alpha_pl * x * tf.math.sigmoid(self.beta_pl * x)
    def get_config(self): return super(ParametricLogish, self).get_config()

class AdaptSigmoidReLU(Layer):
    """f(x) = alpha * x * sigmoid(beta * x) + gamma_param * ReLU(delta * x)"""
    def __init__(self, **kwargs):
        super(AdaptSigmoidReLU, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha_asr = self.add_weight(name='alpha_asr', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.beta_asr = self.add_weight(name='beta_asr', shape=(), initializer='ones', trainable=True)
        self.gamma_param_asr = self.add_weight(name='gamma_param_asr', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.delta_asr = self.add_weight(name='delta_asr', shape=(), initializer='ones', trainable=True)
        super(AdaptSigmoidReLU, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha_asr * x * tf.math.sigmoid(self.beta_asr * x)
        term2 = self.gamma_param_asr * keras_standard_activations.relu(self.delta_asr * x)
        return term1 + term2
    def get_config(self): return super(AdaptSigmoidReLU, self).get_config()

class ParametricLambertWActivation(Layer):
    """f(x) = alpha * x * W(|beta| * exp(gamma * x)) where W is the Lambert W function."""
    def __init__(self, **kwargs):
        super(ParametricLambertWActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_plw', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_plw', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_plw', shape=(), initializer='ones', trainable=True)
        super(ParametricLambertWActivation, self).build(input_shape)
    def call(self, x):
        arg_lambertw = tf.abs(self.beta) * tf.math.exp(self.gamma * x)
        lambertw_val = tf_lambertw_principal(arg_lambertw)
        return self.alpha * x * lambertw_val
    def get_config(self): return super(ParametricLambertWActivation, self).get_config()

class AdaptiveHyperbolicLogarithm(Layer):
    """f(x) = alpha * asinh(beta * x) + gamma * log(|delta| + x^2)"""
    def __init__(self, **kwargs):
        super(AdaptiveHyperbolicLogarithm, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_ahl', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_ahl', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_ahl', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_ahl', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        super(AdaptiveHyperbolicLogarithm, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha * tf.math.asinh(self.beta * x)
        term2 = self.gamma * tf.math.log(tf.math.abs(self.delta) + tf.math.square(x) + 1e-7)
        return term1 + term2
    def get_config(self): return super(AdaptiveHyperbolicLogarithm, self).get_config()

class ParametricGeneralizedGompertzActivation(Layer):
    """f(x) = alpha * exp(-beta * exp(-gamma * x)) - delta"""
    def __init__(self, **kwargs):
        super(ParametricGeneralizedGompertzActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_pgga', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_pgga', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_pgga', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_pgga', shape=(), initializer='zeros', trainable=True)
        super(ParametricGeneralizedGompertzActivation, self).build(input_shape)
    def call(self, x):
        return self.alpha * tf.math.exp(-self.beta * tf.math.exp(-self.gamma * x)) - self.delta
    def get_config(self): return super(ParametricGeneralizedGompertzActivation, self).get_config()

class ComplexHarmonicActivation(Layer):
    """f(x) = alpha * tanh(beta * x) + gamma * sin(delta * x^2 + lambda)"""
    def __init__(self, **kwargs):
        super(ComplexHarmonicActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_cha', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_cha', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_cha', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_cha', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_cha', shape=(), initializer='zeros', trainable=True)
        super(ComplexHarmonicActivation, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha * tf.math.tanh(self.beta * x)
        term2 = self.gamma * tf.math.sin(self.delta * tf.math.square(x) + self.lambda_)
        return term1 + term2
    def get_config(self): return super(ComplexHarmonicActivation, self).get_config()

class WeibullSoftplusActivation(Layer):
    """f(x) = alpha * x * sigmoid(beta * (x - gamma)) + delta * (1 - exp(-|lambda| * |x|^|mu|))"""
    def __init__(self, **kwargs):
        super(WeibullSoftplusActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_wsa', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_wsa', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_wsa', shape=(), initializer='zeros', trainable=True)
        self.delta = self.add_weight(name='delta_wsa', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_wsa', shape=(), initializer='ones', trainable=True)
        self.mu = self.add_weight(name='mu_wsa', shape=(), initializer='ones', trainable=True)
        super(WeibullSoftplusActivation, self).build(input_shape)
    def call(self, x):
        term1 = self.alpha * x * tf.math.sigmoid(self.beta * (x - self.gamma))
        weibull_exponent = tf.math.abs(self.lambda_) * tf.math.pow(tf.math.abs(x) + 1e-7, tf.math.abs(self.mu))
        term2 = self.delta * (1.0 - tf.math.exp(-weibull_exponent))
        return term1 + term2
    def get_config(self): return super(WeibullSoftplusActivation, self).get_config()

class AdaptiveErfSwish(Layer):
    """f(x) = alpha * x * erf(beta * x) * sigmoid(gamma * x)"""
    def __init__(self, **kwargs):
        super(AdaptiveErfSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_aes', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_aes', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_aes', shape=(), initializer='ones', trainable=True)
        super(AdaptiveErfSwish, self).build(input_shape)
    def call(self, x):
        return self.alpha * x * tf.math.erf(self.beta * x) * tf.math.sigmoid(self.gamma * x)
    def get_config(self): return super(AdaptiveErfSwish, self).get_config()

class ParametricBetaSoftsign(Layer):
    """f(x) = alpha * sign(x) * (|x|^|beta|) / (1 + |x|^|gamma|)"""
    def __init__(self, **kwargs):
        super(ParametricBetaSoftsign, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_pbs', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_pbs', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_pbs', shape=(), initializer='ones', trainable=True)
        super(ParametricBetaSoftsign, self).build(input_shape)
    def call(self, x):
        abs_x = tf.math.abs(x)
        pow_beta = tf.math.pow(abs_x, tf.math.abs(self.beta))
        pow_gamma = tf.math.pow(abs_x, tf.math.abs(self.gamma))
        return self.alpha * (pow_beta / (1.0 + pow_gamma + 1e-7)) * tf.math.sign(x)
    def get_config(self): return super(ParametricBetaSoftsign, self).get_config()

class ParametricArcSinhGate(Layer):
    """f(x) = alpha * x * asinh(beta * x)"""
    def __init__(self, **kwargs):
        super(ParametricArcSinhGate, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_pasg', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_pasg', shape=(), initializer='ones', trainable=True)
        super(ParametricArcSinhGate, self).build(input_shape)
    def call(self, x):
        return self.alpha * x * tf.math.asinh(self.beta * x)
    def get_config(self): return super(ParametricArcSinhGate, self).get_config()

class GeneralizedAlphaSigmoid(Layer):
    """f(x) = (alpha * x) / (1 + |beta * x|^|gamma|)^(1/|delta|)"""
    def __init__(self, **kwargs):
        super(GeneralizedAlphaSigmoid, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_gas', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_gas', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_gas', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_gas', shape=(), initializer='ones', trainable=True)
        super(GeneralizedAlphaSigmoid, self).build(input_shape)
    def call(self, x):
        abs_beta_x = tf.math.abs(self.beta * x)
        pow_gamma = tf.math.pow(abs_beta_x, tf.math.abs(self.gamma))
        denominator_base = 1.0 + pow_gamma
        inv_delta = 1.0 / (tf.math.abs(self.delta) + 1e-7)
        denominator = tf.math.pow(denominator_base, inv_delta)
        return (self.alpha * x) / (denominator + 1e-7)
    def get_config(self): return super(GeneralizedAlphaSigmoid, self).get_config()

class EllipticGaussianActivation(Layer):
    """f(x) = x * exp(-cn(x, m)) where cn is the Jacobi elliptic function."""
    def __init__(self, **kwargs):
        super(EllipticGaussianActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.m_param = self.add_weight(name='m_ega', shape=(),
                                 initializer=tf.keras.initializers.Constant(0.5),
                                 constraint=ClipConstraint(0.0, 1.0),
                                 trainable=True)
        super(EllipticGaussianActivation, self).build(input_shape)
    def call(self, x):
        cn_val = tf_ellipj_cn(x, self.m_param)
        return x * tf.math.exp(-cn_val)
    def get_config(self): return super(EllipticGaussianActivation, self).get_config()

class ParametricTanhSwish(Layer):
    """f(x) = alpha * x * tanh(beta * x) * sigmoid(gamma * x)"""
    def __init__(self, **kwargs):
        super(ParametricTanhSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_pts', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_pts', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_pts', shape=(), initializer='ones', trainable=True)
        super(ParametricTanhSwish, self).build(input_shape)
    def call(self, x):
        return self.alpha * x * tf.math.tanh(self.beta * x) * tf.math.sigmoid(self.gamma * x)
    def get_config(self): return super(ParametricTanhSwish, self).get_config()

class GeneralizedHarmonicSwish(Layer):
    """f(x) = alpha * x * sin(beta * x^2 + gamma) * sigmoid(delta * x)"""
    def __init__(self, **kwargs):
        super(GeneralizedHarmonicSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_ghs', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_ghs', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_ghs', shape=(), initializer='zeros', trainable=True)
        self.delta = self.add_weight(name='delta_ghs', shape=(), initializer='ones', trainable=True)
        super(GeneralizedHarmonicSwish, self).build(input_shape)
    def call(self, x):
        harmonic_part = tf.math.sin(self.beta * tf.math.square(x) + self.gamma)
        swish_gate = x * tf.math.sigmoid(self.delta * x)
        return self.alpha * swish_gate * harmonic_part
    def get_config(self): return super(GeneralizedHarmonicSwish, self).get_config()

class A_STReLU(Layer):
    """f(x) = alpha * ReLU(x) + beta * x * sigmoid(gamma * x) + delta * tanh(lambda * x)"""
    def __init__(self, **kwargs):
        super(A_STReLU, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_astrelu', shape=(), initializer=tf.keras.initializers.Constant(0.33), trainable=True)
        self.beta = self.add_weight(name='beta_astrelu', shape=(), initializer=tf.keras.initializers.Constant(0.33), trainable=True)
        self.gamma = self.add_weight(name='gamma_astrelu', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_astrelu', shape=(), initializer=tf.keras.initializers.Constant(0.33), trainable=True)
        self.lambda_ = self.add_weight(name='lambda_astrelu', shape=(), initializer='ones', trainable=True)
        super(A_STReLU, self).build(input_shape)
    def call(self, x):
        relu_part = self.alpha * keras_standard_activations.relu(x)
        swish_part = self.beta * x * tf.math.sigmoid(self.gamma * x)
        tanh_part = self.delta * tf.math.tanh(self.lambda_ * x)
        return relu_part + swish_part + tanh_part
    def get_config(self): return super(A_STReLU, self).get_config()

class ETU(Layer):
    """ExponentialTanhUnit: f(x) = alpha * tanh(beta * x) * e^(-gamma * x^2)"""
    def __init__(self, **kwargs):
        super(ETU, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_etu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_etu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_etu', shape=(), initializer='ones', trainable=True)
        super(ETU, self).build(input_shape)
    def call(self, x):
        return self.alpha * tf.math.tanh(self.beta * x) * tf.math.exp(-self.gamma * tf.math.square(x))
    def get_config(self): return super(ETU, self).get_config()

class PMGLU(Layer):
    """Parametric Multi-Gated Linear Unit: f(x) = (alpha * x + beta) * sigmoid(gamma * x + delta) * tanh(lambda * x)"""
    def __init__(self, **kwargs):
        super(PMGLU, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_pmglu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_pmglu', shape=(), initializer='zeros', trainable=True)
        self.gamma = self.add_weight(name='gamma_pmglu', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_pmglu', shape=(), initializer='zeros', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_pmglu', shape=(), initializer='ones', trainable=True)
        super(PMGLU, self).build(input_shape)
    def call(self, x):
        linear_part = self.alpha * x + self.beta
        sigmoid_gate = tf.math.sigmoid(self.gamma * x + self.delta)
        tanh_gate = tf.math.tanh(self.lambda_ * x)
        return linear_part * sigmoid_gate * tanh_gate
    def get_config(self): return super(PMGLU, self).get_config()

class GPOSoft(Layer):
    """Generalized Parametric Oscillatory Softplus: f(x) = alpha * softplus(beta * x) + gamma * sin(delta * x + lambda)"""
    def __init__(self, **kwargs):
        super(GPOSoft, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_gpos', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_gpos', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_gpos', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_gpos', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_gpos', shape=(), initializer='zeros', trainable=True)
        super(GPOSoft, self).build(input_shape)
    def call(self, x):
        softplus_part = self.alpha * tf.math.softplus(self.beta * x)
        oscillatory_part = self.gamma * tf.math.sin(self.delta * x + self.lambda_)
        return softplus_part + oscillatory_part
    def get_config(self): return super(GPOSoft, self).get_config()

class SHLU(Layer):
    """Sigmoid-Harmonic Linear Unit: f(x)= (alpha * x) * sigmoid(beta * x) + gamma * cos(delta * x^2 + lambda)"""
    def __init__(self, **kwargs):
        super(SHLU, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_shlu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_shlu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_shlu', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_shlu', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_shlu', shape=(), initializer='zeros', trainable=True)
        super(SHLU, self).build(input_shape)
    def call(self, x):
        swish_part = self.alpha * x * tf.math.sigmoid(self.beta * x)
        harmonic_part = self.gamma * tf.math.cos(self.delta * tf.math.square(x) + self.lambda_)
        return swish_part + harmonic_part
    def get_config(self): return super(SHLU, self).get_config()

class GaussSwish(Layer):
    """Gaussian Parametric Swish: f(x) = (alpha * x) * sigmoid(beta * x) * exp(-gamma * x^2)"""
    def __init__(self, **kwargs):
        super(GaussSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_gps', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_gps', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_gps', shape=(), initializer='ones', trainable=True)
        super(GaussSwish, self).build(input_shape)
    def call(self, x):
        swish_part = self.alpha * x * tf.math.sigmoid(self.beta * x)
        gaussian_part = tf.math.exp(-self.gamma * tf.math.square(x))
        return swish_part * gaussian_part
    def get_config(self): return super(GaussSwish, self).get_config()

class ATanSigU(Layer):
    """Adaptive ArcTanSigmoid Unit: f(x) = alpha * arctan(beta * x) + gamma * x * sigmoid(delta * x)"""
    def __init__(self, **kwargs):
        super(ATanSigU, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_atansu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_atansu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_atansu', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_atansu', shape=(), initializer='ones', trainable=True)
        super(ATanSigU, self).build(input_shape)
    def call(self, x):
        arctan_part = self.alpha * tf.math.atan(self.beta * x)
        swish_part = self.gamma * x * tf.math.sigmoid(self.delta * x)
        return arctan_part + swish_part
    def get_config(self): return super(ATanSigU, self).get_config()

class PAPG(Layer):
    """Parametric Adaptive Polynomial Gate: f(x) = (alpha * x + beta * x^3) / (1 + |gamma * x|^delta) + lambda * x * sigmoid(mu * x)"""
    def __init__(self, **kwargs):
        super(PAPG, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_papg', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_papg', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_papg', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_papg', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_papg', shape=(), initializer='ones', trainable=True)
        self.mu = self.add_weight(name='mu_papg', shape=(), initializer='ones', trainable=True)
        super(PAPG, self).build(input_shape)
    def call(self, x):
        numerator = self.alpha * x + self.beta * tf.math.pow(x, 3)
        denominator = 1.0 + tf.math.pow(tf.math.abs(self.gamma * x), self.delta)
        poly_gate_part = numerator / (denominator + 1e-7)
        swish_part = self.lambda_ * x * tf.math.sigmoid(self.mu * x)
        return poly_gate_part + swish_part
    def get_config(self): return super(PAPG, self).get_config()

class SwishLogTanh(Layer):
    """f(x) = alpha * x * sigmoid(beta * x) + gamma * tanh(softplus(delta * x))"""
    def __init__(self, **kwargs):
        super(SwishLogTanh, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_slt', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_slt', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_slt', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_slt', shape=(), initializer='ones', trainable=True)
        super(SwishLogTanh, self).build(input_shape)
    def call(self, x):
        swish_part = self.alpha * x * tf.math.sigmoid(self.beta * x)
        log_tanh_part = self.gamma * tf.math.tanh(tf.math.softplus(self.delta * x))
        return swish_part + log_tanh_part
    def get_config(self): return super(SwishLogTanh, self).get_config()

class ArcGaLU(Layer):
    """f(x) = alpha * arctan(beta * x) + gamma * x * sigmoid(delta * x + lambda)"""
    def __init__(self, **kwargs):
        super(ArcGaLU, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_arcgalu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_arcgalu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_arcgalu', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_arcgalu', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_arcgalu', shape=(), initializer='zeros', trainable=True)
        super(ArcGaLU, self).build(input_shape)
    def call(self, x):
        arctan_part = self.alpha * tf.math.atan(self.beta * x)
        gated_linear_part = self.gamma * x * tf.math.sigmoid(self.delta * x + self.lambda_)
        return arctan_part + gated_linear_part
    def get_config(self): return super(ArcGaLU, self).get_config()

class ParametricHyperbolicQuadraticActivation(Layer):
    """f(x) = alpha * tanh(beta * x^2 + gamma * x) + delta * x * sigmoid(lambda * x)"""
    def __init__(self, **kwargs):
        super(ParametricHyperbolicQuadraticActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_phqa', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_phqa', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_phqa', shape=(), initializer='zeros', trainable=True)
        self.delta = self.add_weight(name='delta_phqa', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_phqa', shape=(), initializer='ones', trainable=True)
        super(ParametricHyperbolicQuadraticActivation, self).build(input_shape)
    def call(self, x):
        tanh_part = self.alpha * tf.math.tanh(self.beta * tf.square(x) + self.gamma * x)
        swish_part = self.delta * x * tf.math.sigmoid(self.lambda_ * x)
        return tanh_part + swish_part
    def get_config(self): return super(ParametricHyperbolicQuadraticActivation, self).get_config()

class RootSoftplus(Layer):
    """f(x) = alpha * x + beta * sqrt(softplus(gamma * x))"""
    def __init__(self, **kwargs):
        super(RootSoftplus, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_rs', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_rs', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_rs', shape=(), initializer='ones', trainable=True)
        super(RootSoftplus, self).build(input_shape)
    def call(self, x):
        linear_part = self.alpha * x
        root_softplus_part = self.beta * tf.math.sqrt(tf.math.softplus(self.gamma * x) + 1e-7)
        return linear_part + root_softplus_part
    def get_config(self): return super(RootSoftplus, self).get_config()

class AdaptiveSinusoidalSoftgate(Layer):
    """f(x) = alpha * x * sigmoid(beta * x) + gamma * sin(delta * x)"""
    def __init__(self, **kwargs):
        super(AdaptiveSinusoidalSoftgate, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_asg', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_asg', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_asg', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_asg', shape=(), initializer='ones', trainable=True)
        super(AdaptiveSinusoidalSoftgate, self).build(input_shape)
    def call(self, x):
        swish_part = self.alpha * x * tf.math.sigmoid(self.beta * x)
        sin_part = self.gamma * tf.math.sin(self.delta * x)
        return swish_part + sin_part
    def get_config(self): return super(AdaptiveSinusoidalSoftgate, self).get_config()

class ExpTanhGatedActivation(Layer):
    """f(x) = alpha * tanh(beta * x) * sigmoid(gamma * exp(delta * x))"""
    def __init__(self, **kwargs):
        super(ExpTanhGatedActivation, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_etg', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_etg', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_etg', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_etg', shape=(), initializer='zeros', trainable=True)
        super(ExpTanhGatedActivation, self).build(input_shape)
    def call(self, x):
        tanh_part = self.alpha * tf.math.tanh(self.beta * x)
        exp_gate = tf.math.sigmoid(self.gamma * tf.math.exp(self.delta * x))
        return tanh_part * exp_gate
    def get_config(self): return super(ExpTanhGatedActivation, self).get_config()

class HybridSinExpUnit(Layer):
    """f(x) = alpha * sin(beta * x) + gamma * x * exp(-delta * x^2)"""
    def __init__(self, **kwargs):
        super(HybridSinExpUnit, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_hseu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_hseu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_hseu', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_hseu', shape=(), initializer='ones', trainable=True)
        super(HybridSinExpUnit, self).build(input_shape)
    def call(self, x):
        sin_part = self.alpha * tf.math.sin(self.beta * x)
        exp_part = self.gamma * x * tf.math.exp(-self.delta * tf.square(x))
        return sin_part + exp_part
    def get_config(self): return super(HybridSinExpUnit, self).get_config()

class ParametricLogarithmicSwish(Layer):
    """f(x) = alpha * x * sigmoid(beta * x) + gamma * log(1 + |delta| * |x|)"""
    def __init__(self, **kwargs):
        super(ParametricLogarithmicSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_plogsw', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_plogsw', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_plogsw', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_plogsw', shape=(), initializer='ones', trainable=True)
        super(ParametricLogarithmicSwish, self).build(input_shape)
    def call(self, x):
        swish_part = self.alpha * x * tf.math.sigmoid(self.beta * x)
        log_part = self.gamma * tf.math.log(1.0 + tf.math.abs(self.delta) * tf.math.abs(x) + 1e-7)
        return swish_part + log_part
    def get_config(self): return super(ParametricLogarithmicSwish, self).get_config()

class AdaptiveCubicSigmoid(Layer):
    """f(x) = alpha * x + beta * x^3 * sigmoid(gamma * x)"""
    def __init__(self, **kwargs):
        super(AdaptiveCubicSigmoid, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_acs', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_acs', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_acs', shape=(), initializer='ones', trainable=True)
        super(AdaptiveCubicSigmoid, self).build(input_shape)
    def call(self, x):
        linear_part = self.alpha * x
        cubic_part = self.beta * tf.math.pow(x, 3) * tf.math.sigmoid(self.gamma * x)
        return linear_part + cubic_part
    def get_config(self): return super(AdaptiveCubicSigmoid, self).get_config()

class SmoothedAbsoluteGatedUnit(Layer):
    """f(x) = alpha * |x| * sigmoid(beta * x) + gamma * x"""
    def __init__(self, **kwargs):
        super(SmoothedAbsoluteGatedUnit, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_sagu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_sagu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_sagu', shape=(), initializer='ones', trainable=True)
        super(SmoothedAbsoluteGatedUnit, self).build(input_shape)
    def call(self, x):
        gated_abs_part = self.alpha * tf.math.abs(x) * tf.math.sigmoid(self.beta * x)
        linear_part = self.gamma * x
        return gated_abs_part + linear_part
    def get_config(self): return super(SmoothedAbsoluteGatedUnit, self).get_config()

class GaussianTanhHarmonicUnit(Layer):
    """f(x) = alpha * tanh(beta * x) + gamma * exp(-delta * (x - lambda)^2)"""
    def __init__(self, **kwargs):
        super(GaussianTanhHarmonicUnit, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_gthhu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_gthhu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_gthhu', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_gthhu', shape=(), initializer='ones', trainable=True)
        self.lambda_ = self.add_weight(name='lambda_gthhu', shape=(), initializer='zeros', trainable=True)
        super(GaussianTanhHarmonicUnit, self).build(input_shape)
    def call(self, x):
        tanh_part = self.alpha * tf.math.tanh(self.beta * x)
        gaussian_part = self.gamma * tf.math.exp(-self.delta * tf.square(x - self.lambda_))
        return tanh_part + gaussian_part
    def get_config(self): return super(GaussianTanhHarmonicUnit, self).get_config()

class SymmetricParametricRationalSigmoid(Layer):
    """f(x) = (alpha * x) / (1 + |beta * x^2|^gamma)"""
    def __init__(self, **kwargs):
        super(SymmetricParametricRationalSigmoid, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_sprs', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_sprs', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_sprs', shape=(), initializer='ones', trainable=True)
        super(SymmetricParametricRationalSigmoid, self).build(input_shape)
    def call(self, x):
        denominator = 1.0 + tf.pow(tf.abs(self.beta * tf.square(x)), self.gamma)
        return (self.alpha * x) / (denominator + 1e-7)
    def get_config(self): return super(SymmetricParametricRationalSigmoid, self).get_config()

class AdaptivePolynomialSwish(Layer):
    """f(x) = alpha * x * sigmoid(beta * x) + gamma * x^2 * sigmoid(delta * x)"""
    def __init__(self, **kwargs):
        super(AdaptivePolynomialSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_apsw', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_apsw', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_apsw', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_apsw', shape=(), initializer='ones', trainable=True)
        super(AdaptivePolynomialSwish, self).build(input_shape)
    def call(self, x):
        swish_part = self.alpha * x * tf.math.sigmoid(self.beta * x)
        poly_swish_part = self.gamma * tf.square(x) * tf.math.sigmoid(self.delta * x)
        return swish_part + poly_swish_part
    def get_config(self): return super(AdaptivePolynomialSwish, self).get_config()

class LogSigmoidGatedElu(Layer):
    """f(x) = alpha * ELU(beta * x) * softplus(gamma * x) * sigmoid(delta * x)"""
    def __init__(self, **kwargs):
        super(LogSigmoidGatedElu, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_lsge', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_lsge', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_lsge', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_lsge', shape=(), initializer='ones', trainable=True)
        super(LogSigmoidGatedElu, self).build(input_shape)
    def call(self, x):
        elu_part = keras_standard_activations.elu(self.beta * x)
        log_gate = tf.math.softplus(self.gamma * x)
        sig_gate = tf.math.sigmoid(self.delta * x)
        return self.alpha * elu_part * log_gate * sig_gate
    def get_config(self): return super(LogSigmoidGatedElu, self).get_config()

class AdaptiveBipolarExponentialUnit(Layer):
    """f(x) = alpha * x + beta * x * exp(-gamma * x^2)"""
    def __init__(self, **kwargs):
        super(AdaptiveBipolarExponentialUnit, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_abexu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_abexu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_abexu', shape=(), initializer='ones', trainable=True)
        super(AdaptiveBipolarExponentialUnit, self).build(input_shape)
    def call(self, x):
        linear_part = self.alpha * x
        exp_part = self.beta * x * tf.math.exp(-self.gamma * tf.square(x))
        return linear_part + exp_part
    def get_config(self): return super(AdaptiveBipolarExponentialUnit, self).get_config()

class ParametricHyperGaussianGate(Layer):
    """f(x) = alpha * x * exp(-beta * |x|^gamma)"""
    def __init__(self, **kwargs):
        super(ParametricHyperGaussianGate, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_phgg', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_phgg', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_phgg', shape=(), initializer='ones', trainable=True)
        super(ParametricHyperGaussianGate, self).build(input_shape)
    def call(self, x):
        gate = tf.math.exp(-tf.abs(self.beta) * tf.pow(tf.abs(x), tf.abs(self.gamma)))
        return self.alpha * x * gate
    def get_config(self): return super(ParametricHyperGaussianGate, self).get_config()

class TanhGatedArcsinhLinearUnit(Layer):
    """f(x) = alpha * x * tanh(beta * asinh(gamma * x))"""
    def __init__(self, **kwargs):
        super(TanhGatedArcsinhLinearUnit, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_tgaslu', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_tgaslu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_tgaslu', shape=(), initializer='ones', trainable=True)
        super(TanhGatedArcsinhLinearUnit, self).build(input_shape)
    def call(self, x):
        gate = tf.math.tanh(self.beta * tf.math.asinh(self.gamma * x))
        return self.alpha * x * gate
    def get_config(self): return super(TanhGatedArcsinhLinearUnit, self).get_config()

class ParametricOddPowerSwish(Layer):
    """f(x) = alpha * x * sigmoid(beta * x) + gamma * x^3"""
    def __init__(self, **kwargs):
        super(ParametricOddPowerSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_popsw', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_popsw', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_popsw', shape=(), initializer='ones', trainable=True)
        super(ParametricOddPowerSwish, self).build(input_shape)
    def call(self, x):
        swish_part = self.alpha * x * tf.math.sigmoid(self.beta * x)
        power_part = self.gamma * tf.math.pow(x, 3)
        return swish_part + power_part
    def get_config(self): return super(ParametricOddPowerSwish, self).get_config()

class AdaptiveLinearLogTanh(Layer):
    """f(x) = alpha * x + beta * tanh(gamma * softplus(delta * x))"""
    def __init__(self, **kwargs):
        super(AdaptiveLinearLogTanh, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_allt', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_allt', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_allt', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_allt', shape=(), initializer='ones', trainable=True)
        super(AdaptiveLinearLogTanh, self).build(input_shape)
    def call(self, x):
        linear_part = self.alpha * x
        log_tanh_part = self.beta * tf.math.tanh(self.gamma * tf.math.softplus(self.delta * x))
        return linear_part + log_tanh_part
    def get_config(self): return super(AdaptiveLinearLogTanh, self).get_config()

class AdaptiveArcTanSwish(Layer):
    """f(x) = α·arctan(β·x) + γ·x·sigmoid(δ·x) + ε·tanh(ζ·x)"""
    def __init__(self, **kwargs):
        super(AdaptiveArcTanSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_aats', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_aats', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_aats', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.delta = self.add_weight(name='delta_aats', shape=(), initializer='ones', trainable=True)
        self.epsilon = self.add_weight(name='epsilon_aats', shape=(), initializer=tf.keras.initializers.Constant(0.3), trainable=True)
        self.zeta = self.add_weight(name='zeta_aats', shape=(), initializer='ones', trainable=True)
        super(AdaptiveArcTanSwish, self).build(input_shape)
    def call(self, x):
        arctan_part = self.alpha * tf.math.atan(self.beta * x)
        swish_part = self.gamma * x * tf.math.sigmoid(self.delta * x)
        tanh_part = self.epsilon * tf.math.tanh(self.zeta * x)
        return arctan_part + swish_part + tanh_part
    def get_config(self): return super(AdaptiveArcTanSwish, self).get_config()

class StabilizedHarmonic(Layer):
    """f(x) = α·tanh(β·x) + γ·sin(δ·tanh(ε·x)) + ζ·x·sigmoid(η·x)"""
    def __init__(self, **kwargs):
        super(StabilizedHarmonic, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_sh', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_sh', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_sh', shape=(), initializer=tf.keras.initializers.Constant(0.2), trainable=True)
        self.delta = self.add_weight(name='delta_sh', shape=(), initializer='ones', trainable=True)
        self.epsilon = self.add_weight(name='epsilon_sh', shape=(), initializer='ones', trainable=True)
        self.zeta = self.add_weight(name='zeta_sh', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.eta = self.add_weight(name='eta_sh', shape=(), initializer='ones', trainable=True)
        super(StabilizedHarmonic, self).build(input_shape)
    def call(self, x):
        tanh_part = self.alpha * tf.math.tanh(self.beta * x)
        sin_part = self.gamma * tf.math.sin(self.delta * tf.math.tanh(self.epsilon * x))
        swish_part = self.zeta * x * tf.math.sigmoid(self.eta * x)
        return tanh_part + sin_part + swish_part
    def get_config(self): return super(StabilizedHarmonic, self).get_config()

class RationalSwish(Layer):
    """f(x) = (α·x·sigmoid(β·x)) / (1 + |γ·x|^δ) + ε·arctan(ζ·x)"""
    def __init__(self, **kwargs):
        super(RationalSwish, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_rs', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_rs', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_rs', shape=(), initializer='ones', trainable=True)
        self.delta = self.add_weight(name='delta_rs', shape=(), initializer=tf.keras.initializers.Constant(1.5), trainable=True)
        self.epsilon = self.add_weight(name='epsilon_rs', shape=(), initializer=tf.keras.initializers.Constant(0.3), trainable=True)
        self.zeta = self.add_weight(name='zeta_rs', shape=(), initializer='ones', trainable=True)
        super(RationalSwish, self).build(input_shape)
    def call(self, x):
        swish_numerator = self.alpha * x * tf.math.sigmoid(self.beta * x)
        rational_denominator = 1.0 + tf.math.pow(tf.math.abs(self.gamma * x) + 1e-7, tf.math.abs(self.delta))
        rational_part = swish_numerator / (rational_denominator + 1e-7)
        arctan_part = self.epsilon * tf.math.atan(self.zeta * x)
        return rational_part + arctan_part
    def get_config(self): return super(RationalSwish, self).get_config()

class AdaptiveGatedUnit(Layer):
    """f(x) = α·x·sigmoid(β·x) + γ·x·tanh(δ·x) + ε·arctan(ζ·x)"""
    def __init__(self, **kwargs):
        super(AdaptiveGatedUnit, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_agu', shape=(), initializer=tf.keras.initializers.Constant(0.4), trainable=True)
        self.beta = self.add_weight(name='beta_agu', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_agu', shape=(), initializer=tf.keras.initializers.Constant(0.4), trainable=True)
        self.delta = self.add_weight(name='delta_agu', shape=(), initializer='ones', trainable=True)
        self.epsilon = self.add_weight(name='epsilon_agu', shape=(), initializer=tf.keras.initializers.Constant(0.2), trainable=True)
        self.zeta = self.add_weight(name='zeta_agu', shape=(), initializer='ones', trainable=True)
        super(AdaptiveGatedUnit, self).build(input_shape)
    def call(self, x):
        sigmoid_gate = self.alpha * x * tf.math.sigmoid(self.beta * x)
        tanh_gate = self.gamma * x * tf.math.tanh(self.delta * x)
        arctan_part = self.epsilon * tf.math.atan(self.zeta * x)
        return sigmoid_gate + tanh_gate + arctan_part
    def get_config(self): return super(AdaptiveGatedUnit, self).get_config()

class ExponentialArcTan(Layer):
    """f(x) = α·arctan(β·x) + γ·x·exp(-δ·|x|) + ε·sigmoid(ζ·x)"""
    def __init__(self, **kwargs):
        super(ExponentialArcTan, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_eat', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_eat', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_eat', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.delta = self.add_weight(name='delta_eat', shape=(), initializer=tf.keras.initializers.Constant(0.1), trainable=True)
        self.epsilon = self.add_weight(name='epsilon_eat', shape=(), initializer=tf.keras.initializers.Constant(0.3), trainable=True)
        self.zeta = self.add_weight(name='zeta_eat', shape=(), initializer='ones', trainable=True)
        super(ExponentialArcTan, self).build(input_shape)
    def call(self, x):
        arctan_part = self.alpha * tf.math.atan(self.beta * x)
        exp_decay = self.gamma * x * tf.math.exp(-tf.math.abs(self.delta * x))
        sigmoid_part = self.epsilon * tf.math.sigmoid(self.zeta * x)
        return arctan_part + exp_decay + sigmoid_part
    def get_config(self): return super(ExponentialArcTan, self).get_config()

class OptimQ(Layer):
    """OptimQ: f(x) = α·arctan(β·x) + γ·x·sigmoid(δ·x) + ε·softplus(ζ·x)·tanh(η·x)"""
    def __init__(self, **kwargs):
        super(OptimQ, self).__init__(**kwargs)
    def build(self, input_shape):
        self.alpha = self.add_weight(name='alpha_oq', shape=(), initializer='ones', trainable=True)
        self.beta = self.add_weight(name='beta_oq', shape=(), initializer='ones', trainable=True)
        self.gamma = self.add_weight(name='gamma_oq', shape=(), initializer=tf.keras.initializers.Constant(0.6), trainable=True)
        self.delta = self.add_weight(name='delta_oq', shape=(), initializer='ones', trainable=True)
        self.epsilon = self.add_weight(name='epsilon_oq', shape=(), initializer=tf.keras.initializers.Constant(0.4), trainable=True)
        self.zeta = self.add_weight(name='zeta_oq', shape=(), initializer=tf.keras.initializers.Constant(0.5), trainable=True)
        self.eta = self.add_weight(name='eta_oq', shape=(), initializer='ones', trainable=True)
        super(OptimQ, self).build(input_shape)
    def call(self, x):
        arctan_part = self.alpha * tf.math.atan(self.beta * x)
        swish_part = self.gamma * x * tf.math.sigmoid(self.delta * x)
        gated_softplus = self.epsilon * tf.math.softplus(self.zeta * x) * tf.math.tanh(self.eta * x)
        return arctan_part + swish_part + gated_softplus
    def get_config(self): return super(OptimQ, self).get_config()

# --- Static Activation Functions (Keras Layers for consistency) ---
# These do not have trainable parameters but are wrapped as Layers for uniform usage.

class SinhGate(Layer):
    """f(x) = x * sinh(x)"""
    def __init__(self, **kwargs): super(SinhGate, self).__init__(**kwargs)
    def call(self, x): return x * tf.math.sinh(x)
    def get_config(self): return super(SinhGate, self).get_config()

class SoftRBF(Layer):
    """f(x) = x * exp(-x^2)"""
    def __init__(self, **kwargs): super(SoftRBF, self).__init__(**kwargs)
    def call(self, x): return x * tf.math.exp(-tf.square(x))
    def get_config(self): return super(SoftRBF, self).get_config()

class ATanSigmoid(Layer):
    """f(x) = arctan(x) * sigmoid(x)"""
    def __init__(self, **kwargs): super(ATanSigmoid, self).__init__(**kwargs)
    def call(self, x): return tf.math.atan(x) * tf.math.sigmoid(x)
    def get_config(self): return super(ATanSigmoid, self).get_config()

class ExpoSoft(Layer):
    """f(x) = softsign(x) * exp(-|x|)"""
    def __init__(self, **kwargs): super(ExpoSoft, self).__init__(**kwargs)
    def call(self, x): return keras_standard_activations.softsign(x) * tf.math.exp(-tf.abs(x))
    def get_config(self): return super(ExpoSoft, self).get_config()

class HarmonicTanh(Layer):
    """f(x) = tanh(x) + sin(x)"""
    def __init__(self, **kwargs): super(HarmonicTanh, self).__init__(**kwargs)
    def call(self, x): return tf.math.tanh(x) + tf.math.sin(x)
    def get_config(self): return super(HarmonicTanh, self).get_config()

class RationalSoftplus(Layer):
    """f(x) = (x * sigmoid(x)) / (0.5 + x * sigmoid(x))"""
    def __init__(self, **kwargs): super(RationalSoftplus, self).__init__(**kwargs)
    def call(self, x):
        swish_x = x * tf.math.sigmoid(x)
        # Add epsilon for numerical stability, especially if the denominator can be close to zero.
        return swish_x / (tf.constant(0.5, dtype=x.dtype) + swish_x + tf.keras.backend.epsilon())
    def get_config(self): return super(RationalSoftplus, self).get_config()

class UnifiedSineExp(Layer):
    """f(x) = x * sin(exp(-x^2))"""
    def __init__(self, **kwargs): super(UnifiedSineExp, self).__init__(**kwargs)
    def call(self, x): return x * tf.math.sin(tf.math.exp(-tf.square(x)))
    def get_config(self): return super(UnifiedSineExp, self).get_config()

class SigmoidErf(Layer):
    """f(x) = sigmoid(x) * erf(x)"""
    def __init__(self, **kwargs): super(SigmoidErf, self).__init__(**kwargs)
    def call(self, x): return tf.math.sigmoid(x) * tf.math.erf(x)
    def get_config(self): return super(SigmoidErf, self).get_config()

class LogCoshGate(Layer):
    """f(x) = x * log(cosh(x))"""
    def __init__(self, **kwargs): super(LogCoshGate, self).__init__(**kwargs)
    def call(self, x):
        # log(cosh(x)) is also known as the logcosh loss function base. Add epsilon for stability.
        return x * tf.math.log(tf.math.cosh(x) + tf.keras.backend.epsilon())
    def get_config(self): return super(LogCoshGate, self).get_config()

class TanhArc(Layer):
    """f(x) = tanh(x) * arctan(x)"""
    def __init__(self, **kwargs): super(TanhArc, self).__init__(**kwargs)
    def call(self, x): return tf.math.tanh(x) * tf.math.atan(x)
    def get_config(self): return super(TanhArc, self).get_config()

class RiemannianSoftsignActivation(Layer):
    """f(x) = (arctan(x) * erf(x)) / (1 + |x|)"""
    def __init__(self, **kwargs): super(RiemannianSoftsignActivation, self).__init__(**kwargs)
    def call(self, x):
        numerator = tf.math.atan(x) * tf.math.erf(x)
        denominator = 1.0 + tf.math.abs(x)
        return numerator / (denominator + 1e-7)
    def get_config(self): return super(RiemannianSoftsignActivation, self).get_config()

class QuantumTanhActivation(Layer):
    """f(x) = tanh(x) * exp(-tan(x)^2)"""
    def __init__(self, **kwargs): super(QuantumTanhActivation, self).__init__(**kwargs)
    def call(self, x):
        tan_x_squared = tf.math.square(tf.math.tan(x))
        return tf.math.tanh(x) * tf.math.exp(-tan_x_squared)
    def get_config(self): return super(QuantumTanhActivation, self).get_config()

class LogExponentialActivation(Layer):
    """f(x) = sign(x) * log(1 + exp(|x| - 1/|x|))"""
    def __init__(self, **kwargs): super(LogExponentialActivation, self).__init__(**kwargs)
    def call(self, x):
        abs_x = tf.math.abs(x)
        abs_x_safe = abs_x + 1e-7
        exponent = abs_x - tf.math.pow(abs_x_safe, -1.0)
        return tf.math.sign(x) * tf.math.log(1.0 + tf.math.exp(exponent) + 1e-7)
    def get_config(self): return super(LogExponentialActivation, self).get_config()

class BipolarGaussianArctanActivation(Layer):
    """f(x) = arctan(x) * exp(-x^2)"""
    def __init__(self, **kwargs): super(BipolarGaussianArctanActivation, self).__init__(**kwargs)
    def call(self, x): return tf.math.atan(x) * tf.math.exp(-tf.math.square(x))
    def get_config(self): return super(BipolarGaussianArctanActivation, self).get_config()

class ExpArcTanHarmonicActivation(Layer):
    """f(x) = exp(-x^2) * arctan(x) * sin(x)"""
    def __init__(self, **kwargs): super(ExpArcTanHarmonicActivation, self).__init__(**kwargs)
    def call(self, x): return tf.math.exp(-tf.math.square(x)) * tf.math.atan(x) * tf.math.sin(x)
    def get_config(self): return super(ExpArcTanHarmonicActivation, self).get_config()

class LogisticWActivation(Layer):
    """f(x) = x / (1 + exp(-x * W(exp(x)))) where W is the Lambert W function."""
    def __init__(self, **kwargs): super(LogisticWActivation, self).__init__(**kwargs)
    def call(self, x):
        exp_x = tf.math.exp(x)
        lambertw_exp_x = tf_lambertw_principal(exp_x)
        denominator_arg = -x * lambertw_exp_x
        return x / (1.0 + tf.math.exp(denominator_arg) + 1e-7)
    def get_config(self): return super(LogisticWActivation, self).get_config()
