import numpy as np
import math

G = 6.6743e-11 # m3 kg-1 s-2

def euler(a:np.ndarray, alpha:np.ndarray, v:np.ndarray, w:np.ndarray, r:np.ndarray, h:float):
    wn = w + alpha*h
    vn = v + a*h
    rn = r + v*h
    return {"vn": vn, "rn": rn, "wn": wn}

def F_gravity(m: float, M:float, r:np.ndarray):
    r_hat = r/(np.linalg.norm(r))
    F = -(G*M*m*r_hat)/(np.linalg.norm(r)**2)

    return F

def F_drag(body_params:dict, fluid_params:dict, v:np.ndarray):
    m = body_params["m"]
    r = body_params["radius"]
    A_sec = body_params["A_sec"]
    D = 2*r
    c_d = body_params["drag_coefficient"]

    rho_fluid = fluid_params["density"]
    mu_fluid = fluid_params["knematic_viscosity"]

    v_hat = v/np.linalg.norm(v)
    F = (-1) * (mu_fluid*D*v + 0.5*rho_fluid*c_d*A_sec*(np.linalg.norm(v)**2)) * v_hat

    return F

def simulate3D(sim_params:dict, body_params:dict, fluid_params:dict, r0:np.ndarray, v0:np.ndarray, dt: float):
    i=0
    t = [0]

    run_drag = sim_params["drag"]

    mass = body_params["m"]
    r_terra = 6378.1e3
    R_terra = np.array([0, r_terra, 0]) #m
    M_terra = 5.972e24 #kg

    radius = body_params["radius"]

    r = [r0.tolist()]
    v = [v0.tolist()]
    w = [[0,0,0]]
    a = []
    alpha = []

    while r[i][1]+radius >= 0:

        drag_force = F_drag(body_params, fluid_params, np.array(v[i]))
        gravity_force = F_gravity(m=mass, M=M_terra, r=np.array(r[0])+R_terra)

        if run_drag:
            a_new = (1/mass) * (gravity_force + drag_force)
        else:
            a_new = (1/mass) * gravity_force

        a.append(np.around(a_new,6).tolist())

        alpha_new = (1/(radius**2)) * np.cross(np.array(r[i]), np.array(a[i]))
        alpha_new = np.array([0,0,0])
        alpha.append(alpha_new.tolist())

        new = euler(a=np.array(a[i]), alpha=np.array(alpha[i]), v=np.array(v[i]), w=np.array(w[i]), r=np.array(r[i]), h=dt)

        v.append(np.around(new["vn"],6).tolist())
        r.append(np.around(new["rn"],6).tolist())
        w.append(np.around(new["wn"],6).tolist())

        t.append(round(t[i]+dt,6))
        i+=1

    result={"t": t, "a": a, "v": v, "r": r, "w": w, "alpha": alpha}

    return result

class SphericalBody:
    def __init__(self, mass:float, radius:float, drag_coefficient:float):
        self.params={}
        self.params["m"] = mass 
        self.params["A_sec"] = math.pi * radius**2
        self.params["radius"] = radius
        self.params["drag_coefficient"] = drag_coefficient

class Fluid:
    def __init__(self, density:float, knematic_viscosity:float):
        self.params={}
        self.params["density"] = density
        self.params["knematic_viscosity"] = knematic_viscosity

class Simulation3D:
    def __init__(self, body_params:dict, fluid_params:dict, r0:list, v0:list, dt: float):
        self.result = {}
        self.r0 = np.array(r0)
        self.v0 = np.array(v0)
        self.dt = dt
        self.body_params = body_params
        self.fluid_params = fluid_params
        self.config = {"drag": False}
    
    def run(self):
        self.result = simulate3D(sim_params=self.config, body_params=self.body_params, fluid_params=self.fluid_params, r0 = self.r0, v0 = self.v0, dt = self.dt)
    def result(self):
        print(self.result)