import numpy as np
import scipy.linalg
from scipy.interpolate import interp1d

class PID_controller:
    def __init__(self, kp_, ki_, kd_, u_max_, dim_, e_dot_given_, dt_):

        self.kp_ = kp_
        self.ki_ = ki_
        self.kd_ = kd_
        self.u_max_ = u_max_
        self.dt_ = dt_
        self.dim_ = dim_

        self.e_old_ = []        
        self.e_int_ = np.zeros(self.dim_)
        self.e_dot_given_ = e_dot_given_

    def PID(self, e_, e_dot_in_, u_fb_, reset_int_):

        e_ = np.array(e_)
        u_fb_ = np.array(u_fb_)

        if reset_int_:
            self.e_int_ = np.zeros(self.dim_)
        
        if self.e_dot_given_:
            e_dot_ = np.array(e_dot_in_)
        else:
            if self.e_old_!=[]:
                e_dot_ = (e_ - self.e_old_)/self.dt_
            else:
                e_dot_ = np.zeros(len(e_))
                
        for i in range(len(u_fb_)):
            u_max_i = (u_fb_[i]/np.linalg.norm(u_fb_, ord=2)) * self.u_max_

            if abs(u_fb_[i]) >= abs(u_max_i) and np.sign(self.e_int_[i]) == np.sign(e_[i]):
                self.e_int_[i] = self.e_int_[i]
            else:
                self.e_int_[i] = self.e_int_[i] + e_[i]*self.dt_
        
        self.e_old_ = e_

        uk_ = np.multiply(self.kp_, e_) + np.multiply(self.ki_, self.e_int_) + np.multiply(self.kd_, e_dot_)
        
        return uk_, e_dot_, self.e_int_




def DLQR_optimizer(A, B, Q, R):
    """
    Solve the discrete time lqr controller.
    x[k+1] = A x[k] + B u[k]
    cost = sum x[k].T*Q*x[k] + u[k].T*R*u[k]
    """
    # first, solve the riccati equation
    P = np.matrix(scipy.linalg.solve_discrete_are(A, B, Q, R))
    # compute the LQR gain
    K = np.matrix(scipy.linalg.inv(B.T*P*B+R)*(B.T*P*A))
    return K


def DLQR(K, xk, u_max, u_min):

    uk = K*xk
    uk = np.clip(uk, u_min, u_max)

    return uk


def gain_scheduling_optimizer(list_states, list_kp, list_ki, list_kd):

    kp_interpolated = interp1d(list_states, list_kp, kind='linear')
    ki_interpolated = interp1d(list_states, list_ki, kind='linear')
    kd_interpolated = interp1d(list_states, list_kd, kind='linear')

    return kp_interpolated, ki_interpolated, kd_interpolated
