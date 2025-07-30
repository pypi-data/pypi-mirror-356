def initialize_model(degree = 1, iterations = 500, n_s_values = 50, s_value_range_factor = [1 / 12, 1 / 6], *, weight_conv_window = 101, val_split = 0.1, s_value_increase = 1.01):
    import matplotlib.pyplot as plot
    import numpy
    plot.style.use('seaborn-v0_8-whitegrid')

    from scipy.interpolate import UnivariateSpline
    from ExoRM import get_exorm_filepath, ExoRM, unique_radius, read_rm_data, preprocess_data, ForecasterRM

    data = read_rm_data()
    data = unique_radius(data)
    data = preprocess_data(data)

    x = data['radius']
    y = data['mass']

    x = numpy.log10(x)
    y = numpy.log10(y)

    w = numpy.diff(x)
    w = numpy.append(w, w[-1])

    window = weight_conv_window
    w = numpy.convolve(w, numpy.ones(window) / window, mode = 'same') # using edge-padding makes the edges have too much weight
    w *= 1 - (data['error_score'])
    w /= numpy.mean(w)

    n = len(x)
    s_values = numpy.linspace(n * s_value_range_factor[0], n * s_value_range_factor[1], n_s_values)

    split = 1 - val_split
    result = []

    def create_model_fast(x, y, w, s):
        model = UnivariateSpline(x, y, k = degree, s = s, w = w)
        model = ExoRM(model, x, y)

        return model

    for _ in range(iterations):
        mask = numpy.zeros(n, dtype = bool)
        i = numpy.sort(numpy.random.default_rng().choice(n, int(n * split), replace = False))
        mask[i] = True

        xt = x[mask]
        yt = y[mask]
        wt = w[mask]

        xv = x[~mask]
        yv = y[~mask]
        wv = w[~mask]

        best_s, best_mape = numpy.inf, numpy.inf
        for s in s_values:
            model = create_model_fast(xt, yt, wt, s * split)
            mape = numpy.mean(wv * (yv - model(xv)) ** 2)

            if mape < best_mape:
                best_mape = mape
                best_s = s

        result.append(best_s)

    best_s = numpy.median(result) * s_value_increase
    print(f'Final s value (increased by 1% to prevent overfitting): {best_s}')

    model = UnivariateSpline(x, y, k = degree, s = best_s, w = w)
    model = ExoRM(model, x, y)
    model.create_error_model()

    x_smooth = numpy.linspace(min(x) - 0.1, max(x) + 0.1, 10000)
    y_smooth = model(x_smooth)

    y_smooth = model(x_smooth)
    e_smooth = model.error(x_smooth)

    plot.scatter(x, y, s = 1)
    plot.plot(x_smooth, y_smooth, color = 'C1')
    plot.plot(x_smooth, y_smooth + e_smooth, color = 'C2')
    plot.plot(x_smooth, y_smooth - e_smooth, color = 'C2')
    # plot.plot(x_smooth, e_smooth)
    plot.show()

    model.save(get_exorm_filepath('radius_mass_model.pkl'))

    return model