st.title("Decision Analysis Tool")

# Set constant values
payout_h = 1320000
sensitivity = 0.85
specificity = 0.95

# User input
p_storm = st.slider("Chance of storm", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
p_botrytis = st.slider("Chance of botrytis", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
p_ns = st.slider("Chance of normal sugar level", min_value=0.0, max_value=1.0, value=0.6, step=0.01)
p_ts = st.slider("Chance of top sugar level", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
p_hs = st.slider("Chance of high sugar level", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

def da(p_storm=0.5, payout_h=payout_h, 
       p_botrytis=0.1,
       p_ns=0.6, p_ts=0.3, p_hs=0.1,
       sensitivity=sensitivity, specificity=specificity):
    
    payout_nh_s = p_botrytis*3300000 + (1-p_botrytis)*420000
    payout_nh_ns = p_ns*960000 + p_ts*1410000 + p_hs*1500000
    
    p_DNS = specificity *(1-p_storm) + (1 - sensitivity)*p_storm
    p_DS = 1 - p_DNS
    
    p_NS_DNS = (specificity * (1-p_storm)) /  p_DNS
    p_S_DNS = 1 - p_NS_DNS
        
    p_NS_DS =  (1-specificity) * (1-p_storm) / p_DS
    
    p_S_DS = (1-p_NS_DS)
    
    EV_DNS = p_DNS * max(payout_h,(payout_nh_ns * p_NS_DNS +  payout_nh_s * p_S_DNS ))
    EV_DS = p_DS * max(payout_h,(payout_nh_ns * p_NS_DS +  payout_nh_s * p_S_DS ))
    
    print(EV_DNS, EV_DS)
    
    EV_sensor = EV_DNS + EV_DS
        
    return EV_sensor

# Calculate and display results
e_value = da(p_storm, payout_h, p_botrytis, p_ns, p_ts, p_hs, sensitivity, specificity)
st.write(f"E-value: {e_value}")

recommended_alternative = "Harvest" if payout_h > e_value else "Wait for sensor"
st.write(f"Recommended alternative: {recommended_alternative}")

