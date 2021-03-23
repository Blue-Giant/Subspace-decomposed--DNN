import numpy as np
import tensorflow as tf


def get_infos2Boltzmann_1D(in_dim=1, out_dim=1, region_a=0.0, region_b=1.0, index2p=2, eps=0.01, eqs_name=None):
    if eqs_name == 'Boltzmann1':
        llam = 20
        mu = 50
        f = lambda x: (llam*llam+mu*mu)*tf.sin(x)
        Aeps = lambda x: 1.0*tf.ones_like(x)
        kappa = lambda x: llam*llam*tf.ones_like(x)
        utrue = lambda x: -1.0*(np.sin(mu)/np.sinh(llam))*tf.sinh(llam*x) + tf.sin(mu*x)
        ul = lambda x: tf.zeros_like(x)
        ur = lambda x: tf.zeros_like(x)
        return Aeps, kappa, utrue, ul, ur, f
    elif eqs_name == 'Boltzmann2':
        kappa = lambda x: tf.ones_like(x)
        Aeps = lambda x: 1.0 / (2 + tf.cos(2 * np.pi * x / eps))

        utrue = lambda x: x - tf.square(x) + (eps / (4*np.pi)) * tf.sin(np.pi * 2 * x / eps)

        ul = lambda x: tf.zeros_like(x)

        ur = lambda x: tf.zeros_like(x)

        if index2p == 2:
            f = lambda x: 2.0/(2 + tf.cos(2 * np.pi * x / eps)) + (4*np.pi*x/eps)*tf.sin(np.pi * 2 * x / eps)/\
                          ((2 + tf.cos(2 * np.pi * x / eps))*(2 + tf.cos(2 * np.pi * x / eps))) + x - tf.square(x) \
                          + (eps / (4*np.pi)) * tf.sin(np.pi * 2 * x / eps)

        return Aeps, kappa, utrue, ul, ur, f


def get_infos2Boltzmann_2D(input_dim=2, out_dim=1, mesh_number=2, intervalL=0.0,
                           intervalR=1.0,equa_name=None):
    if equa_name == 'Boltzmann1':
        lam = 2
        mu = 30
        f = lambda x, y: (lam*lam+mu*mu)*(tf.sin(mu*x) + tf.sin(mu*y))
        A_eps = lambda x, y: 1.0*tf.ones_like(x)
        kappa = lambda x, y: lam*lam*tf.ones_like(x)
        u = lambda x, y: -1.0*(np.sin(mu)/np.sinh(lam))*tf.sinh(lam*x) + tf.sin(mu*x) -1.0*(np.sin(mu)/np.sinh(lam))*tf.sinh(lam*y) + tf.sin(mu*y)
        ux_left = lambda x, y: tf.zeros_like(x)
        ux_right = lambda x, y: tf.zeros_like(x)
        uy_bottom = lambda x, y: tf.zeros_like(x)
        uy_top = lambda x, y: tf.zeros_like(x)
    elif equa_name == 'Boltzmann2':
        # lam = 20
        # mu = 50
        f = lambda x, y: 5 * ((np.pi) ** 2) * (0.5 * tf.sin(np.pi * x) * tf.cos(np.pi * y) + 0.25 * tf.sin(10 * np.pi * x) * tf.cos(10 * np.pi * y)) * \
                        (0.25 * tf.cos(5 * np.pi * x) * tf.sin(10 * np.pi * y) + 0.5 * tf.cos(15 * np.pi * x) * tf.sin(20 * np.pi * y)) + \
                        5 * ((np.pi) ** 2) * (0.5 * tf.cos(np.pi * x) * tf.sin(np.pi * y) + 0.25 * tf.cos(10 * np.pi * x) * tf.sin(10 * np.pi * y)) * \
                        (0.125 * tf.sin(5 * np.pi * x) * tf.cos(10 * np.pi * y) + 0.125 * 3 * tf.sin(15 * np.pi * x) * tf.cos(20 * np.pi * y)) + \
                        ((np.pi) ** 2) * (tf.sin(np.pi * x) * tf.sin(np.pi * y) + 5 * tf.sin(10 * np.pi * x) * tf.sin(10 * np.pi * y)) * \
                        (0.125 * tf.cos(5 * np.pi * x) * tf.cos(10 * np.pi * y) + 0.125 * tf.cos(15 * np.pi * x) * tf.cos(20 * np.pi * y) + 0.5) + \
                         0.5 *np.pi*np.pi* tf.sin(np.pi * x) * tf.sin(np.pi * y) + 0.025 *np.pi*np.pi* tf.sin(10 * np.pi * x) * tf.sin(10 * np.pi * y)

        A_eps = lambda x, y: 0.5 + 0.125*tf.cos(5*np.pi*x)*tf.cos(10*np.pi*y) + 0.125*tf.cos(15*np.pi*x)*tf.cos(20*np.pi*y)
        kappa = lambda x, y: np.pi*np.pi*tf.ones_like(x)
        u = lambda x, y: 0.5*tf.sin(np.pi*x)*tf.sin(np.pi*y)+0.025*tf.sin(10*np.pi*x)*tf.sin(10*np.pi*y)
        ux_left = lambda x, y: tf.zeros_like(x)
        ux_right = lambda x, y: tf.zeros_like(x)
        uy_bottom = lambda x, y: tf.zeros_like(x)
        uy_top = lambda x, y: tf.zeros_like(x)

    return A_eps, kappa, u, ux_left, ux_right, uy_top, uy_bottom, f


def get_infos2Boltzmann_3D(input_dim=1, out_dim=1, mesh_number=2, intervalL=0.0, intervalR=1.0, equa_name=None):
    if equa_name == 'Boltzmann1':
        # mu1= 2*np.pi
        # mu2 = 4*np.pi
        # mu3 = 8*np.pi
        mu1 = np.pi
        mu2 = 5 * np.pi
        mu3 = 10 * np.pi
        f = lambda x, y, z: (mu1*mu1+mu2*mu2+mu3*mu3+x*x+2*y*y+3*z*z)*tf.sin(mu1*x)*tf.sin(mu2*y)*tf.sin(mu3*z)
        A_eps = lambda x, y, z: 1.0*tf.ones_like(x)
        kappa = lambda x, y, z: x*x+2*y*y+3*z*z
        u = lambda x, y, z: tf.sin(mu1*x)*tf.sin(mu2*y)*tf.sin(mu3*z)
        u_00 = lambda x, y, z: tf.sin(mu1*intervalL)*tf.sin(mu2*y)*tf.sin(mu3*z)
        u_01 = lambda x, y, z: tf.sin(mu1*intervalR)*tf.sin(mu2*y)*tf.sin(mu3*z)
        u_10 = lambda x, y, z: tf.sin(mu1*x)*tf.sin(mu2*intervalL)*tf.sin(mu3*z)
        u_11 = lambda x, y, z: tf.sin(mu1*x)*tf.sin(mu2*intervalR)*tf.sin(mu3*z)
        u_20 = lambda x, y, z: tf.sin(mu1*x)*tf.sin(mu2*y)*tf.sin(mu3*intervalL)
        u_21 = lambda x, y, z: tf.sin(mu1*x)*tf.sin(mu2*y)*tf.sin(mu3*intervalR)

    return A_eps, kappa, f, u, u_00, u_01, u_10, u_11, u_20, u_21


def get_infos2Boltzmann_5D(input_dim=1, out_dim=1, mesh_number=2, intervalL=0.0, intervalR=1.0, equa_name=None):
    if equa_name == 'Boltzmann1':
        lam = 2
        mu = 30
        f = lambda x, y: (lam*lam+mu*mu)*(tf.sin(mu*x) + tf.sin(mu*y))
        A_eps = lambda x, y: 1.0*tf.ones_like(x)
        kappa = lambda x, y: lam*lam*tf.ones_like(x)
        u = lambda x, y: -1.0*(np.sin(mu)/np.sinh(lam))*tf.sinh(lam*x) + tf.sin(mu*x) -1.0*(np.sin(mu)/np.sinh(lam))*tf.sinh(lam*y) + tf.sin(mu*y)
        u_00 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_01 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_10 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_11 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_20 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_21 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_30 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_31 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_40 = lambda x, y, z, s, t: tf.zeros_like(x)
        u_41 = lambda x, y, z, s, t: tf.zeros_like(x)

    return A_eps, kappa, u, f, u_00, u_01, u_10, u_11, u_20, u_21, u_30, u_31, u_40, u_41