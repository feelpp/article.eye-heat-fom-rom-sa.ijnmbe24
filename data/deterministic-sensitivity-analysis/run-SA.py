import sys, os
import feelpp.core as fppc
import feelpp.toolboxes.heat as heat
import feelpp.mor as mor
import pandas as pd

PWD = os.getcwd()

o = heat.toolboxes_options("heat")
config = fppc.globalRepository("SA_det")
e = fppc.Environment(sys.argv, opts=o, config=config)

DIM = 3
assert DIM in [2,3]


fppc.Environment.setConfigFile(os.path.join(PWD, "..", "eye.cfg"))

MEASURES_PATH = f"{e.rootRepository()}/SA_det/np_{e.expand('$np')}/heat.measures/values.csv"


def updateParameters(tb, mu):
    for i in range(0,mu.size()):
        tb.addParameterInModelProperties(mu.parameterName(i),mu(i))
    tb.updateParameterValues()

def value(tb, param):
    return tb.modelProperties().parameters().at(param).value()

def printParam(tb, names):
    param = tb.modelProperties().parameters()
    for name in names:
        print(name, param.at(name).value())


def to_kelvin(T_C): return T_C + 273.15
def to_celcius(T):  return T - 273.15

def res_of_meas(meas, points):
    res = {}
    for point in points:
        res[point] = meas[f'Points_{point}_expr_T{point}_C']
    return res

heatBox = heat.heat(dim=DIM, order=2)
heatBox.init()


crb_model_properties = mor.CRBModelProperties(worldComm=fppc.Environment.worldCommPtr())
crb_model_properties.setup(PWD + '/../crb_param.json')
crb_model_parameters = crb_model_properties.parameters()

# modelParameters = heatBox.modelProperties().parameters()
D = mor._mor.ParameterSpace.New(crb_model_parameters, fppc.Environment.worldCommPtr())

control_values = {"k_lens":0.40, "E":40, "h_bl":65, "h_amb":10, "T_amb":to_kelvin(20), "T_bl":to_kelvin(37)}
mu = D.element()
mu.setParameters(control_values)

if e.isMasterRank():
    print(mu.parameterNames())


params = D.parameterNames()
values = {
    "E": [20, 40, 70, 100, 320],
    "T_amb": [273.15, 278, to_kelvin(20), to_kelvin(25), to_kelvin(30), 308],
    "T_bl": [to_kelvin(35), to_kelvin(37), to_kelvin(37.7), to_kelvin(38), to_kelvin(38.5), to_kelvin(39)],
    "h_amb": [8, 10, 12, 15, 100],
    "h_bl": [65, 90, 110],
    "k_lens": [0.21, 0.30, 0.40, 0.544]
}

df_points = pd.read_csv(os.path.join(PWD, "points_coord.csv"))
points_name = list(df_points['Point'])


for param in params:
    if e.isMasterRank():
        print("=================================")
        print("Running for the parameter", param)
        print("param will vary in ", values[param])
    mu.setParameters(control_values)

    df_res = pd.DataFrame(columns=points_name, dtype=float)
    for value in values[param]:
        try:
            mu.setParameterNamed(param, value)
        except RuntimeError as e:
            print(e)
            sys.exit(1)
        if e.isMasterRank():
            print(f"  Running with {param} = {value}")
        updateParameters(heatBox, mu)
        heatBox.solve()
        heatBox.exportResults()
        meas = heatBox.postProcessMeasures().values()

        if param[0] == 'T':
            value = to_celcius(value)
        df_res.loc[value] = res_of_meas(meas, points_name)

    df_res.to_csv(os.path.join(PWD, "results", f"{param}_feel.csv"), index_label=param)
