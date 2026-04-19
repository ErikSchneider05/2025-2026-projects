
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix
import statsmodels.api as sm
from scipy.optimize import minimize
from scipy.optimize import NonlinearConstraint

df = pd.read_csv('indyNXT_IMS_2026_camber_pressure.csv')
print("data Head")
print(df.head())
print("data overview")
print(df.describe())
mean_camber = df['camber_deg'].mean()
mean_psi= df['pressure_psi'].mean()

print(df.corr())

colums_scat = ['camber_deg', 'pressure_psi', 'lat_g', 'tire_temp_C']

scatter_matrix(df[colums_scat], figsize=(8,8), diagonal="hist")


"trends show that camber and pressure have alot to do with tire temp. But Lat_g doesnt really have much impact on those"

camber = df['camber_deg'].to_numpy()
psi = df['pressure_psi'].to_numpy()
y_G = df['lat_g'].to_numpy()

X_G = np.column_stack([np.ones_like(camber), camber, psi, camber**2, psi**2, camber*psi])

model_y_G = sm.OLS(y_G, X_G).fit()
model_y_G_sum = model_y_G.summary()
print(model_y_G_sum)

beta = model_y_G.params
print("\nLaternal Grip Model Coefficients:")
for i, val in enumerate(beta):
    print(f"beta[{i}]: {val:.4f}")

X_G_mean = np.array([[1.0,mean_camber, mean_psi, mean_camber**2, mean_psi**2, mean_camber*mean_psi]])

pred_G_mean = model_y_G.get_prediction(X_G_mean).summary_frame(alpha=0.05) # 95% CI
print("95% CI:")
print(pred_G_mean)

cam_grid = np.linspace(-6.0, 0.0, 100)
psi_grid = np.linspace(17.0, 25.0, 100)
C, P = np.meshgrid(cam_grid, psi_grid)

cam_flat = C.ravel()
Psi_flat = P.ravel()

X_G_Grid = X_Ggrid = np.column_stack([np.ones_like(cam_flat),cam_flat, Psi_flat, cam_flat**2, Psi_flat**2, cam_flat*Psi_flat])

y_G_grid = yG_grid = model_y_G.predict(X_Ggrid).reshape(C.shape)

plt.figure(figsize=(7,5))
contf = plt.contourf(C, P, yG_grid, levels=20, cmap='viridis')
plt.colorbar(contf, label=" Lateral Grip (lat_g)")

plt.scatter(df['camber_deg'], df['pressure_psi'], c=df["lat_g"], edgecolors="k")

plt.xlabel("Camber (deg)")
plt.ylabel("Pressure (psi)")
plt.title(" Plot of Lateral Grip y_G(c, p)")
plt.legend()
plt.grid(True)
plt.tight_layout()





y_T = df['tire_temp_C'].to_numpy()

abs_c = np.abs(camber)

# y_T = gamma0 + gamma1*p + gamma2*|c| + gamma3*log(p) + gamma4*exp(|c|/10)
X_T = np.column_stack([
    np.ones_like(camber), psi, abs_c, np.log(psi), np.exp(abs_c / 10.0)])

model_y_T = sm.OLS(y_T, X_T).fit()
print(model_y_T.summary())

gamma = model_y_T.params
print("\nTire Coefficients:\n")
for i, val in enumerate(gamma):
    print(f"gamma[{i}]: {val:.5f}")

abs_c_mean = np.abs(mean_camber)

X_T_mean = np.array([[1.0,
                        mean_psi,
                        abs_c_mean,
                        np.log(mean_psi),
                        np.exp(abs_c_mean / 10.0)
                        ]])

pred_T_mean = model_y_T.get_prediction(X_T_mean).summary_frame(alpha=0.05) # 95% CI
print(" Predicted Tire 95% CI:")
print(pred_T_mean)

abs_C_flat = np.abs(cam_flat)

X_T_grid = np.column_stack([
    np.ones_like(Psi_flat),
    Psi_flat,
    abs_C_flat,
    np.log(Psi_flat),
    np.exp(abs_C_flat / 10.0)
])

yT_grid = model_y_T.predict(X_T_grid).reshape(C.shape)

plt.figure(figsize=(7, 5))
cf = plt.contourf(C, P, yT_grid, levels=20)
plt.colorbar(cf, label='Tire Temperature (C)')

# Line where y_T = 100 degC
CS = plt.contour(C, P, yT_grid, levels=[100.0], colors='red', linewidths=2)
plt.clabel(CS, fmt="100°C", colors='red')

plt.scatter(df['camber_deg'], df['pressure_psi'], c=df["tire_temp_C"], edgecolors="k")

plt.xlabel("Camber (deg)")
plt.ylabel("Pressure (psi)")
plt.title("Contour Plot of Tire Temperature y_T(c, p)")
plt.legend()
plt.grid(True)
plt.tight_layout()




def y_G_mean(c_val, p_val):
    X = np.array([[1.0, c_val, p_val, c_val**2, p_val**2, c_val*p_val]])
    return (model_y_G.predict(X)[0]).item()

def y_T_mean(c_val, p_val):
    abs_c = abs(c_val)
    X = np.array([[
        1.0,
        p_val,
        abs_c,
        np.log(p_val),
        np.exp(abs_c / 10.0)
    ]])
    return (model_y_T.predict(X)).item()

print(f"Mean Camber: {mean_camber:.3f} deg")
print(f"Mean Pressure: {mean_psi:.3f} psi")
print(f"y_G(mean) = {y_G_mean(mean_camber, mean_psi):.4f} g")
print(f"y_T(mean) = {y_T_mean(mean_camber, mean_psi):.4f} °C")




TEMP_LIMIT = 100.0


def objective(X):
    c_val, p_val = X
    return -y_G_mean(c_val, p_val)

nlc = NonlinearConstraint(
    fun=lambda x: y_T_mean(x[0], x[1]),
    lb=-np.inf,
    ub=TEMP_LIMIT
)

bounds = [(-6.0, 0.0), (17.0, 25.0)]

# Starting Point
c0 = float(np.clip(mean_camber, -6.0, 0.0))
p0 = float(np.clip(mean_psi, 17.0, 25.0))

# If too hot, reduce
if y_T_mean(c0, p0) > TEMP_LIMIT:
    for pp in np.linspace(p0, 17.0, 400):
        if y_T_mean(c0, float(pp)) <= TEMP_LIMIT:
            p0 = float(pp)
            break

x0 = np.array([c0, p0])

print("Start:")
print(f" c0 = {x0[0]:.4f} deg")
print(f" p0 = {x0[1]:.4f} psi")
print(f" y_T(c0, p0), = {y_T_mean(x0[0], x0[1]):.6f} C")

# Solve
result = minimize(
    objective,
    x0,
    method="trust-constr",
    bounds=bounds,
    constraints=[nlc],
    options={
        "verbose": 1,
        "maxiter": 2000
    }
)

print("\nSucess:", result.success)
print(result.message)

c_opt, p_opt = map(float, result.x)
yG_opt = y_G_mean(c_opt, p_opt)
yT_opt = y_T_mean(c_opt, p_opt)

print(f"\nOptimal Camber c  = {c_opt:.4f} deg")
print(f"Optimal Pressure p = {p_opt:.4f} psi")
print(f"Predicted Lateral Grip  = {yG_opt:.4f} g")
print(f"Predicted Tire Temp = {yT_opt:.4f} °C")
print(f"Constraint satisfaction {yT_opt <= 100.0}")

resid = TEMP_LIMIT - yT_opt
print(f"Constraint residual  = {resid:.12e}")
print("Constraint satisfied ", yT_opt <= TEMP_LIMIT)




X_G_opt = np.array([[
    1.0,
    c_opt,
    p_opt,
    c_opt**2,
    p_opt**2,
    c_opt * p_opt
]])

pred_G_opt = model_y_G.get_prediction(X_G_opt).summary_frame(alpha=0.05)

print("95% CI for y_G at optimal point (c*, p*):")
print(pred_G_opt)




print("\nPredicted at optimal setup:")
print(f" c* = {c_opt:.4f} deg, p* = {p_opt:.4f} psi")
print(f" Predicted y_G* = {yG_opt:.6f} g")
print(f" Predicted y_T* = {yT_opt:.6f} °C")




c_grid = np.linspace(-6.0, 0.0, 120)
p_grid = np.linspace(17.0, 25.0, 120)
C, P = np.meshgrid(c_grid, p_grid)

C_flat = C.ravel()
P_flat = P.ravel()

X_Ggrid = np.column_stack([
    np.ones_like(C_flat),
    C_flat,
    P_flat,
    C_flat**2,
    P_flat**2,
    C_flat * P_flat
])
yG_grid = model_y_G.predict(X_Ggrid).reshape(C.shape)


abs_C_flat = np.abs(C_flat)
X_T_grid = np.column_stack([
    np.ones_like(P_flat),
    P_flat,
    abs_C_flat,
    np.log(P_flat),
    np.exp(abs_C_flat / 10.0)
])
yT_grid = model_y_T.predict(X_T_grid).reshape(C.shape)

plt.figure(figsize=(8,6))

#
cf = plt.contour(C, P, yG_grid, levels=25)
plt.colorbar(cf, label="Predicted Lateral Grip y_G (g)")

CS = plt.contour(C, P, yT_grid, levels=[100.0], colors="red", linewidths=2)
plt.clabel(CS, fmt="100°C", colors="red")


plt.scatter(df["camber_deg"], 
            df["pressure_psi"],
            c=df["lat_g"],
            edgecolor="k",
            label="Samples"
            )


plt.scatter(
    c_opt,
    p_opt,
    marker="*",
    s=300,
    color="black",
    label="Optimal Point"
)

plt.xlabel("Camber (deg)")
plt.ylabel("Pressure (psi)")
plt.title("optimal Setup: Maximize y_G with y_T <= 100°C Constraint")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()