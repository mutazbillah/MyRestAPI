from statistics import mean


class Deployment:
    def _init_(self, base_directory, context):
        print("Initialising deployment my-depyloyment-prototype")

    def request(self, data):
        print("Processing request for deployment my-depyloyment-prototype")
        option_type_string_value = data["option-type-string"]
        interest_rate_double_value = data["interest-rate-double"]
        minimum_option_runtime_double_value = data["minimum-option-runtime-double"]
        runtime_fixed_string_value = data["runtime-fixed-string"]
        expected_value_additional_years_double_value = data["expected-value-additional-years-double"]
        cashflow_type_string_value = data["cashflow-type-string"]
        cashflow_process_string_value = data["cashflow-process-string"]
        cashflow_initial_double_value = data["cashflow-initial-double"]
        cashflow_drift_double_value = data["cashflow-drift-double"]
        cashflow_volatility_double_value = data["cashflow-volatility-double"]
        cashflow_velocity_double_value = data["cashflow-velocity-double"]
        cashflow_jumps_per_year_double_value = data["cashflow-jumps-per-year-double"]
        cashflow_volatiliy_of_jump_double_value = data["cashflow-volatiliy-of-jump-double"]

        # <YOUR CODE>

        import numpy as np
        import scipy
        import pandas as pd
        # import matplotlib.pyplot as plt
        # import io
        # import base64

        num_sim = 1000

        investment = 0

        df = pd.DataFrame()

        if runtime_fixed_string_value == "no":
            opt_add_runtime = sum(expected_value_additional_years_double_value)
            x = np.random.poisson(lam=opt_add_runtime, size=num_sim)
            optionRuntime = x + minimum_option_runtime_double_value
        else:
            optionRuntime = np.full(
                num_sim, minimum_option_runtime_double_value)

        for i in range(0, len(cashflow_type_string_value), 1):
            inout = cashflow_type_string_value[i]
            process = cashflow_process_string_value[i]
            s0 = cashflow_initial_double_value[i]
            mu = cashflow_drift_double_value[i]
            sigma = cashflow_volatility_double_value[i]
            # alpha = np.log(2)/cashflow_velocity_double_value[i]
            lamda = cashflow_jumps_per_year_double_value[i]
            sigmaJ = cashflow_volatiliy_of_jump_double_value[i]
            # x0 = # unklar welcher Wert
            colname = 'cf_' + str(i + 1)
            listCashflow = []

            if inout == "outflow":
                investment = investment + s0

            if process == 'gbm':
                for u in range(0, num_sim, 1):
                    temp = s0 * np.exp((mu - (sigma ** (2) / 2)) * optionRuntime[u] + scipy.stats.norm.ppf(
                        np.random.random()) * sigma * np.sqrt(optionRuntime[u]))
                    # print(temp)
                    # print(type(temp))
                    listCashflow.append(temp)

            elif process == 'gmr':
                alpha = np.log(2) / cashflow_velocity_double_value[i]
                # print(alpha)
                for u in range(0, num_sim, 1):
                    temp = np.exp(np.log(s0) * np.exp(-alpha * optionRuntime[u]) + ((np.log(
                        s0 * np.exp(interest_rate_double_value * optionRuntime[u])) + sigma * (2) / (4 * alpha)) - (
                                                                                                sigma * (2) / (
                                                                                                4 * alpha))) * (
                                              1 - np.exp(-alpha * optionRuntime[u])) + scipy.stats.norm.ppf(
                        np.random.random()) * np.sqrt(
                        (1 - np.exp(-2 * alpha * optionRuntime[u])) * (sigma ** (2) / (2 * alpha))))
                    listCashflow.append(temp)

            elif process == 'gbmJ':
                for u in range(0, num_sim, 1):
                    Nt = np.random.poisson(lam=lamda * optionRuntime[u])
                    temp = s0 * np.exp((mu - (sigma ** (2) / 2)) * optionRuntime[u] + scipy.stats.norm.ppf(
                        np.random.random()) * sigma * np.sqrt(
                        optionRuntime[u])) * np.exp(
                        -(sigmaJ / 2) * Nt + np.sqrt(Nt) * sigmaJ * scipy.stats.norm.ppf(np.random.random()))
                    listCashflow.append(temp)

            elif process == 'gmrJ':
                alpha = np.log(2) / cashflow_velocity_double_value[i]
                # print(alpha)
                for u in range(0, num_sim, 1):
                    Nt = np.random.poisson(lam=lamda * optionRuntime[u])
                    temp = np.exp(np.log(s0) * np.exp(-alpha * optionRuntime[u])) + ((np.log(
                        s0 * np.exp(interest_rate_double_value * optionRuntime[u])) + sigma * (2) / (4 * alpha)) - (
                                                                                                 sigma * (2) / (
                                                                                                     4 * alpha))) * (
                                       1 - np.exp(-alpha * optionRuntime[u])) + scipy.stats.norm.ppf(
                        np.random.random()) * np.sqrt(
                        (1 - np.exp(-2 * alpha * optionRuntime[u])) * (sigma ** (2) / (2 * alpha))) * np.exp(
                        -(sigmaJ / 2) * Nt + np.sqrt(Nt) * sigmaJ * scipy.stats.norm.ppf(np.random.random()))
                    listCashflow.append(temp)

            elif process == 'no uncertainities':
                for u in range(0, num_sim, 1):
                    temp = float(s0)
                    listCashflow.append(temp)

            df[colname] = listCashflow

        df['result'] = df.sum(axis=1)

        df['net_value'] = np.where(df['result'] > 0, df['result'], 0)

        final = mean(df['net_value'])

        expected_option_value_value = round(final, 2)

        if investment == 0:
            expected_iption_value_percent_value = 0
        else:
            expected_iption_value_percent_value = round(final / -investment, 2)

        if np.var(df['net_value']) != 0:
            confidence = scipy.stats.t.interval(0.95, len(
                df['net_value']) - 1, loc=np.mean(df['net_value']), scale=scipy.stats.sem(df['net_value']))

            upper_value = round(confidence[1], 2)
            lower_value = round(confidence[0], 2)
        else:
            upper_value = 0
            lower_value = 0

        return {
            # TODO fill in the values of your output fields
            "expected-option-value": expected_option_value_value,
            "expected-iption-value-percent": expected_iption_value_percent_value,
            "95_upper": upper_value,
            "95_lower": lower_value,
            # "graph_1": graph_1_value

        }


if __name__ == '__main__':
    data = Deployment()

    mydic = {



        "option-type-string": "strategic growth option",
        "interest-rate-double":0.49,
        "minimum-option-runtime-double":5,
        "runtime-fixed-string":"no",
        "expected-value-additional-years-double":[0,0],
        "cashflow-type-string":["inflow","inflow"],
        "cashflow-process-string":["","no uncertainities"],
        "cashflow-initial-double":[0, 565896],
        "cashflow-drift-double":[0,0],
        "cashflow-volatility-double":[0,0],
        "cashflow-velocity-double":[0,0],
        "cashflow-jumps-per-year-double":[0,0],
        "cashflow-volatiliy-of-jump-double":[0,0]
    }
    print(data.request(mydic))

