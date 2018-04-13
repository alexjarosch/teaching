'''
Created on Apr 13, 2018
@author: Alexander H. Jarosch

This script implements a 2D benchmark with a bedrock step for Shallow ice
Finite Difference Models

Copyright 2018 Alexander H. Jarosch

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

from __future__ import division, print_function
import numpy
import matplotlib.pyplot as plt


def main():

    # These parameters are defined in section 7.1
    A = 1e-16
    n = 3
    g = 9.81
    rho = 910
    Gamma = 2.*A*(rho*g)**n / (n+2)  # we introduce Gamma for short equations.
    mdot_0 = 2
    x_m = 20000
    x_s = 7000
    c_stab = 0.165

    dx = 500
    dt = 1.0
    t_total = 25000
    Nt = t_total/dt

    # define b_0 as a multiplication of dx
    N = 0.5
    b_0 = N * dx

    # create a space vector
    x = numpy.arange(0, x_m + x_m/2 + dx, dx)
    # define the mass balance vector
    m_dot = accumulation(x, mdot_0, n, x_m)
    # define bed vector. Here we use capital B instead of b.
    B = numpy.zeros(len(x))
    B[x < x_s] = b_0

    # set the intial ice surface S to the bed elevation.
    S = B
    Nx = len(S)

    # finite difference indixes. k is used in this 2D example along x direction
    k = numpy.arange(0, Nx)
    kp = numpy.hstack([numpy.arange(1, Nx), Nx-1])
    km = numpy.hstack([0, numpy.arange(0, Nx-1)])

    # M2 scheme time stepping loop
    S = B
    for t in range(int(Nt)+1):
        stab_t = 0
        while stab_t < dt:
            H = S - B
            # average the ice thickness at flux boundary
            H_up = 0.5 * (H[kp] + H[k])
            H_dn = 0.5 * (H[k] + H[km])
            # calculate the surface slope at flux boundary
            s_grad_up = ((S[kp]-S[k])**2 / dx**2)**((n-1)/2)
            s_grad_dn = ((S[k]-S[km])**2 / dx**2)**((n-1)/2)
            # calculate the diffusivities
            D_up = Gamma * H_up**(n+2) * s_grad_up
            D_dn = Gamma * H_dn**(n+2) * s_grad_dn
            # get the stability time step
            dt_stab = c_stab * dx**2. / max(max(abs(D_up)), max(abs(D_dn)))
            # make sure you finish on an exact year time step
            dt_use = min(dt_stab, dt-stab_t)
            stab_t = stab_t + dt_use

            # explicit time stepping scheme
            div_q = (D_up * (S[kp] - S[k])/dx - D_dn * (S[k] - S[km])/dx)/dx
            S = S[k] + (m_dot + div_q)*dt_use
            # fix the ice surface elevations below bed elevation
            S = numpy.maximum(S, B)
            # print the time step
            print('M2 Year %d, dt_use %f' % (t, dt_use))
        # plot each thousand years
        if numpy.mod(t, 1000) == 0.0:
            plt.plot(x/1000, S, '-r')

    # calculate the volume difference
    p1, = plt.plot(x/1000, S, '-r')
    H = S-B
    vol_M2 = numpy.trapz(H, x)

    # create the explicit steady state solution called s
    s_x_s_x_m = s_eval_x_s_x_m(x, x_s, x_m, n, A, mdot_0, rho, g)
    s_x_s = s_eval_x_s(x, x_s, x_m, n, A, mdot_0, rho, g, b_0)
    # combine the solutions
    s = s_x_s+b_0
    s[x >= x_s] = s_x_s_x_m[x >= x_s]
    # correct s
    s[x > x_m] = 0

    h = s-B
    # calculate the volume error
    vol_exact = numpy.trapz(h, x)
    vol_err_M2 = (vol_M2-vol_exact)/vol_exact*100

    print("vol exact: %e" % vol_exact)
    print("vol M2: %e" % vol_M2)
    print("err M2 %0.3f" % vol_err_M2)

    p2, = plt.plot(x/1000, B, '-k', linewidth=2)
    p3, = plt.plot(x/1000, s, '-', linewidth=3, color='#ff7800')
    plt.xlabel('x [km]')
    plt.ylabel('z [m]')
    plt.title('Model results')
    plt.legend([p1, p2, p3], ["M2", "bed", "Analytical Solution"])
    plt.show()


# define the accumulation function
def accumulation(x, mdot_0, n, x_m):
    # Eq. 54
    mdot = ((n*mdot_0)/(x_m**(2*n-1)))*x**(n-1)*(abs(x_m-x)**(n-1))*(x_m-2*x)
    mdot[x > x_m] = 0
    return mdot


# define the analytical surface shape
def s_eval_x_s_x_m(x, x_s, x_m, n, A, mdot_0, rho, g):
    # Eq. 56
    s_x_s_x_m = (((2*n+2)*(n+2)**(1/n)*mdot_0**(1/n))/(2**(1/n)*6*n*A**(1/n)*rho*g*x_m**((2*n-1)/n))*(x_m+2*x)*(x_m-x)**2)**(n/(2*n+2))
    return s_x_s_x_m


def s_eval_x_s(x, x_s, x_m, n, A, mdot_0, rho, g, b_0):
    # Eq. 58
    h_splus = (((2*n+2)*(n+2)**(1/n)*mdot_0**(1/n))/(2**(1/n)*6*n*A**(1/n)*rho*g*x_m**((2*n-1)/n))*(x_m+2*x_s)*(x_m-x_s)**2)**(n/(2*n+2))
    # Eq. 59
    h_sminus = numpy.maximum(h_splus - b_0, 0)
    # Eq. 57
    h_back = (h_sminus**((2*n+2)/n)-h_splus**((2*n+2)/n)+((2*n+2)*(n+2)**(1/n)*mdot_0**(1/n))/(2**(1/n)*6*n*A**(1/n)*rho*g*x_m**((2*n-1)/n))*(x_m+2*x)*(x_m-x)**2)**(n/(2*n+2))
    return h_back


''' DEFINE which routine to run as the main '''

if __name__ == "__main__":
    main()
