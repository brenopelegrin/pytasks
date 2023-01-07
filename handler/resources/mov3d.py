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

    if(np.linalg.norm(v) == 0):
        v_hat = np.array([0,0,0])
    else:
        v_hat = v/np.linalg.norm(v)

    F = (-1) * (mu_fluid*D*v + 0.5*rho_fluid*c_d*A_sec*(np.linalg.norm(v)**2)) * v_hat

    return F

def K_energy(m: float, v:np.ndarray):
    return (0.5 * m * np.linalg.norm(v)**2)

def P_energy(m:float, M:float, r:np.ndarray):
    return (-G*M*m/np.linalg.norm(r))

def simulate3D(sim_params:dict, body_params:dict, fluid_params:dict, r0:np.ndarray, v0:np.ndarray, dt: float):
    i=0
    t = [0]

    run_drag = sim_params["drag"]

    mass = body_params["m"]
    r_terra = 6378.1e3
    R_terra = np.array([0, r_terra, 0]) #m
    M_terra = 5.972e24 #kg

    round_to = 6

    radius = body_params["radius"]
    r = [r0.tolist()]
    v = [v0.tolist()]
    w = [[0,0,0]]
    a = []
    alpha = []
    ke = [np.around(K_energy(m=mass, v=v0), round_to).tolist()]

    radius_vec = np.array([0, radius, 0])

    pe_EarthSurf = np.around(P_energy(m=mass, M=M_terra, r=R_terra), round_to)
    pe = [np.around(P_energy(m=mass, M=M_terra, r=r0+R_terra-radius_vec)-pe_EarthSurf, round_to).tolist()]
    
    me = [ke[0]+pe[0]]

    while r[i][1]-radius >= 0:
        gravity_force = F_gravity(m=mass, M=M_terra, r=np.array(r[i])+R_terra)

        if run_drag:
            drag_force = F_drag(body_params, fluid_params, np.array(v[i]))
            a_new = (1/mass) * (gravity_force + drag_force)
        else:
            a_new = (1/mass) * gravity_force

        a.append(np.around(a_new, round_to).tolist())

        #alpha_new = (1/(radius**2)) * np.cross(np.array(r[i]), np.array(a[i]))
        alpha_new = np.array([0,0,0])
        alpha.append(alpha_new.tolist())

        new = euler(a=np.array(a[i]), alpha=np.array(alpha[i]), v=np.array(v[i]), w=np.array(w[i]), r=np.array(r[i]), h=dt)

        v.append(np.around(new["vn"], round_to).tolist())
        r.append(np.around(new["rn"], round_to).tolist())
        w.append(np.around(new["wn"], round_to).tolist())
        ke.append(np.around(K_energy(m=mass, v=new["vn"]), round_to).tolist())
        pe.append(np.around(P_energy(m=mass, M=M_terra, r=new["rn"]+R_terra-radius_vec)-pe_EarthSurf, round_to).tolist())
        me.append(ke[i+1]+pe[i+1])

        t.append(round(t[i]+dt, round_to))
        i+=1

    if ke[0] == 0:
        nke = np.around((np.array(ke)/ke[1]), round_to).tolist()
    else:
        nke = np.around((np.array(ke)/ke[0]), round_to).tolist()

    if pe[0] == 0:
        npe = np.around((np.array(pe)/pe[1]), round_to).tolist()
    else:
        npe = np.around((np.array(pe)/pe[0]), round_to).tolist()

    if me[0] == 0:
        nme = np.around((np.array(me)/me[1]), round_to).tolist()
    else:
        nme = np.around((np.array(me)/me[0]), round_to).tolist()

    result={   
        "t": t, "a": a, "v": v, "r": r,
        "w": w, "alpha": alpha, 
        "ke": ke, "pe": pe, "me": me, "nke": nke, "npe": npe, "nme": nme
    }

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