from ..keras_utils import *
from tensorflow.keras.models import Sequential


class GAN:
    def __init__(self):
        self._noise_dim = 100 
        self._img_rows = 28
        self._img_cols = 28
        self._channels = 1
        self._img_shape = (self._img_rows, self._img_cols, self._channels)

    def _generative_model(self):
        noise = Input(shape=(self._noise_dim,), dtype=np.float32)
        x = get_dense(1024, input_dim=self._noise_dim, name='DENSE_0')(noise)
        x = get_dense(7*7*128, name='DENSE_1')(x)

        x = Reshape((7, 7, 128), input_shape=(7*7*128, 1), name='RESHAPE')(x)
        x = get_conv2dTranspose(32, 5, padding='same', strides=2, name='CONV_T1')(x)
        x = get_conv2dTranspose(16, 5, padding='same', strides=2, name='CONV_T2')(x)
        x = get_conv2dTranspose(1, 5, padding='same', strides=1, activation='sigmoid')(x)

        G = Model(inputs=noise, outputs=x)
        return G

    def _discriminator_model(self):
        x = Input(shape=self._img_shape, dtype=np.float32)
        y = x
        y = get_conv2d(64, 5, padding='same', input_shape=self._img_shape)(y)
        y = MaxPooling2D()(y)
        y = get_conv2d(128, 5, padding='same')(y)
        y = MaxPool2D()(y)
        y = Flatten()(y)
        y = get_dense(1024)(y)
        y = get_dense(1, activation='sigmoid')(y)
        D = Model(inputs=x, outputs=y)
        return D

    def get_compiled_models(self):
        """returns: combined_model, generator_model, discriminator_model
        """
        g = self._generative_model()
        d = self._discriminator_model()
        d.compile(optimizer='adam', loss='binary_crossentropy')

        c = Sequential()
        c.add(g)
        d.trainable = False 
        c.add(d)

        # compile 
        c.compile(optimizer='adam', loss='binary_crossentropy')
        
        return c, g, d
