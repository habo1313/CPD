import cpd
import matplotlib.pyplot as plt
import logging

plt.style.use(['mystyle', 'mystyle-vega'])

ua = {'C': 74.12, 'H': 4.96, 'O': 13.18, 'N': 1.45, 'S': 0}
pa = {'FC': 57, 'VM': 43, 'Ash': 0, 'Moist': 0}

operating_conditions = [[0, 700], [0.01, 1200], [0.02, 1200]]


def create_cpd():
    c = cpd.CPD(ultimate_analysis=ua, proximate_analysis=pa,
                pressure=101325, name='Test')
    c.operating_conditions = operating_conditions
    return c


def test_ode():
    coal = create_cpd()
    t, y, fract = coal._bridge_evolution(time_end=1e-2)
    ax = plt.subplot(111)
    l = y[:, 0]
    delta = y[:, 1]
    c = y[:, 2]
    p = l + c
    f = 1 - p
    g1 = 2 * f - delta
    g2 = 2 * (c - c[0])
    ax.plot(t, l, label='$l$')
    ax.plot(t, delta / 2, label='$\delta/2$')
    ax.plot(t, c, label='$c$')
    ax.plot(t, p, label='$p$')
    ax.plot(t, g1 / 2, label='$g_1/2$')
    ax.plot(t, g2 / 2, label='$g_2/2$')
    ax.legend()

    ax = plt.subplot(111)
    labels = ['solid', 'gas', 'tar', 'meta', 'cross']
    for i, l in enumerate(labels):
        ax.plot(t, fract[:, i], label=l)
    ax.legend()


def test_percolation():
    coal = create_cpd()
    y = [0.01, 0.3, 0.05]
    f_tar = 0
    percolation = coal._percolation(y, f_tar, True)


def test_flash():
    coal = create_cpd()
    y = [0.01, 0.3, 0.05]
    percolation = coal._percolation(y, 0, True)
    df_gas = percolation['f_gas'] * 0.0001
    f = 0.01
    f_frag_n = percolation['f_frag_n']
    df_n = f_frag_n * f
    mw_gas = 28.0
    mw_n = percolation['mw_frag_n']
    meta_n = f_frag_n * (1 - f)
    T = 800.0
    fracr = 1.0
    coal._flash_distillation(df_gas=df_gas, df_n=df_n,
                             meta_n=meta_n, mw_n=mw_n, fracr=fracr, T=T)


def test_find_triangle():
    coal = create_cpd()
    ax = coal.find_triangle(plot='show')
    results = coal.run()
    gas = results['delta'] * 0.5 + results['l']
    X_gas = 1 - gas / gas.iloc[0]
    X = coal.calc_lightgases(X_gas)
    return X


log_level = logging.DEBUG

# logging.basicConfig(level=log_level)
# test_flash()
# test_ode()
# plt.show()
