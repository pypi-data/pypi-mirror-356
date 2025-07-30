import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import gamma

class Gravity():
    def __init__(self, planet):
        self.g_dict = {"Mercury": 3.7, "Venus": 8.87, "Earth": 9.81, "Mars": 3.71, "Jupiter": 24.79, 
                       "Saturn": 10.44, "Uranus": 8.69, "Neptune": 11.15, "Pluto": 0.62, "Sun": 274.0,
                       "Io": 1.79, "Moon": 1.62, "Europa": 1.31, "Ganymede": 1.43, "Callisto": 1.24, 
                       "Enceladus": 0.113, "Titan": 1.35, "Rhea": 0.264, "Miranda": 0.079, "Ariel": 0.269,
                       "Triton": 0.779, "Charon": 0.288, "Amalthea": 0.020, "Himalia": 0.062, 
                       "Mimas": 0.064, "Tethys": 0.147, "Dione": 0.233, "Hyperion": 0.017, "Iapetus": 0.224,
                       "Phoebe": 0.042, "Umbriel": 0.2, "Titania": 0.38, "Oberon": 0.35, "Nereid": 0.003,
                       "Styx": 0.005, "Nix": 0.012, "Kerberos": 0.003, "Hydra": 0.008}
        for key, value in self.g_dict.items():
            if planet == key:
                self.g = value
            # else:
            #     raise TypeError('Write only on of this space objects: "Mercury": 3.7, "Venus": 8.87, "Earth": 9.81, "Mars": 3.71, "Jupiter": 24.79, "Saturn": 10.44, "Uranus": 8.69, "Neptune": 11.15, "Pluto": 0.62, "Sun": 274.0,"Io": 1.79, "Moon": 1.62, "Europa": 1.31, "Ganymede": 1.43, "Callisto": 1.24, "Enceladus": 0.113, "Titan": 1.35, "Rhea": 0.264, "Miranda": 0.079, "Ariel": 0.269, "Triton": 0.779, "Charon": 0.288, "Amalthea": 0.020, "Himalia": 0.062,   "Mimas": 0.064, "Tethys": 0.147, "Dione": 0.233, "Hyperion": 0.017, "Iapetus": 0.224,"Phoebe": 0.042, "Umbriel": 0.2, "Titania": 0.38, "Oberon": 0.35, "Nereid": 0.003,"Styx": 0.005, "Nix": 0.012, "Kerberos": 0.003, "Hydra": 0.008')

    def other_g(self, your_g):
        self.g = your_g
        return self.g
    
    def angle__v0x(self, v0: int | float, v0x: int | float):
        return np.acos(v0x / v0)
    def angle__v0y(self, v0: int | float, v0y: int | float):
        return np.asin(v0y / v0)
    
    def v0__v0x_angle(self, v0x: int | float, angle_deg: int | float):
        angle_deg = np.radians(angle_deg)
        return v0x / np.cos(angle_deg)
    def v0__v0y_angle(self, v0y: int | float, angle_deg: int | float):
        angle_deg = np.radians(angle_deg)
        return v0y / np.sin(angle_deg)
    def v0__L_angle(self, L: int | float, angle: int | float):
        return np.sqrt(L * self.g / np.sin(2 * angle))
    
    def v0x__L_tfall(self, L: int | float, tfall: int | float):
        return L / tfall
    def v0x__xt_tfall(self, xt: int | float, tfall: int | float):
        return xt / tfall
    def v0x__v0_angle(self, v0: int | float, angle_deg: int | float):
        angle_deg = np.radians(angle_deg)
        return v0 * np.cos(angle_deg)
    

    def v0y__tfall(self, tfall: int | float):
        return tfall * self.g / 2
    def v0y__H(self, H: int | float):
        return np.sqrt(2 * self.g * H)
    def v0y__vy_tfall(self, vy: int | float, tfall: int | float):
        return vy + (self.g * tfall)
    def v0y__yt_tfall(self, yt: int | float, tfall: int | float):
        return (yt + 0.5 * self.g * tfall ** 2) / tfall
    def v0y__v0_angle(self, v0: int | float, angle_deg: int | float):
        angle_deg = np.radians(angle_deg)
        return v0 * np.sin(angle_deg)
    
    def H(self, v0y: int | float):
        return v0y ** 2 / (2 * self.g)
    
    def tfall__v0y(self, v0y: int | float):
        return 2 * v0y / self.g
    def tfall__L_v0x(self, L: int | float, v0x: int | float):
        return L / v0x

    def L__v0x_tfall(self, v0x: int | float, tfall: int | float):
        return v0x * tfall
    def L__v0_angle(self, v0: int | float, angle_deg: int | float):
        angle_deg = np.radians(angle_deg)
        return v0 ** 2 / self.g * np.sin(2 * angle_deg)
    
    def xt(self, v0x: int | float, tfall: int | float):
        return v0x * tfall
    def yt(self, v0y: int | float, tfall: int | float):
        return v0y * tfall - self.g * tfall ** 2 / 2

    def vx(self, v0x: int | float):
        return v0x
    def vy(self, v0y: int | float, tfall: int | float):
        return v0y - (self.g * tfall)
        
    def trajectory_2_parameters(self, **kwargs):
        x_list = []
        y_list = []
        keys = list(kwargs.keys())
        for i in range(len(keys) - 1):
            if (keys[i] == "v0" or keys[i] == "V0") and (keys[i + 1] == "angle" or keys[i + 1] == "Angle"):
                v0 = kwargs[keys[i]]
                angle = kwargs[keys[i + 1]]
                v0x = self.v0x__v0_angle(v0, angle)
                v0y = self.v0y__v0_angle(v0, angle)
            elif (keys[i] == "angle" or keys[i] == "Angle") and (keys[i + 1] == "v0" or keys[i + 1] == "V0"):
                v0 = kwargs[keys[i + 1]]
                angle = kwargs[keys[i]]
                v0x = self.v0x__v0_angle(v0, angle)
                v0y = self.v0y__v0_angle(v0, angle)

            elif (keys[i] == "angle" or keys[i] == "Angle") and (keys[i + 1] == "time" or keys[i + 1] == "Time"):
                angle = kwargs[keys[i]]
                tfall = kwargs[keys[i + 1]]
                v0y = self.v0y__tfall(tfall)
                v0 = self.v0__v0y_angle(v0y, angle)
                v0x = self.v0x__v0_angle(v0, angle)
            elif (keys[i] == "time" or keys[i] == "Time") and (keys[i + 1] == "angle" or keys[i + 1] == "Angle"):
                angle = kwargs[keys[i + 1]]
                tfall = kwargs[keys[i]]
                angle_deg = np.radians(angle_deg)
                v0y = self.v0y__tfall(tfall)
                v0 = self.v0__v0y_angle(v0y, angle_deg)
                v0x = self.v0x__v0_angle(v0, angle_deg)

            elif (keys[i] == "Length" or keys[i] == "length") and (keys[i + 1] == "time" or keys[i + 1] == "Time" or keys[i + 1] == "T" or keys[i + 1] == "t"):
                l = kwargs[keys[i]]
                tfall = kwargs[keys[i + 1]]
                v0x = self.v0x__L_tfall(l, tfall)
                v0y = self.v0y__tfall(tfall)
            elif (keys[i] == "tfall" or keys[i] == "Time" or keys[i] == "T" or keys[i] == "t") and (keys[i + 1] == "Length" or keys[i + 1] == "length"):
                l = kwargs[keys[i + 1]]
                tfall = kwargs[keys[i]]
                v0x = self.v0x__L_tfall(l, tfall)
                v0y = self.v0y__tfall(tfall)

            elif (keys[i] == "Length" or keys[i] == "length") and (keys[i + 1] == "Height" or keys[i + 1] == "height"):
                l = kwargs[keys[i]]
                h = kwargs[keys[i + 1]]
                v0y = self.v0y__H(h)
                tfall = self.tfall__v0y(v0y)
                v0x = self.v0x__L_tfall(l, tfall)
            elif (keys[i] == "Height" or keys[i] == "height") and (keys[i + 1] == "Length" or keys[i + 1] == "length"):
                l = kwargs[keys[i + 1]]
                h = kwargs[keys[i]]
                v0y = self.v0y__H(h)
                tfall = self.tfall__v0y(v0y)
                v0x = self.v0x__L_tfall(l, tfall)

            elif (keys[i] == "v0x" or keys[i] == "V0X") and (keys[i + 1] == "time" or keys[i + 1] == "Time" or keys[i + 1] == "T" or keys[i + 1] == "t"):
                v0x = kwargs[keys[i]]
                tfall = kwargs[keys[i + 1]]
                v0y = self.v0y__tfall(tfall)
            elif (keys[i] == "time" or keys[i] == "Time" or keys[i] == "T" or keys[i] == "t") and (keys[i + 1] == "v0x" or keys[i + 1] ==  "V0X"):
                v0x = kwargs[keys[i]]
                tfall = kwargs[keys[i + 1]]
                v0y = self.v0y__tfall(tfall)

            elif (keys[i] == "v0x" or keys[i] == "V0X") and (keys[i + 1] == "Height" or keys[i + 1] == "height"):
                v0x = kwargs[keys[i]]
                h = kwargs[keys[i + 1]]
                v0y = self.v0y__H(h)
            elif (keys[i] == "Height" or keys[i] == "height") and (keys[i + 1] == "v0x" or keys[i + 1] == "V0X"):
                h = kwargs[keys[i]]
                v0x = kwargs[keys[i + 1]]
                v0y = self.v0y__H(h)

            elif (keys[i] == "v0" or keys[i] == "V0") and (keys[i + 1] == "Height" or keys[i + 1] == "height"):
                v0 = kwargs[keys[i]]
                h = kwargs[keys[i + 1]]
                v0y = self.v0y__H(h)
                angle = self.angle__v0y(v0, v0y)
                v0x = self.v0x__v0_angle(v0, angle)
            elif (keys[i] == "Height" or keys[i] == "height") and (keys[i + 1] == "v0" or keys[i + 1] == "V0"):
                v0 = kwargs[keys[i]]
                h = kwargs[keys[i + 1]]
                v0y = self.v0y__H(h)
                angle = self.angle__v0y(v0, v0y)
                v0x = self.v0x__v0_angle(v0, angle)

            elif (keys[i] == "v0x" or keys[i] == "V0X") and (keys[i + 1] == "v0y" or keys[i + 1] == "V0Y"):
                v0x = kwargs[keys[i]]
                v0y = kwargs[keys[i + 1]]
            elif keys[i] == "v0y" and keys[i + 1] == "v0x" or keys[i] == "V0Y" and keys[i + 1] == "V0X":
                v0x = kwargs[keys[i + 1]]
                v0y = kwargs[keys[i]]

            else:
                raise KeyError("Write only one of this combinations:v0x and v0y, v0 and height, length and height, v0 and angle, v0x and height, v0x and time, length and time, angle and time")
            
        npoints = 101
        tfall = self.tfall__v0y(v0y)
        dt = tfall / (npoints - 1)
        t=0
        for i in range(101):
            xt = self.xt(v0x, t)
            yt = self.yt(v0y, t)
            x_list.append(xt)
            y_list.append(yt)
            t+=dt

        return x_list, y_list
    
    def impulse(self, m, v):
        return m * v

    def plot_trajectory(self, func: str):
        x_list, y_list = eval(func)

        plt.plot(x_list, y_list)
        plt.title("Trajectory")
        plt.grid()
        plt.show()

        plt.plot(x_list, y_list)
        plt.axis("equal")
        plt.title("Trajectory With Equal Axes")
        plt.grid()
        plt.show()
    
    # Returns angle_list and angle_v_list for phase pendulum trajectory and l or r, t and f of equal math pendulum
    def pendulum(self, shape: str, axis: str, m: int | float, l_or_r: int | float, start_angle_deg: int | float, v0: int | float, d_mc_axis: int | float, rect_width: int | float, rect_height: int | float, plate_inner_r: int | float, plate_outer_r: int | float):
        shape_and_axis = f"['{shape}', '{axis}']"
        start_angle = np.radians(start_angle_deg)
        d_dict = {"['point', 'distance_l_from_the_point']": d_mc_axis,
                  "['rod', 'center']": 0, "['rod', 'end']": l_or_r/2, 
                  "['rod', 'distance_d_from_center']": d_mc_axis, 
                  "['disk', 'center']": 0, "['disk', 'edge']": l_or_r, 
                  "['disk', 'distance_d_from_center']": d_mc_axis,
                  "['hoop', 'center']": 0, 
                  "['hoop', 'point_on_rim']": l_or_r, 
                  "['hoop', 'distance_d_from_center']": d_mc_axis,
                  "['solid_sphere', 'center']": 0, 
                  "['solid_sphere', 'tangential_axis']": l_or_r, 
                  "['solid_sphere', 'distance_d_from_center']": d_mc_axis,
                  "['hollow_sphere', 'center']": 0, 
                  "['hollow_sphere', 'tangential_axis']": l_or_r, 
                  "['hollow_sphere', 'distance_d_from_center']": d_mc_axis,
                  "['rectangle', ''center_vertical']": 0, 
                  "['rectangle', 'center_horizontal']": 0,
                  "['rectangle', 'vertical_edge']": rect_width/2, 
                  "['rectangle', 'horizontal_edge']": rect_height/2,
                  "['rectangle', 'distance_d_from_center']": d_mc_axis,
                  "['half_sphere', 'center']": 0,
                  "['half_sphere', 'diameter']": l_or_r, "['half_sphere, edge']": 5*l_or_r/8,
                  "['half_sphere', 'tangential_axis']": 5/8*l_or_r,
                  "['half_sphere', 'distance_d_from_center']": d_mc_axis,
                  "['annular_plate', 'center']": 0, 
                  "['annular_plate', 'inner_edge']": plate_inner_r,
                  "['annular_plate', 'outer_edge']": plate_outer_r,
                  "['annular_plate, 'distance_d_from_center']": d_mc_axis}
        
        shape_dict = {"['point', 'distance_l_from_point']": m*l_or_r**2,
                      "['rod', 'center']": 1/12*m*l_or_r**2, "['rod', 'end']": 1/2*m*l_or_r**2, 
                      "['rod', 'distance_d_from_center']": 1/12*m*l_or_r**2, 
                      "['disk', 'center']": 1/2*m*l_or_r**2, "['disk', 'edge']": 3/2*m*l_or_r**2, 
                      "['disk', 'distance_d_from_center']": 1/2*m*l_or_r**2+m*d_mc_axis**2,
                      "['hoop', 'center']": m*l_or_r**2, 
                      "['hoop', 'point_on_rim']": 2*m*l_or_r**2, 
                      "['hoop', 'distance_d_from_center']": m*l_or_r**2+m*d_mc_axis**2,
                      "['solid_sphere', 'center']": 2/5*m*l_or_r**2, 
                      "['solid_sphere', 'tangential_axis']": 7/5*m*l_or_r**2, 
                      "['solid_sphere', 'distance_d_from_center']": 2/5*m*l_or_r**2+m*d_mc_axis**2,
                      "['hollow_sphere', 'center']": 2/3*m*l_or_r**2, 
                      "['hollow_sphere', 'tangential_axis']": 5/3*m*l_or_r**2, 
                      "['hollow_sphere', 'distance_d_from_center']": 2/3*m*l_or_r**2+m*d_mc_axis**2,
                      "['rectangle', ''center_vertical']": 1/12*m*rect_height**2, 
                      "['rectangle', 'center_horizontal']": 1/12*m*rect_width**2,
                      "['rectangle', 'vertical_edge']": 1/3*m*l_or_r**2, "['rectangle', 'horizontal_edge']": 1/3*m*rect_height**2,
                      "['rectangle', 'distance_d_from_center']": 1/12*m*(rect_width**2+rect_height**2) + m*d_mc_axis**2,
                      "['half_sphere', 'center']": 83/320*m*l_or_r**2,
                      "['half_sphere', 'diameter']": 1/8*m*l_or_r**2, "['half_sphere, edge']": 83/320*m*l_or_r**2+m*(5*l_or_r/8)**2,
                      "['half_sphere', 'tangential_axis']": 403/320*m*l_or_r**2,
                      "['half_sphere', 'distance_d_from_center']": 83/320*m*l_or_r**2 + m*d_mc_axis**2,
                      "['annular_plate', 'center']": 1/2*m*(plate_inner_r**2 + plate_outer_r**2), 
                      "['annular_plate', 'inner_edge']": 1/2*m*(plate_inner_r**2 + plate_outer_r**2) + m*plate_inner_r**2,
                      "['annular_plate', 'outer_edge']": 1/2*m*(plate_inner_r**2 + plate_outer_r**2) + m*plate_outer_r**2,
                      "['annular_plate, 'distance_d_from_center']": 1/2*m*(plate_inner_r**2 + plate_outer_r**2) + m*d_mc_axis**2}
        
        if shape_and_axis in shape_dict:
            d = d_dict[shape_and_axis]
            i = shape_dict[shape_and_axis]
        else:
            raise KeyError("Shape and axis should be chosen from this options:['point', 'distance_l_from_point'], ['rod', 'center'], ['rod', 'distance_d_from_center'], ['rod', 'end'], ['disk', 'center'], ['disk', 'edge'], ['disk', 'distance_d_from_center'], ['hoop', 'center'], ['hoop', 'point_on_rim'], ['hoop', 'distance_d_from_center'], ['solid_sphere', 'center'], ['solid_sphere', 'tangential_axis'], ['solid_sphere', 'distance_d_from_center'], ['hollow_sphere', 'center'], ['hollow_sphere', 'tangential_axis'], ['hollow_sphere', 'distance_d_from_center'], ['rectangle', ''center_vertical'], ['rectangle', 'center_horizontal'], ['rectangle', 'distance_d_from_center'], ['rectangle', 'vertical_edge'], ['rectangle', 'horizontal_edge'], ['half_sphere', 'center'], ['half_sphere', 'diameter'], ['half_sphere, edge'], ['half_sphere', 'tangential_axis'], ['half_sphere', 'distance_d_from_center'], ['annular_plate', 'center'], ['annular_plate', 'inner_edge'], ['annular_plate', 'outer_edge'], ['annular_plate, 'distance_d_from_center']")
        
        angle_list = []
        angle_v_list = []
        if d != 0:
            t = 2*np.pi*np.sqrt(i/(m*self.g*d))
            f = np.sqrt(m*self.g*d / i)
            l_or_r_math = i/(m*d)
        else:
            t = 2*np.pi*np.sqrt(i/(m*self.g*l_or_r))
            f = np.sqrt(m*self.g*l_or_r / i)
            l_or_r_math = i/(m*l_or_r)

        t_linspace = np.linspace(0, t, 100)

        for j in t_linspace:
            angle = start_angle * np.cos(f*j) + v0/f * np.sin(f*j)
            angle_v = -start_angle * f * np.sin(f*j) + v0*np.cos(f*j)
            angle_list.append(angle)
            angle_v_list.append(angle_v)

        t_math = 2*np.pi*np.sqrt(l_or_r_math/self.g)
        f_math = np.sqrt(self.g/l_or_r_math)
        
        return angle_list, angle_v_list, l_or_r_math, t_math, f_math
    
    def rotate_coords_3D(self, coords_list: list[int | float], angle: int | float, rotate_axes: list[str]):
        if len(coords_list) == 3:
            axes_dict = {"YZ": np.array([[1, 0, 0], 
                                        [0, np.cos(angle), -np.sin(angle)],
                                        [0, np.sin(angle), np.cos(angle)]]),
                        "XZ": np.array([[np.cos(angle), 0, np.sin(angle)], 
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]]),
                        "XY": np.array([[np.cos(angle), -np.sin(angle), 0],  
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]]),
                        "yz": np.array([[1, 0, 0], 
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]]),
                        "xz": np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]]),
                        "xy": np.array([[np.cos(angle), -np.sin(angle), 0], 
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])}
            
            rotate_axes = rotate_axes.split()
            rotate_axes = np.array(rotate_axes)

            coords = np.array(coords_list).reshape(3, 1)

            if len(rotate_axes) == 1:
                xyz = axes_dict[rotate_axes[0]] @ coords
            if len(rotate_axes) == 2:
                xyz = axes_dict[rotate_axes[0]] @ axes_dict[rotate_axes[1]] @ coords
            if len(rotate_axes) == 3:
                xyz = axes_dict[rotate_axes[0]] @ axes_dict[rotate_axes[1]] @ axes_dict[rotate_axes[2]] @ coords

            return [xyz[0][0], xyz[1][0], xyz[2][0]]

    def rotate_coords_nD(self, coords_list: list[int | float], angle: int | float, rotate_axes: list[str]):
        coords_dict = {}
        ij_list = []
        rotate_matrix = np.zeros((len(coords_list), len(coords_list)))
        for i in range(len(coords_list)):
            coords_dict[f"x{i + 1}"] = coords_list[i]
            coords_dict[f"X{i + 1}"] = coords_list[i]
            if f"x{i + 1}" == rotate_axes[0] or f"x{i + 1}"  == rotate_axes[1] or f"X{i + 1}" == rotate_axes[0] or f"X{i + 1}"  == rotate_axes[1]:
                ij_list.append(i + 1)
        for a in range(np.shape(rotate_matrix)[0]):
            for b in range(np.shape(rotate_matrix)[1]):
                if a == ij_list[0] and b == ij_list[1]:
                    rotate_matrix[a - 1][b - 1] = -np.sin(angle)
                if a == ij_list[1] and b == ij_list[0]:
                    rotate_matrix[a - 1][b - 1] = np.sin(angle)
                if a == ij_list[0] and b == ij_list[0]:
                    rotate_matrix[a - 1][b - 1] = np.cos(angle)
                if a == ij_list[1] and b == ij_list[1]:
                    rotate_matrix[a - 1][b - 1] = np.cos(angle)
                else:
                    for k in range(a):
                        rotate_matrix[a][a] = 1

        rotate_matrix = np.array(rotate_matrix)
        coords_list = np.array(coords_list)

        xyz = rotate_matrix @ coords_list

        return xyz

    # def moment_of_inertia(self, shape, rotate_axis, **kwargs):
    #     if shape == "paraboloid":
    #         for key, value in kwargs.items():
    #             if key == "radius":
    #                 r = value
    #             if key == "mass":
    #                 m = value
    #             if rotate_axis == "z":
    #                 inert = (2*m*r**2)/3
    #             else:
    #                 inert = f"{2*m*r**2/6}+height**2/12"
    #         for key, value in kwargs.items():
    #             if key == "radius":
    #                 r = value
    #             if key == "mass_density":
    #                 m_dens = value
    #             if key == "height":
    #                 h = value
    #             if rotate_axis == "z":
    #                 inert = (np.pi*m_dens*h*r**4)
    #     if shape == "torus":
    #         for key, value in kwargs.items():
                

    #     return inert
    # Returns angle_list and angle_v_list for phase pendulum trajectory in n-dimensions space
    def nD_pendulum(self, shape: str, dimensions: int, a_or_r: int | float, start_angles: list[int | float], phases: list[int | float], mass_density: int | float, particles_num: int, **kwargs):
        for j in range(len(start_angles)):
            start_angles[j] = np.radians(start_angles[j])
        f_list = []
        i_list = []
        angle_list = []
        deltas = []
        k_list = []
        for q in range(len(start_angles)):
            angle_list.append([])
            deltas.append([])
        m_inert = 0
        m_t = 0
        m_f = 0
        if shape == "hypersphere":
            volume = np.pi**(dimensions/2)/gamma(dimensions/2+1)*a_or_r**dimensions
            l = a_or_r
        if shape == "hypercube":
            volume = a_or_r**dimensions
            l = a_or_r/2
        if shape == "symplex":
            volume = a_or_r**dimensions/math.factorial(dimensions)*np.sqrt((dimensions+1)/2**dimensions)
            l = np.sqrt(dimensions)/(dimensions+1)*a_or_r
        r = np.linspace(0, l, particles_num)
        total_m = mass_density*volume
        delta_v = total_m/particles_num
        dm = mass_density*delta_v
        for k in r:
            if k == 0 or k < 0:
                continue
            else:
                inert = dm*k**2
                if inert != 0:
                    f = np.sqrt(abs(dm*self.g*k / inert))
                else:
                    continue
                m_inert += mass_density*k*delta_v
                m_t += 2*np.pi*np.sqrt(abs(inert/(dm*self.g*k)))
                if inert != 0:
                    m_f += np.sqrt(abs(dm*self.g*k / inert))
                    f_list.append(f)
                    i_list.append(inert)
                    k_list.append(k)
                else:
                    continue
        t = np.linspace(0, particles_num, len(f_list))
        for g in range(len(start_angles)):
            if len(start_angles) == len(phases):
                for x in range(len(t)):
                    angle = start_angles[g] * np.cos(2*np.pi*f_list[x]*t[x] + phases[g])
                    angle_list[g].append(angle)
                if len(angle_list[g]) != 1:
                    d_angle = np.gradient(angle_list[g])
                    deltas[g].append(d_angle)
                else:
                    deltas[g].append(np.zeros_like(angle_list[g]))
            else:
                raise IndexError("Length phases list should be same with length start angles list.")

        mean_f = m_f/particles_num
        mean_i = m_inert/particles_num

        return t, f_list, i_list, mean_f, mean_i, angle_list, deltas
    
    def plot_pendulum(self, func: str):
        angle_list, angle_v_list, l_or_r_math, t_math, f_math = eval(func)

        plt.plot(angle_list, angle_v_list)
        plt.title("Phase Trajectory")
        plt.grid()
        plt.show()

        plt.plot(angle_list, angle_v_list)
        plt.axis("equal")
        plt.title("Phase Trajectory With Equal Axes")
        plt.grid()
        plt.show()

    def plot_nD_pendulum(self, func: str):
        t, f_list, i_list, mean_f, mean_i, angle_list, deltas = eval(func)
        for k in range(len(angle_list)):
            plt.plot(t, angle_list[k], "b-")
            plt.title(f"Angle {k+1}")
            plt.grid()
            plt.show()
            for i in range(len(deltas[k])):
                plt.plot(t, deltas[k][i], "b-")
                plt.title(f"Angle velocity {k+1}")
                plt.grid()
                plt.show()
                plt.plot(angle_list[k], deltas[k][i], "*b")
                plt.title(f"Pendulum phase trajectory {k+1}")
                plt.grid()
                plt.show()
