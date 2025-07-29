# type: ignore

# ----------------------------------------
# Methods from the old simulator
# - Remove scipy depecencies for now
# ----------------------------------------

import math

# import scipy.integrate as integrate
# from scipy.stats import norm


def mean_spot_gbm(drift: float, spot_0: float, maturity: float):
    """function that returns the mean of spot of geometric brownian motion at maturity t given a
    gbm drift
    """
    result = spot_0 * math.exp(drift * maturity)
    return result


def variance_spot_gbm(drift: float, volatility: float, spot_0: float, maturity: float):
    """function that returns the variance of spot of geometric brownian motion at maturity t given a
    volatility and drift
    """
    result = spot_0 * spot_0 * math.exp(2 * drift * maturity) * (math.exp(volatility * volatility * maturity) - 1.0)
    return result


'''
def probability_spot_bgm_between(
    drift: float, volatility: float, spot_0: float, maturity: float, upper_limit: float, lower_limit: float
):
    """function that returns the probability of spot under bgm model being between Lower and upper limit"""
    if upper_limit < lower_limit:
        raise Exception("upper_limit should be higher than lower_limit ")
    upper = math.log(upper_limit / spot_0)
    lower = math.log(lower_limit / spot_0)
    gaussian_drift = (drift - volatility * volatility * 0.5) * maturity
    upper = (upper - gaussian_drift) / volatility * math.sqrt(maturity)
    lower = (lower - gaussian_drift) / volatility * math.sqrt(maturity)
    probability = norm.cdf(upper) - norm.cdf(lower)
    return probability
'''

'''
def time_spot_bgm_between(
    drift: float, volatility: float, spot_0: float, maturity: float, upper_limit: float, lower_limit: float
):
    """function that returns the average time of spot under bgm model to be between Lower and upper limit
    between time 0 and maturity"""

    def integrand(t: float):
        """integral 0 to T of integrand will give the average time spend between upper and lower range"""
        result = probability_spot_bgm_between(drift, volatility, spot_0, t, upper_limit, lower_limit)
        return result

    integral = integrate.quad(integrand, 0.0, maturity)[0]
    return integral
'''


def effective_fee_uniswap_v3(fee_tiers: float, trading_volume: float, total_liquidity: float):
    """return the effective fee percentage"""
    return fee_tiers * trading_volume / total_liquidity


'''
def uniswap_v3_average_future_fees(
    fee_tiers: float,
    trading_volume: float,
    lp_liquidity: float,
    total_liquidity: float,
    drift: float,
    volatility: float,
    spot_0: float,
    maturity: float,
    upper_limit: float,
    lower_limit: float,
):
    """function that returns an average estimate of trading fees to be accumulated for a given market scenario
    parameters:

        fee_tiers : the % tiers of the pool - for uniswap V3 this is 0.3%
        trading_volume : average trading volume for a duration T
        lp_liquidity : the total liquidity of LP locked between range Lower, Upper
        total_liquidity : the total liquidity of LPs available between the same range
    """
    average_time = time_spot_bgm_between(drift, volatility, spot_0, maturity, upper_limit, lower_limit)
    effective_fee = effective_fee_uniswap_v3(fee_tiers, trading_volume, total_liquidity)
    metric = effective_fee * average_time * lp_liquidity
    return metric
'''


def il_geometric_mean_market(spots: list, original_spots: list, weights: list):
    """function that implements the theoretical IL for a geometric mean market"""
    if len(spots) != len(original_spots) or len(spots) != len(weights) or len(original_spots) != len(weights):
        raise Exception("size of spot, original spots and weights should be equal ")
    abnormal_weight = [w for w in weights if w < 0 or w > 1]
    if len(abnormal_weight) > 0:
        raise Exception("weights should be positive and below 1")
    if sum(weights) != 1.0:
        raise Exception("weights should have a sum of 1")
    product = 1.0
    sum_w = 0
    for s, s0, w in zip(spots, original_spots, weights):
        product *= (s / s0) ** w
        sum_w += w * s / s0
    return product / sum_w - 1


'''
def average_il_geometric_mean_market(drift, volatility, spot_0, maturity, weight):
    """returns the average IL for a given market scenario - for a GMM model for two assets"""
    factor = 1.0 / math.sqrt(2 * math.pi)
    sqrt_t = math.sqrt(maturity)

    def _gbm_distribution(s):
        result = (
            factor
            / volatility
            / sqrt_t
            / s
            * math.exp(
                -((math.log(s / spot_0) - (drift - 0.5 * volatility * volatility) * maturity) ** 2)
                / (2 * volatility * volatility * maturity)
            )
        )
        return result

    def _integrand(s):
        distribution = _gbm_distribution(s)
        il_s = il_geometric_mean_market([s, 1], [spot_0, 1], [weight, 1.0 - weight])
        return distribution * il_s

    integral = integrate.quad(_integrand, 0.0, np.inf)[0]
    return integral
'''


def uniswap_v2_il(initial_price, final_price):
    """return the IL for uniswap V2 for 2
    Parameters:
        initial_price : token B in terms of token A price at inception when the LP joins the pool
        final_price : token B in terms of token A price at final date for which we calculate the IL
    """
    # z = final_price / initial_price
    spots = [final_price, 1.0]
    original_spots = [initial_price, 1.0]
    weights = [0.5, 0.5]
    result = il_geometric_mean_market(spots=spots, original_spots=original_spots, weights=weights)
    return result


def uniswap_v3_il(minimum_range, maximum_range, initial_price, final_price, liquidity):
    """returns the absolute and relative IL for uniswap V3 for an LP deploying his liquidity on a range [pa,pb] and
    the current value of the liquidity position
    Parameters:
        minimum_range : the lower limit of the range = a - Pa unit is the price range of token B in terms of A
        maximum_range : the upper limit of the range = b - Pb unit is the price range of token B in terms of A
        initial_price : token B in terms of token A price at inception when the LP joins the pool
        final_price : token B in terms of token A price at final date for which we calculate the IL
        liquidity : the liquidity in the NFT
    """
    final_price_truncated = (
        minimum_range
        if final_price < minimum_range
        else (maximum_range if final_price > maximum_range else final_price)
    )
    initial_price_truncated = (
        minimum_range
        if initial_price < minimum_range
        else (maximum_range if initial_price > maximum_range else initial_price)
    )
    hodl_position = liquidity * (
        math.sqrt(initial_price_truncated) - math.sqrt(minimum_range)
    ) + liquidity * final_price * (1 / math.sqrt(initial_price_truncated) - 1 / math.sqrt(maximum_range))
    position_value = liquidity * (
        math.sqrt(final_price_truncated) - math.sqrt(minimum_range)
    ) + liquidity * final_price * (1 / math.sqrt(final_price_truncated) - 1 / math.sqrt(maximum_range))

    abs_il = position_value - hodl_position
    perc_il = abs_il / hodl_position
    return perc_il, abs_il, position_value


'''
def average_il_uniswap_v3(drift, volatility, spot_0, maturity, minimum_range, maximum_range):
    """returns the average IL for a given market scenario - for a GMM model for two assets"""
    factor = 1.0 / math.sqrt(2 * math.pi)
    sqrt_t = math.sqrt(maturity)

    def _gbm_distribution(s):
        result = (
            factor
            / volatility
            / sqrt_t
            / s
            * math.exp(
                -((math.log(s / spot_0) - (drift - 0.5 * volatility * volatility) * maturity) ** 2)
                / (2 * volatility * volatility * maturity)
            )
        )
        return result

    def _integrand(s):
        distribution = _gbm_distribution(s)
        il_s = uniwap_v3_il(
            minimum_range=minimum_range, maximum_range=maximum_range, initial_price=spot_0, final_price=s
        )
        return distribution * il_s

    integral = integrate.quad(_integrand, 0.0, np.inf)[0]
    return integral
'''


"""
if __name__ == "__main__":
    drift = 0.2
    volatility = 0.5
    minimum_range = 0.03
    total_liquidity_on_range = 15e6
    maximum_range = 0.2

    spot_0 = 0.10
    maturity = 1.0

    si = [0.01 + 0.2 / 100.0 * i for i in range(100)]
    il_univ2 = [uniswap_v2_il(initial_price=spot_0, final_price=si[i]) for i in range(100)]
    il_univ3 = [
        uniwap_v3_il(minimum_range=minimum_range, maximum_range=maximum_range, initial_price=spot_0, final_price=spot)
        for spot in si
    ]

    # what is the average IL after 1Y of this LP providing his liquidity for a couple XY where the current spot is
    # 0.1 - the range targeted by the LP is 0.03 - 0.2 with the market scenario vol 50% and 20% drift market

    average_univ3_il = average_il_uniswap_v3(
        drift=drift,
        volatility=volatility,
        spot_0=spot_0,
        maturity=maturity,
        minimum_range=minimum_range,
        maximum_range=maximum_range,
    )
    print(average_univ3_il)

    # how is the IL moving the volatility everything else being constant

    vol_i = [0.001 + 0.8 / 100.0 * i for i in range(100)]
    average_univ3_il_i = [
        average_il_uniswap_v3(
            drift=drift,
            volatility=vol,
            spot_0=spot_0,
            maturity=maturity,
            minimum_range=minimum_range,
            maximum_range=maximum_range,
        )
        for vol in vol_i
    ]
    print(average_univ3_il)

    # below we can look at how the probability of staying between the range is behaving function of various parameters
    probability_between_low_high_at_maturity = probability_spot_bgm_between(
        maturity=maturity,
        spot_0=spot_0,
        volatility=volatility,
        lower_limit=minimum_range,
        upper_limit=maximum_range,
        drift=drift,
    )
    print("probability of spot being between low and up limits at maturity", probability_between_low_high_at_maturity)
    probability_function_vol = [
        probability_spot_bgm_between(
            maturity=maturity,
            spot_0=spot_0,
            volatility=vol,
            lower_limit=minimum_range,
            upper_limit=maximum_range,
            drift=drift,
        )
        for vol in vol_i
    ]
    print(probability_function_vol)

    #  what is the uniswap average future fees for a given market scenario
    # trading volume = 1million per day - for 365 days -> 365e6
    # LP liquidity = 100K
    # Liquidity on the same range than the LP = 15M
    lp_liquidity = 100e3
    average_fee = uniswap_v3_average_future_fees(
        fee_tiers=0.003,
        trading_volume=365e6,
        lp_liquidity=lp_liquidity,
        total_liquidity=total_liquidity_on_range,
        drift=drift,
        volatility=volatility,
        spot_0=spot_0,
        maturity=maturity,
        upper_limit=maximum_range,
        lower_limit=minimum_range,
    )
    print("return of the investor", average_fee / lp_liquidity)

    average_fee_vol = [
        uniswap_v3_average_future_fees(
            fee_tiers=0.003,
            trading_volume=365e6,
            lp_liquidity=lp_liquidity,
            total_liquidity=total_liquidity_on_range,
            drift=drift,
            volatility=vol,
            spot_0=spot_0,
            maturity=maturity,
            upper_limit=maximum_range,
            lower_limit=minimum_range,
        )
        for vol in vol_i
    ]
    print(average_fee_vol)
"""
