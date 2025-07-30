from jaxkineticmodel.kinetic_mechanisms.JaxKineticMechanisms import Mechanism


class HOR2_Func_TEMP(Mechanism):
    """Temporary function until I have figured how to deal with simple activator constructs
    and Mechanism object"""

    @staticmethod
    def compute(substrate, vmax, km_substrate, inhibitor, k_I):
        # Initial velocity calculation (without modifiers)
        v = (vmax * substrate / km_substrate) / (1 + substrate / km_substrate)
        v *= 1 + inhibitor / k_I

        return v


class G3PDH_Func_TEMP(Mechanism):
    """Specific Rev BiBi MM with 3 modifiers for G3PDH"""

    @staticmethod
    def compute(substrate1, substrate2, product1, product2,
                modifier1, modifier2, modifier3, vmax,
                k_equilibrium, km_substrate1, km_substrate2,
                km_product1, km_product2, ka1, ka2, ka3):
        denominator = (
                (1 + substrate1 / km_substrate1 + product1 / km_product1)
                * (1 + substrate2 / km_substrate2 + product2 / km_product2)
                * (1 + modifier1 / ka1 + modifier2 / ka2 + modifier3 / ka3)
        )

        numerator = (vmax / (km_substrate1 * km_substrate2)) * (
                substrate1 * substrate2 - (product1 * product2 / k_equilibrium)
        )

        return numerator / denominator


class Jax_PFK(Mechanism):
    """Specifically designed for PFK (for which the functional expression we retrieved from:
    Metabolic Engineering 77 (2023) 128–142
    Available online 23 March 2023
    1096-7176/© 2023 The Authors. Published by Elsevier Inc. on behalf of International Metabolic Engineering Society.
    This is an open access article under the CC
    BY license (http://creativecommons.org/licenses/by/4.0/).

    Elucidating yeast glycolytic dynamics at steady state growth and glucose
    pulses through kinetic metabolic modeling

    Think of reducing the equation by assuming AMP, ATP, ADP are constant
    """

    @staticmethod
    def compute(substrate1, substrate2, product,
                modifiers, vmax, kr_F6P, kr_ATP, gr, c_ATP,
                ci_ATP, ci_AMP, F26BP, ci_F26BP, ci_F16BP, l,
                kATP, kAMP, kF26BP, kF16BP):
        lambda1 = substrate1 / kr_F6P
        lambda2 = substrate2 / kr_ATP
        R = 1 + lambda1 * lambda2 + gr * lambda1 * lambda2
        T = 1 + c_ATP * lambda2
        L = (
                l
                * ((1 + ci_ATP * substrate2 / kATP) / (1 + substrate2 / kATP))
                * ((1 + ci_AMP * modifiers / kAMP) / (modifiers / kAMP))
                * ((1 + ci_F26BP * F26BP / kF26BP + ci_F16BP * product / kF16BP) / (
                1 + F26BP / kF26BP + product / kF16BP))
        )

        return vmax * gr * lambda1 * lambda2 * R / (R ** 2 + L * T ** 2)


class Jax_MM_Rev_BiBi_w_Activation:
    """Specific Rev BiBi MM with 3 modifiers for G3PDH"""

    def __init__(
            self,
            substrate1: str,
            substrate2: str,
            product1: str,
            product2: str,
            modifiers: list,
            vmax: str,
            k_equilibrium: str,
            km_substrate1: str,
            km_substrate2: str,
            km_product1: str,
            km_product2: str,
            ka1: str,
            ka2: str,
            ka3: str,
    ):
        self.vmax = vmax
        self.k_equilibrium = k_equilibrium
        self.km_substrate1 = km_substrate1
        self.km_substrate2 = km_substrate2
        self.km_product1 = km_product1
        self.km_product2 = km_product2
        self.ka1 = ka1
        self.ka2 = ka2
        self.ka3 = ka3
        self.substrate1 = substrate1
        self.substrate2 = substrate2
        self.product1 = product1
        self.product2 = product2
        self.modifier = modifiers

    def __call__(self, eval_dict):
        vmax = eval_dict[self.vmax]
        k_equilibrium = eval_dict[self.k_equilibrium]
        km_substrate1 = eval_dict[self.km_substrate1]
        km_substrate2 = eval_dict[self.km_substrate2]
        km_product1 = eval_dict[self.km_product1]
        km_product2 = eval_dict[self.km_product2]
        ka1 = eval_dict[self.ka1]
        ka2 = eval_dict[self.ka2]
        ka3 = eval_dict[self.ka3]

        substrate1 = eval_dict[self.substrate1]
        substrate2 = eval_dict[self.substrate2]
        product1 = eval_dict[self.product1]
        product2 = eval_dict[self.product2]

        modifier = []
        for mod in self.modifier:
            modifier.append(eval_dict[mod])

        denominator = (
                (1 + substrate1 / km_substrate1 + product1 / km_product1)
                * (1 + substrate2 / km_substrate2 + product2 / km_product2)
                * (1 + modifier[0] / ka1 + modifier[1] / ka2 + modifier[2] / ka3)
        )

        numerator = (vmax / (km_substrate1 * km_substrate2)) * (
                substrate1 * substrate2 - (product1 * product2 / k_equilibrium)
        )

        # numerator = vmax * (substrate1 * substrate2 / (km_substrate1 * km_substrate2)) * \
        #             (1 - 1 / k_equilibrium * (product1 *product2/ (substrate1 * substrate2)))
        return numerator / denominator


# v_GAPDH
class Jax_MM_Ordered_Bi_Tri(Mechanism):
    """Ordered Bi-Tri MM model with co-factor binding first."""

    @staticmethod
    def compute(substrate1, substrate2, substrate3, product1, product2,
                vmax, k_equilibrium, km_substrate1, km_substrate2, km_product1, km_product2, ki):
        s1 = substrate1
        s2 = substrate2
        s3 = substrate3
        p1 = product1
        p2 = product2

        numerator = vmax * (s1 * s2 * s3 - p1 * p2 / k_equilibrium) / (km_substrate1 * km_substrate2 * ki)
        denominator = (
                (1 + substrate1 / km_substrate1) * (1 + s2 / km_substrate2) * (1 + s3 / ki)
                + (1 + p1 / km_product1) * (1 + p2 / km_product2)
                - 1
        )

        return numerator / denominator


class Jax_MM_Irrev_Uni_w_Modifiers:
    """Irreversible Michaelis-Menten model with modifiers."""

    def __init__(
            self, substrate: str, vmax: str, km_substrate: str, modifiers_list: list, modifiers
    ):  # classes of modifier type
        self.vmax = vmax
        self.km_substrate = km_substrate
        self.substrate = substrate
        self.modifiers = modifiers
        self.modifiers_list = modifiers_list

    def __call__(self, eval_dict):
        vmax = eval_dict[self.vmax]
        km_substrate = eval_dict[self.km_substrate]
        substrate = eval_dict[self.substrate]

        # Initial velocity calculation (without modifiers)
        v = (vmax * substrate / km_substrate) / (1 + substrate / km_substrate)

        # Apply each modifier
        for i, modifier in enumerate(self.modifiers):
            modifier_conc = eval_dict[self.modifiers_list[i]]
            v *= modifier.add_modifier(modifier_conc, eval_dict)

        return v


class Jax_Hill_Irreversible_Bi_Activation(Mechanism):
    """Hill Bi-substrate irreversible model with activation. (PYK1)"""

    @staticmethod
    def compute(substrate1, substrate2,
                product, activator, vmax,
                k_substrate1, k_substrate2,
                k_product, k_activator, hill, l):
        # Calculate velocity using Hill equation with activation
        numerator = vmax * substrate1 * substrate2 / (k_substrate1 * k_substrate2)
        denominator = ((1 + substrate1 / k_substrate1) * (1 + substrate2 / k_substrate2)) * (
                (substrate1 / k_substrate1 + 1) ** (hill - 1)
        )

        activator_term = l * (((product / k_product + 1) / (activator / k_activator + 1)) ** hill)
        hill_term = (substrate1 / k_substrate1 + 1) ** hill

        return numerator / (denominator * activator_term + hill_term)


class Jax_Hill_Irreversible_Inhibition(Mechanism):
    """Hill irreversible model with inhibition."""

    @staticmethod
    def compute(substrate, vmax, hill, k_half_substrate,
                ki, inhibitor):
        # Calculate the numerator
        numerator = vmax * ((substrate / k_half_substrate) ** hill)

        # Calculate the denominator
        denominator = 1 + ((substrate / k_half_substrate) ** hill) + (inhibitor / ki)

        # Return the rate
        return numerator / denominator


class Jax_MM_Irrev_Bi_w_Inhibition(Mechanism):
    """Irreversible Michaelis-Menten Bi-substrate model with inhibition."""

    @staticmethod
    def compute(substrate,
                product,
                vmax,
                km_substrate1,
                ki):
        # Calculate the rate
        numerator = (vmax * substrate * product)
        denominator = ((km_substrate1 * ki) + (km_substrate1 * substrate) * product)
        return numerator / denominator


class Jax_MM_Rev_BiBi_w_Inhibition(Mechanism):
    """Reversible Bi-Bi Michaelis-Menten model with inhibition."""

    @staticmethod
    def compute(substrate1, substrate2, product1,
                product2, modifier, ki_inhibitor,
                vmax, k_equilibrium, km_substrate1, km_substrate2,
                km_product1, km_product2):
        # Calculate the denominator
        denominator = (1 + substrate1 / km_substrate1 + product1 / km_product1) * (
                1 + substrate2 / km_substrate2 + product2 / km_product2 + modifier / ki_inhibitor
        )

        # Calculate the numerator
        numerator = (
                vmax
                * (substrate1 * substrate2 / (km_substrate1 * km_substrate2))
                * (1 - 1 / k_equilibrium * (product1 * product2 / (substrate1 * substrate2)))
        )

        # Calculate the rate
        v = numerator / denominator
        return v


class Jax_ADH(Mechanism):
    """JAX class for the ADH reaction with detailed rate expression."""

    @staticmethod
    def compute(NAD, ETOH, NADH, ACE, vmax, k_equilibrium,
                km_substrate1, km_substrate2, km_product1, km_product2,
                ki_substrate1, ki_substrate2, ki_product1, ki_product2, exprs_cor, ):
        # Numerator calculation
        numerator = (vmax / (ki_substrate1 * km_substrate2)) * ((NAD * ETOH - NADH * ACE) / k_equilibrium)

        # Denominator calculation
        term1 = 1 + NAD / ki_substrate1
        term2 = km_substrate1 * ETOH / (ki_substrate1 * km_substrate2)
        term3 = km_product2 * ACE / (ki_substrate1 * km_product1)
        term4 = NADH / ki_product2
        term5 = NAD * ETOH / (ki_substrate1 * km_substrate2)
        term6 = km_product2 * NAD * ACE / (ki_substrate1 * ki_product2 * km_product1)
        term7 = km_substrate1 * ETOH * NADH / (ki_substrate1 * km_substrate2 * ki_product2)
        term8 = NADH * ACE / (ki_product2 * km_product1)
        term9 = NAD * ETOH * ACE / (ki_substrate1 * km_substrate2 * ki_product1)
        term10 = ETOH * NADH * ACE / (ki_substrate1 * km_substrate2 * ki_product2)

        denominator = term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8 + term9 + term10

        return -exprs_cor * (numerator / denominator)


class Jax_ATPase(Mechanism):
    """
    JAX class to represent ATPase reaction with a potentially learnable ATPase ratio.
    """

    @staticmethod
    def compute(substrate, product, ATPase_ratio):
        # Compute the reaction rate
        rate = ATPase_ratio * substrate / product

        return rate


class Jax_MA_Rev_Bi(Mechanism):
    """Mass-action reversible bi-bi kinetic model."""

    @staticmethod
    def compute(substrate1, substrate2, product1, product2, k_equilibrium, k_fwd):
        return k_fwd * (substrate1 * substrate2 - product1 * product2 / k_equilibrium)


class Jax_MA_Rev(Mechanism):
    """Mass-action reversible kinetic model."""

    @staticmethod
    def compute(substrate, steady_state_substrate, k):
        return k * (steady_state_substrate - substrate)


class Jax_Amd1(Mechanism):
    """Amd1 kinetic model."""

    @staticmethod
    def compute(substrate, product, modifier, vmax, k50, ki, k_atp):
        return vmax * substrate / (k50 * (1 + modifier / ki) / (product / k_atp) + substrate)


class Jax_Transport_Flux_Correction(Mechanism):
    """Modelling reaction required for the glycolysis model's transport reaction. """

    @staticmethod
    def compute(substrate, dilution_rate):
        return (substrate / 3600) * dilution_rate
