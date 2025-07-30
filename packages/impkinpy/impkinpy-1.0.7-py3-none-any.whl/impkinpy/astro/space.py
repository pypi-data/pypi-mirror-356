import numpy as np 
import matplotlib.pyplot as plt

class Black_hole():
    def __init__(self):
        self.G = 6.67430e-11
        self.SB_const = 1.380649e-23
        self.proton_m = 1.6726e-27
        self.m_Sun = 1.98847e30
        self.light_speed = 299792458

    def black_hole_Schwarzschild(self, accretion_v: int | float, disk_r: int | float, hole_mass: int | float, H_He_Z_list: list[list[int]], **kwargs):
        t_list = []
        density_list = []
        vr_list = []
        r_list = []

        r_min = 3*(self.G*hole_mass/self.light_speed**2)
        r = np.linspace(r_min, disk_r, 1000)

        Ah = 1
        Ahe = 4
        Az = 16

        sigma_H = H_He_Z_list[0][0]*(1+H_He_Z_list[0][1])/Ah
        sigma_He = H_He_Z_list[1][0]*(1+H_He_Z_list[1][1])/Ahe
        sigma_Z = H_He_Z_list[2][0]*(1+H_He_Z_list[2][1])/Az

        molecular_m = 1/(sigma_H+sigma_He+sigma_Z)
        alpha = 0

        for i in r:
            t = (3*self.G*hole_mass*accretion_v/(8*np.pi*self.SB_const*i**3))**(1/4)
            c_sound = np.sqrt(self.SB_const*t/(molecular_m*self.proton_m))
            angle_v = np.sqrt(self.G*hole_mass/i**3)
            disk_h = c_sound/angle_v
            if len(kwargs) == 0:
                    coeff = 0.3/disk_r
                    alpha += coeff
            else:
                for key, value in kwargs.items():
                    if key == "alpha_viscosity":
                        alpha = value
                    if key == "viscosity":
                        viscosity = value
                        alpha = viscosity/(c_sound*disk_h)

            vK = np.sqrt(self.G*hole_mass/i)
            vr = -alpha*(disk_h/disk_r)**2*vK
            density = accretion_v/(4*np.pi*i*disk_h*abs(vr))

            r_list.append(i)
            density_list.append(density)
            vr_list.append(vr)
            t_list.append(t)

        return density_list, t_list, vr_list, r_list
    
    # def black_hole_Kerr(self, accretion_v, disk_r, disk_h, hole_mass, spin_parameter):
    #     d_ang_v = 0
    #     d_ang_momentum = 0
    #     t_list = []
    #     density_list = []
    #     vr_list = []
    #     r_list = []
    #     ang_v_list = []
    #     l_list = []

    #     integral = 0
        
    #     z1 = 1+(1-spin_parameter**2)**(1/3)*((1+spin_parameter)**(1/3)+(1-spin_parameter)**(1/3))
    #     z2 = np.sqrt(3*spin_parameter**2+z1**2)
    #     rg = self.G*hole_mass/self.light_speed**2
    #     if spin_parameter > 0:
    #         r_min = rg*(3+z2-np.sqrt((3-z1)*(3+z1+2*z2)))
    #     else:
    #         r_min = rg*(3+z2+np.sqrt((3-z1)*(3+z1+2*z2)))

    #     r = np.linspace(r_min, disk_r, 1000)
    #     delta_r = (disk_r-r_min)/1000
        
    #     for i in r:
    #         r_list.append(i)
    #         e_per_m = (i**(3/2)-2*i**(1/2)+spin_parameter)/(i**(3/4)*np.sqrt(abs(i**(3/2)-3*i**(1/2)+2*spin_parameter)))
    #         ang_momentum = (i**2-2*spin_parameter*i**(1/2)+spin_parameter**2)/(i**(3/4)*np.sqrt(abs(i**(3/2)-3*i**(1/2)+2*spin_parameter)))
    #         ang_v = 1/(i**(3/2)+spin_parameter)
    #         ang_v_list.append(ang_v)
    #         l_list.append(ang_momentum)
    #         if len(ang_v_list) > 2:
    #             d_ang_v = np.gradient(ang_v_list)
    #             d_ang_momentum = np.gradient(l_list)
    #             for j in range(len(d_ang_momentum)):
    #                 integral = ((e_per_m-ang_v*ang_momentum)*ang_momentum/i)*d_ang_momentum[j]*delta_r
    #             f = accretion_v/(4*np.pi*i)*(-d_ang_v[j]/(e_per_m-ang_v*ang_momentum)**2)*integral
    #         else:
    #             d_ang_v = 1
    #             d_ang_momentum = 1
    #             integral = ((e_per_m-ang_v*ang_momentum)*ang_momentum/i)*d_ang_momentum*delta_r
    #             f = accretion_v/(4*np.pi*i)*(-d_ang_v/(e_per_m-ang_v*ang_momentum)**2)*integral
    #         power_per_area = accretion_v/(4*np.pi*i)*f
    #         t = (power_per_area/self.SB_const)**(1/4)
    #         t_list.append(t)

    #         g_t_t = -(1-(2*hole_mass*i/i**2))
    #         g_t_ang = -(2*hole_mass*spin_parameter*i/i**2)
    #         g_ang_ang = i**2+spin_parameter**2+(2*hole_mass*spin_parameter/i)
    #         trngl = i**2-2*hole_mass*i+spin_parameter**2
    #         vk = i*ang_v
    #         vr = a

    #         density = accretion_v/(4*np.pi*i*disk_h*vr)
    #         density_list.append(density)

    #     return density_list, t_list, vr_list, r_list
    
    def el_density(self, dt_different_freq, frequency_1, frecuency_2, d_from_pulsar):
        el_d_list = []
        d_list = np.linspace(0.0001, d_from_pulsar, 1000)
        dm = dt_different_freq/(4.5e3*(1/frequency_1**2-1/frecuency_2**2))
        for i in d_list:
            el_d = dm/i
            el_d_list.append(el_d)
        return d_list, el_d_list
    
    def cutoff_freq(self, el_density):
        freq = 8.98*np.sqrt(el_density)
        return freq
    
    def r_Hill(self, moon_m, star_m, d_from_star):
        r_Hill = d_from_star*(moon_m/(3*star_m+moon_m))
        return r_Hill
    
    def kin_energy_relativ(self, part_m, part_v0, pulsar_m, d_from_pulsar):
        d = np.linspace(0.0001, d_from_pulsar, 1000)
        adiabat_0 = 1/np.sqrt(1-part_v0**2/self.light_speed**2)

    def plot_black_hole(self, func):
        density_list, t_list, vr_list, r_list = eval(func)
        plt.plot(r_list, density_list, "-r")
        plt.title("Density of disk on radius r from the black hole")
        plt.grid()
        plt.show()
        plt.plot(r_list, t_list, "-g")
        plt.title("Temperature of disk on radius r from the black hole")
        plt.grid()
        plt.show()
        plt.plot(r_list, vr_list, "-b")
        plt.title("Radial velocity of disk on radius r from the black hole")
        plt.grid()
        plt.show()

b = Black_hole()
print(type(float("inf")))