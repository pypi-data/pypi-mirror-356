from ._utils import check_arr
import math

def support(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Total number of transactions is zero, support is therefore undefined")
    return arr[0]/sum(arr)

def confidence(arr):
    check_arr(arr)
    if (arr[0]+arr[1]) == 0:
        raise ZeroDivisionError("Antecedent is zero, confidence is therefore undefined")
    return arr[0]/(arr[0]+arr[1])

def lift(arr):
    check_arr(arr)
    if(sum(arr)==0) or ((((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr)))==0):
        raise ZeroDivisionError("Lift is undefined, due to division by zero")
    return (arr[0]/(sum(arr))) / (((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr)))

def conviction(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Conviction is undefined, due to division by zero")
    if arr[1]==0:
        raise ZeroDivisionError("Conviction is infinite, due to division by zero")
    return (((arr[0]+arr[1])/sum(arr))*((arr[1]+arr[3])/sum(arr))) / (arr[1]/(sum(arr)))

def leverage(arr):
    check_arr(arr)
    if (arr[0]+arr[1])==0:
        raise ZeroDivisionError("Leverage could not be computed due to division by zero")
    return (arr[0]/(arr[0]+arr[1]))-(((arr[0]+arr[1])/(sum(arr)))*((arr[0]+arr[2])/(sum(arr))))

def coverage(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Coverage is undefined, due to division by zero")
    return (arr[0] + arr[1]) / sum(arr)

def prevalence(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Prevalence is undefined, due to division by zero")
    return (arr[0] + arr[2]) / sum(arr)

def added_value(arr):
    check_arr(arr)
    if (arr[0]+arr[1])==0:
        raise ZeroDivisionError("Added value could not be computed due to division by zero")
    return (arr[0]/(arr[0] + arr[1])) - ((arr[0]+arr[2])/sum(arr))

def recall(arr):
    check_arr(arr)
    if (arr[0]+arr[2])==0:
        raise ZeroDivisionError("Recall could not be computed due to division by zero")
    return arr[0]/(arr[0]+arr[2])

def bi_confidence(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((((arr[0] + arr[1])/sum(arr))*(1-((arr[0]+arr[1])/sum(arr))))==0):
        raise ZeroDivisionError("Bi-confidence is undefined, due to division by zero")
    return ((arr[0]/sum(arr))-(((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr)))) / (((arr[0] + arr[1])/sum(arr))*(1-((arr[0]+arr[1])/sum(arr))))

def bi_lift(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((arr[2]/sum(arr))*((arr[0]+arr[1])/sum(arr)))==0):
        raise ZeroDivisionError("Bi-lift is undefined, due to division by zero")
    return ((arr[0]/sum(arr))*((arr[2]+arr[3])/sum(arr))) / ((arr[2]/sum(arr))*((arr[0]+arr[1])/sum(arr)))

def bi_improve(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((arr[2]+arr[3])/sum(arr))==0):
        raise ZeroDivisionError("Bi-improve is undefined, due to division by zero")
    return ((arr[0]/sum(arr))-(((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr)))) / ((arr[2]+arr[3])/sum(arr))

def jaccard(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((((arr[0]+arr[1])/sum(arr))+((arr[0]+arr[2])/sum(arr))-(arr[0]/sum(arr)))==0):
        raise ZeroDivisionError("Jaccard is undefined, due to division by zero")
    return (arr[0]/sum(arr)) / (((arr[0]+arr[1])/sum(arr))+((arr[0]+arr[2])/sum(arr))-(arr[0]/sum(arr)))

def one_way_support(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]+arr[1])==0) or (((arr[0] + arr[2]) / sum(arr))==0):
        raise ZeroDivisionError("One way support is undefined, due to division by zero.")
    if ((arr[0] / (arr[0] + arr[1])) / ((arr[0] + arr[2]) / sum(arr))) <= 0:
        raise ValueError("Cannot calculate logarithm for non-positive integers.")
    return (arr[0]/(arr[0]+arr[1])) * (math.log2((arr[0]/(arr[0]+arr[1])) / ((arr[0] + arr[2]) / sum(arr))))

def two_way_support(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]+arr[1])==0) or (((arr[0]+arr[2])/sum(arr))==0):
        raise ZeroDivisionError("Two way support is undefined, due to division by zero.")
    if ((arr[0]/(arr[0]+arr[1]))/((arr[0]+arr[2])/sum(arr))) <= 0:
        raise ValueError("Cannot calculate logarithm for non-positive integers.")
    return (arr[0]/sum(arr))*(math.log2((arr[0]/(arr[0]+arr[1]))/((arr[0]+arr[2])/sum(arr))))

def support_causal(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Support causal is undefined, due to division by zero")
    return (arr[0]/sum(arr)) + (arr[3]/sum(arr))

def confirm_descriptive(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Confirm descriptive is undefined, due to division by zero")
    return (arr[0]/sum(arr)) - (arr[1]/sum(arr))

def confirm_causal(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Confirm causal is undefined, due to division by zero")
    return (arr[0]/sum(arr)) + (arr[3]/sum(arr)) - 2*(arr[1]/sum(arr))

def confidence_causal(arr):
    check_arr(arr)
    if ((arr[0]+arr[1])==0) or ((arr[1]+arr[3])==0):
        raise ZeroDivisionError("Confidence causal is undefined, due to division by zero")
    return 1/2 * ((arr[0]/(arr[0]+arr[1])) + (arr[3]/(arr[1]+arr[3])))

def confirmed_confidence_causal(arr):
    check_arr(arr)
    if ((arr[0]+arr[1])==0) or ((arr[1]+arr[3])==0):
        raise ZeroDivisionError("Confirmed confidence causal is undefined, due to division by zero")
    return 1/2 * ((arr[0]/(arr[0]+arr[1])) + (arr[3]/(arr[1]+arr[3]))) - (arr[1]/(arr[0]+arr[1]))

def confirmed_confidence_descriptive(arr):
    check_arr(arr)
    if (arr[0]+arr[1])==0:
        raise ZeroDivisionError("Confirmed confidence descriptive is undefined, due to division by zero")
    return (arr[0]/(arr[0]+arr[1])) - (arr[1]/(arr[0]+arr[1]))

def collective_strength(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))) + (((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr))))==0) or ((1 - (arr[0]/sum(arr)) - (arr[3]/sum(arr)))==0):
        raise ZeroDivisionError("Collective strength is undefined, due to division by zero")
    return ((arr[0]/sum(arr) + arr[3]/sum(arr)) / ((((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))) + (((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr))))) * ((1 - (((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))) - (((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr)))) / (1 - (arr[0]/sum(arr)) - (arr[3]/sum(arr))))

def j_measure(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]+arr[1])==0) or (((arr[0]+arr[2])/sum(arr))==0) or (((arr[1]+arr[3])/sum(arr))==0):
        raise ZeroDivisionError("J-Measure is undefined, due to division by zero")
    if (((arr[0]/(arr[0]+arr[1]))/((arr[0]+arr[2])/sum(arr)))<=0) or ((arr[1]/(arr[0]+arr[1])/((arr[1]+arr[3])/sum(arr)))<=0):
        raise ValueError("Cannot calculate logarithm for non-positive integers.")
    return ((arr[0]/sum(arr))*(math.log2((arr[0]/(arr[0]+arr[1]))/((arr[0]+arr[2])/sum(arr))))) + ((arr[1]/sum(arr))*(math.log2(arr[1]/(arr[0]+arr[1])/((arr[1]+arr[3])/sum(arr)))))

def certainty_factor(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0] + arr[1])==0) or ((1-((arr[0]+arr[2])/sum(arr)))==0):
        raise ZeroDivisionError("Certainty factor is undefined, due to division by zero")
    return ((arr[0]/(arr[0] + arr[1])) - ((arr[0]+arr[2])/sum(arr))) / (1-((arr[0]+arr[2])/sum(arr)))

def example_counterexample_rate(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]/sum(arr))==0):
        raise ZeroDivisionError("Example-Counterexample rate is undefined, due to division by zero")
    return 1 - ((arr[1]/sum(arr))/(arr[0]/sum(arr)))

def complement_class_support(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((arr[1]+arr[3])/sum(arr))==0):
        raise ZeroDivisionError("Complement class support is undefined, due to division by zero")
    return (arr[1]/sum(arr)) / ((arr[1]+arr[3])/sum(arr))

def zhang(arr):
    check_arr(arr)
    if (sum(arr)==0) or (max(((arr[0]/sum(arr)) * (1-((arr[0] + arr[2]) / sum(arr)))),(((arr[0] + arr[2]) / sum(arr))*(((arr[0] + arr[1]) / sum(arr))-(arr[0]/sum(arr)))))==0):
        raise ZeroDivisionError("Zhang is undefined, due to division by zero.")
    return ((arr[0]/sum(arr)) - (((arr[0] + arr[1]) / sum(arr))*((arr[0] + arr[2]) / sum(arr)))) / max(((arr[0]/sum(arr)) * (1-((arr[0] + arr[2]) / sum(arr)))),(((arr[0] + arr[2]) / sum(arr))*(((arr[0] + arr[1]) / sum(arr))-(arr[0]/sum(arr)))))

def chi_square(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((((arr[0] + arr[1]) / sum(arr))*((arr[0] + arr[2]) / sum(arr))*(1-((arr[0] + arr[1]) / sum(arr)))*(1-((arr[0] + arr[2]) / sum(arr))))==0):
        raise ZeroDivisionError("Chi square is undefined, due to division by zero.")
    return (sum(arr)*(pow(((arr[0]/sum(arr))-((arr[0] + arr[1]) / sum(arr))*((arr[0] + arr[2]) / sum(arr))),2)))/(((arr[0] + arr[1]) / sum(arr))*((arr[0] + arr[2]) / sum(arr))*(1-((arr[0] + arr[1]) / sum(arr)))*(1-((arr[0] + arr[2]) / sum(arr))))

def correlation_coefficient(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((math.sqrt((((arr[0] + arr[1]) / sum(arr))*((arr[0] + arr[2]) / sum(arr))*(1-((arr[0] + arr[1]) / sum(arr)))*(1-((arr[0] + arr[2]) / sum(arr))))))==0):
        raise ZeroDivisionError("Correlation coefficient is undefined, due to division by zero.")
    return ((arr[0]/sum(arr)) - (((arr[0] + arr[1]) / sum(arr))*((arr[0] + arr[2]) / sum(arr)))) / (math.sqrt((((arr[0] + arr[1]) / sum(arr))*((arr[0] + arr[2]) / sum(arr))*(1-((arr[0] + arr[1]) / sum(arr)))*(1-((arr[0] + arr[2]) / sum(arr))))))

def correlation_confidence(arr):
    check_arr(arr)
    return correlation_coefficient(arr)*confidence(arr)

def correlation_jaccard(arr):
    check_arr(arr)
    return correlation_coefficient(arr)*jaccard(arr)

def all_confidence(arr):
    check_arr(arr)
    if ((arr[0]+arr[1])==0) or ((arr[0]+arr[2])==0):
        raise ZeroDivisionError("All confidence is undefined, due to division by zero")
    return min((arr[0]/(arr[0]+arr[1])),(arr[0]/(arr[0]+arr[2])))

def correlation_all_confidence(arr):
    check_arr(arr)
    return correlation_coefficient(arr)*all_confidence(arr)

def kappa(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]+arr[1])==0) or ((arr[2]+arr[3])==0) or ((1 - (((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))) - (((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr))))==0):
        raise ZeroDivisionError("Kappa is undefined, due to division by zero.")
    return (((arr[0]/(arr[0]+arr[1]))*((arr[0]+arr[1])/sum(arr))) + ((arr[3]/(arr[2]+arr[3]))*((arr[2]+arr[3])/sum(arr))) - (((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))) - (((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr)))) / (1 - (((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))) - (((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr))))

def correlation_kappa(arr):
    check_arr(arr)
    return correlation_coefficient(arr)*kappa(arr)

def laplace_correction(arr, k=None):
    check_arr(arr)
    if k is not None:
        if (sum(arr)==0) or (((sum(arr))*((arr[0]+arr[1])/sum(arr)) + k)==0):
            raise ZeroDivisionError("Laplace correction is undefined, due to division by zero.")
        return ((sum(arr)) *  (arr[0]/sum(arr)) + 1)/((sum(arr))*((arr[0]+arr[1])/sum(arr)) + k)
    else:
        if (sum(arr)==0) or (((sum(arr))*((arr[0]+arr[1])/sum(arr)) + 2)==0):
            raise ZeroDivisionError("Laplace correction is undefined, due to division by zero.")
        return ((sum(arr)) * (arr[0] / sum(arr)) + 1) / ((sum(arr)) * ((arr[0] + arr[1]) / sum(arr)) + 2)

def yule_q(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((((arr[0]/sum(arr)) * (arr[3]/sum(arr))) + ((arr[1]/sum(arr)) * (arr[2]/sum(arr))))==0):
        raise ZeroDivisionError("Yule's Q is undefined, due to division by zero.")
    return (((arr[0]/sum(arr)) * (arr[3]/sum(arr))) - ((arr[1]/sum(arr)) * (arr[2]/sum(arr)))) / (((arr[0]/sum(arr)) * (arr[3]/sum(arr))) + ((arr[1]/sum(arr)) * (arr[2]/sum(arr))))

def yule_y(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]*arr[3] == 0) and (arr[1]*arr[2] == 0)):
        raise ZeroDivisionError("Yule's Y is undefined, due to division by zero.")
    return (math.sqrt((arr[0]/sum(arr)) * (arr[3]/sum(arr))) - math.sqrt((arr[1]/sum(arr)) * (arr[2]/sum(arr)))) / (math.sqrt((arr[0]/sum(arr)) * (arr[3]/sum(arr))) + math.sqrt((arr[1]/sum(arr)) * (arr[2]/sum(arr))))

def klosgen(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0] + arr[1])==0):
        raise ZeroDivisionError("Klösgen is undefined, due to division by zero.")
    return (math.sqrt(arr[0]/sum(arr))) * ((arr[0]/(arr[0] + arr[1])) - ((arr[0]+arr[2])/sum(arr)))

def gini_index(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]+arr[1])==0) or ((arr[2]+arr[3])==0):
        raise ZeroDivisionError("Gini index is undefined, due to division by zero.")
    return ((arr[0]+arr[1])/sum(arr)) * (((arr[0]/(arr[0]+arr[1]))**2)+((arr[1]/(arr[0]+arr[1]))**2)) + ((arr[2]+arr[3])/sum(arr)) * (((arr[2]/(arr[2]+arr[3]))**2)+((arr[3]/(arr[2]+arr[3]))**2)) - (((arr[0]+arr[2])/sum(arr))**2) - (((arr[1]+arr[3])/sum(arr))**2)

def information_gain(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr)))==0):
        raise ZeroDivisionError("Information gain is undefined, due to division by zero.")
    if ((arr[0]/(sum(arr))) / (((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr)))) <= 0:
        raise ValueError("Cannot calculate logarithm for non-positive integers.")
    return math.log2((arr[0]/(sum(arr))) / (((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))))

def mutual_information(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr)))==0) or ((((arr[0]+arr[1])/sum(arr))*((arr[1]+arr[3])/sum(arr)))==0) or ((((arr[2]+arr[3])/sum(arr))*((arr[0]+arr[2])/sum(arr)))==0) or ((((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr)))==0):
        raise ZeroDivisionError("Mutual information is undefined, due to division by zero.")
    if (((arr[0]/sum(arr))/(((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))))<=0) or (((arr[1]/sum(arr))/(((arr[0]+arr[1])/sum(arr))*((arr[1]+arr[3])/sum(arr))))<=0) or (((arr[2]/sum(arr))/(((arr[2]+arr[3])/sum(arr))*((arr[0]+arr[2])/sum(arr))))<=0) or (((arr[3]/sum(arr))/(((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr))))<=0):
        raise ValueError("Cannot calculate logarithm for non-positive integer.")
    return ((arr[0]/sum(arr)) * math.log2((arr[0]/sum(arr))/(((arr[0]+arr[1])/sum(arr))*((arr[0]+arr[2])/sum(arr))))) + ((arr[1]/sum(arr)) * math.log2((arr[1]/sum(arr))/(((arr[0]+arr[1])/sum(arr))*((arr[1]+arr[3])/sum(arr))))) + ((arr[2]/sum(arr)) * math.log2((arr[2]/sum(arr))/(((arr[2]+arr[3])/sum(arr))*((arr[0]+arr[2])/sum(arr))))) + ((arr[3]/sum(arr)) * math.log2((arr[3]/sum(arr))/(((arr[2]+arr[3])/sum(arr))*((arr[1]+arr[3])/sum(arr)))))

def normalized_mutual_information(arr):
    check_arr(arr)
    if(sum(arr)==0) or ((arr[0] + arr[1])==0) or ((arr[2]+arr[3])==0) or (((-((arr[0]+arr[1])/sum(arr)) * (math.log2(((arr[0] + arr[1])/sum(arr))))) - (((arr[2]+arr[3])/sum(arr)) * (math.log2(((arr[2]+arr[3])/sum(arr))))))==0):
        raise ZeroDivisionError("Normalized mutual information is undefined, due to division by zero.")
    return mutual_information(arr) / ((-((arr[0]+arr[1])/sum(arr)) * (math.log2(((arr[0] + arr[1])/sum(arr))))) - (((arr[2]+arr[3])/sum(arr)) * (math.log2(((arr[2]+arr[3])/sum(arr))))))

def sebag_schoenauer(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[1]/sum(arr))==0):
        raise ZeroDivisionError("Sebag-Schoenauer is undefined due to division by zero.")
    return (arr[0]/sum(arr))/(arr[1]/sum(arr))

def least_contradiction(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((arr[0] + arr[2])/sum(arr))==0):
        raise ZeroDivisionError("Least contradiction is undefined due to division by zero.")
    return ((arr[0]/sum(arr)) - (arr[1]/sum(arr))) / ((arr[0] + arr[2])/sum(arr))

def odd_multiplier(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((((arr[0] + arr[2])/sum(arr)) * (arr[1]/sum(arr)))==0):
        raise ZeroDivisionError("Odd multiplier is undefined due to division by zero.")
    return ((arr[0]/sum(arr)) * ((arr[1] + arr[3])/sum(arr))) / (((arr[0] + arr[2])/sum(arr)) * (arr[1]/sum(arr)))

def piatetsky_shapiro(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Piatetsky-Shapiro is undefined due to division by zero.")
    return (arr[0]/sum(arr))-(((arr[0]+arr[1])/(sum(arr)))*((arr[0]+arr[2])/(sum(arr))))

def odds_ratio(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((arr[1]/sum(arr))*(arr[2]/sum(arr)))==0):
        raise ZeroDivisionError("Odds ratio is undefined due to division by zero.")
    return ((arr[0]/sum(arr))*(arr[3]/sum(arr)))/((arr[1]/sum(arr))*(arr[2]/sum(arr)))

def validity(arr):
    check_arr(arr)
    if sum(arr)==0:
        raise ZeroDivisionError("Validity is undefined due to division by zero.")
    return (arr[0]/sum(arr)) - (arr[2]/sum(arr))

def kulczynski_1(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((arr[1]/sum(arr))+(arr[2]/sum(arr)))==0):
        raise ZeroDivisionError("Kulczynski 1 is undefined due to division by zero.")
    return (arr[0]/sum(arr)) / ((arr[1]/sum(arr))+(arr[2]/sum(arr)))

def kulczynski_2(arr):
    check_arr(arr)
    if (sum(arr)==0) or (((arr[0]+arr[1])/sum(arr))==0) or (((arr[0]+arr[2])/sum(arr))==0):
        raise ZeroDivisionError("Kulczynski 2 is undefined due to division by zero.")
    return 0.5 * (((arr[0]/sum(arr))/((arr[0]+arr[1])/sum(arr)))+((arr[0]/sum(arr))/((arr[0]+arr[2])/sum(arr))))

def conditional_entropy(arr):
    check_arr(arr)
    if (arr[0]+arr[1])==0:
        raise ZeroDivisionError("Conditional entropy is undefined due to division by zero.")
    if ((arr[0]/(arr[0]+arr[1]))<=0) or ((arr[1]/(arr[0]+arr[1]))<=0):
        raise ValueError("Cannot calculate logarithm for non-positive integer.")
    return (-(arr[0]/(arr[0]+arr[1]))*(math.log2(arr[0]/(arr[0]+arr[1]))))-((arr[1]/(arr[0]+arr[1]))*(math.log2(arr[1]/(arr[0]+arr[1]))))

def theil_uncertainty_coefficient(arr):
    check_arr(arr)
    if (sum(arr)==0) or ((arr[0]+arr[2])==0) or ((arr[1]+arr[3])==0)or (((-((arr[0]+arr[2])/sum(arr)) * (math.log2(((arr[0] + arr[2])/sum(arr))))) - (((arr[1]+arr[3])/sum(arr)) * (math.log2(((arr[1]+arr[3])/sum(arr))))))==0):
        raise ZeroDivisionError("Theil-Uncertainty coefficient is undefined due to division by zero.")
    return mutual_information(arr) / ((-((arr[0]+arr[2])/sum(arr)) * (math.log2(((arr[0] + arr[2])/sum(arr))))) - (((arr[1]+arr[3])/sum(arr)) * (math.log2(((arr[1]+arr[3])/sum(arr))))))



clm_4ft_int_functions = {'support':support,
                            'confidence':confidence,
                            'lift':lift,
                            'conviction':conviction,
                            'leverage':leverage,
                            'coverage':coverage,
                            'prevalence':prevalence,
                            'added_value':added_value,
                            'recall':recall,
                            'bi_confidence':bi_confidence,
                            'bi_lift':bi_lift,
                            'bi_improve':bi_improve,
                            'jaccard':jaccard,
                            'one_way_support':one_way_support,
                            'two_way_support':two_way_support,
                            'support_causal':support_causal,
                            'confirm_descriptive':confirm_descriptive,
                            'confirm_causal':confirm_causal,
                            'confidence_causal':confidence_causal,
                            'confirmed_confidence_causal':confirmed_confidence_causal,
                            'confirmed_confidence_descriptive':confirmed_confidence_descriptive,
                            'collective_strength':collective_strength,
                            'j_measure':j_measure,
                            'certainty_factor':certainty_factor,
                            'example_counterexample_rate':example_counterexample_rate,
                            'complement_class_support':complement_class_support,
                            'zhang':zhang,
                            'chi_square':chi_square,
                            'correlation_coefficient':correlation_coefficient,
                            'correlation_confidence':correlation_confidence,
                            'correlation_jaccard':correlation_jaccard,
                            'all_confidence':all_confidence,
                            'correlation_all_confidence':correlation_all_confidence,
                            'kappa':kappa,
                            'correlation_kappa':correlation_kappa,
                            'laplace_correction':laplace_correction,
                            'yule_q':yule_q,
                            'yule_y':yule_y,
                            'klosgen':klosgen,
                            'gini_index':gini_index,
                            'information_gain':information_gain,
                            'mutual_information':mutual_information,
                            'normalized_mutual_information':normalized_mutual_information,
                            'sebag_schoenauer':sebag_schoenauer,
                            'least_contradiction':least_contradiction,
                            'odd_multiplier':odd_multiplier,
                            'piatetsky_shapiro':piatetsky_shapiro,
                            'odds_ratio':odds_ratio,
                            'validity':validity,
                            'kulczynski_1':kulczynski_1,
                            'kulczynski_2':kulczynski_2,
                            'conditional_entropy':conditional_entropy,
                            'theil_uncertainty_coefficient':theil_uncertainty_coefficient
                            }



